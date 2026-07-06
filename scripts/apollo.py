#!/usr/bin/env python3
"""Apollo.io API wrapper for organization enrichment and verified email lookup.

Stdlib only, no pip install needed. Reads APOLLO_API_KEY from .env in the repo root.

Usage:
    python3 scripts/apollo.py enrich-org --domain genesis-ai.company
    python3 scripts/apollo.py enrich-org --name "Genesis AI"
    python3 scripts/apollo.py match-person --first-name Zhou --last-name Xian \
        --org "Genesis AI" --linkedin-url https://www.linkedin.com/in/zhou-xian-588128150/

Prints JSON to stdout. Never prints the API key.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

APOLLO_BASE = "https://api.apollo.io/api/v1"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_api_key():
    env_path = os.path.join(REPO_ROOT, ".env")
    if not os.path.exists(env_path):
        sys.exit("No .env file found. Copy .env.example to .env and add your APOLLO_API_KEY.")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("APOLLO_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key:
                    return key
    sys.exit("APOLLO_API_KEY is missing or empty in .env.")


def apollo_post(path, payload, api_key):
    req = urllib.request.Request(
        f"{APOLLO_BASE}{path}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()}


def cmd_enrich_org(args, api_key):
    payload = {}
    if args.domain:
        payload["domain"] = args.domain
    if args.name:
        payload["name"] = args.name
    if not payload:
        sys.exit("Provide --domain or --name")
    result = apollo_post("/organizations/enrich", payload, api_key)
    org = result.get("organization")
    if org:
        print(json.dumps({
            "name": org.get("name"),
            "domain": org.get("primary_domain"),
            "website_url": org.get("website_url"),
        }, indent=2))
    else:
        print(json.dumps({"match": False, "raw": result}, indent=2))


def cmd_match_person(args, api_key):
    payload = {
        "first_name": args.first_name,
        "last_name": args.last_name,
        "organization_name": args.org,
        "reveal_personal_emails": False,
    }
    if args.linkedin_url:
        payload["linkedin_url"] = args.linkedin_url
    result = apollo_post("/people/match", payload, api_key)
    person = result.get("person")
    if person:
        print(json.dumps({
            "name": person.get("name"),
            "title": person.get("title"),
            "email": person.get("email"),
            "email_status": person.get("email_status"),
            "linkedin_url": person.get("linkedin_url"),
        }, indent=2))
    else:
        print(json.dumps({"match": False, "raw": result}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Apollo.io lookups for the recruiting engine")
    sub = parser.add_subparsers(dest="command", required=True)

    org_parser = sub.add_parser("enrich-org", help="Resolve a company's real domain/details")
    org_parser.add_argument("--domain")
    org_parser.add_argument("--name")

    person_parser = sub.add_parser("match-person", help="Look up a verified email for a named person")
    person_parser.add_argument("--first-name", required=True)
    person_parser.add_argument("--last-name", required=True)
    person_parser.add_argument("--org", required=True)
    person_parser.add_argument("--linkedin-url")

    args = parser.parse_args()
    api_key = load_api_key()

    if args.command == "enrich-org":
        cmd_enrich_org(args, api_key)
    elif args.command == "match-person":
        cmd_match_person(args, api_key)


if __name__ == "__main__":
    main()
