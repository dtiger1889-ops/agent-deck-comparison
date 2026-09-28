#!/usr/bin/env python3
"""Generates assets/linkedin-agent-managers.html: a standalone 1080x1350 page
with tools.json data inlined, for headless screenshotting. Agent managers
only, a curated feature subset."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "..", "data", "tools.json"), encoding="utf-8") as f:
    DATA = json.load(f)

TOOL_ORDER = ["Orca", "VelaTerm", "Pantheon", "Paseo", "GitKraken Kepler", "Agent Orchestrator (AO)"]
FEATURE_ORDER = [
    "harness_count", "needs_you_signal", "usage_hud", "burn_rate_forecast",
    "limit_governor", "vault_task_source", "worktree_management",
    "planner_orchestrator", "native_mobile_app", "runs_in_terminal",
]
SHORT_LABEL = {
    "harness_count": "Harness count",
    "needs_you_signal": "Needs-you signal",
    "usage_hud": "Usage HUD (local logs)",
    "burn_rate_forecast": "Burn-rate forecast",
    "limit_governor": "Limit governor",
    "vault_task_source": "Vault task source",
    "worktree_management": "Worktree mgmt",
    "planner_orchestrator": "Planner/orchestrator",
    "native_mobile_app": "Native mobile app",
    "runs_in_terminal": "Runs in your terminal",
}
DISPLAY_NAME = {"Agent Orchestrator (AO)": "AO", "GitKraken Kepler": "Kepler"}

MARK_STYLE = {
    "yes": ("#dcf5e2", "#1d6b34", "Yes"),
    "partial": ("#fdf1cf", "#8a6100", "Partial"),
    "experimental": ("#ece3fb", "#5b3aa8", "Exp."),
    "planned": ("#e6ecf5", "#3a4f78", "Planned"),
    "no": ("#f8dede", "#9c2b2b", "No"),
    "unknown": ("#ececec", "#6a6a6a", "Unk."),
    "n/a": ("#f2f2f2", "#8a8a8a", "N/A"),
}

tools_by_name = {t["name"]: t for t in DATA["tools"]}
tools = [tools_by_name[n] for n in TOOL_ORDER]
features = [f for f in DATA["features"] if f["key"] in FEATURE_ORDER]
features.sort(key=lambda f: FEATURE_ORDER.index(f["key"]))

def badge_html(cell):
    bg, fg, label = MARK_STYLE[cell["mark"]]
    return f'<span class="b" style="background:{bg};color:{fg}">{label}</span>'

rows_html = []
for f in features:
    cells = "".join(f'<td>{badge_html(t["features"][f["key"]])}</td>' for t in tools)
    rows_html.append(f'<tr><th>{SHORT_LABEL[f["key"]]}</th>{cells}</tr>')

header_cells = "".join(
    f'<th>{DISPLAY_NAME.get(t["name"], t["name"])}</th>'
    for t in tools
)

html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; width: 1080px; height: 1350px;
    font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    background: #f7f7f8; color: #1b1c1f;
    padding: 48px 56px;
  }}
  h1 {{ font-size: 46px; margin: 0 0 6px; }}
  .sub {{ font-size: 22px; color: #5c5f66; margin: 0 0 4px; }}
  .snap {{ font-size: 20px; color: #2f5fd8; font-weight: 600; margin: 0 0 22px; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; border: 1px solid #dcdde1; border-radius: 10px; overflow: hidden; }}
  th, td {{ padding: 22px 10px; font-size: 24px; text-align: center; border-bottom: 1px solid #dcdde1; }}
  th {{ background: #eef0f3; font-size: 22px; }}
  tbody th {{ text-align: left; font-size: 23px; font-weight: 600; white-space: nowrap; }}
  td:first-child, th:first-child {{ text-align: left; padding-left: 16px; width: 260px; }}
  .b {{ display: inline-block; padding: 6px 14px; border-radius: 999px; font-size: 21px; font-weight: 700; }}
  .key {{ margin-top: 24px; font-size: 19px; color: #5c5f66; line-height: 1.5; }}
  .footer {{ margin-top: 18px; font-size: 21px; line-height: 1.5; color: #8a8a8a; }}
</style></head>
<body>
  <h1>Agent-manager comparison</h1>
  <p class="sub">Six AI coding-agent managers, ten features that matter most</p>
  <p class="snap">Snapshot 2026-09-28 &middot; not re-verified beyond each tool's own docs/posts</p>
  <table>
    <thead><tr><th>Feature</th>{header_cells}</tr></thead>
    <tbody>{''.join(rows_html)}</tbody>
  </table>
  <p class="key">Key: <span class="b" style="background:#dcf5e2;color:#1d6b34">Yes</span>
  <span class="b" style="background:#fdf1cf;color:#8a6100">Partial</span>
  <span class="b" style="background:#ece3fb;color:#5b3aa8">Exp.</span>
  <span class="b" style="background:#e6ecf5;color:#3a4f78">Planned</span>
  <span class="b" style="background:#f8dede;color:#9c2b2b">No</span>
  <span class="b" style="background:#ececec;color:#6a6a6a">Unk.</span></p>
  <p class="footer">Full sortable chart: <b style="color:#2f5fd8">dtiger1889-ops.github.io/agent-deck-comparison</b><br>Compiled by Daniel Mack (dtiger1889-ops).</p>
</body></html>
"""

out_path = os.path.join(here, "..", "assets", "linkedin.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Wrote", out_path)
