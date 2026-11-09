# Stored notes — Mahax, "Grok Bot Usage. Fix Everything That Burns Your Limit."

Source: X Article by Mahax (@Mahaximus_), Nov 8, 2026 — 167.7K views, 665 bookmarks.
Link: https://x.com/mahaximus_/status/2119435020704112933
Stored by Dash, Nov 9, 2026, at Christopher's direction ("we need to store this info somewhere").
These are Dash's notes/summary, not the article text. The article also carries paste-ready
prompts for each fix (a usage-detective audit, and a combined one-paste auditor).

## Thesis (paraphrased)

A bot's usage bill is roughly (runs per week) × (how much it carries into each run).
The task itself is usually the smallest part. Most of the spend is re-reading:
instructions, whole chat histories, tool definitions for tools never called,
files and pages already processed. Cut either factor and the bill drops;
almost none of the carried weight improves the output.

## The seven leaks (article's structure, Dash's compression)

1. **Routines that run too often** — a 15-minute inbox check fires 96×/day to find ~6 emails. Match schedule to the data's actual change rate; prefer narrow triggers over schedules; batch items; pause routines whose output nobody reads.
2. **Re-reading everything** — run 50 redoing run 1's reading to find 3 new items. Fix: a persistent "seen" file (IDs/timestamps of handled items, last-run time, capped at 30 days) checked first, written back at the end. State goes in files, not in the bot's memory.
3. **Context that never gets cleaned** — every reply re-reads the whole conversation; summarisation only happens near the limit. Fix: durable rules live in profile/brief files the bot reads on purpose; the chat is disposable; keep lessons capped (~20 lines, replace don't pile); when a chat gets heavy, write a handoff summary into the brief and start a fresh copy; bots pass each other one-line pointers to files, not dumps.
4. **Tools loaded for no reason** — every connected tool's description is read on every run. Fix: turn off unused tools per bot; do heavy data filtering in code and return only the rows that matter; save scripts that work twice as reusable skills.
5. **Browsing when a connector exists** — clicking through a site costs a model-read per screen; a connector does it in one structured call. Audit routines for browsed sites with available connectors (flag connectors with their own separate cost).
6. **Bots doing the same work** — overlap and endless handoffs tax everything. Fix: one owner per job, written down in a shared roles file; max ~3 hops, then it goes to the human; make routing decisions cheap (the article suggests a small typed decision model, "Jev" by TypeSafe AI, with confidence gates — vendor claims large speed/cost multiples, independent tests lower).
7. **Loops that never stop** — a loop without an exit stops when the week runs out. Fix for every loop: a real pass/fail DONE check, a cap on tries, stop-and-report after the same error twice, and a hard usage cap. Bots reviewing each other: max 2 rounds, then to the human.

## Method discipline (the article's own epistemics)

- Measure first: rank bots/routines by estimated spend (runs × weight), say they're estimates.
- Prove savings with a 24-hour pause of the heaviest routine and compare the weekly % before/after. "Don't claim savings you didn't measure."
- Never trade the work for the tokens: a cheaper setup that misses things isn't cheaper.
- Change nothing without the owner's yes; log every change and how to undo it.

## Why this is filed here (Dash's mapping to Christopher's stack)

- Leak 3 is a description of this morning's problem: the main chat clogged by a month of carried context. Our standing mitigations ARE the article's fixes — memory files and daily logs as the brief layer, harvest files as handoff summaries, side chats as fresh copies with pointers.
- Leaks 2 and 7 are Circus design constraints (seen-files for repeated-source routines; DONE/CAP/STUCK on any loop a subagent runs).
- The "prove it with a pause" rule is the same epistemics as the METR re-audit: estimates to start, measurement to conclude.
- Author note: Mahax, verified, 12.4K followers, bio "Mirror of your eyes"; writes agent-ops guides (pinned: "Agents, Loops, Graphs," Aug 5, 2026). NOT filed to the befriend board — stored as reference only, per the instruction that sent it.
