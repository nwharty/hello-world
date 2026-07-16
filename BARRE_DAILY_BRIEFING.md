# Barre, MA Daily News Briefing

This document is the specification for a scheduled Claude routine that produces a
daily briefing on Barre, Massachusetts and the surrounding Quabbin-region towns.
The routine runs daily and delivers the briefing via the session transcript plus
a push/email notification summary.

## Goal

Give a daily pulse of what's going on in the area generally, then go deep on the
Town of Barre specifically — especially official town government activity
(select board and other board/committee meetings, town meeting warrants, newly
posted minutes and meeting recordings).

## Coverage

**Deep coverage — Town of Barre, MA (01005):**
- Official town meetings: Select Board, Planning Board, Finance Committee,
  Zoning Board, Board of Health, and Annual/Special Town Meeting
- Newly posted agendas, minutes, and meeting recordings
- Town announcements and news

**Headline coverage — surrounding towns** (the Barre Gazette's coverage area
plus immediate neighbors):
- Hardwick, Hubbardston, New Braintree, North Brookfield, Oakham, Petersham,
  Rutland, Phillipston
- Quabbin Regional School District (serves Barre, Hardwick, Hubbardston,
  New Braintree, Oakham)

## Sources

| Source | URL | Notes |
|---|---|---|
| Town of Barre, MA official site | https://www.townofbarre.com/ | Government pages, Select Board (`/selectboard`), town meeting info, latest-news list |
| MyTownGovernment meeting postings | https://mytowngovernment.org/01005 | Aggregates official Barre MA meeting postings with dates/times |
| Barre Gazette | https://barregazette.turley.com/ | Worcester County's oldest paper; covers Barre, Hardwick, Hubbardston, New Braintree, North Brookfield, Oakham, Petersham, Rutland |
| Worcester Telegram & Gazette | https://www.telegram.com/ | Regional coverage |
| MassLive (Worcester) | https://www.masslive.com/worcester/ | Regional coverage |
| Athol Daily News | https://www.atholdailynews.com/ | Covers Petersham/Phillipston side |
| YouTube / local cable access | search "Barre MA" meeting recordings | Town meeting videos have been posted to YouTube |

**Disambiguation:** There are several Barres. Barre **Town** and Barre **City**
in Vermont (barretown.org, barrecity.org, townofbarre.org) and Barre, NY are NOT
the target. Only use sources about Barre, **Massachusetts** (Worcester County,
zip 01005).

## Network-policy note

The Claude environment this routine runs in currently blocks direct web fetches
(WebFetch/curl) to arbitrary domains — only WebSearch is available. The routine
is written to degrade gracefully: it always attempts direct fetches of the town
site and Gazette first, and falls back to search when blocked. To unlock full
minutes/recording pull-down, loosen the environment's network access policy in
Claude Code on the web settings (see
https://code.claude.com/docs/en/claude-code-on-the-web).

## Briefing format

1. **TL;DR** — 3–5 bullets on the most notable items.
2. **Town of Barre — official business** — upcoming meetings (next ~7 days) with
   date/time/board; newly posted agendas, minutes, or recordings since the last
   briefing, each with a 2–4 sentence summary of substance (votes, budget items,
   hearings, appointments) and a link.
3. **Barre headlines** — local news stories mentioning Barre, MA from the last
   ~48 hours, each with a one-to-two sentence summary and link.
4. **Around the region** — brief headlines for the surrounding towns and the
   Quabbin school district.
5. **Notes** — anything the routine couldn't reach (blocked fetches, stale
   sources), so gaps are visible rather than silent.

If a section has nothing new, say so in one line rather than padding.

## Schedule

Daily at 11:00 UTC (7:00 a.m. Eastern during daylight time; 6:00 a.m. during
standard time). Managed as a Claude Code Remote routine ("Barre MA daily
briefing") — adjust via the routine settings or by asking Claude to update it.
