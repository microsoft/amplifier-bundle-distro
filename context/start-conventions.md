# Amplifier Start: Environment Conventions

These are the shared conventions that every tool, interface, agent, and
workflow agrees to. They are deliberately opinionated. The guiding principle:
**a choice is better than many, even if you don't agree.** Every convention
exists to eliminate a decision that would otherwise cost human attention.

## The One Rule

**Minimize human attentional load.**

Every convention below derives from this. If a convention doesn't reduce
the attention a human spends on plumbing, configuration, debugging, or
context-switching, it shouldn't be here.

---

## 1. Project Identity

Project identity is automatic. When you start a session in a directory,
Amplifier derives the project slug from the directory name and stores
all per-project state under `~/.amplifier/projects/<slug>/`.

- `cd ~/dev/my-project && amplifier` → project slug is `my-project`
- Sessions, handoffs, and project state all keyed by this slug
- No manual tagging, no configuration needed
- We recommend organizing your code repos under a single root (e.g.
  `~/dev/`), but Amplifier does not require or configure this

## 2. Identity

Your GitHub handle is your identity. One handle, everywhere.

- Sessions are indexed by GitHub handle.
- Git config uses your GitHub email.
- Memory is yours.
- Detected automatically from `gh auth status`.

## 3. Memory

One memory system, one location, one format.

```
~/.amplifier/memory/
  memory-store.yaml     # Facts, preferences, learnings
  work-log.yaml         # Active work, pending decisions
```

- The CLI remembers what the TUI learned. Voice can query your memory.
- Agents share context. YAML format: human-readable, git-trackable, grep-able.
  No daemon, no service, no migration.

## 4. Sessions

Sessions are files. They live at `~/.amplifier/projects/`. Every interface
creates sessions the same way.

```
~/.amplifier/projects/
  <project-slug>/
    sessions/
      <session-id>/
        transcript.jsonl
        events.jsonl
        metadata.json
        handoff.md          # Auto-generated at session end
```

- Any interface can resume any session. Start in CLI, continue in TUI.
- Handoffs are automatic. When a session ends, a summary is written.
  When a session starts in the same project, the summary is injected.
- Session discovery is filesystem-based. No database, no service.

## 5. Bundle Configuration

One bundle per user. Validated before every session. Errors are loud, not
silent.

- Pre-flight checks run before session start. Missing API keys, broken
  includes, unresolvable sources — caught immediately with clear messages.
- No silent failures. A broken include is an error, not a warning you
  never see.

## 6. Interfaces

Interfaces are viewports into the same system. They share state, sessions,
memory, and configuration. They do NOT have their own isolated worlds.

- Start a session in CLI, continue in TUI, review in voice. Same project,
  same session files, same handoff.
- Every interface reads `~/.amplifier/settings.yaml` for configuration.

## 7. Providers

API keys in environment variables. Provider config in your bundle.

- Pre-flight checks verify keys are set and non-empty.
- Model names are centralized in the bundle, not scattered across files.
- Multi-provider is assumed.

## 8. Updates and Cache

Git-based updates. TTL-based cache. Auto-refresh on error. You never
manually clear cache.

- Stale cache auto-refreshes. Failed loads trigger cache invalidation
  and re-clone. No "have you tried clearing your cache?" debugging.
- `amplifier reset --remove cache` exists for the nuclear option.

## 9. Health and Diagnostics

The system monitors itself. Problems are surfaced before they waste
human attention.

- Pre-flight on every session start. Fast (<5 seconds).
- `amplifier doctor` for on-demand diagnostics.
- Health is not optional. Pre-flight can be non-blocking (`preflight: warn`),
  but not disabled entirely.

## 10. Setup

A setup guide at a known location that any agent can read. Contains
machine-parseable instructions.

- "Point an agent at the setup guide." A new team member's first experience.
- Human-readable AND machine-readable.

## 11. Credentials

All secrets in environment variables. All configuration in
`~/.amplifier/settings.yaml`. One pattern for all integrations.

- No per-integration config files. No scattered secrets.
- One config file to manage. One set of env vars to protect.

---

## What These Conventions Replace

| Before (Many Choices) | After (One Choice) |
|------------------------|---------------------|
| Projects anywhere, manual tagging | Project identity from directory name |
| Memory in various locations | Memory in `~/.amplifier/memory/` |
| Each interface creates sessions differently | Standard session lifecycle |
| Bundle errors are silent warnings | Bundle errors are loud failures |
| Cache cleared manually when things break | Cache auto-refreshes |
| Identity scattered across configs | GitHub handle is identity |
| Health checked when something breaks | Health checked every session |
| Setup is tribal knowledge | Setup is one guide, one command |

## Non-Opinions (Deliberately Left Open)

- Which LLM provider you prefer
- Which interface you use day-to-day
- Which agents you compose
- What workflows you run
- Your editor/IDE
- Your shell
