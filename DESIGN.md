# Design

Visuelles System für HELIX PEPTIDES. Quelle der Wahrheit ist `css/style.css`
(Block *Design-Tokens*); dieses Dokument beschreibt die Absicht dahinter.
Format angelehnt an Google Stitch DESIGN.md.

## Aesthetic / Reference

**„Lab instrument readout, committed."** Klinisch-präzise Schweizer Labor-Ästhetik:
helle, ruhige Browsing-Flächen für Produkte, kombiniert mit **gedrenchten,
near-black Sektionen** (Hero, CTA-Bänder, Footer) in denen ein vives Teal die
Marke trägt. Datenwerte erscheinen in Monospace wie auf einem Messgerät.
Nicht: SaaS-Landingpage, nicht Editorial-Magazin, nicht Neon-Supplement-Shop.

## Color (committed)

Strategie: **Committed** – Teal trägt die Identität, Near-Black drenched die
Akzent-Sektionen, Violett als sekundärer Spannungspol.

| Rolle | Token | Wert | Einsatz |
|-------|-------|------|---------|
| Ink (Text) | `--c-ink` | `#0b1016` | Text, dunkle Drench-Flächen |
| Ink soft | `--c-ink-2` | `#1a2230` | sekundäre dunkle Fläche |
| Text muted | `--c-muted` | `#566273` | Sekundärtext (≥4.5:1 auf Weiss) |
| BG | `--c-bg` | `#ffffff` | helle Seiten |
| Surface | `--c-surface` | `#f1f5f8` | Karten, getönte Sektionen |
| Line | `--c-line` | `#d7dee7` | Rahmen |
| **Teal (Akzent)** | `--c-accent` | `#0c8f8f` | Buttons, Links auf Hell |
| **Teal vivid** | `--c-accent-bright` | `#19e3c4` | Akzent auf Dunkel (Drench) |
| Violett | `--c-accent-2` | `#6a5cf0` | „Neu", Verläufe, Spannung |
| OK / Warn | `--c-ok` / `--c-warn` | `#1f9d57` / `#c98a00` | Feedback, Disclaimer |

Kontrast verifiziert: `#0b1016` auf Weiss ≈ 17:1; `#566273` auf Weiss ≈ 4.7:1;
`#19e3c4` auf `#0b1016` ≈ 11:1 (heller Text auf Dunkel).

## Typography

**Eine Familie, committet über Gewicht + Breite** (statt timider Display+Body-Paarung):

| Einsatz | Font | Stil |
|---------|------|------|
| Display / H1–H2 | **Archivo Expanded** | 700/800, Breitlauf, leicht negatives Tracking |
| UI / H3 / Body | **Archivo** | 400/500/600 |
| Datenwerte (MW, Reinheit, Preis, Charge) | **Spline Sans Mono** | 500, tabellarisch – „Messgerät" |

Bewusst **nicht** Inter/Space Grotesk (Reflex-Defaults). Skala modular, fluid
`clamp()`, Verhältnis ≥1.25. `text-wrap: balance` auf Überschriften.

| Element | Grösse |
|---------|--------|
| Display (Hero) | `clamp(2.6rem, 7vw, 5rem)` |
| H2 | `clamp(1.7rem, 4vw, 2.8rem)` |
| H3 | `1.25rem` |
| Body | `1rem` / line-height 1.65 |
| Mono-Daten | `0.85–1rem`, `letter-spacing -.01em` |

## Layout

- Container max. 1180px, fluide Abstände (`clamp`) für Rhythmus.
- **Grid** für Produktraster (`repeat(auto-fill, minmax(250px,1fr))`), Footer, Specs.
- **Flex** für 1D (Nav, Filter, Buttons).
- Asymmetrischer Hero (Text links breiter, Molekül-Art rechts).
- Drench-Sektionen voller Breite mit Molekül-/Raster-Hintergrund.
- Kein Eyebrow über jeder Section (Slop). Höchstens ein bewusster Kicker.

## Components

- **Button** `.btn` (`--primary` Teal, `--ghost`, `--light`, `--dark`), `--lg`/`--block`.
- **Produktkarte** mit Media (4:3 SVG), Kategorie, Titel, Mono-Preis, „In den Warenkorb".
- **Spec-Chip** Mono-Datenwert (Reinheit/MW/Charge).
- **Cart**: Header-Button mit Anzahl-Badge, Warenkorbseite mit Web-Storage.
- **Disclaimer-Band** „Research Use Only" (warn-getönt).
- **Filter-Pills** mit aktivem Zustand.

## Motion

- Ein orchestrierter Page-Load-Reveal im Hero (Staffelung), sonst zurückhaltend.
- Hover: Karten heben + Akzentkante; Buttons leichtes Press.
- Jede Animation mit `@media (prefers-reduced-motion: reduce)`-Fallback (Crossfade/instant).
- Ease-out (quart/expo), kein Bounce.

## Imagery

Selbst generierte **SVG-Molekül-/Vial-Grafiken** je Produkt (kategoriefarbig),
plus Logo und Team-Avatare. SVG zählt als Imagery, ist offline-robust und passt
zum „100 % eigener Code"-Anspruch des Auftrags.
