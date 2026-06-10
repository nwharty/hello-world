# Handoff: Executor & Estate Settlement Kit — Visual Redesign + Etsy Listing Carousel

## Overview

A complete visual design direction for the **Executor & Estate Settlement Kit** (repo: `nwharty/hello-world`, branch `claude/quirky-gauss-yjkwjo`, folder `executor-kit/`). Two deliverables:

1. **A 10-image Etsy listing carousel** (1080×1350, 4:5 portrait) — the marketing images that win the click and the sale.
2. **A visual redesign of the product itself** — the 12-tab workbook (`build_workbook.py`) and the "First 30 Days" PDF guide (`build_guide.py`), so the product matches the listing's promise.

Design strategy: calm, reassuring, human, quietly premium. The buyer is a grieving, overwhelmed executor. Every design choice reduces noise and signals "you're in safe hands." The carousel leads with the product's true differentiators (from `research_notes.md`): automatic Final Accounting, death-certificate tracking, the emotional First-30-Days onboarding, and Excel + Google Sheets in one purchase.

## About the Design Files

The files in this bundle are **design references created in HTML** — they show intended look and content, they are not production code. The task is to **recreate these designs in the existing codebase environment**:

- The **workbook redesign** → applied as styling changes in `executor-kit/build_workbook.py` (openpyxl: fills, fonts, borders, column widths, freeze panes, tab colors).
- The **guide redesign** → applied as styling changes in `executor-kit/build_guide.py` (reportlab: colors, type hierarchy, page furniture).
- The **listing carousel** → 10 final PNG/JPG images at 1080×1350. Options: render the bundled HTML cards headless (e.g. Playwright screenshot of each artboard at native size) or rebuild in an image tool. The HTML is the source of truth for layout/copy.

Open `Executor Kit — Product & Listing Design.html` in a browser to view everything on a pan/zoom canvas (it loads React via CDN; needs network for fonts/CDN).

## Fidelity

**High-fidelity.** Colors, type, spacing, and copy are final-intent. Recreate faithfully; exact px values below.

## Design Tokens

### Colors
| Token | Hex | Usage |
|---|---|---|
| Navy | `#223A52` | Primary text, dark panels, table header rows |
| Navy deep | `#182B3E` | Deepest gradient stop on covers |
| Navy soft | `#3A566F` | Secondary dark fill |
| Paper | `#FAF7F1` | Main warm off-white background |
| Paper 2 | `#F4EDE1` | Alt card background, zebra-stripe rows (at ~45% opacity over white) |
| Paper 3 | `#EFE6D6` | Deeper warm neutral |
| White | `#FFFDF9` | Card/sheet surfaces |
| Sage | `#E7EFE5` | Calm tint — "done" chips, callout panels, card-03 bg |
| Sage deep | `#C4D6C0` | Sage accents |
| Sage ink | `#4A6450` | Text on sage |
| Brass/Gold | `#B58A34` | THE accent: eyebrows, rules, numerals. Use sparingly |
| Gold soft | `#D4B164` | Gold on dark backgrounds |
| Gold pale | `#ECDCB4` | "In progress" chip background (text `#7C5D1A`) |
| Clay | `#BD7B5C` | Warm human accent — used ONCE (the "calculates itself" badge) |
| OK green | `#5D8A63` | Money-in amounts |
| Ink 70/55/40 | navy at 70%/55%/40% alpha | Body text, captions, faint labels |
| Line | navy at 13% / 8% alpha | Hairline borders |

This evolves the original in-code brand (navy `#1F3A5F`, gold `#C9A227`, sage `#E8EFE5`) — warmer, softer. The workbook scripts should adopt these hex values.

### Typography
| Role | Family | Weights | Notes |
|---|---|---|---|
| Display/headlines | **Spectral** (serif) | 400/500/600 | 500 for display; line-height ~1.02–1.1; letter-spacing −0.012em |
| Body/UI | **Hanken Grotesk** (sans) | 400–800 | Body 1.45–1.6 line-height |
| Eyebrows/data/captions | **Spline Sans Mono** | 400/500 | Eyebrows: 13px, UPPERCASE, letter-spacing 0.22em, brass color |

All on Google Fonts. For the Excel workbook (limited fonts), map: Spectral → Georgia, Hanken Grotesk → Calibri/Aptos, Spline Sans Mono → Consolas. For the reportlab PDF, embed the real TTFs if possible.

### Spacing & Shape
- Radii: 8 / 14 / 22 / 30 px (sm/md/lg/xl); chips/pills fully rounded (999px)
- Card padding: 24px (small tiles) – 76px (listing card margins)
- Listing card safe padding: 70–76px on all sides
- Shadows: soft navy-tinted, e.g. `0 8px 24px rgba(24,43,62,.10)`; large hero: `0 30px 70px rgba(24,43,62,.18)`
- Thin brass rule: 64×2px, radius 2px — signature divider

### Logo / Mark
"The Executor Kit" wordmark: a navy circle containing a brass four-point star (clip-path polygon, 38% of circle size) with an inner 1.5px ring at `rgba(212,177,100,.5)`; Spectral wordmark + mono sub-line "ESTATE SETTLEMENT, ORGANIZED" (0.2em tracking, 55% ink).

## Screens / Views

### A. Etsy listing carousel (10 images, 1080×1350 each)
Common furniture on every card: top row = small wordmark (left) + mono "NN / 10" counter (right); 70–76px padding; eyebrow → serif headline → sans lede pattern.

| # | Card | BG | Key content |
|---|---|---|---|
| 01 | Hero | Paper | "The complete executor system." (74px Spectral) + sheet mock rotated −1.2°, guide booklet overlapping right, trust strip bottom (5 stars · "Excel + Google Sheets" · "12-tab workbook + 30-day guide") |
| 02 | 12 tabs | Paper | 2-col grid of 12 white cards: brass serif number + tab name + one-line description |
| 03 | First 30 Days | Sage | Headline "Know what's urgent — and what can wait." + sheet mock with Priority/Task/Why/Status table |
| 04 | Final Accounting | Navy | "The hardest report writes itself." White accounting summary card (5 lines, sage total row) + rotated clay badge "calculates itself ✦" |
| 05 | The guide | Paper 2 | Guide cover (340px) + 4-item check-list of guide contents |
| 06 | What's included | Sage | Tile grid: workbook minisheet (span 2), guide cover, Excel+Sheets pills, final accounting, setup |
| 07 | Three rules | Navy | 3 numbered rule cards (brass serif numerals, `rgba(250,247,241,.06)` fill, gold 22% border) |
| 08 | Cert. tracker | Paper 2 | Notifications sheet mock (620px) + navy stat card "11 / 15 certified copies used" with gold progress bar |
| 09 | Both formats | Paper | Two browser-chrome frames (Excel green `#3A7150` / Sheets green `#2F7D5A`) joined by serif "+", sage pill below |
| 10 | Why this one | Paper 2 | 3 numbered steps, lifestyle-photo slot (user image), quote "Calmly. Completely. In the order that matters.", disclaimer in 13.5px ink-40 |

Exact copy for all cards is in `executor-design/listing-cards-1.jsx` and `listing-cards-2.jsx` — use it verbatim; it was written to convert.

### B. Workbook redesign (`build_workbook.py`)
The "sheet" visual language (see `ProdStartHere`, `ProdAssets`, `ProdLedger` in `product-cards.jsx`):

- **Header rows**: navy `#223A52` fill, white 12.5px semibold, generous 13×16px cell padding equivalent
- **Zebra striping**: warm `#F4EDE1` at ~45% (≈ `#F9F4EB` solid) on even rows
- **Status chips** (render as filled cells with colored text in Excel): Done = sage bg/sage-ink text; In progress = gold-pale bg/`#7C5D1A`; Not started = `#EEF1F4`/55% ink
- **Money**: tabular numerals, semibold navy; money-in green `#5D8A63` with "+" prefix, money-out navy with "−"
- **Phase/priority labels** ("Week 1" etc.): mono, brass, 11px, 0.06em tracking
- **Total rows**: sage fill, 2px navy top border, bold
- **Tab colors**: brass for key tabs (Start Here, Assets, Estate Ledger), navy for First 30 Days, red `#B00020` for Final Accounting, neutral for the rest
- **Start Here tab**: two-zone layout — left: mark + title + 5 numbered "How to use this kit" steps (numbered sage squares); right: tab directory list + sage Google Sheets instructions panel

### C. Guide redesign (`build_guide.py`)
- **Cover**: navy gradient (165°, `#27425D` → `#172838`), double brass keyline inset frame (1px at 40% + 6px at 10% gold), mark top-left, "PDF GUIDE" mono top-right, brass eyebrow "THE COMPANION GUIDE", Spectral 64px title "The Executor's First 30 Days", brass rule, 21px lede at 74% paper
- **Interior pages**: white, 52×50px margins; brass mono eyebrow → Spectral 34px heading → 16px body at 1.6; numbered lists use brass serif numerals; checklists use 26px sage circles with sage-ink checkmarks; callout = sage panel, 12px radius, 18×20px padding; folios: mono 12px 40% ink, alternating corners ("2 — The Executor's First 30 Days")

## Interactions & Behavior
Static deliverables — no interactions to implement. (The HTML canvas's pan/zoom is the review tool, not part of the design.)

## State Management
None required.

## Assets
- All graphics are CSS/SVG-drawn in the bundled files (mark, star icons, checkmarks, sheet mocks) — no binary assets
- Card 10 contains an `<image-slot>` placeholder for an optional warm lifestyle photo (sunlit desk / hands & notebook) — to be supplied by the owner
- Fonts: Google Fonts — Spectral, Hanken Grotesk, Spline Sans Mono

## Files
| File | Contents |
|---|---|
| `Executor Kit — Product & Listing Design.html` | Main canvas — open in a browser to view all 16 artboards |
| `executor-design/brand.css` | All design tokens + sheet-mock component CSS (source of truth for values) |
| `executor-design/kit-primitives.jsx` | Mark, wordmark, sheet frame, tab strip, chips, icons |
| `executor-design/listing-cards-1.jsx` | Listing cards 01–05 (incl. hero) |
| `executor-design/listing-cards-2.jsx` | Listing cards 06–10 |
| `executor-design/product-cards.jsx` | Workbook tab redesigns + guide cover & spread |
| `executor-design/design-canvas.jsx`, `browser-window.jsx`, `image-slot.js` | Canvas/review scaffolding only — not part of the design |

## Suggested implementation order
1. Adopt the new tokens in `build_workbook.py` (colors, fonts, chip fills, zebra rows, tab colors) — biggest product-quality lift
2. Restyle `build_guide.py` cover + interior per section C
3. Export the 10 listing images at 1080×1350 (screenshot each artboard from the HTML, or rebuild) and upload to the Etsy listing in the order given
