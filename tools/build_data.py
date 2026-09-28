#!/usr/bin/env python3
"""Generates data/tools.json from the hardcoded transcription of the source
comparison doc (project_pantheon/docs/feature-comparison.md, section 6 cross
table + section 5 thinner entries). No web calls, no invented data."""
import json
import os

MARKS = {"yes", "partial", "experimental", "planned", "no", "unknown", "n/a", "info"}

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
    ("multi_provider_supervision", "Multi-provider agent supervision", "Can it drive more than one coding-agent CLI/tool at once.", G_AGENTS),
    ("harness_count", "Harness count", "How many distinct agent CLIs/tools it can drive.", G_AGENTS),
    ("needs_you_signal", "Needs-you signal quality", "How it tells you an agent is waiting on you, and how reliable that signal is.", G_AGENTS),
    ("approve_deny_prompt", "Approve/deny a waiting permission prompt", "Whether you can answer an agent's permission prompt from the manager itself.", G_AGENTS),
    ("cross_provider_delegation", "Cross-provider delegation visible in one place", "Handoffs between different providers/agents show up in one unified view.", G_AGENTS),
    ("always_on_assistant", "Always-on assistant session", "A persistent standing assistant session you can reach any time (not a task-bound worker).", G_AGENTS),
    ("conversation_gui_view", "Conversation (GUI) view of a session", "A chat-style view of a session's plan/edits/results, as opposed to raw terminal text.", G_SESSIONS),
    ("real_terminal", "The real terminal of a session", "Whether you can drop into the session's actual terminal.", G_SESSIONS),
    ("session_organization", "Session organization", "How sessions are grouped and browsed (list, worktrees, kanban, nested groups).", G_SESSIONS),
    ("prompt_scratchpad", "Prompt scratchpad with insert-not-send", "A place to draft prompts and insert them into a session without immediately sending.", G_SESSIONS),
    ("saved_prompt_library", "Saved prompt library", "Reusable, saved prompts/actions you can fire with prior context pre-attached.", G_SESSIONS),
    ("builtin_editors_browser", "Built-in editors / browser", "Ships its own code/markdown editors and/or an embedded browser.", G_SESSIONS),
    ("appearance_control", "Appearance control incl. host-terminal font", "How much you can customize its look, including your actual terminal's font/settings.", G_SESSIONS),
    ("usage_hud", "Subscription usage HUD (from local logs)", "Shows your subscription usage/limits, read from local logs rather than a fragile API endpoint.", G_USAGE),
    ("burn_rate_forecast", "Usage HUD with burn-rate + time-to-limit forecast", "Predicts when you'll hit your usage limit, not just showing current usage.", G_USAGE),
    ("limit_governor", "Session-limit governor (park/resume at reset)", "Automatically pauses work near a usage limit and resumes after the reset.", G_USAGE),
    ("account_hotswap", "Account switch / hot-swap without re-login", "Can switch between provider accounts without logging in again each time.", G_USAGE),
    ("vault_task_source", "Personal-notes-vault task source", "Can read your own personal notes vault (e.g. Obsidian) as its task queue, instead of only an issue tracker.", G_TASKS),
    ("issue_tracker_pipeline", "Issue-tracker / PR pipeline to merge", "Integrates with GitHub/GitLab/Linear/Jira issues and pull requests.", G_TASKS),
    ("worktree_management", "Worktree management for agents", "Manages isolated git worktrees per agent/task on your behalf.", G_TASKS),
    ("planner_orchestrator", "Planner/orchestrator that splits and runs work", "A higher-level agent that breaks a goal into sub-tasks and runs them.", G_TASKS),
    ("agent_to_agent_messaging", "Agent-to-agent messaging across sessions", "Sessions or orchestrators can message each other directly.", G_TASKS),
    ("knowledge_base", "Knowledge base agents can query", "A notes/knowledge store agents can query before acting.", G_TASKS),
    ("native_mobile_app", "Native mobile app", "A dedicated iOS/Android app, as opposed to reusing a terminal app.", G_REMOTE),
    ("phone_no_new_app", "Phone access without a new app/account", "Can be reached from a phone using tools you already have, no new app or account.", G_REMOTE),
    ("remote_ssh", "Remote hosts (SSH)", "Can drive or edit sessions on a remote machine over SSH.", G_REMOTE),
    ("voice_input", "Voice input", "Can dictate to it by voice.", G_REMOTE),
    ("app_shell", "App shell", "What the desktop/app UI is actually built on: Electron (with version, if pinned), Tauri 2, native, terminal UI, web app, or hosted cloud service.", G_HOOD),
    ("languages", "Main languages", "The top 2-3 languages in the project's own repo, from GitHub's language breakdown, with rough percentages.", G_HOOD),
    ("background_process", "Background process", "Whether it runs a separate daemon/server process alongside the UI, and what it does, per its own source or docs.", G_HOOD),
    ("download_size", "Download size", "The latest release's desktop installer size(s) per OS, from the release's own asset listing. Not a claim about how much it uses once running.", G_HOOD),
    ("ram_vs_claude_desktop", "Memory weight vs Claude Desktop (estimate)", "A labeled ESTIMATE, not a measurement: Claude Desktop is itself an Electron app, so this compares app shells only. Electron ~= about the same (heavier if it also runs a background daemon or several windows/an embedded terminal — the value says which); Tauri/system-WebView = lighter; terminal UI = much lighter; hosted service = cloud, local cost is a browser tab; unknown shell = not verified. The coding agents themselves (Claude Code, Codex, etc.) cost the same memory under every tool in this table — only the manager's own shell differs.", G_HOOD),
    ("runs_in_terminal", "Runs inside a terminal you already have", "Lives inside your existing terminal app, rather than shipping its own app/window.", G_HOOD),
    ("license_cost", "License / cost", "Open-source license, or commercial pricing model.", G_PROJECT),
    ("extensibility", "Extensibility for others (plugins/SDK)", "Whether outside developers can extend it via a plugin or SDK surface.", G_PROJECT),
    ("teams_multiuser", "Teams / multi-user", "Built for more than one person to use together, as opposed to single-user.", G_PROJECT),
    ("stability_maturity", "Stability / maturity (honest)", "How mature and stable it currently is, stated plainly.", G_PROJECT),
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
        "harness_count": c("yes", "27+ (\"any CLI agent\")"),
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
        "appearance_control": c("n/a", "Ships its own GPU terminal instead of using the host's"),
        "extensibility": c("partial", "CLI supports \"any agent\""),
        "teams_multiuser": c("unknown", "Not verified"),
        "voice_input": c("unknown", "Not verified"),
        "license_cost": c("yes", "MIT, free, uses your own subscriptions"),
        "app_shell": c("info", "Electron 43.7.5"),
        "languages": c("info", "TypeScript ~95%, JavaScript ~4%, Swift <1%"),
        "background_process": c("info", "Yes: a daemon-host process (docs/reference/windows-daemon-host-relocation.md)"),
        "download_size": c("info", "v1.4.216: 193 MB Windows setup.exe, 218-226 MB mac dmg, 207-209 MB Linux AppImage"),
        "ram_vs_claude_desktop": c("info", "Heavier (Electron + background daemon)"),
        "runs_in_terminal": c("no", "Embeds its own GPU terminal instead"),
        "stability_maturity": c("partial", "\"Features shipped daily\"; chat, orchestration and mobile are experimental"),
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
        "harness_count": c("yes", "8+ (Claude, Codex, OpenCode, Copilot, Cursor, Antigravity, Cline, Pi...)"),
        "needs_you_signal": c("yes", "Live status plus phone push (underlying mechanism not stated)"),
        "approve_deny_prompt": c("yes", "\"Answer agents\" from the phone"),
        "conversation_gui_view": c("yes", "Default view, plus the same session's terminal view alongside it"),
        "real_terminal": c("yes", "Each session is a real PTY that keeps running in the background"),
        "session_organization": c("yes", "Projects, then nested groups to any depth, then sessions"),
        "usage_hud": c("no", "Not claimed anywhere in the posts"),
        "burn_rate_forecast": c("no", "Not claimed"),
        "limit_governor": c("no", "Not claimed"),
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
        "license_cost": c("yes", "MIT, free, uses your own subscriptions"),
        "app_shell": c("info", "Tauri 2 (Rust + system WebView); repo also carries a secondary Electron shell, not the primary build"),
        "languages": c("info", "TypeScript ~46%, Rust ~39%, Python ~8%"),
        "background_process": c("unknown", "not verified: a minimal headless `vela-server` build exists but isn't documented as running alongside the desktop app"),
        "download_size": c("info", "v0.2.5: 59 MB Windows min-setup / 148 MB full-setup, 49-51 MB mac dmg"),
        "ram_vs_claude_desktop": c("info", "Lighter"),
        "runs_in_terminal": c("no", "Own app; the Windows installer bundles Git Bash"),
        "stability_maturity": c("unknown", "v0.2.x, launched 2026-09-28, not independently verified"),
    },
}

# ---- Pantheon ----
pantheon = {
    "name": "Pantheon", "url": "https://github.com/dtiger1889-ops/pantheon", "category": "agent manager",
    "where_agents_run": "your machine (terminal-native, tmux-hosted; phone reaches it over an existing SSH tunnel)",
    "license": "MIT, free, your own subscriptions", "checked_on": "2026-09-28 (author's own build, cells refreshed for the 2026-09-22..27 builds)",
    "source_note": "Author's own project (open source, pre-release, published as-is). Scored by the same rules as every other row here, including its weak spots.",
    "is_authors_own": True,
    "features": {
        "multi_provider_supervision": c("yes", "Hooks-based"),
        "harness_count": c("partial", "2 harnesses today, local-model support planned"),
        "needs_you_signal": c("yes", "Exact: derived from hook events, not inferred from silence"),
        "approve_deny_prompt": c("partial", "Allow/deny/view a waiting prompt from the deck, built, not yet tested live"),
        "conversation_gui_view": c("partial", "Detail panel shows recent actions and the latest ask read from the transcript, not a full chat view"),
        "real_terminal": c("yes", "Clicking a session opens its own real tmux window"),
        "session_organization": c("yes", "Sidebar session list plus a live fleet table"),
        "usage_hud": c("partial", "Local logs shipped; reading the same account-usage numbers claude.ai shows is built, not yet tested live"),
        "burn_rate_forecast": c("partial", "Built, with ranges; not yet checked against real usage"),
        "limit_governor": c("partial", "Built: wind down near a limit, park, and resume after reset, plus limit hand-off to another provider and timed starts; not yet tested live, off by default"),
        "vault_task_source": c("yes", "Unique in this table: reads a personal notes vault directly as its live task source"),
        "issue_tracker_pipeline": c("no", "Deliberately absent; the notes vault is the tracker"),
        "worktree_management": c("no", "Agents use worktrees; the deck itself doesn't manage them"),
        "planner_orchestrator": c("planned", "Planning card built; dispatching from it is still greyed out"),
        "agent_to_agent_messaging": c("no", "None"),
        "cross_provider_delegation": c("yes", "Visible in the deck, with auto-fallback to console mode"),
        "always_on_assistant": c("partial", "Pinned Assistant window built; reachable from the phone over the existing remote-control link"),
        "knowledge_base": c("n/a", "The vault is read only as tasks, not queried as a knowledge base"),
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
        "license_cost": c("yes", "MIT, free; pre-release, published as-is; uses your own subscriptions"),
        "app_shell": c("info", "Terminal UI: Python 3.12 + Textual, running inside your existing terminal, no separate installer"),
        "languages": c("info", "Python (Textual TUI)"),
        "background_process": c("info", "Yes: a separate small Python usage-collector process alongside the Textual UI process"),
        "download_size": c("info", "No installer; runs from source (git clone + Python)"),
        "ram_vs_claude_desktop": c("info", "Much lighter"),
        "runs_in_terminal": c("yes", "Only one in this table that runs entirely inside a terminal you already have"),
        "stability_maturity": c("partial", "Personal, pre-release; its terminal-multiplexer server froze four times on one day (cause still open)"),
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
        "harness_count": c("yes", "~39 agent harnesses"),
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
        "account_hotswap": c("n/a", "Not applicable"),
        "prompt_scratchpad": c("no", "None"),
        "saved_prompt_library": c("no", "None"),
        "appearance_control": c("n/a", "Not applicable"),
        "extensibility": c("yes", "Best in this table: MCP server, CLI and TypeScript SDK for automation"),
        "teams_multiuser": c("yes", "Teams plus triggers from GitHub/Slack/Discord"),
        "voice_input": c("yes", "Yes"),
        "license_cost": c("yes", "Apache-2.0, free"),
        "app_shell": c("info", "Electron 44.2.0"),
        "languages": c("info", "TypeScript ~98%, JavaScript ~1%"),
        "background_process": c("info", "Yes: a Node daemon (package.json `dev:server` runs `PASEO_LISTEN=... dev-daemon.sh`)"),
        "download_size": c("info", "v0.10.0: 137 MB Windows Setup x64, 186 MB mac x64 dmg, 129 MB Linux .deb"),
        "ram_vs_claude_desktop": c("info", "Heavier (Electron + background daemon)"),
        "runs_in_terminal": c("no", "Own desktop/mobile/web app"),
        "stability_maturity": c("yes", "Mature"),
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
        "harness_count": c("yes", "\"Any agent\""),
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
        "planner_orchestrator": c("n/a", "Not applicable"),
        "agent_to_agent_messaging": c("no", "None"),
        "cross_provider_delegation": c("yes", "Visible in one place"),
        "always_on_assistant": c("no", "None"),
        "knowledge_base": c("no", "None"),
        "builtin_editors_browser": c("yes", "Diffs plus in-app commit/PR"),
        "native_mobile_app": c("partial", "Mobile check-and-answer, not a full session manager"),
        "phone_no_new_app": c("no", "Requires its own app"),
        "remote_ssh": c("yes", "SSH/WSL remote execution"),
        "account_hotswap": c("n/a", "Not applicable"),
        "prompt_scratchpad": c("partial", "\"Actions\": saved one-click prompts"),
        "saved_prompt_library": c("yes", "Best in this table: Actions come with issue, diff and repo state pre-attached"),
        "appearance_control": c("n/a", "Not applicable"),
        "extensibility": c("partial", "Partial"),
        "teams_multiuser": c("yes", "Org-level analytics on agent spend"),
        "voice_input": c("no", "None"),
        "license_cost": c("partial", "Commercial with a free tier"),
        "app_shell": c("unknown", "not verified: not stated on gitkraken.com/kepler or help.gitkraken.com; not extrapolated from GitKraken's separate main git client"),
        "languages": c("unknown", "not verified: closed source, no public repo"),
        "background_process": c("unknown", "not verified"),
        "download_size": c("unknown", "not verified: not stated on the vendor's pages"),
        "ram_vs_claude_desktop": c("unknown", "not verified: app shell unknown"),
        "runs_in_terminal": c("no", "Own desktop app"),
        "stability_maturity": c("yes", "Commercial product"),
    },
}

# ---- AO ----
ao = {
    "name": "Agent Orchestrator (AO)", "url": "https://github.com/Untrivial-ai/agent-orchestrator", "category": "agent manager",
    "where_agents_run": "your machine + mobile companion (LAN/Tailscale)",
    "license": "OSS-ish, ~11k stars", "checked_on": "2026-09-06 (site-verified)",
    "source_note": "Site-verified, not installed.",
    "is_authors_own": False,
    "features": {
        "multi_provider_supervision": c("yes", "25 harnesses, per-project defaults"),
        "harness_count": c("yes", "25"),
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
        "account_hotswap": c("n/a", "Not applicable"),
        "prompt_scratchpad": c("no", "None"),
        "saved_prompt_library": c("no", "None"),
        "appearance_control": c("n/a", "Not applicable"),
        "extensibility": c("partial", "Partial"),
        "teams_multiuser": c("partial", "Partial"),
        "voice_input": c("no", "None"),
        "license_cost": c("partial", "Open-ish, roughly 11k stars"),
        "app_shell": c("info", "Electron ^33.0.0 (frontend/package.json), plus a separate Go backend"),
        "languages": c("info", "Go ~59%, TypeScript ~38%"),
        "background_process": c("info", "Yes: a separate Go backend process (repo has a distinct backend/ Go module via go.work, apart from the Electron frontend/)"),
        "download_size": c("info", "v0.13.2-nightly: 136 MB Windows Setup.exe, 177-189 MB mac zip, 181 MB Linux AppImage"),
        "ram_vs_claude_desktop": c("info", "Heavier (Electron + background daemon)"),
        "runs_in_terminal": c("no", "Own desktop app"),
        "stability_maturity": c("partial", "Active development"),
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
     "license_cost": c("yes", "MIT")},
)

superset = thin(
    "Superset", "https://superset.sh", "agent manager", "your machine (macOS, experimental Linux)",
    "Elastic-2.0", "Site/discussion pass only, 2026-09-07. Ships a TypeScript SDK and MCP server so agents can spawn agents.",
    {"extensibility": c("yes", "TypeScript SDK plus MCP server so agents can spawn agents"),
     "license_cost": c("yes", "Elastic-2.0")},
)

conductor = thin(
    "Conductor", "https://www.conductor.build", "agent manager", "your machine (macOS only)",
    "proprietary", "Site/discussion pass only, 2026-09-07. Checkpoint/rollback called best-in-class.",
    {"license_cost": c("no", "Proprietary")},
)

jenny = thin(
    "Jenny", "https://github.com/SaltyPretz3l/jenny", "other tool we looked at", "your machine",
    "MIT", "A single-agent local-LLM chat app and IDE (llama.cpp / vLLM / any OpenAI-compatible endpoint), not a fleet manager, so it doesn't compete on most rows here. Recorded for its file-edit checkpointing, destructive-command approval, and a scratchpad/calendar the model can read and modify.",
    {"multi_provider_supervision": c("no", "Single local-model chat app, not a multi-agent fleet manager"),
     "license_cost": c("yes", "MIT")},
)

micracode = thin(
    "micracode", "https://github.com/Jamessdevops/micracode", "other tool we looked at", "your machine",
    "open-source", "An AI web-app builder (Next.js, exports components as a zip), a different category from a fleet manager; recorded for completeness only. Local-model support is planned by its author.",
    {"multi_provider_supervision": c("no", "App builder, not a fleet/agent manager"),
     "license_cost": c("yes", "open-source")},
)

teleclod = thin(
    "Teleclod", "https://teleclod.com", "agent manager", "cloud (Windows/macOS/Linux/Android/browser plus a Chrome extension)",
    "commercial (Free / EUR49 Pro / EUR99 Studio)", "Site-only pass, 2026-09-22; no independent verification found (no reviews, repo, or discussion beyond the single source comment).",
    {"multi_provider_supervision": c("yes", "Claims 14+ providers including Claude Code, Codex, OpenRouter, Ollama, Kimi"),
     "usage_hud": c("no", "No usage/burn-rate/token HUD on the page"),
     "vault_task_source": c("no", "It is its own task store"),
     "limit_governor": c("no", "None"),
     "session_organization": c("yes", "Task list, kanban, and a global dashboard"),
     "runs_in_terminal": c("no", "Replaces the terminal outright"),
     "license_cost": c("no", "Closed-source, paid tiers")},
)

oyren = thin(
    "Oyren", "https://oyren.ai/development", "agent manager", "cloud (remote codespaces, deliberately not your machine)",
    "commercial, hourly", "Site-verified, 2026-09-23. Remote disposable codespaces with several agent CLIs preinstalled and tmux in every codespace.",
    {"multi_provider_supervision": c("yes", "Claude Code, Codex, Cursor, opencode, Qwen Code, DeepSeek Harness, Antigravity preinstalled"),
     "usage_hud": c("no", "No usage/burn-rate/token HUD on the page"),
     "vault_task_source": c("no", "Its own kanban board is the tracker"),
     "limit_governor": c("partial", "A blocked card emails the human a specific question and resumes on reply, but only for one card, not a whole session against a usage window"),
     "issue_tracker_pipeline": c("yes", "Its own kanban board with an importance/urgency matrix and calendar/milestone views, read and written by agents over its own MCP server"),
     "builtin_editors_browser": c("yes", "Streamed VS Code/Zed IDE plus a Playwright-driven built-in browser"),
     "remote_ssh": c("n/a", "It is itself the remote machine"),
     "app_shell": c("info", "Hosted cloud service, browser-based, no local install (vendor: \"VS Code runs as web app in your browser while Zed editor is streamed\")"),
     "background_process": c("n/a", "It is itself the remote machine; there is no separate local process to report"),
     "ram_vs_claude_desktop": c("info", "Runs in the cloud (local cost: a browser tab)"),
     "runs_in_terminal": c("no", "Cloud codespace, not a local terminal tool"),
     "license_cost": c("no", "Commercial: hourly compute plus an optional credit wallet")},
)

TOOLS = [orca, velaterm, pantheon, paseo, kepler, ao,
         ccmanager, opencove, wave, vibekanban, t3code, superset, conductor,
         jenny, micracode, teleclod, oyren]

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
