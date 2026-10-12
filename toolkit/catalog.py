"""Deterministic catalog discovery and minimal-context routing.

No network calls, model dependency, automatic skill activation, or script execution.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from toolkit.adaptive_policy import ChangeSignals, assess

ROOT = Path(__file__).resolve().parents[1]
_WORDS = re.compile(r"[a-z0-9]+")
_STOP = frozenset(
    "a an and are as at be build by code create de des do en et for from how i in is "
    "it la le les of on or our ou pour project projet que qui the to un une use using "
    "want when with you your this that implement implementation skill skills feature"
    .split()
)
# Bounded aliases, not translation or semantic intent recognition. Compound
# database phrases are collapsed before tokenization so "base" cannot select UI.
_PHRASES = ((r"\bbases? de donnees\b", "database"),
            (r"\bdata bases?\b", "database"))
_ALIASES = {
    "choisir": "selection", "choose": "selection", "choosing": "selection",
    "select": "selection", "selecting": "selection", "comparer": "compare",
    "diagnostiquer": "debug", "debugging": "debug", "diagnose": "debug",
    "paiement": "payment", "fournisseur": "provider", "duplique": "duplicate",
    "authentification": "authentication", "autorisation": "authorization",
    "modifier": "modify", "restreindre": "restrict", "supprimer": "remove",
    "migrer": "migrate", "donnees": "data",
    "ajouter": "add", "implementer": "implement", "executer": "execute",
    "predicat": "predicate", "tenants": "tenant", "faute": "typo",
    "coquille": "typo", "corriger": "fix", "stockage": "storage",
    "refactorisation": "refactor", "locale": "local",
}
_NEGATIVE = re.compile(r"\b(?:do not|don't|not for|avoid using|ne pas utiliser)\b", re.I)
_ACTIONS = frozenset("modify change fix edit update refactor restrict remove migrate delete destroy deploy rotate disable relax bypass alter rewrite perform execute implement add create build".split())
_BOUNDARIES = frozenset("auth authentication authorization permissions iam secrets credentials tenant ownership encryption production prod sensitive personal".split())
_EXCLUSION_SCOPE = re.compile(r"^(?:do not use|don't use|do not apply|do not substitute|not for|avoid using|ne pas utiliser)\b", re.I)
_GENERIC_IDENTITY = frozenset("ui cloud python data api service engineering selection design quality platform architecture library components".split())
_WORDING_ACTIONS = frozenset({"fix", "edit", "update"})
_OPERATIONAL = frozenset("predicate filter endpoint policy code checks guard rule rules handler".split())
_COMPLEXITY = frozenset("architecture api endpoint backend frontend integration refactor workflow design component pipeline selection compare".split())


def tokenize(text: str) -> set[str]:
    clean = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return {w for w in _WORDS.findall(clean) if len(w) > 1 and w not in _STOP}


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Skill:
    name: str
    domain: str
    path: str
    description: str
    keywords: tuple[str, ...]

    def metadata(self) -> str:
        return f"{self.name}: {self.description}"


@dataclass(frozen=True)
class Match:
    skill: Skill
    score: int
    reasons: tuple[str, ...]
    unfavorable: tuple[str, ...] = ()


def load_catalog(root: Path = ROOT) -> dict[str, Skill]:
    manifest = load_yaml(root / "registry" / "skills.yaml")
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise ValueError("unsupported catalog version")
    skills: dict[str, Skill] = {}
    for item in manifest["skills"]:
        path = root / item["path"] / "SKILL.md"
        source = path.read_text(encoding="utf-8")
        if not source.startswith("---\n"):
            raise ValueError(f"invalid skill frontmatter: {path}")
        try:
            _, header, _ = source.split("---\n", 2)
        except ValueError as exc:
            raise ValueError(f"invalid skill frontmatter: {path}") from exc
        meta = yaml.safe_load(header)
        name = item["name"]
        if name in skills:
            raise ValueError(f"duplicate skill: {name}")
        if meta["name"] != name or meta.get("domain") != item["domain"]:
            raise ValueError(f"skill metadata mismatch: {path}")
        labels = item.get("keywords", [])
        if not isinstance(labels, list) or any(not isinstance(label, str) for label in labels):
            raise ValueError(f"invalid keywords: {name}")
        skills[name] = Skill(
            name=name, domain=item["domain"], path=item["path"],
            description=meta["description"], keywords=tuple(labels),
        )
    return skills


def load_profile(name: str, root: Path = ROOT) -> tuple[str, ...]:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("invalid profile name")
    path = root / "profiles" / (name + ".yaml")
    if not path.is_file():
        raise ValueError(f"unknown profile: {name}")
    data = load_yaml(path)
    return tuple(data["skills"])


@dataclass(frozen=True)
class Exclusion:
    skill: Skill
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Discovery:
    candidates: tuple[Match, ...]
    excluded: tuple[Exclusion, ...]
    uncertainty: str
    required_checks: tuple[str, ...]


@dataclass(frozen=True)
class WorkflowAdvice:
    workflow: str
    risk: str
    source: str
    rationale: tuple[str, ...]
    required_checks: tuple[str, ...]


def _normalized(text: str) -> str:
    clean = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    for pattern, replacement in _PHRASES:
        clean = re.sub(pattern, replacement, clean)
    return clean


def _routing_tokens(text: str) -> set[str]:
    return {_ALIASES.get(w, w) for w in tokenize(_normalized(text))}


def _description_parts(description: str) -> tuple[str, tuple[str, ...]]:
    # Exclusions are metadata, never positive evidence. Unknown negative syntax
    # must still be reviewed by the caller; this recognizes the library's form.
    boundaries = list(_NEGATIVE.finditer(description))
    if not boundaries:
        return description, ()
    ends = [match.start() for match in boundaries[1:]] + [len(description)]
    return description[:boundaries[0].start()], tuple(description[match.start():end] for match, end in zip(boundaries, ends))


def _action_words(text: str) -> set[str]:
    # Discovery stopwords include "build"/"implement"; workflow consequences must
    # retain these requested actions without changing the public tokenizer.
    return {_ALIASES.get(word, word) for word in _WORDS.findall(_normalized(text))} & _ACTIONS


def _simple_edit(words: set[str], actions: set[str] | None = None) -> bool:
    return (bool(words & {"typo", "spelling"})
            and bool(words & {"documentation", "docs", "label"})
            and not ((words & _ACTIONS) if actions is None else actions) - _WORDING_ACTIONS
            and not words & _OPERATIONAL)


def discover(
    query: str, catalog: dict[str, Skill], *,
    allowed: Iterable[str] | None = None, limit: int = 3,
) -> Discovery:
    """Generate explainable candidates; never activate/install or decide safety.

    Fully matched short exclusion clauses suppress candidates. Partial matches
    and missing stack evidence remain explicit checks, not fabricated facts.
    """
    clean = _normalized(query)
    negated: set[str] = set()
    def remove_negative(match: re.Match[str]) -> str:
        negated.update(_routing_tokens(match.group(1)))
        return " "
    positive_query = re.sub(r"\b(?:do not use|don't use|exclude|without|sans|ne pas utiliser)\s+([^,.;]+?)(?=[,;.]|\bbut\b|\bmais\b|\band\b|\bet\b|$)",
                            remove_negative, clean)
    tokens = _routing_tokens(positive_query)
    checks = ("Inspect task scope and the selected stack before activation; zero skills is valid.",)
    if not tokens or limit < 1 or _simple_edit(tokens):
        return Discovery((), (), "insufficient" if not tokens else "lexical", checks)
    names = set(allowed) if allowed is not None else None
    matches: list[Match] = []
    excluded: list[Exclusion] = []
    for skill in catalog.values():
        if names is not None and skill.name not in names:
            continue
        positive, negative = _description_parts(skill.description)
        groups = (("name", _routing_tokens(skill.name), 6),
                  ("keywords", _routing_tokens(" ".join(skill.keywords)), 4),
                  ("domain", _routing_tokens(skill.domain), 2),
                  ("description", _routing_tokens(positive), 1))
        score = 0
        reasons: list[str] = []
        for label, words, weight in groups:
            overlap = tokens & words
            score += weight * len(overlap)
            if overlap:
                reasons.append(label + ": " + ", ".join(sorted(overlap)))
        negative_reasons: list[str] = []
        unfavorable: list[str] = []
        for text in negative:
            marker = _EXCLUSION_SCOPE.match(text)
            if marker is None:
                continue  # Safety/procedure warnings are not activation scopes.
            text = text[marker.end():]
            # Conservative literal clauses: no negation inference from one word.
            for clause in re.split(r"[,.;]|\bor\b", text):
                terms = _routing_tokens(clause) - {"not", "only", "selected", "existing", "specific"}
                if len(terms) >= 2 and terms <= tokens:
                    negative_reasons.append("explicit exclusion: " + clause.strip())
                elif len(terms & tokens) >= 2:
                    unfavorable.append("check exclusion scope: " + clause.strip())
        if score and skill.name.endswith("-selection") and not tokens & {"selection", "compare", "choice", "decision", "revising"}:
            negative_reasons.append("technology choice is not requested explicitly")
        identity = _routing_tokens(skill.name) - _GENERIC_IDENTITY
        negated_identity = negated & identity
        if negated_identity and not tokens & negated_identity:
            negative_reasons.append("explicitly negated in request: " + ", ".join(sorted(negated & identity)))
        if negative_reasons:
            # Record matched exclusions even when removing their description
            # tokens leaves no positive score.
            excluded.append(Exclusion(skill, tuple(negative_reasons)))
            continue
        if not score:
            continue
        if "debug" in tokens and "debug" in _routing_tokens(" ".join(skill.keywords)):
            score += 10
            reasons.append("diagnosis intent")
        if skill.domain == "ui":
            identity = _routing_tokens(skill.name) - {"ui", "components"}
            if not identity & tokens:
                unfavorable.append("component library not identified; confirm selected stack")
        matches.append(Match(skill, score, tuple(reasons), tuple(unfavorable)))
    ranked = sorted(matches, key=lambda m: (-m.score, m.skill.name))
    candidates = tuple(ranked[:limit])
    ambiguous = bool(candidates and (candidates[0].unfavorable or
                                    (len(ranked) > 1 and ranked[0].score == ranked[1].score)))
    uncertainty = "ambiguous" if ambiguous else "lexical" if candidates else "insufficient"
    return Discovery(candidates, tuple(excluded), uncertainty, checks)


def search(
    query: str, catalog: dict[str, Skill], *,
    allowed: Iterable[str] | None = None, limit: int = 3,
) -> list[Match]:
    """Compatible candidate-list interface; use discover for diagnostics."""
    return list(discover(query, catalog, allowed=allowed, limit=limit).candidates)


def workflow_advice(query: str, *, observed: ChangeSignals | None = None) -> WorkflowAdvice:
    """Keep inferred text separate from observed policy inputs and authorization."""
    if observed is not None:
        decision = assess(observed)
        return WorkflowAdvice(decision.workflow, "confirmed" if decision.workflow == "deep" else "observed",
                              "observed_change_signals", decision.rationale, decision.unmet_gates)
    clauses = [part.strip() for part in re.split(r"[;.]|\b(?:and then|and|then|et|puis)\b", _normalized(query)) if part.strip()]
    if len(clauses) > 1:
        suggestions = []
        inherited_actions: set[str] = set()
        for clause in clauses:
            clause_actions = _action_words(clause) | (_routing_tokens(clause) & {"explain", "describe", "expliquer", "decrire"})
            if clause_actions:
                inherited_actions = clause_actions
            elif inherited_actions:
                # Coordinated objects share the request's action: "delete files
                # and customer data" cannot lose the deletion consequence.
                clause = " ".join(sorted(inherited_actions)) + " " + clause
            suggestions.append(workflow_advice(clause))
        order = {"light": 0, "standard": 1, "deep": 2}
        strongest = max(suggestions, key=lambda item: order[item.workflow])
        return WorkflowAdvice(strongest.workflow, strongest.risk, strongest.source,
                              ("compound request: strongest indicated consequence retained",) + strongest.rationale,
                              strongest.required_checks)
    words = _routing_tokens(query)
    checks = ("Inspect affected code/data, reversibility and permissions; suggestion is not authorization.",)
    action = _action_words(query)
    # An explanation about a migration is not a request to execute it.
    informational = bool(words & {"explain", "describe", "expliquer", "decrire"})
    boundary = words & _BOUNDARIES
    if _simple_edit(words, action):
        return WorkflowAdvice("light", "insufficient", "request_heuristic",
                              ("isolated wording edit; inspect diff to confirm scope",), checks)
    doc_only = bool(words & {"documentation", "docs"}) and not action - _WORDING_ACTIONS and not words & _OPERATIONAL
    if doc_only:
        return WorkflowAdvice("light", "insufficient", "request_heuristic",
                              ("documentation request; no operational change established",), checks)
    consequential = bool(action and (boundary or words & {"irreversible", "destructive"} or
                                     {"ownership", "filter"} <= words or
                                     (action & {"delete", "remove", "destroy"} and
                                      words & {"data", "database", "records", "customer"})))
    if consequential or (not informational and words & {"migrate", "migration"} and words & {"data", "database"}):
        return WorkflowAdvice("deep", "potential", "request_heuristic",
                              ("requested action may change a trust/data/rollback boundary",), checks)
    if {"local", "reversible"} <= words and not (action - {"refactor", "fix", "edit", "update"}) and not boundary and not words & {"shared", "contract", "integration"}:
        return WorkflowAdvice("light", "insufficient", "request_heuristic",
                              ("request describes a local reversible change; scope remains unverified",), checks)
    if action or words & _COMPLEXITY:
        return WorkflowAdvice("standard", "potential" if boundary or action else "insufficient", "request_heuristic",
                              ("engineering action or integration; consequences require inspection",), checks)
    return WorkflowAdvice("light", "insufficient", "request_heuristic",
                          ("insufficient impact information; no safety conclusion",), checks)


def suggest_workflow(query: str) -> tuple[str, str]:
    """Compatible advisory tuple; never a security decision or authorization."""
    advice = workflow_advice(query)
    return advice.workflow, "; ".join(advice.rationale) + " (risk: " + advice.risk + ")"
