"""Command-line entry point for the experimental IntentSpec profile."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .parser import VERSION, collect_files, validate_files


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="intentspec",
        description="Validate and export draft IntentSpec 0.1 requirements",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="check syntax, structure and local links")
    validate.add_argument("paths", nargs="+", type=Path, help="requirement files or directories")
    validate.add_argument("--json", action="store_true", help="print machine-readable diagnostics")

    export = subcommands.add_parser("export-json", help="export parsed, validated requirements")
    export.add_argument("paths", nargs="+", type=Path, help="requirement files or directories")
    export.add_argument("--output", "-o", type=Path, help="write JSON to this path")

    args = parser.parse_args(argv)
    files = collect_files(args.paths)
    if not files:
        parser.error("no *.req.md files found")

    docs = validate_files(files)
    diagnostics = [d for doc in docs for d in doc.diagnostics]
    valid = not any(d.severity == "error" for d in diagnostics)

    if args.command == "validate":
        if args.json:
            print(
                json.dumps(
                    {
                        "intentspec": VERSION,
                        "valid": valid,
                        "files": [doc.path for doc in docs],
                        "diagnostics": [d.to_dict() for d in diagnostics],
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            for diag in diagnostics:
                print(f"{diag.path}:{diag.line}: {diag.severity} {diag.code}: {diag.message}")
            print(f"Checked {len(docs)} requirement(s): {'valid' if valid else 'invalid'}")
        return 0 if valid else 1

    if not valid:
        for diag in diagnostics:
            print(f"{diag.path}:{diag.line}: {diag.severity} {diag.code}: {diag.message}")
        return 1

    payload = {
        "intentspec": VERSION,
        "requirements": [doc.export() for doc in sorted(docs, key=lambda d: d.metadata["id"])],
    }
    output = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
