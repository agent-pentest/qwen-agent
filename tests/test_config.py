from __future__ import annotations

import pytest

from qwen_github_agent.config import ConfigurationError, Settings


def test_settings_reject_placeholders(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "replace-with-your-dashscope-api-key")
    monkeypatch.setenv("GITHUB_TOKEN", "replace-with-your-github-token")

    with pytest.raises(ConfigurationError):
        Settings.from_env()


def test_settings_load_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-dashscope-key")
    monkeypatch.setenv("GITHUB_TOKEN", "test-github-token")
    monkeypatch.setenv("QWEN_MODEL", "qwen-max")

    settings = Settings.from_env()

    assert settings.dashscope_api_key == "test-dashscope-key"
    assert settings.github_token == "test-github-token"
    assert settings.qwen_model == "qwen-max"

