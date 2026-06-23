# Claude Code Handoff — anavvanzin.com

## Context

You are continuing work on **anavvanzin.com** (repo: `anavvanzin.github.io`, branch: `main`). The site is a personal academic website for Ana Vanzin (PPGD/UFSC PhD candidate), combining a retro desktop metaphor with a luxury design system called "Vanguard Protocol."

## What Was Done (this session)

All committed and pushed to `main`:

| Commit | Feature |
|--------|---------|
| `20d83db` | Mobile Premium (drag handle, slideUp animation, touch targets) |
| `b62032a` | Mover-se (4 navigation paradigms standalone page) |
| `bb20f4f` | Sala de Leitura (React component, 4 shelves, theme filtering) |
| `a9474a3` | Manifesto (6 cinematic slides standalone page) |
| `73cfbae` | Leitura-Iconografia (interactive SVG, pins, blindfold toggle) |
| `11191b8` | Vanguard Design System (tokens, Double-Bezel, Fluid Island) |
| `bb9470d` | Design specs and implementation plans (docs/) |

## Architecture

```
anavvanzin.github.io/
├── index.html              ← Desktop (React shell)
├── Desktop.js              ← Window manager, menu bar, dock, boot
├── window-contents.js      ← Window body components (WTese, WSobre, etc.)
├── styles.css              ← Vanguard Design System tokens + global styles
├── WLeituraIconografia.js  ← Interactive thesis reading page (React)
├── WSalaLeitura.js         ← Reading room with theme filtering (React)
├── manifesto.html          ← Standalone cinematic slide presentation
├── mover-se.html           ← Standalone 4-paradigm navigation studio
├── conceitos.html          ← Concepts page
├── tokens/                 ← Color, typography, spacing, base tokens
├── fonts/                  ← Cormorant Garamond, Hanken Grotesk, JetBrains Mono
├── assets/                 ← Monograms, seals, atlas images
└── docs/superpowers/       ← Design specs + implementation plans
```

## Design System (Vanguard Protocol)

Read the handoff at `/Users/ana/Downloads/design_handoff_research_wing/Ana Vanzin Design System/` for the complete visual bible. Key principles:

### Colors (Iuris Memoria palette)
- `--paper: #EFE5CF` (vellum ground)
- `--ink: #1A1612` (warm black)
- `--rubric: #9B2C1C` (iron-gall red, accents)
- `--brand-amethyst: #8A5FA8` (feminine archival voice)
- `--terracotta: #A04030` (living margin)
- `--cabinet-top: #1B2B4A` (institutional deep blue)

### Typography (Three Voices)
- Display: `Instrument Serif` or `Cormorant Garamond` (sartorial, rubrics, inscriptions)
- Body: `Crimson Pro` (thesis voice, fluid reading)
- Mono: `JetBrains Mono` (technical precision, labels, metadata)

### Motion
- NO bounces. Only fades + slides with deceleration
- Cubic-bezier: `0.22, 1, 0.36, 1` (deceleration), `0.5, 0, 0.18, 1` (risco), `0.34, 1.5, 0.5, 1` (spring)
- Animations ONLY use `transform` and `opacity`
- `prefers-reduced-motion` must disable all animations

### Anti-Patterns (NEVER do these)
- NO Inter, Roboto, Arial, Open Sans, Helvetica
- NO Lucide/FontAwesome/Material icons
- NO `1px solid gray` borders or `shadow-md`
- NO sticky navbar edge-to-edge
- NO 3-column Bootstrap grids
- NO `linear` or `ease-in-out` transitions

## What's Pending

### High Priority
1. **Polish Mover-se** — The 4 paradigms are implemented but may need visual refinement
2. **Cross-page consistency** — Ensure all standalone pages (Manifesto, Mover-se) share identical top bar styling and back navigation
3. **Mobile audit** — Test all pages on mobile viewport, fix any overflow/spacing issues

### Medium Priority
4. **More handoff pages** — Other HiFi pages in the handoff that could become standalone pages:
   - `Tese (Leitura-Iconografia).html` — already implemented as WLeituraIconografia.js
   - `Pagina-Impressa.html` — could become a print-optimized view
   - `Leitura-Iconografia.html` — already implemented

### Low Priority
5. **Performance** — Audit bundle size, lazy-load heavy assets
6. **SEO** — Add meta tags, structured data for academic content
7. **Accessibility** — Full WCAG 2.1 AA audit

## Key Files to Read Before Starting

1. `Desktop.js` — The heart of the site. Window manager, menu, dock, boot sequence.
2. `styles.css` — All design tokens and global styles.
3. `docs/superpowers/specs/` — Design specs for implemented features.
4. `/Users/ana/Downloads/design_handoff_research_wing/Ana Vanzin Design System/` — The visual bible.

## Git Rules

- Email for commits: `77904873+anavvanzin@users.noreply.github.com`
- Name: `anavvanzin`
- Branch: `main` (push-to-main is gated, but authorized)
- Use `GIT_EDITOR=true` for commits (vim locks terminal)

## User Preferences

- Ana speaks Portuguese, English, and French
- She prefers practical, direct communication
- "Brainstorming" skill must be used before any creative work
- She values premium visual quality — "sem graça" is not acceptable
- She uses Claude Code and Hermes Agent interchangeably
- She is a PhD candidate at PPGD/UFSC with cotutela at UGent
- Her thesis is ICONOCRACIA — female allegories in legal iconography
