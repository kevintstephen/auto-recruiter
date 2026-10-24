---
description: Draft personalized Gmail outreach for contacts not yet reached out to, up to the per-run cap
---

Read `CLAUDE.md` first for the email drafting rules and hard rules — apply them throughout this command. Read `data/resume.md` for Kevin's positioning details to personalize with.

1. Query the Contacts database for rows with `Outreach Status = Not Contacted`, joined to their related Company row for score and hook material (`Last Round`, `Notes`).
2. Filter out any contact whose company scores below `scoring.min_score_to_map_contacts`, and any `Bridge = Cold` contact whose company scores below `scoring.min_score_for_cold_outreach` (see `config/targets.yaml`).
3. Sort remaining contacts by company score (desc), then by contact priority tier (1st-degree > CEO > alumni > cold). Take the top N up to `scoring.max_drafts_per_run`.
4. For each contact:
   a. Search Gmail for any prior thread with this person's email or anyone @ the company's domain.
   b. If a prior thread exists: draft an in-thread follow-up (shorter, references the earlier exchange) instead of a fresh email. Flag this in the run log.
   c. If no prior thread: pick a template based on `Bridge` — `1st-degree`/strong mutual → `config/templates/warm-mutual.md`; alumni tiers → `config/templates/alum-cold.md`; `CEO`/`Cold` → `config/templates/pure-cold.md`. Personalize heavily using the company hook and Kevin's background from `data/resume.md` — don't just fill in the template mechanically.
   d. Create a Gmail draft (never send).
   e. Update the Contact's `Outreach Status` to `Drafted` and `Last Contacted` to today's date.
5. Append a "Draft" section to `runs/YYYY-MM-DD.md` listing: who was drafted, which template/tone was used, and anything skipped (and why — score too low, over the cap, etc.).
6. If Gmail search/draft creation fails for a contact, note it in the run log and continue with the rest — don't fail the whole run.
