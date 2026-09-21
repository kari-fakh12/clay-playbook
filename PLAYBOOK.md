# Claude Code + Clay without burning your credits

Everything I got wrong in my first two weeks, written down so you can skip it.

I'm 90 days into GTM. I'm not selling a course. This is the doc I would have paid for on day 1.

---

## 1. The 2 rules that stopped me wasting credits

### Rule 1: Clay charges you twice, and only one half is obvious

Every enrichment in Clay costs you two separate things:

- a **data credit** for the lookup itself (the provider finding the email)
- an **Action** for Clay running the step at all

Almost everyone optimises the first one and never notices the second. It matters the moment you connect Claude Code, because Claude will happily re-run a column across your whole table when you ask it to "refresh the emails". The lookups may cost you nothing if you're on your own API keys. The Actions still bill.

What I do now: before any run that touches more than a handful of rows, I ask Claude how many rows it's about to touch and how many columns fire per row. Rows times columns is your Action count. If that number surprises you, stop.

### Rule 2: Conditional run on every enrichment column, no exceptions

In the enrichment column settings there's a conditional run option. Set it to run **only if the target field is empty**.

This is the single most useful setting in Clay and it's off by default. Without it, every table refresh re-enriches rows that already have the answer. With it, a refresh only fills gaps.

If you set this on nothing else, set it on your email and phone columns.

---

## 2. The prompt I run before Claude builds anything

The failure mode with Claude Code and Clay is not that Claude builds the wrong thing. It's that Claude builds *something* immediately, using your credits, based on a guess about what you meant.

So I never let it build on the first message. This goes first, every time:

```
Before you build or run anything in Clay, stop and ask me questions.

Do not create a table, do not add an enrichment column, and do not run
any enrichment until I say "go".

First, tell me back:
1. What you understood the goal to be, in one sentence
2. The exact source you plan to pull companies or people from
3. Every enrichment step you plan to add, in order
4. Roughly how many rows this will touch
5. Which steps cost Clay credits and which are free
6. Anything you are unsure about

Then ask me every question you need answered to avoid guessing.
Ask them all at once. I will answer, and then I will say "go".
```

Two things this does. It surfaces the plan while changing the plan is still free. And point 6 is the one that saves you, because Claude will tell you what it was about to assume.

The version of this I actually keep is saved as a `CLAUDE.md` line in my project folder so I don't have to paste it every time.

---

## 3. Why I test every workflow on 10 rows first

Because a broken workflow does not fail. It succeeds, quietly, 2,000 times.

The thing that gets you is not a crash. It's a column that returns a plausible-looking wrong answer on every row, and you don't notice until you've paid for all of them. Wrong domain matched to the right company name. Enrichment pointed at the parent company instead of the subsidiary. A prompt that returns "Unknown" for 80% of rows and still bills.

So the rule is: no workflow runs at full scale until it has run clean on 10 rows that I checked **by hand**. Not skimmed. Opened, and verified against the actual company.

The 10 rows should not be your 10 easiest. Pick a mix:
- 2 companies you know well, so you can spot a wrong answer instantly
- 2 with generic or ambiguous names
- 2 that are subsidiaries or recently renamed
- 2 outside your main geography
- 2 that are tiny, where the data providers usually have nothing

If it holds on those 10, it will mostly hold on 2,000. If it breaks, it breaks for the price of 10 rows.

Tell Claude this explicitly, because it will not do it on its own:

```
Run this on 10 rows only. Then stop and show me the output for all 10
before touching the rest of the table.
```

---

## 4. How to use your own API keys so you stop paying twice

This is called BYOK, bring your own key. You connect your own account with a data provider, and Clay runs the enrichment through your API instead of charging you Clay credits for the data.

**Where:** Settings → Connections → Add Connection.

**Providers you can connect:** Apollo, Better Contact, Prospeo, Lead Magic, Contact Out, among others. You need to be on a paid Clay plan for this.

**The one people miss:** connect your **AI model** key too, Anthropic or OpenAI, in the same Connections menu. AI enrichment columns are where the money actually goes, and running them on your own key cuts that cost by roughly 80 to 95%. Published figures put 1,000 rows of AI enrichment at $30 to $50 on Clay defaults versus $1 to $3 on your own key.

**Two things to know before you do it:**

Fund the Anthropic account properly before you connect it. Low API tiers hit rate limits on big tables, and a rate limited enrichment fails in a way that looks like bad data rather than an error. Around $200 deposited gets you to a tier that holds up on tables in the thousands.

BYOK removes the data credit. It does not remove the Action. You are still paying Clay to execute the step, which is why rule 1 above still applies even after you've done all of this.

**Email waterfalls:** connect your own key for each provider in the waterfall, not just the first one. Every provider the waterfall falls through to bills separately, so the savings compound across the chain.

---

## 5. The full setup, step by step

### Step 1: Install Claude Code

If you don't have it, install it and sign in. Everything below runs from your terminal, inside whatever folder you want the project to live in.

### Step 2: Connect Clay

One command:

```bash
claude mcp add clay --transport http <Clay MCP server URL from Clay's MCP setup docs>
```

This is Clay's hosted MCP server. Nothing runs on your machine, you're talking to Clay's server over HTTP. Copy the current URL from Clay's MCP setup docs.

### Step 3: Authorise

The first time you use it, Clay opens a browser window and asks you to sign in and authorise. Do that once and it reuses the credentials after that.

### Step 4: Confirm it actually connected

In Claude Code, run:

```
/mcp
```

You should see Clay listed with its tools. The ones you'll actually use:

- `get-current-workspace` and `get-credits-available`, for checking where you are and what you have left
- `find-and-enrich-company`, for sourcing and enriching companies
- `find-and-enrich-contacts-at-company`, for decision makers at a specific account
- `find-and-enrich-list-of-contacts`, for enriching a list you already have
- `add-company-data-points` and `add-contact-data-points`, for adding enrichment fields
- `query-objects` and `ask-question-about-accounts`, for reading what's already in your workspace
- the subroutine tools, one to list them and `run_subroutine` to run one, for running the enrichment functions your workspace already has built

If `/mcp` shows Clay but no tools, the OAuth didn't complete. Re-run the add command.

### Step 5: Check your credits before you do anything else

Ask Claude to run `get-credits-available`. Write the number down. Check it again after your first real run. That difference is the only honest measure of what a workflow costs you, and it takes 5 seconds.

### Step 6: Set up your own API keys

Go do section 4 above. Do it before your first big run, not after.

### Step 7: Put the guardrails in writing

Create a `CLAUDE.md` file in your project folder with your standing rules, so you don't have to repeat them every session. Mine has these lines:

```
- Never run a Clay enrichment without asking me first.
- Always run on 10 rows and show me the output before scaling.
- Always tell me the row count and estimated Action count before running.
- Set conditional run "only if empty" on every enrichment column.
```

Claude reads this at the start of every session. This is the difference between a tool that saves you money and one that spends it while you're making coffee.

### Step 8: Now build something small

Do not start with your real campaign. Take one company you know well and ask Claude to find 3 decision makers and enrich them. Watch what it does. Check the credits before and after.

Then scale.

---

## The honest summary

The integration is genuinely good. You describe a workflow once and it sources, enriches, qualifies and writes, without you building a table by hand.

It's also the fastest way to spend money in GTM that I've found, because nothing about it feels expensive while it's happening.

Everything in this doc is one idea: make it show you the plan and the price before it acts.

---

*Written by Karim Fakhri. 90 days into GTM, learning in public.*
*If something here is wrong or out of date, tell me and I'll fix it.*

**Sources for the technical claims:** Clay's MCP server setup docs, Clay's Connections/BYOK documentation, and published Clay credit cost breakdowns. Commands and settings verified 31 July 2026.
