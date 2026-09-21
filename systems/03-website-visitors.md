# 03. Website visitor de-anonymisation

## Purpose

Most people who visit a B2B website never fill in a form. But a company that's reading about global payroll data is warmer than one picked off a list. This table works out which companies those anonymous visitors came from and whether they're worth contacting.

## Input

Anonymous website visits, identified at company level by a visitor-identification tool connected to Clay.

## Column flow

Steps in order. Names describe the step. The two contact fields match the fields in the output table.

| # | Column | What it does | Cost note |
|---|---|---|---|
| 1 | Visit | The raw visit, matched to a company | Free |
| 2 | Company enrichment | Domain, headcount, countries | Conditional run: only if empty |
| 3 | ICP check (AI column) | Same company rules as the other systems | Only runs once step 2 is filled |
| 4 | Contact Name | Finds the right senior person at a qualified company | Only on rows that passed step 3 |
| 5 | Email | Finds their email | Conditional run: only if empty |
| 6 | Write to table | Adds the qualified visitor to the Website Visitors table in Notion | Only on qualified rows |

The order matters. The ICP check sits before the person and email steps, because most visitors are students, job seekers, competitors and small companies. Finding a contact for those is money thrown away.

## Qualification rules

Same company rules as system 01: a large multinational running its own workforce, not a vendor, EOR, staffing firm, consultancy or university.

## Output

Qualified visitors land in a Website Visitors table in Notion, and from there go into outreach through the MNC list (system 02).

Every Monday a summary goes to Slack: new visitors this week, total in the table, how many have a contact and an email. If nothing new came in, it says so and suggests checking the Clay flow is still running. A cleaned version of that script is in [../digests/website_visitors_weekly.py](../digests/website_visitors_weekly.py).
