"""Conservative static Python import-boundary checker.

Config contains explicit source module prefixes and forbidden import prefixes.
This checker intentionally does not attempt to resolve dynamic imports, module
attribute aliases, filesystem namespace magic, or implicit framework coupling.
Treat PASS as evidence about static imports only, not system architecture.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    source: str
    forbidden: tuple[str, ...]


def _module_from_path(root: Path, file: Path) -> tuple[str, str]:
    parts = list(file.relative_to(root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
        module = ".".join(parts)
        package = module
    else:
        module = ".".join(parts)
        package = ".".join(parts[:-1])
    return module, package


def _under(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(prefix + ".")


def _imports(tree: ast.AST, package: str) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                if not package:
                    continue
                target = "." * node.level + (node.module or "")
                try:
                    base = importlib.util.resolve_name(target, package)
                except ImportError:
                    continue
            else:
                base = node.module or ""
            if base:
                found.append((node.lineno, base))
            for alias in node.names:
                if alias.name != "*" and base:
                    # A conservative superset: a from-imported name may
                    # also be an attribute, which is documented as a limit.
                    found.append((node.lineno, base + "." + alias.name))
    return found


def scan(root: Path, rules: tuple[Rule, ...]) -> list[str]:
    if not root.is_dir():
        raise ValueError(f"source root is not a directory: {root}")
    findings: list[str] = []
    for file in sorted(root.rglob("*.py")):
        if file.is_symlink():
            findings.append(f"{file.relative_to(root)}: symlink source forbidden")
            continue
        module, package = _module_from_path(root, file)
        applicable = [r for r in rules if _under(module, r.source)]
        if not applicable:
            continue
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
        except (SyntaxError, UnicodeError) as exc:
            findings.append(f"{file.relative_to(root)}: invalid Python: {exc}")
            continue
        # One actionable finding per instruction, source-rule and
        # forbidden prefix. An ImportFrom yields both its base module
        # and its qualified imported names; those are one violation.
        reported: set[tuple[int, str, str]] = set()
        for line, imported in _imports(tree, package):
            for rule in applicable:
                blocked = next(
                    (item for item in rule.forbidden if _under(imported, item)),
                    None,
                )
                if blocked is None:
                    continue
                key = (line, rule.source, blocked)
                if key in reported:
                    continue
                reported.add(key)
                findings.append(
                    f"{file.relative_to(root)}:{line}: {module} imports forbidden {imported}"
                )
    return findings


def load_rules(config: Path) -> tuple[Rule, ...]:
    data = json.loads(config.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise ValueError("config must include rules list")
    rules: list[Rule] = []
    for item in data["rules"]:
        if not isinstance(item, dict) or not isinstance(item.get("source"), str):
            raise ValueError("each rule must have string source")
        forbidden = item.get("forbidden")
        if not isinstance(forbidden, list) or not forbidden or not all(
            isinstance(name, str) and name.strip() for name in forbidden
        ):
            raise ValueError("each rule must have nonempty forbidden module list")
        rules.append(Rule(item["source"], tuple(forbidden)))
    return tuple(rules)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    try:
        findings = scan(args.root, load_rules(args.config))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for item in findings:
        print("BOUNDARY:", item)
    if findings:
        return 1
    print("Static import boundaries OK (not runtime architecture certification).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
