#!/usr/bin/env python3
"""Inventory and sanity-check files produced by hepdata-cli downloads."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys


def iter_files(paths: list[Path]):
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from sorted(item for item in path.rglob("*") if item.is_file())
        else:
            raise ValueError(f"unsupported path type: {path}")


def validate_file(path: Path) -> dict[str, object]:
    size = path.stat().st_size
    if size == 0:
        raise ValueError(f"empty file: {path}")

    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open(encoding="utf-8") as stream:
            json.load(stream)
    elif suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as stream:
            if next(csv.reader(stream), None) is None:
                raise ValueError(f"CSV has no rows: {path}")

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return {
        "path": str(path.resolve()),
        "bytes": size,
        "sha256": digest.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that HEPData download outputs exist and are non-empty; parse JSON and CSV files."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Downloaded files or directories")
    parser.add_argument(
        "--require-suffix",
        action="append",
        default=[],
        metavar="SUFFIX",
        help="Require at least one file with this suffix; repeat as needed (example: .yaml)",
    )
    args = parser.parse_args()

    try:
        files = list(dict.fromkeys(iter_files(args.paths)))
        if not files:
            raise ValueError("no downloaded files found")
        required = {value.lower() if value.startswith(".") else f".{value.lower()}" for value in args.require_suffix}
        present = {path.suffix.lower() for path in files}
        missing = sorted(required - present)
        if missing:
            raise ValueError(f"required suffixes not found: {', '.join(missing)}")
        report = {"ok": True, "file_count": len(files), "files": [validate_file(path) for path in files]}
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
