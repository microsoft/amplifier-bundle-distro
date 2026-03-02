"""Pre-flight checks hook - validates environment health at session start.

Runs once per session on the first prompt:submit event. Checks configuration,
API keys, cache health, and bundle integrity. Reports results to the user
and optionally injects warnings into the session context.
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amplifier_core import HookResult

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    """Result of a single pre-flight check."""

    name: str
    status: str  # "pass", "warn", "fail"
    message: str
    fix: str = ""


@dataclass
class PreflightConfig:
    """Configuration for the preflight hook."""

    enabled: bool = True
    blocking: bool = False  # If True, fail status blocks the session
    check_api_keys: bool = True
    check_cache: bool = True
    check_config: bool = True
    check_python: bool = True
    check_git: bool = True


class PreflightHook:
    """Runs environment health checks at session start."""

    def __init__(self, config: PreflightConfig) -> None:
        self.config = config
        self._has_run = False

    async def on_session_start(self, event: str, data: dict[str, Any]) -> HookResult:
        """Run pre-flight checks once at session start."""
        if self._has_run:
            return HookResult(action="continue")
        if not self.config.enabled:
            return HookResult(action="continue")

        # Skip sub-sessions (agent spawns)
        if data.get("parent_id"):
            return HookResult(action="continue")

        self._has_run = True

        results = await self._run_checks()
        return self._build_result(results)

    async def _run_checks(self) -> list[CheckResult]:
        """Run all configured checks."""
        results: list[CheckResult] = []

        if self.config.check_config:
            results.append(self._check_config())

        if self.config.check_python:
            results.append(self._check_python())

        if self.config.check_api_keys:
            results.extend(self._check_api_keys())

        if self.config.check_cache:
            results.append(self._check_cache())

        if self.config.check_git:
            results.append(self._check_git())

        return results

    def _check_config(self) -> CheckResult:
        """Check that settings.yaml exists and is readable."""
        home = os.environ.get("AMPLIFIER_HOME", os.path.expanduser("~/.amplifier"))
        settings_path = Path(home) / "settings.yaml"

        if not settings_path.exists():
            return CheckResult(
                name="Configuration",
                status="warn",
                message="~/.amplifier/settings.yaml not found",
                fix="Run `amplifier init` to create configuration",
            )

        try:
            content = settings_path.read_text(encoding="utf-8")
            if not content.strip():
                return CheckResult(
                    name="Configuration",
                    status="warn",
                    message="settings.yaml exists but is empty",
                    fix="Run `amplifier init` to populate configuration",
                )
        except Exception as e:
            return CheckResult(
                name="Configuration",
                status="fail",
                message=f"Cannot read settings.yaml: {e}",
                fix="Check file permissions on ~/.amplifier/settings.yaml",
            )

        return CheckResult(
            name="Configuration",
            status="pass",
            message="settings.yaml valid",
        )

    def _check_python(self) -> CheckResult:
        """Check Python version meets requirements."""
        version = sys.version_info
        if version < (3, 11):
            return CheckResult(
                name="Python",
                status="fail",
                message=f"Python {version.major}.{version.minor} (need >=3.11)",
                fix="Install Python 3.11 or later",
            )
        return CheckResult(
            name="Python",
            status="pass",
            message=f"Python {version.major}.{version.minor}.{version.micro}",
        )

    def _check_api_keys(self) -> list[CheckResult]:
        """Check that provider API keys are set."""
        results = []
        key_names = [
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("OPENAI_API_KEY", "OpenAI"),
        ]

        found_any = False
        for env_var, provider in key_names:
            value = os.environ.get(env_var, "")
            if value:
                found_any = True
                results.append(
                    CheckResult(
                        name=f"API Key ({provider})",
                        status="pass",
                        message=f"{env_var} is set",
                    )
                )

        if not found_any:
            results.append(
                CheckResult(
                    name="API Keys",
                    status="fail",
                    message="No provider API keys found",
                    fix="Set ANTHROPIC_API_KEY or OPENAI_API_KEY in your environment",
                )
            )

        return results

    def _check_cache(self) -> CheckResult:
        """Check cache directory health."""
        home = os.environ.get("AMPLIFIER_HOME", os.path.expanduser("~/.amplifier"))
        cache_dir = Path(home) / "cache"

        if not cache_dir.exists():
            return CheckResult(
                name="Cache",
                status="warn",
                message="Cache directory not found (first run?)",
                fix="Cache will be populated on first module load",
            )

        try:
            entries = list(cache_dir.iterdir())
            if not entries:
                return CheckResult(
                    name="Cache",
                    status="warn",
                    message="Cache directory is empty",
                    fix="Modules will be cached on next session start",
                )
            return CheckResult(
                name="Cache",
                status="pass",
                message=f"{len(entries)} cached entries",
            )
        except Exception as e:
            return CheckResult(
                name="Cache",
                status="fail",
                message=f"Cannot read cache directory: {e}",
                fix="Run `amplifier reset --remove cache -y` to rebuild cache",
            )

    def _check_git(self) -> CheckResult:
        """Check git configuration."""
        import subprocess

        try:
            result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0 or not result.stdout.strip():
                return CheckResult(
                    name="Git",
                    status="warn",
                    message="git user.email not configured",
                    fix='Run `git config --global user.email "you@example.com"`',
                )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return CheckResult(
                name="Git",
                status="warn",
                message="git not found or not responding",
                fix="Install git",
            )

        return CheckResult(
            name="Git",
            status="pass",
            message=f"git configured ({result.stdout.strip()})",
        )

    def _build_result(self, checks: list[CheckResult]) -> HookResult:
        """Build HookResult from check results."""
        failures = [c for c in checks if c.status == "fail"]
        warnings = [c for c in checks if c.status == "warn"]
        passes = [c for c in checks if c.status == "pass"]

        # Build display message
        lines = ["Pre-flight Checks", "=================", ""]
        for check in checks:
            icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[check.status]
            lines.append(f"[{icon}] {check.name}: {check.message}")
            if check.fix:
                lines.append(f"       Fix: {check.fix}")
        lines.append("")
        lines.append(
            f"Summary: {len(passes)} passed, {len(warnings)} warnings, {len(failures)} failures"
        )

        display = "\n".join(lines)

        if failures and self.config.blocking:
            return HookResult(
                action="inject_context",
                context_injection=f'<system-reminder source="preflight">\n{display}\n</system-reminder>',
                context_injection_role="system",
                user_message=display,
                user_message_level="error",
            )

        if failures or warnings:
            return HookResult(
                action="inject_context",
                context_injection=f'<system-reminder source="preflight">\n{display}\n</system-reminder>',
                context_injection_role="system",
                ephemeral=True,
                user_message=display,
                user_message_level="warning" if not failures else "error",
            )

        # All clear — show brief message, no context injection needed
        return HookResult(
            action="continue",
            user_message=f"Pre-flight: {len(passes)} checks passed",
            user_message_level="info",
        )


async def mount(
    coordinator: Any, config: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Mount the preflight hook module."""
    config = config or {}

    hook_config = PreflightConfig(
        enabled=config.get("enabled", True),
        blocking=config.get("blocking", False),
        check_api_keys=config.get("check_api_keys", True),
        check_cache=config.get("check_cache", True),
        check_config=config.get("check_config", True),
        check_python=config.get("check_python", True),
        check_git=config.get("check_git", True),
    )

    hook = PreflightHook(hook_config)

    coordinator.hooks.register(
        "session:start", hook.on_session_start, priority=5, name="preflight-checks"
    )

    return {
        "name": "hooks-preflight",
        "version": "0.1.0",
        "description": "Pre-flight environment health checks at session start",
        "config": {
            "enabled": hook_config.enabled,
            "blocking": hook_config.blocking,
        },
    }
