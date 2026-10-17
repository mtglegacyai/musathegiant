# MTG 👑 Dashboard Standard

Every dashboard page on MusaTheGiant.com (and MTG's other sites) uses the same layout, so visitors learn it once and find content faster everywhere. The design reference is the Bellver Card guide sidebar: https://www.musathegiant.com/cards/bellvercards/learn/

## What every dashboard has

| Part | Rule |
|---|---|
| Side menu | Label groups, icon chip + title + one-line subtitle per item, glowing bar on the active item, sticky bottom block |
| Collapse pill | Vertical pill on the menu edge, vertically centred. Laptops and desktops (1061px and wider): collapses the menu and widens the page. Choice remembered in `localStorage` key `mtg-side` |
| Phones and tablets | Menu becomes a slide-out drawer with a dimmed page behind it. Menu button (bars turn into a cross) plus the small edge tab both open it. Escape and tapping outside close it |
| Top bar | Menu button (phones), breadcrumb, then actions on the right: 🏡 GO HOME always, DASHBOARD where it helps |
| 🏡 GO HOME | Top bar and bottom of the side menu. Goes to the home page of that site or section |
| Button motion | GO HOME and DASHBOARD wear the slow orbiting light ring used on every CTA. Calm static ring for reduced motion |
| Theme | Colours and fonts follow the page's own tool, opportunity or income stream. Sizes, positions and behaviour never change |

## How to build a new dashboard on musathegiant.com

1. Load `/assets/mtg-dash.css` after the page's own styles and `/assets/mtg-dash.js` (defer) at the end of the body.
2. Use this skeleton (copy from `dashboard.html`):
   - `<div class="md-shell">` with the one-line pre-paint script first
   - `<aside class="md-side" id="mtg-menu">` with `.md-label` groups, `.md-nav` items and a `.md-bot` block holding the GO HOME button
   - `<button class="md-toggle">` and `<div class="md-scrim">`
   - `<div class="md-main">` with `<header class="md-top">` (`.md-menu`, `.md-crumb`, `.md-act`) and the page's `<main>`
3. Buttons: `<a class="md-btn md-home" href="/"><span class="emo" aria-hidden="true">🏡</span>Go Home</a>` and `<a class="md-btn md-dash" href="/dashboard.html"><span class="emo" aria-hidden="true">📊</span>Dashboard</a>`.
4. To match a page's theme, override only the `--md-*` tokens (accent, ring colours, panel backgrounds, fonts).

Regular (non-dashboard) pages: give the header Dashboard link the `mtg-ring` class and the 📊 icon (styles live in `/assets/pages.css`).

## Where it is used

- musathegiant.com: `/dashboard.html`, `/cards/`, `/101/` (course menu), all Bellver guide pages (built by `cards/bellvercards/_build/`, which also builds the team copies)
- clickbaitpaysus.com: every course page in the learning dashboard (`assets/styles.css`, `assets/app.js`, class `side-pill` and `go-home`)
