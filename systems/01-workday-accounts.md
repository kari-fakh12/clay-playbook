# 01. Workday account list

## Purpose

A company running Workday is a good sign it's the kind of multinational the client sells to: lots of countries, lots of payroll providers, and HR data that has to be stitched together by hand. This table takes those companies and decides which ones are real targets.

## Input

Rows come in from my [workday-signal-agent](https://github.com/kari-fakh12/workday-signal-agent) through a Clay webhook. The agent finds companies from their public Workday careers sites, drops anything it has already seen, and sends each new company once. A send-once ledger on the agent side means the same company never lands in the table twice.

What arrives per row is thin on purpose: the careers-site slug, the careers URL, the search term that found it, and the date found. Clay does the rest.

## Column flow

These are the steps in order. The names are descriptions, not the exact column names in the table.

| # | Column | What it does | Cost note |
|---|---|---|---|
| 1 | Webhook input | Receives the slug, careers URL, search term and date from the agent | Free. The ledger stops repeat sends |
| 2 | Company name and domain | Turns the slug into the real company name and website | Conditional run: only if domain is empty |
| 3 | Company enrichment | Pulls headcount, HQ country and the countries it operates in | Conditional run: only if headcount is empty |
| 4 | ICP check (AI column) | Checks size, countries and company type against the rules below. Returns pass, fail or needs check, with a source URL | Only runs once step 3 is filled |
| 5 | Dedupe against the master list | Looks the domain up in the MNC master list so an existing account isn't added again | Lookup, no data credit |
| 6 | Send to master list | Writes passing companies to the MNC master list | Only runs on pass |

## Qualification rules

- a large multinational, with payroll in many countries
- a multinational running its own workforce. Not a payroll provider, HR software vendor, EOR, staffing firm, consultancy, broker or university
- no sourced number means "needs check", never a guess

The agent does a first pass with a tighter bar before anything reaches Clay (see its repo). Clay does the real check with sources.

## Output

Passing companies go into the MNC master list (system 02), where people get found and put into campaigns. A daily Slack digest tells the team how many companies the agent sent to Clay that day and how many qualified ones landed in the master list. It lives in the agent's repo: `digests/clay_daily_digest.py`.
