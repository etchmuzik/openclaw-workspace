#!/usr/bin/env python3
"""Local config server for the openclaw workspace.

Serves workspace configuration files as structured JSON at /config.
Runs on port 18789 by default.
"""

import json
import os
import re
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
PORT = int(os.environ.get("OPENCLAW_PORT", 18789))


def read_file(name: str) -> str | None:
    """Read a workspace file, return None if missing."""
    path = WORKSPACE / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def parse_identity(text: str) -> dict:
    """Parse IDENTITY.md into structured data."""
    data = {}
    for line in text.splitlines():
        m = re.match(r"- \*\*(.+?):\*\*\s*(.*)", line)
        if m:
            key = m.group(1).strip().lower()
            val = m.group(2).strip()
            if val:
                data[key] = val
    return data


def parse_user(text: str) -> dict:
    """Parse USER.md into structured data."""
    data = {}
    for line in text.splitlines():
        m = re.match(r"- \*\*(.+?):\*\*\s*(.*)", line)
        if m:
            key = m.group(1).strip().lower().replace(" ", "_")
            val = m.group(2).strip()
            if val:
                data[key] = val
    return data


def parse_tools(text: str) -> dict:
    """Parse TOOLS.md into structured sections."""
    sections: dict = {}
    current_section = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)", line)
        if heading:
            current_section = heading.group(1).strip()
            sections[current_section] = {}
            continue
        if current_section is None:
            continue
        m = re.match(r"- \*\*(.+?):\*\*\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            # Strip inline markdown code ticks
            val = re.sub(r"`([^`]+)`", r"\1", val)
            # Split on " — " for descriptions
            if " — " in val:
                val_id, desc = val.split(" — ", 1)
                sections[current_section][key] = {"id": val_id, "description": desc}
            else:
                sections[current_section][key] = val
    return sections


def parse_memory(text: str) -> dict:
    """Parse MEMORY.md into structured sections."""
    sections: dict = {}
    current_section = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)", line)
        if heading:
            current_section = heading.group(1).strip()
            sections[current_section] = {}
            continue
        if current_section is None:
            continue
        m = re.match(r"- \*\*(.+?):\*\*\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            if val and not val.startswith("_("):
                sections[current_section][key] = val
    return sections


def list_skills() -> list[dict]:
    """List installed skills with metadata from SKILL.md."""
    skills_dir = WORKSPACE / "skills"
    if not skills_dir.is_dir():
        return []
    skills = []
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        skill: dict = {"name": entry.name}
        skill_md = entry / "SKILL.md"
        if skill_md.is_file():
            text = skill_md.read_text(encoding="utf-8")
            # Extract first heading as display name
            heading = re.search(r"^#\s+(.+)", text, re.MULTILINE)
            if heading:
                skill["title"] = heading.group(1).strip()
        skills.append(skill)
    return skills


def build_config() -> dict:
    """Aggregate all workspace config into a single dict."""
    config: dict = {"workspace": str(WORKSPACE)}

    # Identity
    text = read_file("IDENTITY.md")
    if text:
        config["identity"] = parse_identity(text)

    # User
    text = read_file("USER.md")
    if text:
        config["user"] = parse_user(text)

    # Tools
    text = read_file("TOOLS.md")
    if text:
        config["tools"] = parse_tools(text)

    # Memory
    text = read_file("MEMORY.md")
    if text:
        config["memory"] = parse_memory(text)

    # Skills
    config["skills"] = list_skills()

    return config


class ConfigHandler(BaseHTTPRequestHandler):
    """HTTP handler for the config API."""

    def do_GET(self):
        if self.path == "/config":
            payload = build_config()
            body = json.dumps(payload, indent=2, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/health":
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        """Quieter logging: only print to stderr."""
        sys.stderr.write(f"[config-server] {args[0]}\n")


def main():
    server = HTTPServer(("127.0.0.1", PORT), ConfigHandler)
    print(f"openclaw config server listening on http://127.0.0.1:{PORT}")
    print(f"  GET /config  — workspace configuration")
    print(f"  GET /health  — health check")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
