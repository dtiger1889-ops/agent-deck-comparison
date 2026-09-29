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
        "agent_to_agent_messaging": c("yes", "Best in this table: search another session's conversation, ask about it, or message/steer a running session, across providers"),
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
        "conversation_gui_view": c("yes", "Best in this table"),
        "real_terminal": c("yes", "Yes"),
        "session_organization": c("yes", "Per workspace"),
        "usage_hud": c("partial", "Risky reverse-engineered endpoint, display-only, no rate-limit mitigation seen"),
        "burn_rate_forecast": c("no", "None"),
        "limit_governor": c("no", "None"),
        "vault_task_source": c("no", "None"),
        "issue_tracker_pipeline": c("partial", "Partial"),
        "worktree_management": c("yes", "Mature: rollback, recovery, git-contention queue"),
        "planner_orchestrator": c("yes", "The agent itself gets control-plane tools such as creating agents and responding to permission requests"),
        "agent_to_agent_messaging": c("yes", "Via its control-plane tools"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("unknown", "Not stated in this doc"),
        "native_mobile_app": c("yes", "Best in this table: celebrated mobile experience across iOS/Android"),
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
        "issue_tracker_pipeline": c("yes", "Best in this table: Jira, Trello, GitHub, GitLab Issues, Linear"),
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
        "saved_prompt_library": c("yes", "Best in this table: Actions come with issue, diff and repo state pre-attached"),
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
        "teams_multiuser": c("partial", "Partial"),
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

TOOLS = [orca, velaterm, herdr, pantheon, paseo, kepler, ao,
         ccmanager, opencove, wave, vibekanban, t3code, superset, conductor,
         jenny, micracode, teleclod, oyren]

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
    t["features"]["os"] = OS.get(t["name"], c("unknown", "not verified"))

out = {
    "snapshot_date": "2026-09-28",
    "snapshot_note": "Snapshot as of 2026-09-28. Cells come from each tool's own docs/posts at the dates shown; not re-verified beyond that pass.",
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
