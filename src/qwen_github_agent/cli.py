"""Interactive command-line interface."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import Any

from .agent import build_agent
from .config import ConfigurationError, Settings


def _content(message: Any) -> str:
    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(getattr(message, "content", ""))


def _last_text(responses: Iterable[Any]) -> str:
    visible = [_content(message) for message in responses if _content(message)]
    return visible[-1] if visible else ""


def main() -> int:
    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    agent = build_agent(settings)
    messages: list[dict[str, str]] = []
    print(f"Qwen GitHub agent ({settings.qwen_model}). Type 'exit' to quit.")

    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            return 0

        messages.append({"role": "user", "content": prompt})
        final_responses: list[Any] = []
        try:
            for responses in agent.run(messages=messages):
                final_responses = list(responses)
                text = _last_text(final_responses)
                if text:
                    print(f"qwen> {text}", end="\r", flush=True)
        except Exception as exc:  # Qwen-Agent normalizes provider-specific errors inconsistently.
            print(f"\nRequest failed: {exc}", file=sys.stderr)
            messages.pop()
            continue

        print()
        messages.extend(final_responses)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

