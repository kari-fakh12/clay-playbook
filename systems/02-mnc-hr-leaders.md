# 02. MNC list and senior HR leaders

## Purpose

This is the main engine. Every qualified multinational goes here, and this is where I find the people to talk to and sort them into the segments the outreach test runs on (see [../outreach/segmentation-test.md](../outreach/segmentation-test.md)).

Every other system feeds this one.

## Input

- qualified companies from the Workday account list (system 01)
- qualified companies from website visitors (system 03)
- other target lists I built for the client, which go through the same company check

## Column flow

Steps in order. Names describe the step, they are not the exact column names.

| # | Column | What it does | Cost note |
|---|---|---|---|
| 1 | Company row | The qualified company, its domain and where it came from | Free |
| 2 | HR system | Which HR system the company runs | Conditional run: only if empty |
| 3 | Years on the system | Roughly when they went live, turned into a tenure tier (1 to 4) | Conditional run: only if empty |
| 4 | Find people | People search at the company for buyer titles: CHRO and senior HR, CFO and finance, IT and HR systems, global payroll and HRIS | Runs once per company. Capped number of people per company |
| 5 | Gate 1: person check (AI column) | Is this the right kind of person? A real buyer title, still at the company, senior enough | Runs on every new person |
| 6 | Gate 2: company check (AI column) | Is this the right kind of company? Same rules as system 01 | Only if Gate 1 passes |
| 7 | Segment label | Role bucket times tenure tier, so every lead sits in exactly one of the 16 cells | Formula, free |
| 8 | Contact details | LinkedIn profile and email where needed | Conditional run: only if empty, and only on rows that passed both gates |
| 9 | Push to HeyReach | Sends the lead to the campaign for its segment | Only on rows that passed both gates |

## Why two gates

At first one AI column did everything: title, company size, countries, industry. It did all of them badly and let junk through, like tiny companies, a university and board members.

So I split it. Gate 1 only asks about the person. Gate 2 only asks about the company. Two small checks are much easier to get right than one big one.

Then I ran a set of leads I already knew were bad back through both gates to prove every one of them now gets rejected. If one still passes, the fix isn't done.

And qualification runs on every new batch, not once. People search always drags in some wrong titles, so this can't be a one-time cleanup.

## Qualification rules

Company (Gate 2):
- a large multinational with complex global payroll
- not a university, vendor, consultancy, EOR or payroll provider

Person (Gate 1):
- a real buyer title in one of the four role buckets
- currently at the company
- senior enough to own the problem

## Output

Leads go to HeyReach, one campaign per segment. Qualified companies are also kept in a Notion master list the client team works from, and the daily Slack digest counts what landed there each day.
