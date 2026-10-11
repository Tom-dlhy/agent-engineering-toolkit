"""Safe, explicit indexing and reading of expert reference leaves.

The repository catalog stays lightweight: only an activated SKILL.md exposes
its Markdown reference links. The CLI never reads all leaves to rank skills.
"""
from __future__ import annotations

import re
from pathlib import Path

from toolkit.catalog import ROOT, Skill

_REF_PATTERN = re.compile(r"\[[^\]]+\]\((references/[a-zA-Z0-9_./-]+\.md)\)")


def indexed_references(skill: Skill, root: Path = ROOT) -> tuple[str, ...]:
    """Read only the selected SKILL.md, returning its declared local leaves."""
    skill_dir = root / skill.path
    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    return tuple(dict.fromkeys(_REF_PATTERN.findall(content)))


def resolve_reference(skill: Skill, reference: str, root: Path = ROOT) -> Path:
    """Authorize ONLY a link declared in that skill's SKILL.md.

    Rejects traversal and symlinks, including symlinked parents.
    """
    if not isinstance(reference, str) or not re.fullmatch(
        r"references/[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*\.md", reference
    ):
        raise ValueError("invalid reference path")
    if reference not in indexed_references(skill, root):
        raise ValueError("reference not declared by skill")
    skill_dir = root / skill.path
    candidate = skill_dir / reference
    if not candidate.is_file():
        raise ValueError("missing reference")
    if skill_dir.is_symlink():
        raise ValueError("symlink in skill directory")
    current = skill_dir
    for segment in Path(reference).parts:
        current = current / segment
        if current.is_symlink():
            raise ValueError("symlink in reference path")
    if not candidate.resolve().is_relative_to(skill_dir.resolve()):
        raise ValueError("reference escapes skill directory")
    return candidate


def read_reference(skill: Skill, reference: str, root: Path = ROOT) -> str:
    return resolve_reference(skill, reference, root).read_text(encoding="utf-8")
