---
description: Daily cross-app briefing — calendar, tasks, email, files — delivered as a push notification
---

# Morning Briefing

You are producing a single daily briefing for the user by sweeping their connected
services, then delivering the highlights as a **push notification**. Run this end to
end without asking follow-up questions — it is meant to run unattended on a schedule.

## Step 1 — Gather (run these queries in parallel)

Resolve "today" from the current date in context. Then collect:

1. **Calendar** — list events from now through the next 7 days, ordered by start time.
   Check the primary calendar; if it looks empty, list the user's other calendars and
   check those too.
2. **Todoist** — tasks due from `today` across the next 7 days, **including overdue**.
   Treat overdue and due-today items as the highest priority.
3. **Email** — unread inbox threads from the last ~3 days. Triage: separate genuine
   action items (replies needed, bills, deadlines, personal mail) from marketing/promos.
   Do NOT mark anything as read — this is read-only triage.
4. **Files** — recent files, to surface anything time-sensitive (e.g. shared schedules,
   event/date docs). Skip personal/financial docs unless they contain a dated action.

## Step 2 — Synthesize

Build a prioritized briefing with these buckets (omit any bucket that's empty):

- 🔴 **Needs attention now** — overdue tasks, bills due today, emails awaiting a reply.
- 🟡 **Coming up** — events and deadlines in the next few days.
- 📧 **Email** — one line on whether the inbox is clear or has real items (ignore promos).
- 🗓️ **Calendar** — today's events; note if the day is clear.

Be concrete: include amounts, dates, and names. Flag anything overdue explicitly.

## Step 3 — Deliver

1. Print the full briefing in the session (Markdown).
2. Send a **push notification** with just the headline items — lead with anything
   overdue or due today, then a count of what else is coming. Keep it under 200
   characters, one line, no markdown. Example:
   `Overdue: activate AmEx Gold. Today: clear. This week: Tesla $316 (Mon), 2 school events.`
   If there is genuinely nothing actionable, say so briefly rather than padding it.

## Notes

- This runs in an ephemeral container, so it does not persist state between runs — every
  run is a fresh sweep of live data.
- Read-only by default. Do not send email, complete tasks, or modify calendar/files
  unless the user has explicitly asked for that behavior.
