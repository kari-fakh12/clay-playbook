#!/usr/bin/env python3
"""
Weekly digest for the Website Visitors (de-anonymised) Notion table (system 03).
Reads the table, counts what came in this week, and posts a short update to Slack.
Meant to run weekly, for example on a GitHub Actions schedule.

Env (all required, no defaults):
  NOTION_API_TOKEN   - Notion integration token
  SLACK_WEBHOOK_URL  - Slack incoming webhook URL
  VISITORS_DB_ID     - the Notion database id

Expected Notion properties: "Contact Name" (rich text), "Email" (email).
"""
import os, json, urllib.request, datetime


def env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing env var: {name}")
    return value


NOTION = env("NOTION_API_TOKEN")
WEBHOOK = env("SLACK_WEBHOOK_URL")
DBID = env("VISITORS_DB_ID")
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


def has_email(p):
    return bool(p["properties"].get("Email", {}).get("email"))


def has_contact(p):
    return bool(p["properties"].get("Contact Name", {}).get("rich_text"))


def post_slack(text):
    body = json.dumps({"text": text, "unfurl_links": False}).encode()
    req = urllib.request.Request(
        WEBHOOK, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        resp = r.read().decode()
    if resp.strip() != "ok":
        raise SystemExit(f"Slack webhook error: {resp[:200]}")


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    rows = notion_query()
    total = len(rows)
    new7 = sum(1 for p in rows if (now - created(p)).days < 7)
    with_email = sum(1 for p in rows if has_email(p))
    with_contact = sum(1 for p in rows if has_contact(p))

    if new7 == 0:
        health = ":warning: No new visitors added this week. Worth checking the Clay flow is still running."
    elif with_email < total:
        health = f":white_check_mark: Healthy. Note: {total - with_email} row(s) still missing an email."
    else:
        health = ":white_check_mark: Healthy. Every visitor has a contact and email."

    msg = (
        ":bar_chart: *Website Visitors - weekly update*\n"
        f"• *New this week:* {new7}\n"
        f"• *Total qualified visitors in table:* {total}\n"
        f"• *With email:* {with_email}/{total}   •   *With contact:* {with_contact}/{total}\n"
        f"{health}\n"
        f"Table: {DB_URL}"
    )
    post_slack(msg)
    print("posted:\n" + msg)


if __name__ == "__main__":
    main()
