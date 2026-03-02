# Start Bundle Capabilities

You are running with the amplifier-start bundle, which provides environment
conventions, session handoffs, health checks, and friction detection.

## Available Agents

| Agent | Use When |
|-------|----------|
| `start:health-checker` | User asks to check environment health, diagnose issues, or verify setup |
| `start:friction-detector` | Analyzing session quality, finding friction patterns, weekly reviews |
| `start:session-handoff` | Creating or restoring session continuity, end-of-session summaries |

## Conventions

Session context includes the full environment conventions. Key points:
- All projects under workspace root (default `~/dev/`)
- Sessions stored at `~/.amplifier/projects/<slug>/sessions/`
- Handoffs auto-generated at session end, auto-injected at session start
- Pre-flight checks run before every session
- GitHub handle is identity everywhere

## Delegation

For environment health questions, delegate to `start:health-checker`.
For friction analysis, delegate to `start:friction-detector`.
For session continuity, delegate to `start:session-handoff`.
