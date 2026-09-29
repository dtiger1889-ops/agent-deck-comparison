#!/usr/bin/env python3
"""Generates data/tools.json from the hardcoded transcription of the source
comparison doc (project_pantheon/docs/feature-comparison.md, section 6 cross
table + section 5 thinner entries). No web calls, no invented data."""
import json
import os

MARKS = {"yes", "partial", "experimental", "planned", "no", "undocumented", "unknown", "n/a", "info"}

# Groups render as full-width heading rows in the matrix view, in this fixed order.
G_AGENTS = "Agents & supervision"
G_SESSIONS = "Sessions & views"
G_USAGE = "Usage & limits"
G_TASKS = "Tasks, planning & merging"
G_REMOTE = "Remote & mobile"
G_HOOD = "Under the hood"
G_PROJECT = "Project & openness"
GROUP_ORDER = [G_AGENTS, G_SESSIONS, G_USAGE, G_TASKS, G_REMOTE, G_HOOD, G_PROJECT]

FEATURES = [
    ("multi_provider_supervision", "Runs more than one kind of agent", "Can drive more than one coding agent (Claude Code, Codex and so on) side by side.", G_AGENTS),
    ("harness_count", "Coding agents supported", "How many different coding agents it can run, per its own docs.", G_AGENTS),
    ("needs_you_signal", "Alerts when you're needed", "How it tells you an agent is waiting on you.", G_AGENTS),
    ("approve_deny_prompt", "Answer \"Allow?\" prompts from the manager", "When an agent stops to ask permission (run this command? edit this file?), you can allow or deny it from the manager or your phone instead of opening that agent's own window.", G_AGENTS),
    ("cross_provider_delegation", "Hand-offs between agents in one view", "Work passed from one agent to another shows up in the same place.", G_AGENTS),
    ("always_on_assistant", "Always-on assistant", "A standing assistant session you can reach any time.", G_AGENTS),
    ("conversation_gui_view", "Chat view of a session", "Read a session as a conversation instead of raw terminal text.", G_SESSIONS),
    ("real_terminal", "Open the real terminal", "Drop into the session's actual terminal.", G_SESSIONS),
    ("session_organization", "How sessions are organized", "List, worktrees, kanban or nested groups.", G_SESSIONS),
    ("prompt_scratchpad", "Prompt drafts", "Draft prompts and insert them without sending.", G_SESSIONS),
    ("saved_prompt_library", "Saved prompts", "Reusable prompts you can fire with context attached.", G_SESSIONS),
    ("builtin_editors_browser", "Built-in editor / browser", "Ships its own editor or browser.", G_SESSIONS),
    ("appearance_control", "Look and font control", "How far you can change its look, including your terminal's font.", G_SESSIONS),
    ("usage_hud", "Shows your usage limits", "Your subscription usage and resets, read from local logs.", G_USAGE),
    ("burn_rate_forecast", "Predicts when you'll hit a limit", "Burn rate and time to the limit, not just current usage.", G_USAGE),
    ("limit_governor", "Pause and resume at usage limits", "Pauses work near a limit and picks it back up after the reset.", G_USAGE),
    ("account_hotswap", "Switch accounts without logging in again", "Move between provider accounts without re-login.", G_USAGE),
    ("vault_task_source", "Tasks from your notes vault", "Reads your own notes vault (such as Obsidian) as the task list.", G_TASKS),
    ("issue_tracker_pipeline", "Turns GitHub or Jira issues into pull requests", "Picks up an issue from GitHub, GitLab, Linear or Jira, hands it to an agent, and carries the resulting pull request through review.", G_TASKS),
    ("worktree_management", "Manages git worktrees", "Gives each agent or task its own git worktree.", G_TASKS),
    ("planner_orchestrator", "Planner that splits the work", "Breaks a goal into parts and runs them.", G_TASKS),
    ("agent_to_agent_messaging", "Agents message each other", "One session can message or query another.", G_TASKS),
    ("knowledge_base", "Knowledge base for agents", "A notes store agents can look things up in.", G_TASKS),
    ("native_mobile_app", "Phone app", "A dedicated iOS or Android app.", G_REMOTE),
    ("phone_no_new_app", "Phone access with no new app", "Reach it from your phone with tools you already have.", G_REMOTE),
    ("remote_ssh", "Remote machines over SSH", "Run or edit sessions on another machine.", G_REMOTE),
    ("voice_input", "Voice input", "Dictate to it.", G_REMOTE),
    ("os", "Operating systems", "Which systems it runs on, plus phone or browser access, per its own release files or docs.", G_HOOD),
    ("app_shell", "App shell", "What the app is built on: Electron, Tauri, a terminal UI, or a hosted service.", G_HOOD),
    ("languages", "Main languages", "Top languages in its repo, from GitHub's breakdown.", G_HOOD),
    ("background_process", "Background process", "Whether it runs a separate server or daemon next to the app.", G_HOOD),
    ("download_size", "Download size", "Installer size from its latest release. Not memory use.", G_HOOD),
    ("ram_vs_claude_desktop", "Memory vs Claude Desktop", "Size as a share of Claude Desktop, which measured about 7.5 GB on one Windows PC on 2026-09-28 (about 3.7 GB for the app across 24 processes, plus about 4 GB for the virtual machine it starts for Cowork). Scale: Tiny = under 5%, Small = 5-15%, Medium = 15-40%. Measured where the cell says so; otherwise an estimate from what the tool is built on. The coding agents themselves cost the same under every tool.", G_HOOD),
    ("runs_in_terminal", "Runs in your own terminal", "Lives inside the terminal you already use.", G_HOOD),
    ("license_cost", "License / cost", "Open-source license or pricing.", G_PROJECT),
    ("extensibility", "Plugins / SDK", "Outside developers can extend it.", G_PROJECT),
    ("teams_multiuser", "Teams", "Built for more than one person.", G_PROJECT),
    ("stability_maturity", "Maturity", "How far along and how stable it is.", G_PROJECT),
]

def c(mark, value):
    assert mark in MARKS, mark
    return {"value": value, "mark": mark}

# ---- Orca ----
orca = {
    "name": "Orca", "url": "https://onorca.dev", "category": "agent manager",
    "where_agents_run": "your machine + remote (SSH worktrees, headless Linux server, phone companion)",
    "license": "MIT, free", "checked_on": "2026-09-22 (installed + shipped-code read)",
    "source_note": "Source-verified: installed desktop + phone, shipped app.asar read, own docs.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "27+ agents / \"any CLI agent\""),
        "harness_count": c("info", "27+ (\"any CLI agent\")"),
        "needs_you_signal": c("yes", "Hook-driven + unread/attention state"),
        "approve_deny_prompt": c("unknown", "Not verified"),
        "conversation_gui_view": c("experimental", "Experimental Chat UI"),
        "real_terminal": c("yes", "Embedded GPU terminal, infinite splits, restored scrollback"),
        "session_organization": c("yes", "Worktree per task"),
        "usage_hud": c("yes", "Local state + account read, 6 providers, weekly resets, 80% warning chip"),
        "burn_rate_forecast": c("no", "Usage % and reset windows only, no burn rate or forecast"),
        "limit_governor": c("no", "None"),
        "vault_task_source": c("no", "Task providers are GitHub, GitLab, Linear, Jira only"),
        "issue_tracker_pipeline": c("yes", "GitHub, GitLab, Linear, Jira"),
        "worktree_management": c("yes", "Core: every task gets one, fan-out across N, SSH worktrees"),
        "planner_orchestrator": c("experimental", "Experimental Orchestration (CLI-driven), off by default"),
        "agent_to_agent_messaging": c("experimental", "Via experimental Orchestration"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("yes", "Browser and computer-use via its CLI"),
        "native_mobile_app": c("experimental", "Companion app, beta"),
        "phone_no_new_app": c("no", "Requires its own companion app"),
        "remote_ssh": c("yes", "SSH worktrees + Remote Server (beta)"),
        "account_hotswap": c("yes", "Hot-swap between Codex accounts without re-login"),
        "prompt_scratchpad": c("unknown", "Not verified"),
        "saved_prompt_library": c("unknown", "Not verified"),
        "appearance_control": c("yes", "Terminal font, theme, cursor and padding; imports Ghostty and Warp themes (docs, 2026-09-29)"),
        "extensibility": c("partial", "Scriptable CLI and installable agent skills; no plugin system or SDK (docs, 2026-09-29)"),
        "teams_multiuser": c("unknown", "Not verified"),
        "voice_input": c("unknown", "Not verified"),
        "license_cost": c("info", "MIT, free, uses your own subscriptions"),
        "app_shell": c("info", "Electron 43.7.5"),
        "languages": c("info", "TypeScript ~95%, JavaScript ~4%, Swift <1%"),
        "background_process": c("info", "Yes: a daemon-host process (docs/reference/windows-daemon-host-relocation.md)"),
        "download_size": c("info", "v1.4.216: 193 MB Windows setup.exe, 218-226 MB mac dmg, 207-209 MB Linux AppImage"),
        "ram_vs_claude_desktop": c("info", "Medium: about 30% (measured 2.3 GB with five projects and agents running)"),
        "runs_in_terminal": c("no", "Embeds its own GPU terminal instead"),
        "stability_maturity": c("info", "\"Features shipped daily\"; chat, orchestration and mobile are experimental"),
    },
}

# ---- VelaTerm ----
velaterm = {
    "name": "VelaTerm", "url": "https://velaterm.com", "category": "agent manager",
    "where_agents_run": "your machine + remote (SSH), plus browser pairing and a phone app",
    "license": "MIT, v0.2.x, free", "checked_on": "2026-09-28, author's posts only",
    "source_note": "Not independently verified — every cell comes from two of the developer's own launch posts, not the repo or site.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "8+ named agents (Claude Code, Codex, OpenCode, Copilot, Cursor, Antigravity, Cline, Pi) \"and more\""),
        "harness_count": c("info", "8+ (Claude Code, Codex, OpenCode, Copilot, Cursor, Antigravity, Cline, Pi...)"),
        "needs_you_signal": c("yes", "Live status plus phone push (underlying mechanism not stated)"),
        "approve_deny_prompt": c("yes", "\"Answer agents\" from the phone"),
        "conversation_gui_view": c("yes", "Default view, plus the same session's terminal view alongside it"),
        "real_terminal": c("yes", "Each session is a real PTY that keeps running in the background"),
        "session_organization": c("yes", "Projects, then nested groups to any depth, then sessions"),
        "usage_hud": c("yes", "Plan quota, context and tokens in its side panel (README, checked 2026-09-29)"),
        "burn_rate_forecast": c("undocumented", "Not mentioned in its launch posts"),
        "limit_governor": c("undocumented", "Not mentioned in its launch posts"),
        "vault_task_source": c("no", "Has a notes knowledge base, not a task queue"),
        "issue_tracker_pipeline": c("unknown", "Not claimed either way"),
        "worktree_management": c("yes", "Optional per launch: none, one shared worktree, or one per session"),
        "planner_orchestrator": c("yes", "Plan/Execute: a planner splits the task, you approve the split, executors build each part in parallel"),
        "agent_to_agent_messaging": c("yes", "Search another session's conversation, ask about it, or message/steer a running session, across providers"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("yes", "Save what a session learned; agents query it before acting; local code-graph queries with no model call"),
        "builtin_editors_browser": c("yes", "Markdown editor, code editor, image viewer, browser tab, also usable remotely"),
        "native_mobile_app": c("yes", "iOS/Android app with push notifications"),
        "phone_no_new_app": c("yes", "Any browser via an end-to-end-encrypted pairing link, no install"),
        "remote_ssh": c("yes", "SSH including editing remote files"),
        "account_hotswap": c("unknown", "Not claimed either way"),
        "prompt_scratchpad": c("unknown", "Not claimed either way"),
        "saved_prompt_library": c("unknown", "Not claimed either way"),
        "appearance_control": c("unknown", "Not claimed either way"),
        "extensibility": c("unknown", "Not claimed either way"),
        "teams_multiuser": c("partial", "Account device list"),
        "voice_input": c("unknown", "Not claimed either way"),
        "license_cost": c("info", "MIT, free, uses your own subscriptions"),
        "app_shell": c("info", "Tauri 2 (Rust + system WebView); repo also carries a secondary Electron shell, not the primary build"),
        "languages": c("info", "TypeScript ~46%, Rust ~39%, Python ~8%"),
        "background_process": c("unknown", "not verified: a minimal headless `vela-server` build exists but isn't documented as running alongside the desktop app"),
        "download_size": c("info", "v0.2.5: 59 MB Windows min-setup / 148 MB full-setup, 49-51 MB mac dmg"),
        "ram_vs_claude_desktop": c("info", "Small (estimate: Tauri app on the system WebView)"),
        "runs_in_terminal": c("no", "Own app; the Windows installer bundles Git Bash"),
        "stability_maturity": c("info", "v0.2.x, launched 2026-09-28, not independently verified"),
    },
}

# ---- Pantheon ----
herdr = {
    "name": "herdr", "url": "https://herdr.dev", "category": "agent manager",
    "where_agents_run": "your machine + saved SSH machines, in one window",
    "license": "Apache-2.0, free", "checked_on": "2026-09-28 (repo README, release assets, herdr.dev and its integrations docs)",
    "source_note": "Checked against its own README, latest release (v0.9.1), herdr.dev and the integrations docs. Not installed or run here.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Claude Code, Codex, Cursor, opencode, Grok and more; it owns their terminals rather than wrapping them"),
        "harness_count": c("info", "22 detected out of the box"),
        "needs_you_signal": c("partial", "Every pane marked working, blocked or idle, read from the screen (hooks are used only to restore sessions)"),
        "approve_deny_prompt": c("no", "Marks the pane blocked; you answer in the pane itself"),
        "conversation_gui_view": c("no", "Terminal panes only"),
        "real_terminal": c("yes", "Every agent runs in its own real pane"),
        "session_organization": c("yes", "Workspaces and split panes, with one agent list across local and SSH machines"),
        "prompt_scratchpad": c("undocumented", "Not mentioned in its docs"),
        "saved_prompt_library": c("undocumented", "Not mentioned in its docs"),
        "builtin_editors_browser": c("no", "Runs your tools in panes; no editor or browser of its own"),
        "appearance_control": c("partial", "Uses the terminal you already have; its own configuration file"),
        "usage_hud": c("no", "None in its docs or changelog (checked 2026-09-29); the rate-limit line in its demo is Claude Code's own status line"),
        "burn_rate_forecast": c("undocumented", "Not mentioned in its docs"),
        "limit_governor": c("undocumented", "Not mentioned in its docs"),
        "account_hotswap": c("undocumented", "Not mentioned in its docs"),
        "vault_task_source": c("no", "No task source"),
        "issue_tracker_pipeline": c("no", "None in its docs, changelog or code (checked 2026-09-29)"),
        "worktree_management": c("yes", "Creates, opens and removes worktrees from the sidebar or the herdr worktree command (changelog, checked 2026-09-29)"),
        "planner_orchestrator": c("partial", "No planner of its own, but agents can spawn panes and prompt each other through its CLI and socket API"),
        "agent_to_agent_messaging": c("yes", "Agents spawn panes, prompt each other and wait until another agent is really blocked (socket API + agent skill)"),
        "cross_provider_delegation": c("yes", "All agents in one list, local and remote"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "native_mobile_app": c("no", "None (a separate community macOS console, herdrm, exists)"),
        "phone_no_new_app": c("yes", "Any SSH app reattaches to the background server"),
        "remote_ssh": c("yes", "Saved SSH machines sit beside local ones with independent reconnects; a hosted option is announced"),
        "voice_input": c("undocumented", "Not mentioned in its docs"),
        "app_shell": c("info", "Terminal UI: one Rust binary, no Electron"),
        "languages": c("info", "Rust ~93%, Python ~3%"),
        "background_process": c("info", "Yes: a background server keeps terminals running after you close the client or lose SSH"),
        "download_size": c("info", "v0.9.1: 9 MB Windows zip, 20-22 MB macOS, 23-25 MB Linux"),
        "ram_vs_claude_desktop": c("info", "Tiny (estimate: terminal app, one small Rust binary)"),
        "runs_in_terminal": c("yes", "Runs in whatever terminal you already use"),
        "license_cost": c("info", "Apache-2.0, free, uses your own subscriptions"),
        "extensibility": c("yes", "Plugin marketplace plus a CLI and socket API"),
        "teams_multiuser": c("undocumented", "Not mentioned in its docs"),
        "stability_maturity": c("info", "v0.9.1, ~41k GitHub stars, fast-moving; Windows build is in beta"),
    },
}

pantheon = {
    "name": "Pantheon", "url": "https://github.com/dtiger1889-ops/pantheon", "category": "agent manager",
    "where_agents_run": "your machine (terminal-native, tmux-hosted; phone reaches it over an existing SSH tunnel)",
    "license": "MIT, free, your own subscriptions", "checked_on": "2026-09-28 (author's own build, cells refreshed for the 2026-09-22..27 builds)",
    "source_note": "Author's own project (open source, pre-release, published as-is). Scored by the same rules as every other row here, including its weak spots.",
    "is_authors_own": True,
    "features": {
        "multi_provider_supervision": c("yes", "Hooks-based"),
        "harness_count": c("info", "2 (Claude Code, Codex); local models planned"),
        "needs_you_signal": c("yes", "Exact: derived from hook events, not inferred from silence"),
        "approve_deny_prompt": c("partial", "Allow/deny/view a waiting prompt from the deck, built, not yet tested live"),
        "conversation_gui_view": c("partial", "Detail panel shows recent actions and the latest ask read from the transcript, not a full chat view"),
        "real_terminal": c("yes", "Clicking a session opens its own real tmux window"),
        "session_organization": c("yes", "Sidebar session list plus a live fleet table"),
        "usage_hud": c("yes", "Shipped, from local logs; reading the same account-usage numbers claude.ai shows is built, not yet tested live"),
        "burn_rate_forecast": c("partial", "Built, with ranges; not yet checked against real usage"),
        "limit_governor": c("partial", "Built: wind down near a limit, park, and resume after reset, plus limit hand-off to another provider and timed starts; not yet tested live, off by default"),
        "vault_task_source": c("yes", "Unique in this table: reads a personal notes vault directly as its live task source"),
        "issue_tracker_pipeline": c("no", "Deliberately absent; the notes vault is the tracker"),
        "worktree_management": c("no", "Agents use worktrees; the deck itself doesn't manage them"),
        "planner_orchestrator": c("planned", "Planning card built; dispatching from it is still greyed out"),
        "agent_to_agent_messaging": c("no", "None"),
        "cross_provider_delegation": c("yes", "Visible in the deck, with auto-fallback to console mode"),
        "always_on_assistant": c("partial", "Pinned Assistant window built; reachable from the phone over the existing remote-control link"),
        "knowledge_base": c("n/a", "Reads the vault only as a task list"),
        "builtin_editors_browser": c("partial", "A terminal editor pane is built"),
        "native_mobile_app": c("no", "Reuses a terminal app over an existing SSH tunnel at a narrower column width instead"),
        "phone_no_new_app": c("yes", "Reuses an existing terminal app and SSH tunnel already on the phone"),
        "remote_ssh": c("no", "None"),
        "account_hotswap": c("no", "None"),
        "prompt_scratchpad": c("yes", "Autosaved tabbed drafts, insert-without-send, slash completion"),
        "saved_prompt_library": c("planned", "Idea logged, not built"),
        "appearance_control": c("yes", "Unusual for this table: palette and per-token overrides write directly into the host terminal's own settings file"),
        "extensibility": c("no", "None"),
        "teams_multiuser": c("no", "Single-user by design"),
        "voice_input": c("no", "None"),
        "license_cost": c("info", "MIT, free; pre-release, published as-is; uses your own subscriptions"),
        "app_shell": c("info", "Terminal UI: Python 3.12 + Textual, running inside your existing terminal, no separate installer"),
        "languages": c("info", "Python (Textual TUI)"),
        "background_process": c("info", "Yes: a separate small Python usage-collector process alongside the Textual UI process"),
        "download_size": c("info", "No installer; runs from source (git clone + Python)"),
        "ram_vs_claude_desktop": c("info", "Tiny: about 1% (measured 77 MB)"),
        "runs_in_terminal": c("yes", "Runs inside the terminal you already have, under tmux"),
        "stability_maturity": c("info", "Personal, pre-release; its terminal-multiplexer server froze four times on one day (cause still open)"),
    },
}

# ---- Paseo ----
paseo = {
    "name": "Paseo", "url": "https://paseo.sh", "category": "agent manager",
    "where_agents_run": "your machine + cloud (self-hosted relay or Tailscale) + mobile + web",
    "license": "Apache-2.0, free", "checked_on": "2026-09-06 (source- and hands-on-verified)",
    "source_note": "Source-verified and installed/live-tested.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Deep per-provider SDK adapters"),
        "harness_count": c("info", "~39"),
        "needs_you_signal": c("yes", "SDK-level"),
        "approve_deny_prompt": c("yes", "Dedicated control-plane tool to respond to a permission request"),
        "conversation_gui_view": c("yes", "Shows messages, reasoning and tool calls as a readable timeline (changelog and docs, 2026-09-29)"),
        "real_terminal": c("yes", "Yes"),
        "session_organization": c("yes", "Per workspace"),
        "usage_hud": c("partial", "Risky reverse-engineered endpoint, display-only, no rate-limit mitigation seen"),
        "burn_rate_forecast": c("no", "None"),
        "limit_governor": c("no", "None"),
        "vault_task_source": c("no", "None"),
        "issue_tracker_pipeline": c("partial", "Mention its bot on a GitHub issue and an agent works it and can open a PR; GitHub only, no Jira, Linear or GitLab (Paseo Hub, 2026-09-29)"),
        "worktree_management": c("yes", "Mature: rollback, recovery, git-contention queue"),
        "planner_orchestrator": c("yes", "The agent itself gets control-plane tools such as creating agents and responding to permission requests"),
        "agent_to_agent_messaging": c("yes", "Via its control-plane tools"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("unknown", "Not stated in this doc"),
        "native_mobile_app": c("yes", "Native iOS and Android apps"),
        "phone_no_new_app": c("no", "Requires its own app"),
        "remote_ssh": c("yes", "Via its daemon"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-06)"),
        "prompt_scratchpad": c("no", "None"),
        "saved_prompt_library": c("no", "None"),
        "appearance_control": c("yes", "App theme, interface and code fonts, text sizes, content width (GitHub, 2026-09-29)"),
        "extensibility": c("yes", "MCP server, CLI and TypeScript SDK for automation"),
        "teams_multiuser": c("yes", "Teams plus triggers from GitHub/Slack/Discord"),
        "voice_input": c("yes", "Yes"),
        "license_cost": c("info", "Apache-2.0, free"),
        "app_shell": c("info", "Electron 44.2.0"),
        "languages": c("info", "TypeScript ~98%, JavaScript ~1%"),
        "background_process": c("info", "Yes: a Node daemon (package.json `dev:server` runs `PASEO_LISTEN=... dev-daemon.sh`)"),
        "download_size": c("info", "v0.10.0: 137 MB Windows Setup x64, 186 MB mac x64 dmg, 129 MB Linux .deb"),
        "ram_vs_claude_desktop": c("info", "Medium (estimate: Electron app plus a background server)"),
        "runs_in_terminal": c("no", "Own desktop/mobile/web app"),
        "stability_maturity": c("info", "Mature"),
    },
}

# ---- Kepler ----
kepler = {
    "name": "GitKraken Kepler", "url": "https://www.gitkraken.com/kepler", "category": "agent manager",
    "where_agents_run": "your machine (Win/Mac/Linux) plus SSH/WSL remote execution",
    "license": "commercial, free tier", "checked_on": "2026-09-06 (site-verified)",
    "source_note": "Site-verified, not installed.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Agent-agnostic model choice per task"),
        "harness_count": c("info", "\"Any agent\" (not counted)"),
        "needs_you_signal": c("yes", "Yes"),
        "approve_deny_prompt": c("unknown", "Not stated"),
        "conversation_gui_view": c("yes", "Agent Graph: live tree of every session, turn, tool call and subagent"),
        "real_terminal": c("unknown", "Not stated"),
        "session_organization": c("yes", "Three views of one fleet: live, kanban, dense list"),
        "usage_hud": c("no", "Org-level spend analytics, not a live burn view"),
        "burn_rate_forecast": c("no", "None"),
        "limit_governor": c("no", "None"),
        "vault_task_source": c("no", "None"),
        "issue_tracker_pipeline": c("yes", "Jira, Trello, GitHub, GitLab Issues, Linear"),
        "worktree_management": c("yes", "Parallel worktrees with per-branch diffs, plus setup hooks that run repo scripts before the agent starts"),
        "planner_orchestrator": c("undocumented", "Not in its feature list (checked 2026-09-06)"),
        "agent_to_agent_messaging": c("no", "None"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("yes", "Diffs plus in-app commit/PR"),
        "native_mobile_app": c("partial", "Mobile check-and-answer, not a full session manager"),
        "phone_no_new_app": c("no", "Requires its own app"),
        "remote_ssh": c("yes", "SSH/WSL remote execution"),
        "account_hotswap": c("undocumented", "Not in its feature list (checked 2026-09-06)"),
        "prompt_scratchpad": c("partial", "\"Actions\": saved one-click prompts"),
        "saved_prompt_library": c("yes", "Actions come with issue, diff and repo state pre-attached"),
        "appearance_control": c("yes", "Two themes, dark/light/system, terminal font and spacing (help docs, 2026-09-29)"),
        "extensibility": c("partial", "Custom Actions: your own prompt, agent and skill per action; no plugins, SDK or API (help docs, 2026-09-29)"),
        "teams_multiuser": c("yes", "Org-level analytics on agent spend"),
        "voice_input": c("no", "None"),
        "license_cost": c("info", "Commercial with a free tier"),
        "app_shell": c("unknown", "not verified: not stated on gitkraken.com/kepler or help.gitkraken.com; not extrapolated from GitKraken's separate main git client"),
        "languages": c("unknown", "not verified: closed source, no public repo"),
        "background_process": c("unknown", "not verified"),
        "download_size": c("unknown", "not verified: not stated on the vendor's pages"),
        "ram_vs_claude_desktop": c("unknown", "not verified: app shell unknown"),
        "runs_in_terminal": c("no", "Own desktop app"),
        "stability_maturity": c("info", "Commercial product"),
    },
}

# ---- AO ----
ao = {
    "name": "Agent Orchestrator (AO)", "url": "https://github.com/Untrivial-ai/agent-orchestrator", "category": "agent manager",
    "where_agents_run": "your machine + mobile companion (LAN/Tailscale)",
    "license": "Apache-2.0, free, ~12.5k stars", "checked_on": "2026-09-06 (site-verified)",
    "source_note": "Site-verified, not installed.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "25 harnesses, per-project defaults"),
        "harness_count": c("info", "25+"),
        "needs_you_signal": c("yes", "Escalates only what needs a human"),
        "approve_deny_prompt": c("yes", "Escalations to a human"),
        "conversation_gui_view": c("yes", "Yes"),
        "real_terminal": c("unknown", "Not stated"),
        "session_organization": c("yes", "Kanban board: Pending / Iterating / In Review / Ready-to-merge"),
        "usage_hud": c("no", "None"),
        "burn_rate_forecast": c("no", "None"),
        "limit_governor": c("no", "None"),
        "vault_task_source": c("no", "None"),
        "issue_tracker_pipeline": c("yes", "CI feedback loop: failed checks and review comments route back to the owning session until approved"),
        "worktree_management": c("yes", "Orchestrator spawns worktree workers per task"),
        "planner_orchestrator": c("yes", "Core: a per-project main orchestrator agent that plans and spawns worktree workers; orchestrators can message each other"),
        "agent_to_agent_messaging": c("yes", "Orchestrators message other orchestrators"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("unknown", "Not stated"),
        "native_mobile_app": c("yes", "Mobile companion with working/need-you/mergeable counts"),
        "phone_no_new_app": c("no", "Requires its own companion app"),
        "remote_ssh": c("unknown", "Not stated"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-06)"),
        "prompt_scratchpad": c("no", "None"),
        "saved_prompt_library": c("no", "None"),
        "appearance_control": c("partial", "Light/dark and named color themes; no font setting found (source, 2026-09-29)"),
        "extensibility": c("partial", "Scriptable ao CLI over a local API; its plugin system was removed in the Go rewrite (docs, 2026-09-29)"),
        "teams_multiuser": c("planned", "Organizations and sharing are built for AO Cloud, which is waitlist-only (site and repo, 2026-09-29)"),
        "voice_input": c("no", "None"),
        "license_cost": c("info", "Apache-2.0, free (license per GitHub, 2026-09-29)"),
        "app_shell": c("info", "Electron ^33.0.0 (frontend/package.json), plus a separate Go backend"),
        "languages": c("info", "Go ~59%, TypeScript ~38%"),
        "background_process": c("info", "Yes: a separate Go backend process (repo has a distinct backend/ Go module via go.work, apart from the Electron frontend/)"),
        "download_size": c("info", "v0.13.2-nightly: 136 MB Windows Setup.exe, 177-189 MB mac zip, 181 MB Linux AppImage"),
        "ram_vs_claude_desktop": c("info", "Medium (estimate: Electron app plus a Go backend)"),
        "runs_in_terminal": c("no", "Own desktop app"),
        "stability_maturity": c("info", "Active development"),
    },
}

# ---- Thinner §5 entries: unknown for every §6-style feature, only what §5 explicitly states filled in ----
def thin(name, url, category, where, license_, note, extra=None):
    t = {
        "name": name, "url": url, "category": category, "where_agents_run": where,
        "license": license_, "checked_on": "2026-09-07 (site/discussion pass only, no full comparison run)",
        "source_note": note, "is_authors_own": False,
        "features": {k: c("unknown", "not verified") for k, _, _, _ in FEATURES},
    }
    if extra:
        for k, v in extra.items():
            t["features"][k] = v
    return t

ccmanager = thin(
    "CCManager", "https://github.com/kbwo/ccmanager", "agent manager", "your machine (Linux/macOS)",
    "unknown", "Evaluated and not adopted (2026-09-01). Terminal session manager; state detection parses tool output rather than reading structured hook events.",
    {"needs_you_signal": c("partial", "Output-parsed, coarser than hook-event-based detection"),
     "runs_in_terminal": c("yes", "TUI session manager")},
)

opencove = thin(
    "OpenCove", "https://github.com/DeadWaveWave/opencove", "agent manager", "your machine (desktop)",
    "unknown", "Alpha desktop canvas of agent sessions, used here as a visual-design reference; its state-detection mechanism is undocumented.",
)

wave = thin(
    "Wave Terminal", "https://www.waveterm.dev", "agent manager", "your machine",
    "unknown", "Terminal with waiting/done badges built on the same hook events Pantheon uses; project has been quiet since 2026-04.",
    {"needs_you_signal": c("yes", "Waiting/done badges from the same hook events"),
     "runs_in_terminal": c("yes", "Yes, it is a terminal")},
)

vibekanban = thin(
    "vibe-kanban", "https://github.com/BloopAI/vibe-kanban", "agent manager", "your machine",
    "unknown", "Used here as a deliberate anti-example: functional but, in the compiler's words, \"boring af.\"",
    {"session_organization": c("yes", "Kanban board")},
)

t3code = thin(
    "T3 Code", "https://github.com/pingdotgg/t3code", "agent manager", "your machine + mobile",
    "MIT", "Site/discussion pass only, 2026-09-07. All-platform desktop plus mobile; standout feature is switching models mid-conversation.",
    {"native_mobile_app": c("yes", "Mobile app"),
     "license_cost": c("info", "MIT")},
)

superset = thin(
    "Superset", "https://superset.sh", "agent manager", "your machine (macOS, experimental Linux)",
    "Elastic-2.0", "Site/discussion pass only, 2026-09-07. Ships a TypeScript SDK and MCP server so agents can spawn agents.",
    {"extensibility": c("yes", "TypeScript SDK plus MCP server so agents can spawn agents"),
     "license_cost": c("info", "Elastic-2.0")},
)

conductor = thin(
    "Conductor", "https://www.conductor.build", "agent manager", "your machine (macOS only)",
    "proprietary", "Site/discussion pass only, 2026-09-07. Checkpoint/rollback called best-in-class.",
    {"license_cost": c("info", "Proprietary")},
)

jenny = thin(
    "Jenny", "https://github.com/SaltyPretz3l/jenny", "other tool we looked at", "your machine",
    "MIT", "A single-agent local-LLM chat app and IDE (llama.cpp / vLLM / any OpenAI-compatible endpoint), not a fleet manager, so it doesn't compete on most rows here. Recorded for its file-edit checkpointing, destructive-command approval, and a scratchpad/calendar the model can read and modify.",
    {"multi_provider_supervision": c("no", "Single local-model chat app, not a multi-agent fleet manager"),
     "license_cost": c("info", "MIT")},
)

micracode = thin(
    "micracode", "https://github.com/Jamessdevops/micracode", "other tool we looked at", "your machine",
    "open-source", "An AI web-app builder (Next.js, exports components as a zip), a different category from a fleet manager; recorded for completeness only. Local-model support is planned by its author.",
    {"multi_provider_supervision": c("no", "App builder, not a fleet/agent manager"),
     "license_cost": c("info", "open-source")},
)

teleclod = thin(
    "Teleclod", "https://teleclod.com", "agent manager", "cloud (Windows/macOS/Linux/Android/browser plus a Chrome extension)",
    "commercial (Free / EUR49 Pro / EUR99 Studio)", "Site-only pass, 2026-09-22; no independent verification found (no reviews, repo, or discussion beyond the single source comment).",
    {"multi_provider_supervision": c("yes", "Claims 14+ providers including Claude Code, Codex, OpenRouter, Ollama, Kimi"),
     "usage_hud": c("undocumented", "Not mentioned on its site"),
     "vault_task_source": c("no", "It is its own task store"),
     "limit_governor": c("no", "None"),
     "session_organization": c("yes", "Task list, kanban, and a global dashboard"),
     "runs_in_terminal": c("no", "Replaces the terminal outright"),
     "license_cost": c("info", "Closed-source, paid tiers")},
)

oyren = thin(
    "Oyren", "https://oyren.ai/development", "agent manager", "cloud (remote codespaces, deliberately not your machine)",
    "commercial, hourly", "Site-verified, 2026-09-23. Remote disposable codespaces with several agent CLIs preinstalled and tmux in every codespace.",
    {"multi_provider_supervision": c("yes", "Claude Code, Codex, Cursor, opencode, Qwen Code, DeepSeek Harness, Antigravity preinstalled"),
     "usage_hud": c("undocumented", "Not mentioned on its site"),
     "vault_task_source": c("no", "Its own kanban board is the tracker"),
     "limit_governor": c("partial", "A blocked card emails the human a specific question and resumes on reply, but only for one card, not a whole session against a usage window"),
     "issue_tracker_pipeline": c("yes", "Its own kanban board with an importance/urgency matrix and calendar/milestone views, read and written by agents over its own MCP server"),
     "builtin_editors_browser": c("yes", "Streamed VS Code/Zed IDE plus a Playwright-driven built-in browser"),
     "remote_ssh": c("n/a", "Hosted service: it already is the remote machine"),
     "app_shell": c("info", "Hosted cloud service, browser-based, no local install (vendor: \"VS Code runs as web app in your browser while Zed editor is streamed\")"),
     "background_process": c("n/a", "Hosted service: nothing runs on your machine"),
     "ram_vs_claude_desktop": c("info", "Runs in the cloud (local cost: a browser tab)"),
     "runs_in_terminal": c("no", "Cloud codespace, not a local terminal tool"),
     "license_cost": c("info", "Commercial: hourly compute plus an optional credit wallet")},
)

# ---- Added 2026-09-29 with a research pass each; sources in project_pantheon/archive/research_raw/2026-09-29-new-agent-managers/ ----
# Research entry for Google Antigravity 2.0 (https://antigravity.google), checked 2026-09-29.
# Shape matches the orca/ao entries in portfolio_repos/agent-deck-comparison/tools/build_data.py.
# Findings and sources: project_pantheon/archive/research_raw/2026-09-29-new-agent-managers/antigravity.md
antigravity = {
    "name": "Google Antigravity", "url": "https://antigravity.google", "category": "agent manager",
    "where_agents_run": "your machine (projects, local folders or git worktrees, optional WSL connection on Windows), driven from any browser or phone through its Remote Control web page",
    "license": "Proprietary, closed source; free tier plus paid Google AI plans", "checked_on": "2026-09-29 (docs/site pass)",
    "source_note": "Docs-verified: official docs, changelog, launch blog and download page read; installer sizes and app shell read from the v2.18.1 downloads; not installed or run.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("no", "Runs only its own Antigravity agent. You can switch that agent's model between Gemini, Claude Sonnet and Opus 4.6, and GPT-OSS 120B, but it does not drive Claude Code, Codex or other coding tools (models and overview docs, 2026-09-29)"),
        "harness_count": c("info", "1: its own agent, with a model picker (Gemini 3.x, Claude Sonnet 4.6, Claude Opus 4.6, GPT-OSS 120B) (models docs, 2026-09-29)"),
        "needs_you_signal": c("yes", "A desktop notification and a bell chime when a task finishes or needs you, plus browser push notifications through Remote Control (settings and remote-control docs, 2026-09-29)"),
        "approve_deny_prompt": c("yes", "An approval card in the app for commands, files, web and tool calls, which you can widen before allowing; also answerable from the Remote Control web page on your phone (permissions and remote-control docs, 2026-09-29)"),
        "cross_provider_delegation": c("partial", "Has: subagents the main agent starts show as live cards inside the same conversation. Lacks: every hand-off is between its own agents, not to other coding tools (changelog v2.16.0 and launch blog, 2026-09-29)"),
        "always_on_assistant": c("undocumented", "Not in its docs (checked 2026-09-29); it has scheduled tasks and a background Remote Control service, but no standing assistant session"),
        "conversation_gui_view": c("yes", "Each agent session is a chat conversation with plans and other work shown as artifacts (overview and artifacts docs, 2026-09-29)"),
        "real_terminal": c("partial", "Has: a built-in terminal panel in the sidebar (Ctrl or Cmd plus backtick) with split layouts. Lacks: the agent session itself is a chat, not a terminal you drop into (features docs and changelog v2.12.0, 2026-09-29)"),
        "session_organization": c("info", "Projects in a sidebar, each holding conversations; each conversation works in the local folder or a new git worktree; archived conversations can be filtered (projects docs and changelog v2.18.1, 2026-09-29)"),
        "prompt_scratchpad": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "saved_prompt_library": c("undocumented", "Not in its docs (checked 2026-09-29); it saves reusable rules and skills, not saved prompts"),
        "builtin_editors_browser": c("partial", "Has: a built-in browser the agent drives, with Chrome DevTools and video recording, plus diff viewers. Lacks: no code editor in the 2.0 app, by design; editing lives in the separate Antigravity IDE (features docs and launch blog, 2026-09-29)"),
        "appearance_control": c("partial", "Has: dark, light or automatic theme. Lacks: no font setting in its docs (features docs, 2026-09-29)"),
        "usage_hud": c("yes", "Shows its own quota: weekly and five-hour limits remaining as percentages, separately for Gemini and for Claude and GPT models (models docs, 2026-09-29)"),
        "burn_rate_forecast": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "limit_governor": c("undocumented", "Not in its docs (checked 2026-09-29); a setting chooses between spending paid credits or waiting for the quota to refresh, with no mention of pausing and resuming work"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-29); settings only say they manage sign-in sessions"),
        "vault_task_source": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "issue_tracker_pipeline": c("undocumented", "Not in its docs (checked 2026-09-29); its git panel can commit and push a branch, but nothing picks up issues"),
        "worktree_management": c("yes", "A conversation can run in a new isolated git worktree so agents work in parallel (projects docs and FAQ, 2026-09-29)"),
        "planner_orchestrator": c("yes", "The main agent splits work into subagents on its own; a preview teamwork mode runs a coordinated team of planner, worker and checker agents (launch blog and teamwork docs, 2026-09-29)"),
        "agent_to_agent_messaging": c("experimental", "In the preview teamwork mode, agents pass work to each other through shared artifacts; background helper processes can also message conversations through its agentapi tool (teamwork and sidecars docs, 2026-09-29)"),
        "knowledge_base": c("partial", "Has: saved rules and skills, and a Documents section for files such as Google Drive, PDF and Office documents. Lacks: no searchable notes store for agents in its docs (skills docs and changelog v2.13.0, 2026-09-29)"),
        "native_mobile_app": c("no", "No phone app; phone access is the Remote Control web page, which can be added to the home screen as a web app for push notifications (remote-control docs, 2026-09-29)"),
        "phone_no_new_app": c("yes", "Sign in to the Remote Control page in any phone browser to watch sessions, send prompts and answer approvals (remote-control docs, 2026-09-29)"),
        "remote_ssh": c("partial", "Has: its command-line version can run on a machine you reach over SSH, and the desktop app can connect to a WSL Linux install. Lacks: no SSH-remote mode for the desktop app in its docs (CLI voice docs and changelog v2.16.0, 2026-09-29)"),
        "voice_input": c("yes", "Built-in live dictation with cleanup of filler words, toggled with Ctrl+M (features docs, 2026-09-29)"),
        "os": c("info", "macOS 12 or later (Apple Silicon and Intel), Windows 10 or later (x64 and ARM64), Linux x64 and ARM64 (glibc 2.28 or later); plus any browser or phone through Remote Control (getting-started and remote-control docs, 2026-09-29)"),
        "app_shell": c("info", "Electron (the v2.18.1 Linux package ships Electron and Chromium license files, checked 2026-09-29)"),
        "languages": c("n/a", "Closed source: no public repo for the app to break down (checked 2026-09-29)"),
        "background_process": c("info", "Optional: a headless Remote Control service that keeps sessions reachable, plus helper processes (sidecars) you define, which it launches and restarts (remote-control and sidecars docs, 2026-09-29)"),
        "download_size": c("info", "v2.18.1: 164 MB Windows x64 installer (154 MB ARM64), 206-220 MB mac dmg, 178-180 MB Linux tar.gz (download server, 2026-09-29)"),
        "ram_vs_claude_desktop": c("info", "Medium (estimate: Electron app)"),
        "runs_in_terminal": c("partial", "Has: its separate command-line version (agy) runs in your own terminal. Lacks: the 2.0 desktop app is its own window (getting-started docs, 2026-09-29)"),
        "license_cost": c("info", "Proprietary. Free tier with a weekly quota; higher quotas through Google AI Pro and Ultra (Ultra $100 or $200 a month at launch); company use through Gemini Enterprise (plans docs and TechCrunch, 2026-09-29)"),
        "extensibility": c("yes", "Plugins from its Marketplace (skills, rules, subagents, MCP servers, hooks), JSON hooks, and a Python SDK in preview (marketplace, hooks and home docs, 2026-09-29)"),
        "teams_multiuser": c("partial", "Has: company sign-in, license assignment and central admin controls through Gemini Enterprise. Lacks: no shared workspaces or collaboration between people in its docs (enterprise docs, 2026-09-29)"),
        "stability_maturity": c("info", "Version 2.18.1 (2026-09-28); 2.0 launched at Google I/O on 2026-05-19, with releases several times a month; the teamwork mode and SDK are previews (changelog and TechCrunch, 2026-09-29)"),
    },
}

# ---- Pane (greenfield-inc/Pane, "RunPane by Dcouple") ----
# Findings + sources: project_pantheon/archive/research_raw/2026-09-29-new-agent-managers/pane.md
pane = {
    "name": "Pane", "url": "https://github.com/greenfield-inc/Pane", "category": "agent manager",
    "where_agents_run": "your machine + a self-hosted remote host (VM, server, WSL, Mac mini) over Tailscale or SSH; phone or browser through its web app",
    "license": "AGPL-3.0, free", "checked_on": "2026-09-29 (repo/docs pass)",
    "source_note": "Checked against its README, docs/ folder, source code, latest release (v2.4.138) and runpane.com. Not installed or run here.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Runs any terminal agent side by side; Claude Code, Codex and Cursor Agent get built-in status reading (README, 2026-09-29)"),
        "harness_count": c("info", "Any command-line agent; 3 with built-in status detection (Claude Code, Codex, Cursor Agent), Aider and Goose named as working (README and source, 2026-09-29)"),
        "needs_you_signal": c("yes", "Status dots per pane (red when blocked on approval, amber while working, a done cue), read from each agent's screen; phone push on a blocked turn or finish (README and docs, 2026-09-29)"),
        "approve_deny_prompt": c("partial", "Has an allow/deny dialog on desktop and remote clients for Claude Code when a pane runs in approve mode; lacks it for other agents, and the default mode skips permission prompts (source, 2026-09-29)"),
        "cross_provider_delegation": c("yes", "Pane Chat hands work to Claude, Codex or Cursor panes and lists them under its Session in the sidebar (README and docs, 2026-09-29)"),
        "always_on_assistant": c("yes", "Pane Chat: a standing orchestrator chat not tied to any repository, kept as named Sessions and reachable from the phone (README and docs, 2026-09-29)"),
        "conversation_gui_view": c("no", "Terminals only by design (\"just terminals, no abstractions\"); a command can read an agent's last reply from its transcript (README and changelog, 2026-09-29)"),
        "real_terminal": c("yes", "Every agent runs in a real terminal drawn with xterm.js, 50,000 lines of scrollback (README, 2026-09-29)"),
        "session_organization": c("yes", "Projects, then panes (one git worktree each), then tabs; Sessions group related panes (README and docs, 2026-09-29)"),
        "prompt_scratchpad": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "saved_prompt_library": c("partial", "Has saved text snippets pasted with a keyboard shortcut; lacks context attached to a saved prompt (README, 2026-09-29)"),
        "builtin_editors_browser": c("yes", "Browser tab, file explorer, code editor (Monaco), diff viewer and git tree (README and source, 2026-09-29)"),
        "appearance_control": c("yes", "Light and dark palettes that follow the system or stay fixed, plus terminal font family and size (docs and source, 2026-09-29)"),
        "usage_hud": c("partial", "Has token and estimated-cost totals per pane from local Claude and Codex logs, and plan limits with reset times for Codex; lacks plan limits for Claude (source, 2026-09-29)"),
        "burn_rate_forecast": c("no", "Shows current limit use and reset time only, no rate or forecast (source, 2026-09-29)"),
        "limit_governor": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "vault_task_source": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "issue_tracker_pipeline": c("partial", "Has pull request watching (conflicts, checks, merged) through the GitHub command-line tool and lets an agent open a pane per issue; lacks its own tracker connection, leaving GitHub, Linear and Jira to the agents' own tools by design (README and changelog, 2026-09-29)"),
        "worktree_management": c("yes", "Creates a worktree per pane and cleans it up on delete; rebase, squash and merge from the keyboard (README, 2026-09-29)"),
        "planner_orchestrator": c("yes", "Pane Chat turns a goal into tickets or briefs and starts agents in panes to do them (README, 2026-09-29)"),
        "agent_to_agent_messaging": c("yes", "Agents start, check on and send follow-ups to other panes through its MCP server and command-line tool; @mention pulls another terminal's output (README, 2026-09-29)"),
        "knowledge_base": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "native_mobile_app": c("experimental", "iOS and Android companion in the repo with a TestFlight test build; not yet in the App Store or Play Store (docs and open pull requests 740 and 748, 2026-09-29)"),
        "phone_no_new_app": c("yes", "Browser web app at runpane.com/app, paired with a connection code; the phone must be on the same Tailscale network or use an SSH tunnel (README, 2026-09-29)"),
        "remote_ssh": c("yes", "Remote Pane: agents, terminals, files and git run on another machine over Tailscale or SSH (README, 2026-09-29)"),
        "voice_input": c("partial", "Has dictation in the phone and browser client using your own transcription service keys; lacks it in the desktop app (docs and source, 2026-09-29)"),
        "os": c("info", "Windows, macOS, Linux (x64 and ARM64 each); phone or tablet through the browser web app (release files and README, 2026-09-29)"),
        "app_shell": c("info", "Electron 41.10.3 (package.json, 2026-09-29)"),
        "languages": c("info", "TypeScript ~84%, Python ~7% (GitHub, 2026-09-29)"),
        "background_process": c("info", "Yes: a separate terminal-host process started by the app; a remote host runs Pane as a background service (source and docs, 2026-09-29)"),
        "download_size": c("info", "v2.4.138: 115 MB Windows x64 installer, 133-142 MB mac dmg, 107 MB Linux .deb / 140 MB AppImage (GitHub release, 2026-09-29)"),
        "ram_vs_claude_desktop": c("info", "Medium (estimate: Electron app plus a separate terminal-host process)"),
        "runs_in_terminal": c("no", "Own desktop app with its own terminals (README, 2026-09-29)"),
        "license_cost": c("info", "AGPL-3.0, free, no paid plan; uses your own subscriptions (LICENSE and runpane.com pricing, 2026-09-29)"),
        "extensibility": c("partial", "Has a scriptable command-line tool, a documented command contract and an MCP server; lacks a plugin system or SDK (README, 2026-09-29)"),
        "teams_multiuser": c("undocumented", "Not in its docs (checked 2026-09-29); the README names teams only as an audience"),
        "stability_maturity": c("info", "v2.4.138 released 2026-09-29, repo started 2026-02-27, ~500 GitHub stars, frequent releases (GitHub, 2026-09-29)"),
    },
}

claudedesktop = {
    "name": "Claude Desktop", "url": "https://claude.com/download", "category": "agent manager",
    "where_agents_run": "your machine (local, SSH, or WSL sessions) + Anthropic-managed cloud sessions; your phone reaches it through Dispatch and the Claude mobile app",
    "license": "Subscription: Pro $17-20/mo, Max $100-200/mo, Team $20-100/seat/mo (5-seat minimum), Enterprise $20/seat/mo plus API-rate usage",
    "checked_on": "2026-09-29 (docs pass)",
    "source_note": "Checked against code.claude.com/docs/en/desktop (the Code tab reference), support.claude.com (Cowork, install, voice), and claude.com/pricing. Not installed or run here.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("partial", "Natively runs only Claude Code sessions (local, cloud, SSH, WSL). Other coding agents such as Codex are reachable only through unofficial community MCP plugins/servers (e.g. a third-party \"codex\" plugin or an npm codex-mcp-server), not an Anthropic-built connector (GitHub plugin listings, checked 2026-09-29)"),
        "harness_count": c("info", "1 built in (Claude Code). Community MCP plugins can bridge to the Codex CLI, but that bridge is not a documented, Anthropic-supported integration (docs pass, 2026-09-29)"),
        "needs_you_signal": c("yes", "Sends a desktop OS notification when a Code session finishes a task you aren't viewing; Dispatch also sends a push notification to your phone when a session finishes or needs your approval (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "approve_deny_prompt": c("yes", "Permission prompts appear in the session, and Dispatch pushes them to your phone; approvals for Dispatch-spawned sessions expire after 30 minutes instead of lasting the whole session (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "cross_provider_delegation": c("partial", "Has: Dispatch hands tasks to Code sessions that show in the same sidebar. Lacks: every hand-off is between Claude sessions, not other coding tools (docs, 2026-09-29)"),
        "always_on_assistant": c("yes", "Dispatch is a persistent conversation living in the Cowork tab that you can message any time; it decides whether a task stays in Cowork or spawns a Code session (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "conversation_gui_view": c("yes", "Normal, Thinking, and Verbose transcript view modes read a session as a conversation with tool calls collapsed into summaries (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "real_terminal": c("yes", "Integrated terminal pane opens in the session's working directory and shares its environment with Claude; local sessions only (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "session_organization": c("yes", "Sidebar session list, filterable by status/project/environment and groupable by project, plus an optional Git worktree per session (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "prompt_scratchpad": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "saved_prompt_library": c("undocumented", "Not in its docs (checked 2026-09-29); slash commands and skills cover reusable workflows but the docs don't describe a saved-prompt library with context pre-attached"),
        "builtin_editors_browser": c("yes", "Ships its own file editor pane and a tabbed Browser pane with a clean, separate browser profile for previewing and verifying your app (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "appearance_control": c("partial", "Has a light/dark theme toggle only; no font control in the native desktop app, unlike claude.ai's own Chat font options, and font/accent-color customization is an open feature request (support.claude.com + open GitHub issues, checked 2026-09-29)"),
        "usage_hud": c("yes", "A usage ring next to the model picker shows context usage for the current session and plan usage for the period, shared across every Claude Code surface (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "burn_rate_forecast": c("undocumented", "Not in its docs (checked 2026-09-29): the usage ring shows current usage, not a burn rate or time-to-limit"),
        "limit_governor": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "vault_task_source": c("no", "Tasks come from chat prompts and Dispatch messages, not a personal notes vault (docs, 2026-09-29)"),
        "issue_tracker_pipeline": c("partial", "Connects to GitHub, Linear, and other trackers as connectors, and once a PR is open it can auto-fix failing CI and auto-merge, but the docs don't describe an automatic issue-to-PR pipeline the way a dedicated tracker connector does (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "worktree_management": c("yes", "Optional Git worktree per session, stored under .claude/worktrees/ by default with a configurable location and branch prefix (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "planner_orchestrator": c("partial", "Dynamic workflows run multi-step work inside one session, and Claude can spin off a suggested task into a new session as a task chip, but there's no dedicated planner that splits one goal across several agents up front (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "agent_to_agent_messaging": c("yes", "Claude can list, check on, message, and archive your other Code tab sessions (\"work across sessions\"); cross-session messaging also reaches terminal CLI sessions (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "knowledge_base": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "native_mobile_app": c("yes", "The Claude iOS/Android app can view and steer cloud sessions and Dispatch tasks, and receives Dispatch push notifications (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "phone_no_new_app": c("no", "Requires installing the Claude mobile app; no route through tools you already have is documented (docs, 2026-09-29)"),
        "remote_ssh": c("yes", "SSH sessions run Claude Code on a remote Linux or macOS machine that Desktop installs on first connect; support permission modes, connectors, plugins, and MCP servers (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "voice_input": c("partial", "Quick Entry voice dictation (press Caps Lock, real-time transcription) is macOS-only and needs macOS 14 or later; not available on Windows Desktop (support.claude.com, checked 2026-09-29)"),
        "os": c("info", "macOS 11+; Windows 10+ (x64 and ARM64); Linux beta (Ubuntu 22.04+ and other apt-based distributions, x64/arm64) (support.claude.com, 2026-09-29)"),
        "app_shell": c("info", "Electron (exact bundled version not published in official docs; not independently confirmed)"),
        "languages": c("n/a", "Closed source: no public repo to measure"),
        "background_process": c("info", "Yes: Cowork starts a virtual machine alongside the app (measured 2026-09-28)"),
        "download_size": c("info", "Not published by Anthropic; the Windows installer is a small bootstrapper that downloads the app (checked 2026-09-29)"),
        "ram_vs_claude_desktop": c("info", "The reference: about 7.5 GB measured on one Windows PC, 2026-09-28 (about 3.7 GB app across 24 processes plus about 4 GB Cowork virtual machine)"),
        "runs_in_terminal": c("no", "Its own desktop app window; it embeds a terminal pane but is not itself a terminal tool (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "license_cost": c("info", "Subscription only: Pro $17-20/mo, Max $100-200/mo (5x or 20x Pro usage), Team $20-100/seat/mo (5-seat minimum), Enterprise $20/seat/mo plus API-rate usage; Claude Code is included in every paid plan (claude.com/pricing, checked 2026-09-29)"),
        "extensibility": c("yes", "Connectors (MCP servers with a graphical setup flow), a plugin manager for skills/agents/hooks/MCP/LSP configs, and manual MCP server configuration via settings files (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "teams_multiuser": c("yes", "Team and Enterprise plans add SSO, managed settings, an admin console, and org-wide connector/plugin/SSH controls (code.claude.com/docs/en/desktop, 2026-09-29)"),
        "stability_maturity": c("info", "GA product on macOS and Windows; the Linux desktop app is beta (no Computer use yet); Computer use and Cowork are labeled research preview features (code.claude.com/docs/en/desktop and support.claude.com, checked 2026-09-29)"),
    },
}

# Research entry for agent-manager (https://github.com/YoanWai/agent-manager), checked 2026-09-29.
# Shape matches the orca/ao entries in portfolio_repos/agent-deck-comparison/tools/build_data.py.
# Findings and sources: project_pantheon/archive/research_raw/2026-09-29-new-agent-managers/agent-manager.md
agentmanager = {
    "name": "agent-manager", "url": "https://github.com/YoanWai/agent-manager", "category": "agent manager",
    "where_agents_run": "your machine, each agent in its own tmux session (Windows only inside WSL2)",
    "license": "Apache-2.0, free", "checked_on": "2026-09-29 (repo pass)",
    "source_note": "Repo-verified: README, docs/, release assets, go.mod and source read; not installed.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Nine coding agents run side by side in one list, each in its own tmux session (README, 2026-09-29)"),
        "harness_count": c("info", "9: Claude Code, Codex, OpenCode, Grok Build, Gemini CLI, Pi, Command Code, Hermes Agent, Muse Code, plus plain shell tabs (README, 2026-09-29)"),
        "needs_you_signal": c("yes", "A waiting mark on the session row, an attention filter, and a desktop notification when a session starts waiting or errors (docs/usage.md Status and Notifications, 2026-09-29)"),
        "approve_deny_prompt": c("partial", "Has: the waiting permission prompt shows in the preview, and you can answer it by typing into the session from the list without attaching. Lacks: no dedicated allow or deny control, and no phone route (README and docs/usage.md, 2026-09-29)"),
        "cross_provider_delegation": c("yes", "An agent can start another agent on any supported CLI; the new session appears in the same list (docs/usage.md, MCP section, 2026-09-29)"),
        "always_on_assistant": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "conversation_gui_view": c("partial", "Has: list rows can show your last message and the agent's last reply. Lacks: no full conversation view; sessions are read as their terminal (docs/usage.md Full-screen sessions, 2026-09-29)"),
        "real_terminal": c("yes", "Focus a session in place or attach to its real tmux session full screen (docs/usage.md Keys, 2026-09-29)"),
        "session_organization": c("yes", "Folding tree of nested groups, drag to reorder, optional git worktree per session, shell tabs nested under agents (docs/usage.md Groups, 2026-09-29)"),
        "prompt_scratchpad": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "saved_prompt_library": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "builtin_editors_browser": c("partial", "Has: a built-in diff review screen with line comments sent back to the agent. Lacks: no editor or browser of its own; it opens your editor and your browser (docs/usage.md, 2026-09-29)"),
        "appearance_control": c("partial", "Has: 17 color themes, can follow the system light or dark mode, two list densities, split or full-screen layout. Lacks: no font setting; the font is your terminal's (docs/usage.md Themes, 2026-09-29)"),
        "usage_hud": c("no", "README says \"Not here yet: cost tracking\"; its stats show only computer CPU, memory and disk (README and docs/usage.md Stats, 2026-09-29)"),
        "burn_rate_forecast": c("no", "No usage tracking at all, so no forecast (README, 2026-09-29)"),
        "limit_governor": c("no", "A rate-limit banner only marks the session as errored; nothing pauses or resumes work (docs/usage.md Status, 2026-09-29)"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "vault_task_source": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "issue_tracker_pipeline": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "worktree_management": c("yes", "Optional git worktree and branch per session, on the new-session form or as a default; deleting the session removes a clean worktree and its branch (docs/usage.md Worktree sessions, 2026-09-29)"),
        "planner_orchestrator": c("partial", "Has: agents can start other agents, share a task list with claim and finish, and wait on each other. Lacks: no built-in planner that splits a goal; the agent itself decides (docs/usage.md MCP section, 2026-09-29)"),
        "agent_to_agent_messaging": c("yes", "Agents send each other queued messages and read each other's screens through its built-in MCP server (docs/usage.md Messages between agents, 2026-09-29)"),
        "knowledge_base": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "native_mobile_app": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "phone_no_new_app": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "remote_ssh": c("partial", "Has: runs on a remote machine you log into over SSH, with notifications and links still reaching you. Lacks: no way to manage another machine's sessions from your own (docs/usage.md Notifications, 2026-09-29)"),
        "voice_input": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "os": c("info", "macOS and Linux; Windows only inside WSL2 (README and docs/install.md, 2026-09-29)"),
        "app_shell": c("info", "Terminal UI: Bubble Tea 1.3.10 in Go, over tmux 3.1+ (go.mod, 2026-09-29)"),
        "languages": c("info", "Go ~99.8%, Shell ~0.2% (GitHub languages, 2026-09-29)"),
        "background_process": c("info", "Its own private tmux server keeps sessions running after the manager quits; no separate daemon of its own (README, 2026-09-29)"),
        "download_size": c("info", "v0.39.0: 7.7-8.3 MB Linux archive, 8.2-8.7 MB macOS archive; no Windows file (GitHub release, 2026-09-29)"),
        "ram_vs_claude_desktop": c("info", "Tiny (estimate: one Go terminal program plus tmux)"),
        "runs_in_terminal": c("yes", "A terminal program you start with agent-manager in your own terminal (README, 2026-09-29)"),
        "license_cost": c("info", "Apache-2.0, free; runs your own installed CLIs on your own subscriptions (README, 2026-09-29)"),
        "extensibility": c("partial", "Has: a built-in MCP server and command-line subcommands that agents and scripts can drive. Lacks: no plugin system; support for a new CLI is a feature request (docs/usage.md and docs/configuration.md, 2026-09-29)"),
        "teams_multiuser": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "stability_maturity": c("info", "Public since July 2026, 540 stars, v0.39.0 released 2026-09-26 with releases most weeks; one navigation feature marked beta (GitHub, 2026-09-29)"),
    },
}

# ---- VibeTree ----
vibetree = {
    "name": "VibeTree", "url": "https://github.com/sahithvibudhi/vibe-tree", "category": "agent manager",
    "where_agents_run": "your machine, or a server you run yourself (home server or VM) reached from any browser or phone",
    "license": "MIT, free", "checked_on": "2026-09-29 (repo pass)",
    "source_note": "Repo-verified: README, docs site, v0.2.0 release notes and source read at commit f889077 (2026-07-25); not installed.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "Any terminal program runs in each worktree's terminal: Claude Code, Codex CLI, Gemini CLI, Aider, opencode named (README, 2026-09-29)"),
        "harness_count": c("info", "Any terminal program; 5 named: Claude Code, Codex CLI, Gemini CLI, Aider, opencode (README, 2026-09-29)"),
        "needs_you_signal": c("yes", "Sidebar shows working, needs input or done per worktree, plays a ding, and sends desktop notifications (README and v0.2.0 release notes, 2026-09-29)"),
        "approve_deny_prompt": c("partial", "Spots yes/no and choice prompts in the terminal and flags the worktree as needing input; no allow or deny buttons, you answer by typing in that agent's terminal, which also works from the phone web app (source: packages/core/src/utils/agent-activity.ts, 2026-09-29)"),
        "cross_provider_delegation": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "always_on_assistant": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "conversation_gui_view": c("no", "Sessions show only as terminals; the app has terminal, diff and browser preview panes but no chat view (README and source tree, 2026-09-29)"),
        "real_terminal": c("yes", "Each worktree gets a persistent terminal with splits and search; scrollback survives reloads and reconnects (README, 2026-09-29)"),
        "session_organization": c("yes", "Projects open as tabs; each project has a sidebar list of worktrees, each with its own terminals and live status (docs, 2026-09-29)"),
        "prompt_scratchpad": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "saved_prompt_library": c("undocumented", "Not in its docs (checked 2026-09-29); it has a one-click agent launch command, not saved prompts"),
        "builtin_editors_browser": c("partial", "Has a browser preview pane for dev servers and a diff viewer; lacks a code editor, and opens files in your installed Cursor or VS Code instead (README and source: apps/desktop/src/main/ide-detector.ts, 2026-09-29)"),
        "appearance_control": c("partial", "Has terminal font, font size and cursor blink settings; lacks a theme picker, light or dark just follows your system setting (source: apps/desktop/src/main/terminal-settings.ts and ipc-handlers.ts, 2026-09-29)"),
        "usage_hud": c("no", "No usage or limit tracking anywhere in its source; its Stats window lists terminal processes only (source search, 2026-09-29)"),
        "burn_rate_forecast": c("no", "No usage tracking in its source (source search, 2026-09-29)"),
        "limit_governor": c("no", "No usage-limit handling in its source; its scheduler only re-sends a typed command after a set delay (source search, 2026-09-29)"),
        "account_hotswap": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "vault_task_source": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "issue_tracker_pipeline": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "worktree_management": c("yes", "Core: one git worktree and branch per task, created and deleted from the app or its CLI, with setup and cleanup hook scripts (README and docs, 2026-09-29)"),
        "planner_orchestrator": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "agent_to_agent_messaging": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "knowledge_base": c("undocumented", "Not in its docs (checked 2026-09-29)"),
        "native_mobile_app": c("no", "No store app; the phone route is its installable web app (docs, 2026-09-29)"),
        "phone_no_new_app": c("yes", "Open the server address in the phone's browser, paired by QR code, over your home network or Tailscale; optionally install it as a web app (docs, 2026-09-29)"),
        "remote_ssh": c("partial", "Has a standalone server you install on another machine and reach from a browser; lacks any SSH connection mode (docs: server page, 2026-09-29)"),
        "voice_input": c("no", "No speech or dictation code in its source (source search, 2026-09-29)"),
        "os": c("info", "Windows, macOS (Intel and Apple Silicon, not notarized), Linux (AppImage, deb); plus any browser or phone through its standalone server (v0.2.0 release and README, 2026-09-29)"),
        "app_shell": c("info", "Electron 38.0.0 (apps/desktop/package.json), plus a React web app served by the same Node server"),
        "languages": c("info", "TypeScript ~89%, HTML ~8% (GitHub languages, 2026-09-29)"),
        "background_process": c("info", "Desktop: no, its server runs inside the app's own main process on a local-only port (ARCHITECTURE.md); browser and phone use need a separate standalone Node server"),
        "download_size": c("info", "v0.2.0: 98 MB Windows Setup.exe, 121-126 MB mac dmg, 127 MB Linux AppImage, 85 MB deb (GitHub release, 2026-09-29)"),
        "ram_vs_claude_desktop": c("info", "Small (estimate: one Electron app with its server in the same process)"),
        "runs_in_terminal": c("partial", "Its command-line tool lists worktrees, shows agent states and starts agents from your own terminal; the terminals themselves live in its desktop or web app (docs: CLI page, 2026-09-29)"),
        "license_cost": c("info", "MIT, free; no cloud component and no telemetry (license per GitHub and site FAQ, 2026-09-29)"),
        "extensibility": c("partial", "Has worktree hook scripts and a command-line tool that talks to its server; lacks a plugin system or SDK (docs, 2026-09-29)"),
        "teams_multiuser": c("partial", "Has project settings and hook scripts you commit to share with a team; lacks user accounts, the server has one shared login (docs: config page, 2026-09-29)"),
        "stability_maturity": c("info", "Early: v0.2.0 released 2026-07-24, two releases in total, last push 2026-07-25, about 270 stars, mac builds not notarized (GitHub, 2026-09-29)"),
    },
}

# ---- Listed 2026-09-29, not researched yet: every cell Unknown until a research pass ----
def placeholder(name, url, note):
    return {
        "name": name, "url": url, "category": "agent manager", "where_agents_run": "not verified",
        "license": "not verified", "checked_on": "not researched yet (listed 2026-09-29)",
        "source_note": note, "is_authors_own": False,
        "features": {k: c("unknown", "Not researched yet") for k, _, _, _ in FEATURES},
    }

agtx = placeholder("AGTX", "https://github.com/thereal4th/AGTX",
                   "Listed 2026-09-29, research pending. Its README describes an orchestrator agent that hands tasks from a terminal kanban board to coding agents running in parallel.")
nimbalyst = placeholder("Nimbalyst", "https://nimbalyst.com", "Listed 2026-09-29, research pending.")
parallelcode = placeholder("Parallel Code", "https://github.com/johannesjo/parallel-code", "Listed 2026-09-29, research pending.")

TOOLS = [orca, velaterm, herdr, pantheon, paseo, kepler, ao,
         antigravity, pane, claudedesktop, agentmanager, vibetree,
         ccmanager, opencove, wave, vibekanban, t3code, superset, conductor,
         jenny, micracode, teleclod, oyren,
         agtx, nimbalyst, parallelcode]

# Operating systems: release assets / vendor pages as recorded in the source doc and the raw-evidence
# file (2026-09-28). Anything not on record stays "not verified".
OS = {
    "Orca": c("info", "Windows, macOS, Linux; phone companion (beta)"),
    "VelaTerm": c("info", "Windows, macOS, Linux; iOS/Android app; any browser"),
    "herdr": c("info", "macOS, Linux, Windows (beta)"),
    "Pantheon": c("info", "Windows only (MSYS2 + tmux); phone over SSH"),
    "Paseo": c("info", "Windows, macOS, Linux; iOS/Android; web"),
    "GitKraken Kepler": c("info", "Windows, macOS, Linux; mobile check-and-answer"),
    "Agent Orchestrator (AO)": c("info", "Windows, macOS, Linux; mobile companion"),
    "CCManager": c("info", "Linux, macOS"),
    "T3 Code": c("info", "Windows, macOS, Linux; iOS/Android; web"),
    "Superset": c("info", "macOS; Linux experimental"),
    "Conductor": c("info", "macOS only"),
    "Jenny": c("info", "Windows (macOS untested, no Linux)"),
    "Teleclod": c("info", "Windows, macOS, Linux, Android; browser"),
    "Oyren": c("info", "Any browser (hosted)"),
}
for t in TOOLS:
    if t["name"] in OS:
        t["features"]["os"] = OS[t["name"]]

out = {
    "snapshot_date": "2026-09-29",
    "snapshot_note": "Snapshot as of 2026-09-29. Cells come from each tool's own docs/posts at the dates shown; not re-verified beyond that pass.",
    "features": [{"key": k, "label": label, "description": desc, "group": group} for k, label, desc, group in FEATURES],
    "group_order": GROUP_ORDER,
    "tools": TOOLS,
}

here = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(here, "..", "data", "tools.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

unknown_counts = {}
for t in TOOLS:
    n = sum(1 for v in t["features"].values() if v["mark"] == "unknown")
    unknown_counts[t["name"]] = n

print("Wrote", out_path)
print("Tools:", len(TOOLS))
for name, n in unknown_counts.items():
    print(f"  {name}: {n} unknown cells")
