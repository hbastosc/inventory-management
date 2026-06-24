---
name: saas-ui-redesign
description: Redesign a Vue 3 app's UI into a modern SaaS-style interface with a dark vertical navigation sidebar (replacing a top nav bar), a design-token system, consistent spacing, and a polished professional look. Use when asked to modernize the UI, convert a top nav to a left sidebar, apply a SaaS look, or improve overall visual consistency/spacing.
---

# SaaS UI Redesign

A playbook for transforming a Vue 3 (Composition API) application from a **top navigation bar** into a **modern SaaS layout with a dark vertical sidebar**, backed by a small design-token system and a consistent spacing scale. It is written to be reusable on any Vue 3 app, and is grounded with a concrete reference implementation for this repository (the Catalyst Components inventory app) at the end.

## When to use this skill

Invoke when the user wants to:
- Convert a top nav bar into a left vertical sidebar
- Make the app look like a modern SaaS product (Linear / Stripe / Vercel-style)
- Improve spacing consistency and overall polish
- Introduce a design-token system (CSS variables) for layout/color/spacing

## Project rules (do not skip)

- **Any `.vue` file creation or significant edit MUST be delegated to the `vue-expert` subagent** (project rule in `CLAUDE.md`). This skill describes *what* to build; `vue-expert` builds it.
- **No emojis** anywhere in the UI.
- **Preserve all behavior**: routes, active-link highlighting, i18n keys (`t('...')`), global filters, and any existing design-system classes (`.card`, `.stat-card`, `.badge`, tables, `.page-header`). The redesign is structural/visual only.
- Verify in the real app with the browser MCP before declaring done (see Verification).

## Design philosophy (the "SaaS look")

1. **Vertical sidebar as the primary nav.** Fixed-width, full-height, dark, scrolls independently of content. Icons + labels. One clear accent color marks the active route.
2. **Calm, dark chrome + light canvas.** A dark sidebar (`#0f172a`) frames a light content area (`#f8fafc`). Content cards stay white. High contrast, low noise.
3. **A spacing scale, not magic numbers.** Standardize on a 4/8px-based scale exposed as CSS variables. Every gap/padding references the scale.
4. **Design tokens over hard-coded values.** Layout dimensions, colors, radius, and spacing live in `:root` custom properties so the look is tunable in one place.
5. **One accent, used sparingly.** A single brand/action color (here blue `#2563eb`) for the active nav item, primary buttons, and focus rings — nothing else competes.
6. **Consistent density & alignment.** Equal page padding everywhere; consistent card radius and border treatment; aligned headers.
7. **Accessible & responsive.** Keyboard focus states, `aria-current` on the active link, and a graceful collapse to an icon rail on narrow viewports.

## Design tokens (add to the root component's global stylesheet)

Define once in `:root` and consume everywhere in the new layout:

```css
:root {
  /* Layout */
  --sidebar-width: 248px;
  --sidebar-rail-width: 72px;     /* collapsed (narrow viewport) */
  --sidebar-bg: #0f172a;          /* slate-900 */
  --sidebar-fg: #cbd5e1;          /* slate-300 (default nav text) */
  --sidebar-fg-strong: #ffffff;
  --sidebar-hover-bg: rgba(255, 255, 255, 0.06);
  --sidebar-border: rgba(255, 255, 255, 0.08);
  --content-bg: #f8fafc;
  --accent: #2563eb;              /* active pill, primary actions, focus */

  /* Spacing scale (4px base) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Radius & elevation */
  --radius: 10px;
  --radius-sm: 8px;
}
```

Keep the app's existing palette (slate/blue) so the new chrome is cohesive with current cards and badges.

## The transformation (general steps)

Work in this order. Steps 2–5 are `.vue` edits → hand them to `vue-expert` with the precise spec.

### 1. Map the current layout
Read the root component (e.g. `App.vue`). Identify:
- The top-nav element and its parts: brand/logo, the list of nav links, and any right-aligned controls (language switcher, profile menu, notifications).
- Where nav links come from (router config + i18n keys) and their order.
- Any sticky sub-bars (e.g. a filter bar) and their `top:` offsets that assume the nav height.

### 2. Build a `Sidebar` component
A fixed-width dark column, `position: sticky; top: 0; height: 100vh`, flex-column with three regions:
- **Brand (top):** product name (white, bold) + subtitle (slate-400), with a bottom hairline border.
- **Nav (middle, `flex:1; overflow-y:auto`):** each link is `<router-link>` with an 18px inline-SVG icon (use `currentColor`) + label. States:
  - default `color: var(--sidebar-fg)`; padding `var(--space-3) 0.875rem`; gap `var(--space-3)`; `border-radius: var(--radius-sm)`.
  - hover `background: var(--sidebar-hover-bg); color: var(--sidebar-fg-strong)`.
  - active "pill" `background: var(--accent); color:#fff; font-weight:600`.
  - The home route (`/`) must use exact matching so it isn't always active (router-link `exact-active-class`, or `v-slot` with `isExactActive`).
  - `:focus-visible` outline for keyboard nav.
- **Footer (bottom):** relocate the right-aligned controls (language, profile) here, separated by a top border. They must be legible on dark and their dropdowns must open **upward** so they aren't clipped at the viewport bottom.

### 3. Re-theme relocated controls for the dark footer
If the profile/language components are scoped light-themed, add an optional `dark` prop (default `false`). When `dark`: light trigger text/icons (`#e2e8f0`, hover `#fff`, hover bg `var(--sidebar-hover-bg)`) and dropdowns positioned `bottom: 100%` (open upward). Leave the light behavior untouched when the prop is absent. Dropdown panels can remain white.

### 4. Restructure the root shell
```
<div class="app">                     /* display:flex; flex-direction:row */
  <Sidebar @show-profile-details="…" @show-tasks="…" />
  <div class="content-area">          /* flex:1; min-width:0; flex-column */
    <FilterBar />                      /* or any sticky sub-bar */
    <main class="main-content"><router-view /></main>
  </div>
  …modals…
</div>
```
- `.app { display:flex; flex-direction:row; min-height:100vh; }`
- `.content-area { flex:1; min-width:0; display:flex; flex-direction:column; }` (the `min-width:0` is essential so wide tables don't blow out the flex item).
- `.main-content`: drop any centered `max-width/margin:auto` that the old top-nav used; make it fluid: `flex:1; padding: var(--space-6) var(--space-8);`.
- Remove now-dead top-nav CSS (`.top-nav`, `.nav-tabs`, etc.). Do **not** touch the design-system classes.

### 5. Fix sticky sub-bars
Any bar that was `top: <nav-height>` becomes `top: 0`. Remove its centered `max-width/margin:auto` so it spans the content area; keep horizontal padding equal to the page padding (`var(--space-8)`).

### 6. Responsive collapse
Below ~900px, collapse the sidebar to a `--sidebar-rail-width` icon rail: hide labels, subtitle, and footer button text; center the icons; keep routing functional. Pure CSS media query — no JS toggle required for the default.

## Verification

1. Build the client (`npm run build` in `client/`) — must pass with no errors.
2. Start the app (use the project's start skill if present) and drive it with the browser MCP:
   - Sidebar renders dark, full height; every nav link routes correctly.
   - The active route shows the accent pill; `/` is highlighted only on the home page.
   - The filter/sub-bar still sticks and works; filters unchanged.
   - Profile + language controls work from the footer and their dropdowns are not clipped.
   - Spot-check 2–3 views (a table-heavy one and a chart/stat one) for spacing/alignment.
   - Narrow the viewport to confirm the icon-rail collapse.
3. Take a screenshot for the user.

---

## Reference implementation: Catalyst Components inventory app (this repo)

Concrete bindings for this codebase.

**Files**
- `client/src/App.vue` — root shell + global (non-scoped) design-system CSS. Restructure the shell and add the `:root` tokens here.
- `client/src/components/Sidebar.vue` — **new** dark sidebar.
- `client/src/components/FilterBar.vue` — sticky filter bar; change `top: 70px` → `top: 0`, drop the `max-width:1600px; margin:0 auto` centering, keep `padding: 0 var(--space-8)`.
- `client/src/components/ProfileMenu.vue`, `client/src/components/LanguageSwitcher.vue` — add the `dark` prop + upward dropdown for the footer.

**Nav links (order / route / i18n key / suggested icon)**
1. `/` — `t('nav.overview')` — grid/home
2. `/inventory` — `t('nav.inventory')` — box
3. `/orders` — `t('nav.orders')` — clipboard
4. `/restocking` — `t('nav.restocking')` — refresh/arrows
5. `/spending` — `t('nav.finance')` — dollar
6. `/demand` — `t('nav.demandForecast')` — trending-up
7. `/reports` — `t('nav.reports')` (fall back to the literal "Reports" if the key is absent) — document

Brand text: `t('nav.companyName')` + `t('nav.subtitle')`.

**Existing design system to preserve** (defined in `App.vue`): slate/blue palette — text `#0f172a`/`#64748b`, borders `#e2e8f0`, canvas `#f8fafc`, accent `#2563eb`, status green `#059669` / orange `#ea580c` / red `#dc2626`. Classes: `.page-header`, `.stats-grid`, `.stat-card` (+ `.success/.info/.warning/.danger`), `.card`, `.card-header`, `.card-title`, `.badge` (+ status modifiers), `.table-container` and base table styles. The sidebar is the only dark surface; cards stay white.

**Servers (for verification):** frontend `http://localhost:3000`, backend `http://localhost:8001` (use the project's `start` skill). Browser testing per `CLAUDE.md` uses the Playwright MCP when connected; otherwise the chrome-devtools MCP provides equivalent navigation/snapshot/screenshot capability.
