#!/usr/bin/env python3
"""Generates assets/linkedin-agent-managers.html: a standalone 1080x1350 page
with tools.json data inlined, for headless screenshotting. Agent managers
only, a curated feature subset."""
import json
import os
import sys

# --set 2 renders the second share image (the rows most people choose a tool on);
# the default is the original LinkedIn image.
SET = "2" if "--set" in sys.argv and sys.argv[sys.argv.index("--set") + 1] == "2" else "1"

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "..", "data", "tools.json"), encoding="utf-8") as f:
    DATA = json.load(f)

TOOL_ORDER = ["Orca", "VelaTerm", "herdr", "Pantheon", "Paseo", "GitKraken Kepler", "Agent Orchestrator (AO)"]
FEATURE_ORDER = [
    "harness_count", "app_shell", "usage_hud", "burn_rate_forecast",
    "limit_governor", "vault_task_source", "worktree_management",
    "planner_orchestrator", "native_mobile_app", "runs_in_terminal",
]
SHORT_LABEL = {
    "harness_count": "Coding agents supported",
    "app_shell": "App shell",
    "usage_hud": "Shows usage limits",
    "burn_rate_forecast": "Predicts limit hits",
    "limit_governor": "Pause/resume at limits",
    "vault_task_source": "Tasks from notes vault",
    "worktree_management": "Manages worktrees",
    "planner_orchestrator": "Splits the work",
    "native_mobile_app": "Phone app",
    "runs_in_terminal": "Runs in your terminal",
}
SUBTITLE = "Seven AI coding-agent managers, ten features that matter most"
OUT_NAME = "linkedin.html"
if SET == "2":
    # Rows chosen where the seven tools split most (yes on some, no on others), 2026-09-29.
    FEATURE_ORDER = [
        "harness_count", "usage_hud", "planner_orchestrator", "phone_access",
        "agent_to_agent_messaging", "conversation_gui_view", "issue_tracker_pipeline",
        "extensibility", "app_shell", "license_cost",
    ]
    SHORT_LABEL = {
        "harness_count": "Coding agents supported",
        "usage_hud": "Shows usage limits",
        "planner_orchestrator": "Splits a goal into tasks",
        "phone_access": "Phone access",
        "agent_to_agent_messaging": "Agents message each other",
        "conversation_gui_view": "Read sessions as chat",
        "issue_tracker_pipeline": "GitHub/Jira issues to PRs",
        "extensibility": "Plugins / SDK",
        "app_shell": "App shell",
        "license_cost": "License",
    }
    SUBTITLE = "Seven AI coding-agent managers, the ten features where they differ most"
    OUT_NAME = "share-2.html"

# Short text for the text rows, condensed from each cell in data/tools.json.
TEXT_ROWS = {
    "phone_access": {
        "Orca": "Own app (beta)", "VelaTerm": "Own app or browser", "herdr": "Any SSH app",
        "Pantheon": "Any SSH app", "Paseo": "Own app", "GitKraken Kepler": "Own app (limited)",
        "Agent Orchestrator (AO)": "Own app",
    },
    "os": {
        "Orca": "Win, Mac, Linux", "VelaTerm": "Win, Mac, Linux", "herdr": "Mac, Linux, Win (beta)",
        "Pantheon": "Windows", "Paseo": "Win, Mac, Linux", "GitKraken Kepler": "Win, Mac, Linux",
        "Agent Orchestrator (AO)": "Win, Mac, Linux",
    },
    "license_cost": {
        "Orca": "Free (MIT)", "VelaTerm": "Free (MIT)", "herdr": "Free (Apache)", "Pantheon": "Free (MIT)",
        "Paseo": "Free (Apache)", "GitKraken Kepler": "Paid, free tier", "Agent Orchestrator (AO)": "Free (Apache)",
    },
}

SHORT_AGENTS = {
    "Orca": "27+",
    "VelaTerm": "8+",
    "herdr": "22",
    "Pantheon": "2",
    "Paseo": "~39",
    "GitKraken Kepler": "Any (claimed)",
    "Agent Orchestrator (AO)": "25+",
}
DISPLAY_NAME = {"Agent Orchestrator (AO)": "AO", "GitKraken Kepler": "Kepler"}
SHORT_SHELL = {
    "Orca": "Electron",
    "VelaTerm": "Tauri 2",
    "herdr": "Terminal UI",
    "Pantheon": "Terminal UI",
    "Paseo": "Electron",
    "GitKraken Kepler": "Unknown",
    "Agent Orchestrator (AO)": "Electron",
}

MARK_STYLE = {
    "yes": ("#dcf5e2", "#1d6b34", "Yes"),
    "partial": ("#fdf1cf", "#8a6100", "Partial"),
    "experimental": ("#ece3fb", "#5b3aa8", "Beta"),
    "planned": ("#e6ecf5", "#3a4f78", "Planned"),
    "no": ("#f8dede", "#9c2b2b", "No"),
    "undocumented": ("#ffffff", "#6a6a6a", "Not documented"),
    "unknown": ("#ececec", "#6a6a6a", "Unknown"),
    "n/a": ("#f2f2f2", "#8a8a8a", "N/A"),
}

tools_by_name = {t["name"]: t for t in DATA["tools"]}
tools = [tools_by_name[n] for n in TOOL_ORDER]
features = [f for f in DATA["features"] if f["key"] in FEATURE_ORDER]
if "phone_access" in FEATURE_ORDER:
    features.append({"key": "phone_access"})
features.sort(key=lambda f: FEATURE_ORDER.index(f["key"]))

def badge_html(cell):
    bg, fg, label = MARK_STYLE[cell["mark"]]
    border = ";border:2px dashed #9a9a9a;padding:3px 7px" if cell["mark"] == "undocumented" else ""
    cls = "b nd" if cell["mark"] == "undocumented" else "b"
    return f'<span class="{cls}" style="background:{bg};color:{fg}{border}">{label}</span>'

rows_html = []
for f in features:
    if f["key"] == "harness_count":
        cells = "".join(f'<td class="plain">{SHORT_AGENTS.get(t["name"], "not verified")}</td>' for t in tools)
    elif f["key"] == "app_shell":
        cells = "".join(f'<td class="plain">{SHORT_SHELL.get(t["name"], "not verified")}</td>' for t in tools)
    elif f["key"] in TEXT_ROWS:
        cells = "".join(f'<td class="plain small">{TEXT_ROWS[f["key"]][t["name"]]}</td>' for t in tools)
    else:
        cells = "".join(f'<td>{badge_html(t["features"][f["key"]])}</td>' for t in tools)
    rows_html.append(f'<tr><th>{SHORT_LABEL[f["key"]]}</th>{cells}</tr>')

used = {t["features"][f["key"]]["mark"] for f in features for t in tools if f["key"] in t["features"]}
key_html = " ".join(badge_html({"mark": m}) for m in MARK_STYLE if m in used and m != "n/a")

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
    padding: 44px 40px;
  }}
  h1 {{ font-size: 46px; margin: 0 0 6px; }}
  .sub {{ font-size: 22px; color: #5c5f66; margin: 0 0 4px; }}
  .snap {{ font-size: 20px; color: #2f5fd8; font-weight: 600; margin: 0 0 22px; }}
  table {{ table-layout: fixed; border-collapse: collapse; width: 100%; background: #fff; border: 1px solid #dcdde1; border-radius: 10px; overflow: hidden; }}
  th, td {{ padding: 22px 4px; font-size: 22px; text-align: center; border-bottom: 1px solid #dcdde1; }}
  th {{ background: #eef0f3; font-size: 22px; }}
  tbody th {{ text-align: left; font-size: 21px; font-weight: 600; white-space: nowrap; }}
  td:first-child, th:first-child {{ text-align: left; padding-left: 16px; width: 290px; }}
  .b {{ white-space: nowrap; display: inline-block; padding: 5px 11px; border-radius: 999px; font-size: 19px; font-weight: 700; }}
  td .b.nd {{ white-space: normal; border-radius: 12px; line-height: 1.2; font-size: 17px; padding: 3px 4px !important; }}
  td.plain {{ font-size: 22px; color: #3a3c40; font-weight: 600; }}
  td.plain.small {{ font-size: 18px; line-height: 1.25; padding: 14px 4px; }}
  .key {{ margin-top: 24px; font-size: 19px; color: #5c5f66; line-height: 1.5; }}
  .wm {{ display: block; margin-top: 4px; font-size: 16px; font-weight: 500; color: #8a8d94; white-space: nowrap; }}
  .wm .gh {{ vertical-align: -3px; margin-right: 5px; }}
  .footer {{ margin-top: 18px; font-size: 21px; line-height: 1.5; color: #8a8a8a; }}
</style></head>
<body>
  <h1>Agent-manager comparison</h1>
  <p class="sub">{SUBTITLE}</p>
  <p class="snap">Snapshot 2026-09-28 &middot; not re-verified beyond each tool's own docs/posts</p>
  <table>
    <thead><tr><th>Feature<span class="wm"><svg class="gh" viewBox="0 0 16 16" width="17" height="17" aria-hidden="true"><path fill="currentColor" d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.37A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>dtiger1889-ops</span></th>{header_cells}</tr></thead>
    <tbody>{''.join(rows_html)}</tbody>
  </table>
  <p class="key">Key: {key_html}</p>
  <p class="footer">Full sortable chart: <b style="color:#2f5fd8">dtiger1889-ops.github.io/agent-deck-comparison</b></p>
</body></html>
"""

out_path = os.path.join(here, "..", "assets", OUT_NAME)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Wrote", out_path)
