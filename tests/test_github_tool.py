from __future__ import annotations

import json

from qwen_github_agent.github_tool import GitHubRepositoryTool


def test_tool_rejects_path_injection() -> None:
    tool = GitHubRepositoryTool({"github_token": "test-token"})

    result = json.loads(
        tool.call(json.dumps({"owner": "../users", "repo": "repo", "resource": "repository"}))
    )

    assert "error" in result


def test_compacts_repository_payload() -> None:
    result = GitHubRepositoryTool._compact(
        "repository",
        {"full_name": "octocat/Hello-World", "stargazers_count": 42, "private": True},
    )

    assert result["full_name"] == "octocat/Hello-World"
    assert result["stargazers_count"] == 42
    assert "private" not in result

