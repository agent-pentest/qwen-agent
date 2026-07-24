"""A small read-only GitHub tool for Qwen-Agent."""

from __future__ import annotations

import json
from typing import Any

import requests
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool("github_repository")
class GitHubRepositoryTool(BaseTool):
    """Fetch public or token-accessible GitHub repository information."""

    description = (
        "Read metadata, open issues, or recent commits from a GitHub repository. "
        "This tool never changes GitHub data."
    )
    parameters = [
        {
            "name": "owner",
            "type": "string",
            "description": "Repository owner or organization.",
            "required": True,
        },
        {
            "name": "repo",
            "type": "string",
            "description": "Repository name without the owner.",
            "required": True,
        },
        {
            "name": "resource",
            "type": "string",
            "description": "The resource to read: repository, issues, or commits.",
            "enum": ["repository", "issues", "commits"],
            "required": True,
        },
    ]

    def __init__(self, cfg: dict[str, Any] | None = None):
        super().__init__(cfg)
        cfg = cfg or {}
        self._token = str(cfg.get("github_token", ""))
        self._api_url = str(cfg.get("github_api_url", "https://api.github.com")).rstrip("/")

    def call(self, params: str, **kwargs: Any) -> str:
        try:
            arguments = json.loads(params)
            owner = self._safe_segment(arguments["owner"])
            repo = self._safe_segment(arguments["repo"])
            resource = arguments["resource"]
            if resource not in {"repository", "issues", "commits"}:
                raise ValueError("resource must be repository, issues, or commits")

            suffix = "" if resource == "repository" else f"/{resource}"
            response = requests.get(
                f"{self._api_url}/repos/{owner}/{repo}{suffix}",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {self._token}",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                params={"state": "open", "per_page": 10} if resource == "issues" else {"per_page": 10},
                timeout=20,
            )
            response.raise_for_status()
            return json.dumps(self._compact(resource, response.json()), ensure_ascii=False)
        except (KeyError, TypeError, ValueError, requests.RequestException) as exc:
            return json.dumps({"error": str(exc)}, ensure_ascii=False)

    @staticmethod
    def _safe_segment(value: Any) -> str:
        segment = str(value).strip()
        if not segment or "/" in segment or segment in {".", ".."}:
            raise ValueError("owner and repo must each be one valid path segment")
        return segment

    @staticmethod
    def _compact(resource: str, payload: Any) -> Any:
        if resource == "repository":
            keys = (
                "full_name",
                "description",
                "html_url",
                "default_branch",
                "language",
                "stargazers_count",
                "forks_count",
                "open_issues_count",
                "updated_at",
            )
            return {key: payload.get(key) for key in keys}

        if resource == "issues":
            return [
                {
                    "number": item.get("number"),
                    "title": item.get("title"),
                    "state": item.get("state"),
                    "html_url": item.get("html_url"),
                    "author": (item.get("user") or {}).get("login"),
                    "is_pull_request": "pull_request" in item,
                }
                for item in payload
            ]

        return [
            {
                "sha": item.get("sha", "")[:12],
                "message": ((item.get("commit") or {}).get("message") or "").splitlines()[0],
                "author": (((item.get("commit") or {}).get("author") or {}).get("name")),
                "html_url": item.get("html_url"),
            }
            for item in payload
        ]

