# Recruiting Engine

Weekly pipeline that finds interesting/funded AI & robotics companies, maps contacts there who share background with you (Harvard, Bain, Stanford GSB, Cambio AI, or the CEO), and creates Gmail drafts for review. Company- and relationship-first — there's no job-posting matching in this version. Human-in-the-loop by design: it never sends anything.

## Repo structure

```
auto-recruiter/
├── CLAUDE.md                    # agent operating rules + scoring rubric (read every run)
├── config/
│   ├── targets.yaml              # your criteria: company types, stage, triggers, scoring thresholds
│   ├── shortlist.yaml             # always-screened companies
│   └── templates/                 # email scaffolds: warm-mutual, alum-cold, pure-cold
├── data/                         # gitignored: connections.csv + resume.md (see data/README)
├── .claude/commands/              # slash commands: /weekly-run, /discover, /contacts, /draft
├── scripts/cron-run.sh            # headless entry point for cron + manual runs
└── runs/                          # per-run summaries + logs
```

## Setup (one-time)

**1. MCP connectors.** You need Gmail, Google Drive, Notion, and Google Calendar connected.
- If you're running this inside a Cowork/Desktop session (like the one used to build this), these are typically already connected at the account level — no setup needed. Verify with a quick read-only call (e.g. list Gmail drafts) if unsure.
- If you're running the bare `claude` CLI instead, you'll need to add them yourself:
  ```bash
  claude mcp add --transport http gmail   https://gmailmcp.googleapis.com/mcp/v1
  claude mcp add --transport http gdrive  https://drivemcp.googleapis.com/mcp/v1
  claude mcp add --transport http notion  https://mcp.notion.com/mcp
  claude mcp add --transport http gcal    https://calendarmcp.googleapis.com/mcp/v1
  ```
  Then run `claude` interactively once and complete each OAuth prompt (`/mcp` shows status). Exact commands/URLs can change — verify against https://code.claude.com/docs/en/mcp if anything fails.

**2. Drop in your data.** See `data/README.md` — LinkedIn connections export + resume.

**3. Notion databases** — two, linked, both under your workspace's Home Page:

**Companies** (one row per company)

| Property | Type | Options |
|---|---|---|
| Company | Title | |
| AI/Robotics Category | Select | AI Startup, Robotics Startup, Large AI Company, Frontier Lab |
| Stage | Select | Series A, B, C, D+, Pre-IPO, Frontier Lab |
| Last Round | Text | e.g. "$120M Series C, May 2026, a16z" |
| HQ Location | Select | SF, NYC, Remote, Other |
| Discovery Source | Select | Shortlist, Funding Trigger, Manual |
| Notes | Text | |
| Contacts | Relation | → Contacts database |

If you already track job applications in a "Companies" database, build on that one — just add these properties alongside your existing ones rather than replacing them.

**Contacts** (one row per person)

| Property | Type | Options |
|---|---|---|
| Name | Title | |
| Company | Relation | → Companies database |
| Title | Text | |
| Bridge | Select | 1st-degree, Harvard Alum, Bain Alum, GSB Alum, Cambio Alum, Knight-Hennessy, CEO, Cold |
| Bridge Detail | Text | the specific connection, e.g. "Harvard '19, overlapped at Bain 2020-21" |
| LinkedIn URL | URL | |
| Email | Email | |
| Source | Select | Connections Export, Web Search, Apollo, Manual |
| Outreach Status | Select | Not Contacted, Drafted, Sent, Replied, No Response, Meeting Booked |
| Last Contacted | Date | |
| Notes | Text | |

Share both databases with the Notion integration you authorized in step 1.

**4. Fill in `config/shortlist.yaml`** with your real target companies.

**5. Test manually:**

```bash
cd auto-recruiter
claude          # interactive first run — watch it work, fix anything odd
> /weekly-run   # or run stages one at a time: /discover, /contacts, /draft
```

Do 2–3 supervised runs before automating. Tune the rubric (in `CLAUDE.md`) and templates as you see real output.

**6. Install the cron job** (Friday 2:00 PM):

```bash
crontab -e
# add:
0 14 * * 5 /full/path/to/auto-recruiter/scripts/cron-run.sh
```

Note for macOS: cron works, but the machine must be awake at 2pm Friday. If your laptop sleeps, either use `launchd` with a `StartCalendarInterval` (fires on wake if missed) or just run `./scripts/cron-run.sh` manually — it's the same entry point.

Before relying on cron, double-check `scripts/cron-run.sh`'s `--allowedTools` list actually matches the tool names your environment exposes for Gmail/Notion/Drive — these can be connector-specific and don't always match the generic `mcp__gmail__*`-style names shown above.

## Manual trigger

```bash
./scripts/cron-run.sh        # full headless run, logs to runs/logs/
# or interactively:
claude
> /weekly-run                # or any single stage: /discover, /contacts, /draft
```

## Safety rails baked in

- Gmail **drafts only** — the send permission is never in `--allowedTools`
- Duplicate-contact and duplicate-thread checks before any draft or new Notion row
- Max 8 drafts/run; cold outreach (no shared background) only for companies scoring 80+
- No LinkedIn scraping — contacts come from your connections export + targeted, single-person web searches; ambiguous cases are left off rather than guessed
- `--max-turns 80` caps runaway runs; everything logs to `runs/`

## Weekly rhythm

Friday 2pm: run fires → ~2:30pm you get a run summary in `runs/` and drafts in Gmail → 10–15 min Friday afternoon review: verify emails, tweak drafts, hit send → Notion tracks everything.
