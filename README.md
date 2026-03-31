# amplifier-start

An opinionated Amplifier environment bundle that eliminates configuration
friction, preserves context across sessions, and continuously detects
attention drains.

## What This Is

A proper Amplifier bundle that carries 11 settled conventions and 6
objectives derived from analysis of 91 user sessions. The value is in the
opinions and policies, not infrastructure.

## Quick Start

Add to your bundle:

```yaml
includes:
  - bundle: git+https://github.com/payneio/amplifier-start@main
```

Or compose just the behavior:

```yaml
includes:
  - bundle: git+https://github.com/payneio/amplifier-start@main#subdirectory=behaviors/start.yaml
```

## What You Get

| Capability | Artifact | Description |
|------------|----------|-------------|
| **Environment conventions** | `context/start-conventions.md` | 11 opinions that eliminate recurring decisions |
| **Session handoffs** | `modules/hooks-handoff/` | Auto-summarize sessions, inject context on next start |
| **Pre-flight checks** | `modules/hooks-preflight/` | Catch config problems before they waste time |
| **Health diagnostics** | `agents/health-checker.md` | In-session environment health checks |
| **Friction detection** | `agents/friction-detector.md` | Analyze sessions for attention drains |
| **Session continuity** | `agents/session-handoff.md` | Manage handoff notes and session context |
| **Morning brief** | `recipes/morning-brief.yaml` | Daily intelligence summary |
| **Friction report** | `recipes/friction-report.yaml` | Weekly friction analysis |

## The 11 Conventions

1. **Workspace** — All projects under one root (`~/dev/`)
2. **Identity** — GitHub handle everywhere
3. **Memory** — One location, YAML format
4. **Sessions** — Files at `~/.amplifier/projects/`, any interface resumes
5. **Bundle config** — One bundle, validated, errors loud
6. **Interfaces** — Viewports into the same system
7. **Providers** — Env vars for keys, bundle for config
8. **Cache** — TTL-based, auto-refresh on error
9. **Health** — Pre-flight every session, doctor on demand
10. **Setup** — One guide, machine-parseable
11. **Credentials** — Env vars for secrets, settings.yaml for config

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the Ring 1/2/3
attention allocation model.

## Planning

See [planning/](planning/) for the original friction analysis, design
documents, and build plan.

## Contributing

> [!NOTE]
> This project is not currently accepting external contributions, but we're actively working toward opening this up. We value community input and look forward to collaborating in the future. For now, feel free to fork and experiment!

Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit [Contributor License Agreements](https://cla.opensource.microsoft.com).

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
