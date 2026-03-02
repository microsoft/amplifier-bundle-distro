# Amplifier Start: Architecture

## The Three Rings (Attention Allocation Model)

This is an attention allocation model that determines what gets built where.

| Ring | Attention Budget | Changes | Contains |
|------|-----------------|---------|----------|
| **Ring 1: Foundation** | Zero ongoing attention (set once, forget) | Rarely (setup, repair) | Workspace, identity, config, keys, bundle, cache, memory, health checks, session handoffs |
| **Ring 2: Interfaces** | Minimal attention (muscle memory) | Per-interaction (pick an interface) | CLI, TUI, Voice, Web — all viewports into the same system |
| **Ring 3: Workflows** | All attention (this is where work happens) | Daily (adapts to context) | Morning brief, idea capture, friction detection, project execution, knowledge synthesis |

## The North Star Experience

```
$ amplifier
Good morning. Since your last session:
  - Build for project-a is green, project-b has 2 test failures
  - 2 ideas captured from recent sessions

Your top priorities today:
  1. Voice pipeline: WebRTC client missing [high impact, low effort]
  2. Bundle validation: fix silent include failures [high impact, med effort]

What would you like to focus on?
```

This requires: Ring 1 is invisible, Ring 2 is muscle memory, Ring 3 gets
all the attention. The user's deep focus goes to judgment, creativity, and
decisions — not plumbing, re-explaining context, or debugging configuration.

## How It Maps to This Bundle

| Ring | Bundle Artifact | Purpose |
|------|----------------|---------|
| Ring 1 | `context/start-conventions.md` | The 11 opinions that make foundation invisible |
| Ring 1 | `modules/hooks-preflight/` | Pre-flight checks catch problems before they waste time |
| Ring 1 | `modules/hooks-handoff/` | Session handoffs preserve context automatically |
| Ring 1 | `agents/health-checker.md` | In-session diagnostics when something does break |
| Ring 3 | `agents/friction-detector.md` | Self-improving friction detection |
| Ring 3 | `agents/session-handoff.md` | Session continuity management |
| Ring 3 | `recipes/morning-brief.yaml` | Daily intelligence brief |
| Ring 3 | `recipes/friction-report.yaml` | Weekly friction analysis |

## The Self-Improving Loop

```
OBSERVE (analyze sessions for friction patterns)
    -> DIAGNOSE (classify root cause, estimate attention cost)
        -> ACT (apply fix: config change, new recipe, behavior update)
            -> VERIFY (did friction go down? measure.)
                -> back to OBSERVE
```

The friction-detector agent and friction-report recipe implement this loop.
Instead of project management tools (Gantt charts, sprint planning), the
system tells you what hurts most. You fix that. The system confirms it's
better.

## Ecosystem Integration

This bundle makes targeted changes across the Amplifier ecosystem:

| Change | Where | Type |
|--------|-------|------|
| Environment conventions as session context | This bundle | Policy |
| Pre-flight checks | This bundle (hook) | Policy |
| Session handoff generation | This bundle (hook) | Policy |
| Morning brief | This bundle (recipe) | Workflow |
| Friction detection | This bundle (recipe + agent) | Workflow |
| Directory contract documentation | amplifier-foundation PR | Mechanism |
| Cache TTL + auto-refresh | amplifier-foundation PR | Mechanism |
| Handoff injection on session start | amplifier-foundation PR | Mechanism |
| `amplifier doctor` command | amplifier-app-cli PR | Mechanism |
| Pre-flight hook point | amplifier-app-cli PR | Mechanism |
| Extended `amplifier init` | amplifier-app-cli PR | Mechanism |
