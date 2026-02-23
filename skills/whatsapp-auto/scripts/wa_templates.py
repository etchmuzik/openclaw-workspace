#!/usr/bin/env python3
"""WhatsApp template quick-reply system for Beyond DXB"""

import argparse
import json
import os
import subprocess
import sys

TEMPLATES_PATH = os.path.expanduser("~/.openclaw/workspace/whatsapp-templates.json")

def load_templates():
    with open(TEMPLATES_PATH) as f:
        return json.load(f)["templates"]

def list_templates():
    templates = load_templates()
    print("📋 Available templates:\n")
    for name, t in templates.items():
        triggers = ", ".join(t["trigger"][:3]) if t["trigger"] else "(manual only)"
        preview = t["message"][:80].replace("\n", " ") + "..."
        print(f"  📌 {name}")
        print(f"     Triggers: {triggers}")
        print(f"     Preview: {preview}\n")

def send_template(template_name, recipient, dry_run=False):
    templates = load_templates()
    if template_name not in templates:
        print(f"❌ Unknown template: {template_name}")
        print(f"Available: {', '.join(templates.keys())}")
        sys.exit(1)
    
    message = templates[template_name]["message"]
    
    if dry_run:
        print(f"📝 Template: {template_name}")
        print(f"📱 To: {recipient}")
        print(f"💬 Message:\n\n{message}")
        return
    
    cmd = ["wacli", "send", "text", "--to", recipient, "--message", message]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Sent '{template_name}' to {recipient}")
    else:
        print(f"❌ Failed: {result.stderr}")
        sys.exit(1)

def match_template(text):
    """Find the best matching template for incoming text"""
    templates = load_templates()
    text_lower = text.lower().strip()
    
    matches = []
    for name, t in templates.items():
        for trigger in t["trigger"]:
            if trigger.lower() in text_lower:
                matches.append((name, trigger))
                break
    
    if matches:
        print("🎯 Suggested templates:\n")
        for name, trigger in matches:
            preview = templates[name]["message"][:100].replace("\n", " ")
            print(f"  📌 {name} (matched: '{trigger}')")
            print(f"     {preview}...\n")
    else:
        print("🤷 No template matches. Available templates:")
        for name in templates:
            print(f"  📌 {name}")

def main():
    parser = argparse.ArgumentParser(description="WhatsApp template manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")

    s = sub.add_parser("send")
    s.add_argument("template", help="Template name")
    s.add_argument("--to", required=True, help="Recipient JID or phone number")
    s.add_argument("--dry-run", action="store_true")

    m = sub.add_parser("match")
    m.add_argument("text", help="Incoming message text to match")

    args = parser.parse_args()

    if args.command == "list":
        list_templates()
    elif args.command == "send":
        send_template(args.template, args.to, args.dry_run)
    elif args.command == "match":
        match_template(args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
