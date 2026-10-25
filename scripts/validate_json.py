"""Validate JSON syntax, duplicate keys, and nonstandard numeric constants."""
import json
import sys
from pathlib import Path

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate key: {key}")
        result[key] = value
    return result

def reject_constant(value):
    raise ValueError(f"Nonstandard numeric constant: {value}")

root = Path(__file__).resolve().parents[1]
files = sorted((root / "Topics").rglob("*.json"))
errors = []
for path in files:
    try:
        json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        errors.append(f"{path.relative_to(root)}: {exc}")
for error in errors:
    print(error)
print(f"Checked {len(files)} JSON files; {len(errors)} failures.")
sys.exit(1 if errors or not files else 0)
