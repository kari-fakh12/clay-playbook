# 04. Job-change and new-hire alerts

## Purpose

A new CEO or CHRO usually reviews vendors and spends budget in their first months. So a fresh appointment at a target company is a buying moment. This table watches a fixed set of companies and flags when one of them gets a new CEO or CHRO.

## Input

A watch list of target companies.

## Column flow

Steps in order. Names describe the step. Bucket and Email match fields in the output table.

| # | Column | What it does | Cost note |
|---|---|---|---|
| 1 | Watched company | The company on the watch list | Free |
| 2 | Job-change / new-hire signal | Clay's monitor for people who joined or moved into a role at the company | Runs on the monitor's schedule, not on every table refresh |
| 3 | Title filter | Keeps only CEO and CHRO level appointments | Formula, free |
| 4 | Recency check | Keeps only appointments inside the window we agreed counts as "new" | Formula, free |
| 5 | Email | Finds the new leader's email | Conditional run: only if empty |
| 6 | Bucket | Sorts the row, for example Ready or Regional, so the team knows what to act on first | Formula or AI column |
| 7 | Write to table | Adds the row to the New CEOs & CHROs table in Notion | Only on rows that pass steps 3 and 4 |

Steps 3 and 4 are cheap filters and they sit before the email step on purpose. Most job changes on a watch list are not CEO or CHRO level, and there's no point paying for an email on those.

## Qualification rules

- the company is on the watch list of target accounts
- the new person is CEO or CHRO level
- the appointment is recent

## Output

Rows go into the New CEOs & CHROs table in Notion, and the ready ones go to outreach.

Every Monday a summary goes to Slack: new appointments this week, total signals, how many are Ready, how many have an email. If nothing came in, it flags it. A cleaned version is in [../digests/ceo_chro_weekly.py](../digests/ceo_chro_weekly.py).
