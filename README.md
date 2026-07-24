# ModelScope Qwen GitHub Agent

A small Python CLI built with Alibaba's `qwen-agent` framework. Qwen can answer normal
questions and call a read-only GitHub tool to inspect repository metadata, open issues, and
recent commits.

## Prerequisites

- Python 3.10 or newer
- A DashScope API key for Qwen
- A fine-grained GitHub personal access token with read-only access to the repositories you
  want the agent to inspect

## Setup

The repository contains a synthesized `.env` with deliberately invalid placeholders. Replace
those values with credentials from your own accounts. `.env` is ignored by Git and must never
be committed.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Edit `.env`:

```dotenv
DASHSCOPE_API_KEY=your-real-dashscope-key
GITHUB_TOKEN=your-read-only-github-token
QWEN_MODEL=qwen-plus
GITHUB_API_URL=https://api.github.com
```

Run the interactive agent:

```bash
qwen-github-agent
```

Example prompt:

```text
Summarize the repository octocat/Hello-World and list its open issues.
```

## Development

```bash
pytest
ruff check .
```

The test suite does not make network calls and does not require real credentials.
