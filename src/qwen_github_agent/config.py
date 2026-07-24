"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


PLACEHOLDER_PREFIX = "replace-with-"


class ConfigurationError(RuntimeError):
    """Raised when required credentials are missing or are placeholders."""


def _required_secret(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.lower().startswith(PLACEHOLDER_PREFIX):
        raise ConfigurationError(
            f"{name} is not configured. Copy .env.example to .env and replace its placeholder."
        )
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    dashscope_api_key: str
    github_token: str
    qwen_model: str = "qwen-plus"
    github_api_url: str = "https://api.github.com"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            dashscope_api_key=_required_secret("DASHSCOPE_API_KEY"),
            github_token=_required_secret("GITHUB_TOKEN"),
            qwen_model=os.getenv("QWEN_MODEL", "qwen-plus").strip() or "qwen-plus",
            github_api_url=os.getenv("GITHUB_API_URL", "https://api.github.com").rstrip("/"),
        )

