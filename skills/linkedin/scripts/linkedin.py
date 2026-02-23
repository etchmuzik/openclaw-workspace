#!/usr/bin/env python3
"""LinkedIn API CLI - Post, authenticate, and manage LinkedIn content."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import http.server
import threading
import webbrowser

CONFIG_PATH = os.path.expanduser("~/.openclaw/linkedin_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def api_request(method, url, token, data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202601",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {"status": resp.status}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)

def cmd_auth(args):
    config = load_config()
    client_id = args.client_id or config.get("client_id")
    client_secret = args.client_secret or config.get("client_secret")
    
    if not client_id or not client_secret:
        print("Error: --client-id and --client-secret required (or set in config)")
        sys.exit(1)
    
    config["client_id"] = client_id
    config["client_secret"] = client_secret
    
    # OAuth2 flow with local redirect
    redirect_uri = "http://127.0.0.1:9876/callback"
    scope = args.scope if hasattr(args, 'scope') and args.scope else "openid profile email w_member_social w_organization_social r_organization_social"
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={client_id}"
        f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&scope={urllib.parse.quote(scope)}"
    )
    
    code_holder = {}
    
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if "code" in params:
                code_holder["code"] = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h1>LinkedIn authorized! You can close this tab.</h1>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<h1>Authorization failed</h1>")
        def log_message(self, format, *args):
            pass
    
    server = http.server.HTTPServer(("127.0.0.1", 9876), Handler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()
    
    print(f"Opening browser for LinkedIn authorization...")
    print(f"If browser doesn't open, visit:\n{auth_url}")
    webbrowser.open(auth_url)
    
    thread.join(timeout=300)
    server.server_close()
    
    if "code" not in code_holder:
        print("Error: No authorization code received")
        sys.exit(1)
    
    # Exchange code for token
    token_data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code_holder["code"],
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    
    req = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as resp:
        token_resp = json.loads(resp.read().decode())
    
    config["access_token"] = token_resp["access_token"]
    config["expires_in"] = token_resp.get("expires_in")
    
    # Get user profile
    profile = api_request("GET", "https://api.linkedin.com/v2/userinfo", config["access_token"])
    config["person_urn"] = f"urn:li:person:{profile.get('sub', '')}"
    config["name"] = profile.get("name", "")
    
    save_config(config)
    print(f"✅ Authenticated as: {config['name']}")
    print(f"   URN: {config['person_urn']}")
    print(f"   Token expires in: {config.get('expires_in', '?')}s")

def cmd_post(args):
    config = load_config()
    token = config.get("access_token")
    person_urn = config.get("person_urn")
    
    if not token or not person_urn:
        print("Error: Not authenticated. Run: linkedin.py auth --client-id X --client-secret Y")
        sys.exit(1)
    
    text = args.text
    if args.file:
        with open(args.file) as f:
            text = f.read()
    
    if not text:
        print("Error: --text or --file required")
        sys.exit(1)
    
    post_data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    
    # Try Posts API first (newer)
    author = f"urn:li:organization:{args.org}" if args.org else person_urn
    
    post_data_v2 = {
        "author": author,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    
    # Handle image upload if provided
    if args.image:
        import mimetypes
        mime = mimetypes.guess_type(args.image)[0] or "image/jpeg"
        file_size = os.path.getsize(args.image)
        
        # Step 1: Initialize upload
        init_data = {
            "initializeUploadRequest": {
                "owner": author,
            }
        }
        init_resp = api_request("POST", "https://api.linkedin.com/rest/images?action=initializeUpload", token, init_data)
        upload_url = init_resp["value"]["uploadUrl"]
        image_urn = init_resp["value"]["image"]
        
        # Step 2: Upload binary
        with open(args.image, "rb") as f:
            img_data = f.read()
        upload_req = urllib.request.Request(upload_url, data=img_data, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": mime,
        }, method="PUT")
        urllib.request.urlopen(upload_req)
        
        # Step 3: Add image to post
        post_data_v2["content"] = {
            "media": {
                "altText": "Event production by Beyond DXB",
                "id": image_urn,
            }
        }
        print(f"   Image uploaded: {os.path.basename(args.image)}")
    
    result = api_request("POST", "https://api.linkedin.com/rest/posts", token, post_data_v2)
    print(f"✅ Posted to LinkedIn!")
    if isinstance(result, dict) and result.get("status") == 201:
        print("   Post published successfully")
    else:
        print(f"   Response: {json.dumps(result, indent=2)}")

def cmd_me(args):
    config = load_config()
    token = config.get("access_token")
    if not token:
        print("Not authenticated")
        sys.exit(1)
    
    profile = api_request("GET", "https://api.linkedin.com/v2/userinfo", token)
    print(json.dumps(profile, indent=2))

def cmd_status(args):
    config = load_config()
    if config.get("access_token"):
        print(f"✅ Authenticated as: {config.get('name', 'unknown')}")
        print(f"   URN: {config.get('person_urn', 'unknown')}")
    else:
        print("❌ Not authenticated")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn API CLI")
    sub = parser.add_subparsers(dest="command")
    
    auth_p = sub.add_parser("auth", help="Authenticate with LinkedIn")
    auth_p.add_argument("--client-id", help="OAuth Client ID")
    auth_p.add_argument("--client-secret", help="OAuth Client Secret")
    
    post_p = sub.add_parser("post", help="Create a LinkedIn post")
    post_p.add_argument("--text", "-t", help="Post text")
    post_p.add_argument("--file", "-f", help="Read post text from file")
    post_p.add_argument("--org", help="Organization ID (post as company page)")
    post_p.add_argument("--image", "-i", help="Image file path to include")
    
    sub.add_parser("me", help="Show profile info")
    sub.add_parser("status", help="Check auth status")
    
    args = parser.parse_args()
    
    commands = {"auth": cmd_auth, "post": cmd_post, "me": cmd_me, "status": cmd_status}
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
