#!/usr/bin/env python3
"""Assembles data/tools.json from the per-tool files shipped in this repository.

Inputs (all in this repository, nothing outside it):
  data/chart.json        chart settings, feature list and tool order
  data/tools/<id>.json   one file per tool, listed in chart.json

Only files named in chart.json are read; any other file in data/tools/ stops the
build, so a stray copy can never become an extra tool. A published chart has no
Unknown cells: pass --allow-unknown only for a local draft that will not be pushed.
"""
import json
import os
import sys

MARKS = {"yes", "partial", "experimental", "planned", "no", "undocumented", "unknown", "n/a", "info"}

here = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(here, "..", "data")
tools_dir = os.path.join(data_dir, "tools")

with open(os.path.join(data_dir, "chart.json"), encoding="utf-8") as f:
    chart = json.load(f)

listed = [tool_id + ".json" for tool_id in chart["tools"]]
stray = sorted(set(os.listdir(tools_dir)) - set(listed))
if stray:
    print("REFUSED: files in data/tools/ that chart.json does not list:", ", ".join(stray))
    sys.exit(1)

feature_keys = [f["key"] for f in chart["features"]]
tools = []
problems = []
for name in listed:
    with open(os.path.join(tools_dir, name), encoding="utf-8") as f:
        tool = json.load(f)
    cells = tool["features"]
    if set(cells) != set(feature_keys):
        problems.append(f"{name}: cells do not match the feature list")
    for key, cell in cells.items():
        if cell.get("mark") not in MARKS:
            problems.append(f"{name}: {key}: bad mark {cell.get('mark')!r}")
    tools.append(tool)
if problems:
    print("REFUSED:", *problems, sep="\n  ")
    sys.exit(1)

unknown = [(t["name"], k) for t in tools for k, v in t["features"].items() if v["mark"] == "unknown"]
if unknown and "--allow-unknown" not in sys.argv:
    print(f"REFUSED: {len(unknown)} Unknown cell(s); research them first:")
    for name, key in unknown:
        print(f"  {name}: {key}")
    sys.exit(1)

out = {
    "snapshot_date": chart["snapshot_date"],
    "snapshot_note": chart["snapshot_note"],
    "features": chart["features"],
    "group_order": chart["group_order"],
    "tools": tools,
}
out_path = os.path.join(data_dir, "tools.json")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print("Wrote", os.path.normpath(out_path))
print("Tools:", len(tools))
