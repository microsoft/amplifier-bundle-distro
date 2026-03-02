---
bundle:
  name: start
  version: 0.1.0
  description: >
    Opinionated Amplifier environment with conventions, health checks,
    session handoffs, and friction detection. Eliminates configuration
    friction, preserves context across sessions, and continuously
    detects attention drains.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: start:behaviors/start
---

# Amplifier Start

@start:context/start-conventions.md
