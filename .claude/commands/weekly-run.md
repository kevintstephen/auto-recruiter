---
description: Full weekly pipeline — discover companies, map contacts, draft outreach
---

Run the three stages in order, in this same session so context (companies/contacts just found) carries forward without re-querying Notion from scratch:

1. `/discover` — find/update companies
2. `/contacts` — find/update contacts at qualifying companies
3. `/draft` — draft outreach for un-contacted contacts, up to the per-run cap

After all three stages finish, write (don't just append) a final summary at the top of `runs/YYYY-MM-DD.md` above the three stage sections: total companies screened, new vs. updated, contacts found, drafts created, and a short "needs Kevin's attention" list (e.g. qualifying companies with no contact found, data sources that failed, anything ambiguous).
