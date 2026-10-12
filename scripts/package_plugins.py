"""CLI entry point for native Claude Code and Codex plugin packaging."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from toolkit.plugin_packager import main

if __name__ == "__main__":
    raise SystemExit(main())
