# Road to 40

Personal life-plan tracker for Nathaniel Harty — six lanes (Financial, Career, Family, Health, Home, Personal) spanning age 37 (Sep 2026) to 40 (Sep 16, 2029), plus a live credit-card payoff and emergency-fund tracker.

## What this is

A single self-contained HTML file (`index.html`). No build step, no dependencies, no framework, no network calls — the Archivo and IBM Plex Mono fonts are embedded as data URIs. Open it in any browser and it works.

## Where it's published

The live copy is a **private Claude artifact** (hosted on claude.ai, visible only when logged into the owner's Claude account). To redeploy after editing, ask Claude Code to republish `index.html` as an artifact to the same URL.

⚠️ **Do not merge this into `master` / serve it via GitHub Pages.** This repo's Pages site is public, and this page contains real financial details. The subfolder only exists here as source control for the private artifact.

## Passcode gate

- First visit on a device asks you to set a passcode (4+ characters). It's stored on that device as a salted SHA-256 hash — each device/browser sets its own.
- Unlock lasts for the browser tab session; the **Lock** button in the header re-locks immediately.
- This is a light second layer against casual access (shared computer, shoulder-surfing). The real protection is the artifact being private to the Claude account — anyone who can read the raw file can see the data regardless of the gate.
- Forgot the passcode? Clear the site's localStorage key `road-to-40-pass` (this keeps your goal/payment data, which lives under a different key).

## Layout

- **Landing page**: headline stats (time to 40 in y/m/d, current phase, goals done, baby ETA → baby age after Nov 5 2026) + a journey timeline bar across ages 37/38/39 (Roots → Build → Reach) + the six lane cards. No finance figures on the landing page at all.
- **Financial lane**: yearly goals, then a **Debt payoff & emergency fund** section with the two card trackers, the windfall kill sequence, and the EF tracker.

## Storage

The app uses a storage adapter (`store` object near the top of the `<script>`):

- Inside Claude artifacts → uses `window.storage` (Claude's persistent key-value store) when present
- Everywhere else → falls back to `localStorage` automatically

State is saved under the key `road-to-40-state` as a single JSON blob:
`{ lanes: { financial: { y37: [{text, done}], ... }, ... }, tracker: { payments, windfalls, efTarget } }`

Saves are debounced (500ms) with automatic retries. Note: state is per-browser — there is no sync between devices yet (see ideas below).

## Key facts baked into the code

- Year blocks are the ages 37 (Sep 26–27), 38 (Sep 27–28), 39 (Sep 28–29), plus a “40 · The Marker” finish-line block; all timers count down to the 40th birthday, Sep 16 2029

- Card 1: BoA ···3215, start balance $11,314.50, 0% promo dies **Oct 20, 2026** (then 19.49%)
- Card 2: BofA/Merrill transfer, start balance $10,000, 0% promo dies **July 2027** (then 18.49%)
- Windfall plan: Aug 15 2026 RSU (~$10K net) → Card 1; Sep 2026 bonus (~$10K net) → Card 2
- Emergency fund target: editable, default $55,000
- Baby ETA: ~Nov 5, 2026 · 40th birthday: Sep 16, 2029

## Run locally

Just open `index.html` in a browser, or:

```
python3 -m http.server 8000
```

## Ideas for next iterations

- Export/import state as JSON (backup + move data between devices)
- Net worth chart over time
- Quarterly check-in notes per lane
- Home equity loan payoff tracker (~$110K @ 7.44%, target $0 by Sep 2029)
