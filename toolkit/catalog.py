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

ROOT = Path(__file__).resolve().parents[1]
_WORDS = re.compile(r"[a-z0-9]+")
_STOP = frozenset(
    "a an and are as at be build by code create de des do en et for from how i in is "
    "it la le les of on or our ou pour project projet que qui the to un une use using "
    "want when with you your this that implement implementation skill skills feature"
    .split()
)
_DEEP = frozenset({
    "auth", "authentication", "authorization", "production", "prod", "migration",
    "migrate", "secrets", "credential", "credentials", "billing", "payment",
    "gdpr", "rgpd", "security", "permissions", "iam", "encryption", "incident",
    "delete", "destroy", "destructive", "terraform", "database",
})
_STANDARD = frozenset({
    "architecture", "architect", "api", "endpoint", "backend", "frontend", "integration",
    "refactor", "refactoring", "workflow", "design", "feature", "component", "test",
    "deploy", "cloud", "stack", "ux", "ui", "pipeline",
})


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


def search(
    query: str, catalog: dict[str, Skill], *,
    allowed: Iterable[str] | None = None, limit: int = 3,
) -> list[Match]:
    """Deterministic lexical ranking; empty query / no evidence -> no result."""
    tokens = tokenize(query)
    if not tokens or limit < 1:
        return []
    names = set(allowed) if allowed is not None else None
    matches: list[Match] = []
    for skill in catalog.values():
        if names is not None and skill.name not in names:
            continue
        name_parts = tokenize(skill.name)
        domain_parts = tokenize(skill.domain)
        keyword_parts = tokenize(" ".join(skill.keywords))
        desc_parts = tokenize(skill.description)
        in_name, in_keywords = tokens & name_parts, tokens & keyword_parts
        in_domain, in_desc = tokens & domain_parts, tokens & desc_parts
        # Generic "core" or "quality" domains should not dominate a specific match.
        score = 6 * len(in_name) + 4 * len(in_keywords) + 2 * len(in_domain) + len(in_desc)
        if not score:
            continue
        reasons: list[str] = []
        if in_name:
            reasons.append("name: " + ", ".join(sorted(in_name)))
        if in_keywords:
            reasons.append("keywords: " + ", ".join(sorted(in_keywords)))
        if in_domain:
            reasons.append("domain: " + ", ".join(sorted(in_domain)))
        if not reasons and in_desc:
            reasons.append("description: " + ", ".join(sorted(in_desc)))
        matches.append(Match(skill, score, tuple(reasons)))
    return sorted(matches, key=lambda m: (-m.score, m.skill.name))[:limit]


def suggest_workflow(query: str) -> tuple[str, str]:
    """Advisory heuristic, not a security decision or authorization mechanism."""
    words = tokenize(query)
    deep = words & _DEEP
    if deep:
        return "deep", "potentially high-impact topic: " + ", ".join(sorted(deep))
    standard = words & _STANDARD
    if standard:
        return "standard", "nontrivial engineering topic: " + ", ".join(sorted(standard))
    return "light", "no higher-risk indicator in the request"
