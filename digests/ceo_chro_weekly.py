#!/usr/bin/env python3
"""
Weekly digest for the "New CEOs & CHROs" Notion table (system 04).
Reads the table, counts what came in this week, and posts a short update to Slack.
Meant to run weekly, for example on a GitHub Actions schedule.

Env (all required, no defaults):
  NOTION_API_TOKEN   - Notion integration token
  SLACK_WEBHOOK_URL  - Slack incoming webhook URL
  CEO_CHRO_DB_ID     - the Notion database id

Expected Notion properties: "Bucket" (select, e.g. Ready / Regional), "Email" (email).
"""
import os, json, urllib.request, datetime
from collections import Counter


def env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing env var: {name}")
    return value


NOTION = env("NOTION_API_TOKEN")
WEBHOOK = env("SLACK_WEBHOOK_URL")
DBID = env("CEO_CHRO_DB_ID")
DB_URL = "https://www.notion.so/" + DBID.replace("-", "")
NH = {"Authorization": f"Bearer {NOTION}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}


def notion_query():
    rows, cur = [], None
    while True:
        body = {"page_size": 100}
        if cur:
            body["start_cursor"] = cur
        req = urllib.request.Request(
            f"https://api.notion.com/v1/databases/{DBID}/query",
            data=json.dumps(body).encode(), headers=NH, method="POST")
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
        rows.extend(d.get("results", []))
        if d.get("has_more"):
            cur = d.get("next_cursor")
        else:
            return rows


def created(p):
    return datetime.datetime.fromisoformat(p["created_time"].replace("Z", "+00:00"))


def bucket(p):
    b = p["properties"].get("Bucket", {}).get("select")
    return b["name"] if b else "none"


def has_email(p):
    return bool(p["properties"].get("Email", {}).get("email"))


def post_slack(text):
    req = urllib.request.Request(
        WEBHOOK, data=json.dumps({"text": text, "unfurl_links": False}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        resp = r.read().decode()
    if resp.strip() != "ok":
        raise SystemExit(f"Slack webhook error: {resp[:200]}")


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    rows = notion_query()
    total = len(rows)
    new7 = sum(1 for p in rows if (now - created(p)).days < 7)
    b = Counter(bucket(p) for p in rows)
    ready = b.get("Ready", 0)
    regional = b.get("Regional", 0)
    with_email = sum(1 for p in rows if has_email(p))

    if new7 == 0:
        health = ":warning: No new CEO/CHRO appointments detected this week."
    else:
        health = f":white_check_mark: {new7} fresh appointment(s) to work."

    msg = (
        ":bar_chart: *New CEOs & CHROs - weekly update*\n"
        f"• *New this week:* {new7}\n"
        f"• *Total signals:* {total}   (Ready: {ready} · Regional: {regional})\n"
        f"• *With email:* {with_email}/{total}\n"
        f"{health}\n"
        f"Table: {DB_URL}"
    )
    post_slack(msg)
    print("posted:\n" + msg)


if __name__ == "__main__":
    main()
