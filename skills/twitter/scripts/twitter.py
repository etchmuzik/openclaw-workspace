#!/usr/bin/env python3
"""Twitter/X automation for Beyond DXB / @etchdxb"""

import argparse
import json
import os
import sys
import hmac
import hashlib
import base64
import time
import urllib.parse
import uuid
import requests

CONFIG_PATH = os.path.expanduser("~/.openclaw/twitter_config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("❌ Not configured. Run: python3 twitter.py setup --api-key KEY --api-secret SECRET --access-token TOKEN --access-secret SECRET --bearer-token BEARER")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    print(f"✅ Config saved to {CONFIG_PATH}")

def oauth1_sign(method, url, params, consumer_key, consumer_secret, token, token_secret):
    """Generate OAuth 1.0a signature"""
    oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    all_params = {**params, **oauth_params}
    sorted_params = "&".join(f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(str(v), safe='')}" for k, v in sorted(all_params.items()))
    base_string = f"{method.upper()}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(sorted_params, safe='')}"
    signing_key = f"{urllib.parse.quote(consumer_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
    signature = base64.b64encode(hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()).decode()
    oauth_params["oauth_signature"] = signature
    auth_header = "OAuth " + ", ".join(f'{k}="{urllib.parse.quote(v, safe="")}"' for k, v in sorted(oauth_params.items()))
    return auth_header

def post_tweet(text, cfg):
    """Post a tweet using Twitter API v2"""
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}
    auth_header = oauth1_sign(
        "POST", url, {},
        cfg["api_key"], cfg["api_secret"],
        cfg["access_token"], cfg["access_secret"]
    )
    resp = requests.post(url, json=payload, headers={
        "Authorization": auth_header,
        "Content-Type": "application/json",
    })
    if resp.status_code in (200, 201):
        data = resp.json()
        tweet_id = data["data"]["id"]
        print(f"✅ Posted tweet: https://x.com/etchdxb/status/{tweet_id}")
        return data
    else:
        print(f"❌ Failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

def post_tweet_with_media(text, image_path, cfg):
    """Post a tweet with an image using v1.1 media upload + v2 tweet"""
    # Upload media via v1.1
    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
    with open(image_path, "rb") as f:
        files = {"media_data": base64.b64encode(f.read()).decode()}
    auth_header = oauth1_sign(
        "POST", upload_url, files,
        cfg["api_key"], cfg["api_secret"],
        cfg["access_token"], cfg["access_secret"]
    )
    resp = requests.post(upload_url, data=files, headers={"Authorization": auth_header})
    if resp.status_code not in (200, 201):
        print(f"❌ Media upload failed ({resp.status_code}): {resp.text}")
        sys.exit(1)
    media_id = resp.json()["media_id_string"]

    # Post tweet with media
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text, "media": {"media_ids": [media_id]}}
    auth_header = oauth1_sign(
        "POST", url, {},
        cfg["api_key"], cfg["api_secret"],
        cfg["access_token"], cfg["access_secret"]
    )
    resp = requests.post(url, json=payload, headers={
        "Authorization": auth_header,
        "Content-Type": "application/json",
    })
    if resp.status_code in (200, 201):
        data = resp.json()
        tweet_id = data["data"]["id"]
        print(f"✅ Posted tweet with image: https://x.com/etchdxb/status/{tweet_id}")
        return data
    else:
        print(f"❌ Tweet failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

def check_status(cfg):
    """Verify credentials"""
    url = "https://api.twitter.com/2/users/me"
    auth_header = oauth1_sign(
        "GET", url, {},
        cfg["api_key"], cfg["api_secret"],
        cfg["access_token"], cfg["access_secret"]
    )
    resp = requests.get(url, headers={"Authorization": auth_header})
    if resp.status_code == 200:
        user = resp.json()["data"]
        print(f"✅ Authenticated as: @{user['username']} ({user['name']})")
        print(f"   ID: {user['id']}")
        return user
    else:
        print(f"❌ Auth failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

def adapt_linkedin_to_tweet(linkedin_text):
    """Convert a LinkedIn post to tweet format (≤280 chars)"""
    lines = linkedin_text.strip().split("\n")
    # Get the hook (first non-empty line)
    hook = ""
    for line in lines:
        line = line.strip()
        if line:
            hook = line
            break
    
    # Extract hashtags from the post
    hashtags = []
    for line in lines:
        for word in line.split():
            if word.startswith("#") and len(word) > 1:
                hashtags.append(word)
    
    # Keep top 3 hashtags
    hashtags = hashtags[:3]
    hashtag_str = " ".join(hashtags)
    
    # Build tweet: hook + hashtags, trim to 280
    tweet = hook
    if hashtag_str:
        max_hook = 280 - len(hashtag_str) - 2  # 2 for \n\n
        if len(tweet) > max_hook:
            tweet = tweet[:max_hook-1] + "…"
        tweet = f"{tweet}\n\n{hashtag_str}"
    else:
        if len(tweet) > 280:
            tweet = tweet[:279] + "…"
    
    return tweet

def main():
    parser = argparse.ArgumentParser(description="Twitter/X automation")
    sub = parser.add_subparsers(dest="command")

    # setup
    s = sub.add_parser("setup")
    s.add_argument("--api-key", required=True)
    s.add_argument("--api-secret", required=True)
    s.add_argument("--access-token", required=True)
    s.add_argument("--access-secret", required=True)
    s.add_argument("--bearer-token", required=True)

    # status
    sub.add_parser("status")

    # post
    p = sub.add_parser("post")
    p.add_argument("--text", help="Tweet text")
    p.add_argument("--file", help="Read text from file")
    p.add_argument("--image", help="Image path to attach")
    p.add_argument("--adapt", action="store_true", help="Adapt LinkedIn post to tweet format")

    # adapt (preview only)
    a = sub.add_parser("adapt")
    a.add_argument("--file", required=True, help="LinkedIn post file to preview as tweet")

    args = parser.parse_args()

    if args.command == "setup":
        save_config({
            "api_key": args.api_key,
            "api_secret": args.api_secret,
            "access_token": args.access_token,
            "access_secret": args.access_secret,
            "bearer_token": args.bearer_token,
            "handle": "etchdxb",
        })
        # Verify
        check_status(load_config())

    elif args.command == "status":
        cfg = load_config()
        check_status(cfg)

    elif args.command == "post":
        cfg = load_config()
        text = args.text
        if args.file:
            with open(args.file) as f:
                text = f.read().strip()
        if not text:
            print("❌ No text provided (use --text or --file)")
            sys.exit(1)
        if args.adapt:
            text = adapt_linkedin_to_tweet(text)
            print(f"📝 Adapted tweet ({len(text)} chars):\n{text}\n")
        if len(text) > 280:
            print(f"⚠️  Tweet is {len(text)} chars (max 280). Truncating...")
            text = text[:279] + "…"
        if args.image:
            post_tweet_with_media(text, args.image, cfg)
        else:
            post_tweet(text, cfg)

    elif args.command == "adapt":
        with open(args.file) as f:
            linkedin_text = f.read().strip()
        tweet = adapt_linkedin_to_tweet(linkedin_text)
        print(f"📝 Tweet preview ({len(tweet)} chars):\n\n{tweet}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
