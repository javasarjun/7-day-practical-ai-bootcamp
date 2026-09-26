"""Author mode for Lab Studio.

Generates Lab-Mode .md files from a project's code + teaching notes by sending
them through `lab_authoring_prompt.md` to a frontier LLM (Anthropic or OpenAI).
Uses plain HTTP so there are no SDK version headaches.
"""

import os
import re
from pathlib import Path

import requests

from editor_render import EXT_LANG

PROMPT_FILE = "lab_authoring_prompt.md"

DEFAULT_MODELS = {
    "Anthropic": "claude-sonnet-4-5",
    "OpenAI": "gpt-4o",
}
ENV_KEY = {
    "Anthropic": "ANTHROPIC_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
}


def read_env(app_dir, key):
    env = Path(app_dir) / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip().strip('"').strip("'")
    return os.environ.get(key, "").strip()


def load_system_prompt(app_dir):
    """Pull the instruction portion out of lab_authoring_prompt.md (everything
    from 'You are a' up to the '## PROJECT CODE' placeholder)."""
    p = Path(app_dir) / PROMPT_FILE
    if not p.exists():
        raise RuntimeError(f"{PROMPT_FILE} not found next to the app.")
    text = p.read_text()
    start = text.find("You are a")
    end = text.find("## PROJECT CODE")
    if start != -1 and end != -1 and end > start:
        return text[start:end].strip()
    return text


def build_user_message(code_files, notes):
    """code_files: dict {filename: contents}. notes: str."""
    parts = ["## PROJECT CODE"]
    for name, content in code_files.items():
        lang = EXT_LANG.get(Path(name).suffix, "")
        parts.append(f"### file: {name}\n```{lang}\n{content}\n```")
    parts.append("## TEACHING NOTES\n" + (notes.strip() or "(none provided)"))
    parts.append(
        "## TASK\n"
        "Produce the Lab-Mode .md files for the lectures described above, "
        "following every rule in your instructions. Before each file, output a "
        "line EXACTLY like:\n\n===== FILE: <filename>.md =====\n\n"
        "then that file's full markdown. Output only those file blocks, nothing else."
    )
    return "\n\n".join(parts)


def generate(provider, model, api_key, system, user, max_tokens=8000, timeout=600):
    if provider == "Anthropic":
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
            timeout=timeout,
        )
        if r.status_code != 200:
            raise RuntimeError(f"Anthropic HTTP {r.status_code}: {r.text[:400]}")
        data = r.json()
        return "".join(b.get("text", "") for b in data.get("content", []))

    # OpenAI
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
        },
        timeout=timeout,
    )
    if r.status_code != 200:
        raise RuntimeError(f"OpenAI HTTP {r.status_code}: {r.text[:400]}")
    return r.json()["choices"][0]["message"]["content"]


def split_files(text):
    """Split LLM output on '===== FILE: name =====' markers.
    Returns list of (filename, content). Falls back to one file."""
    parts = re.split(r"^=====\s*FILE:\s*(.+?)\s*=====\s*$", text, flags=re.MULTILINE)
    out = []
    it = iter(parts[1:])
    for name, body in zip(it, it):
        name = name.strip()
        if not name.endswith(".md"):
            name += ".md"
        out.append((name, body.strip()))
    if not out:
        out = [("generated_lab.md", text.strip())]
    return out
