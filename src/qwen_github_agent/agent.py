"""Qwen assistant construction."""

from __future__ import annotations

from qwen_agent.agents import Assistant

from .config import Settings
from .github_tool import GitHubRepositoryTool


SYSTEM_MESSAGE = """You are a concise repository research assistant.
Use github_repository when the user asks about a GitHub repository and the answer depends on
current repository data. State when a conclusion is inferred. Never claim to have changed a
repository: the available GitHub tool is read-only. Do not expose API keys or access tokens.
"""


def build_agent(settings: Settings) -> Assistant:
    github_tool = GitHubRepositoryTool(
        {
            "github_token": settings.github_token,
            "github_api_url": settings.github_api_url,
        }
    )
    return Assistant(
        llm={
            "model": settings.qwen_model,
            "model_server": "dashscope",
            "api_key": settings.dashscope_api_key,
        },
        system_message=SYSTEM_MESSAGE,
        function_list=[github_tool],
    )

