# Styleguide – HELIX PEPTIDES

Visuelles Konzept für den Webshop. Die Werte sind 1:1 als CSS-Variablen in
`css/style.css` (Block *Design-Tokens*) hinterlegt, damit Design und Code
synchron bleiben.

---

## 1. Designprinzip

**Klinisch, ruhig, vertrauenswürdig.** Viel Weissraum, ein klarer Teal-Akzent
(Labor/Wissenschaft) und ein violetter Sekundärakzent für Verläufe und „Neu"-Badges.
Dunkler Hero/Footer als Rahmen, helle Inhaltsflächen dazwischen.

---

## 2. Farben

| Rolle | Variable | HEX | Verwendung |
|-------|----------|-----|------------|
| Text (primär) | `--c-ink` | `#0b1016` | Fliesstext, dunkle Drench-Flächen |
| Text (sekundär) | `--c-muted` | `#566273` | Hilfetexte, Captions (≥4.5:1 auf Weiss) |
| Hintergrund | `--c-bg` | `#ffffff` | helle Seiten |
| Fläche | `--c-surface` | `#f1f5f8` | Karten, getönte Sektionen |
| Linien | `--c-line` | `#d7dee7` | Rahmen, Trenner |
| **Akzent Teal** | `--c-accent` | `#0c8f8f` | Buttons, Links auf Hell |
| Akzent dunkel | `--c-accent-dark` | `#0a7373` | Hover, Linktext |
| **Teal vivid** | `--c-accent-bright` | `#19e3c4` | Akzent auf Dunkel (Drench-CTA) |
| **Akzent Violett** | `--c-accent-2` | `#6a5cf0` | Verläufe, „Neu"-Badge, Cart-Badge |
| Erfolg | `--c-ok` | `#1f9d57` | Formular-Feedback, Toast |
| Warnung | `--c-warn` | `#c98a00` | Disclaimer-Banner |

**Strategie: Committed.** Teal trägt die Identität, near-black `#0b1016` „drencht"
Hero/Footer/USP-Sektion, Violett ist der sekundäre Spannungspol.

**Kontrast (geprüft):** `#0b1016` auf Weiss ≈ 17:1, `#566273` auf Weiss ≈ 4.7:1,
`#19e3c4` auf `#0b1016` ≈ 11:1 → erfüllt WCAG AA.

### Farbverlauf (Hero, drenched)
```
radial(rgba(106,92,240,.42)) + radial(rgba(25,227,196,.30)) + Raster-Mask auf #0b1016
```

---

## 3. Typografie

Bewusst **nicht** Inter/Space Grotesk (häufige KI-Default-Fonts) → eine Familie,
committet über Gewicht + Breite, plus Mono für Datenwerte:

| Einsatz | Font | Gewichte |
|---------|------|----------|
| Display / H1–H2 | **Archivo Expanded** | 700 / 800 (breit, neg. Tracking) |
| UI / H3 / Body | **Archivo** | 400 / 500 / 600 |
| Datenwerte (Reinheit, MW, Preis, Charge) | **Spline Sans Mono** | 400 / 500 |

Eingebunden über Google Fonts. Fallback: `system-ui, "Segoe UI", sans-serif`.

### Typo-Skala (responsive via `clamp()`)

| Element | Grösse | Zeilenhöhe |
|---------|--------|-----------|
| Hero-H1 | `clamp(2.4rem, 6vw, 4.4rem)` | 1.08 |
| H2 | `clamp(1.7rem, 4vw, 2.8rem)` | 1.08 |
| H3 | `1.25rem` | 1.15 |
| Lead | `clamp(1.05rem, 1.6vw, 1.2rem)` | 1.65 |
| Body | `1rem` (16px) | 1.65 |
| Mono-Daten | `0.72–1.1rem`, `tnum`, neg. Tracking | – |

> Slop bewusst vermieden: **kein** Eyebrow über jeder Section (stattdessen ein
> einziger Kicker-Stil), keine Hero-Metrik-Kacheln (stattdessen Trust-Ticker),
> kein Gradient-Text.

---

## 4. Abstände (8-px-Raster)

`--sp-1` … `--sp-6` = `0.5 / 1 / 1.5 / 2 / 3 / 4.5 rem`.
Sektionen nutzen `--sp-6` vertikal, Karten-Innenabstand `--sp-2`/`--sp-3`.

## 5. Radius & Schatten

| Token | Wert | Einsatz |
|-------|------|---------|
| `--r-sm` | 8px | Buttons, Inputs |
| `--r-md` | 14px | Karten |
| `--r-lg` | 22px | Produktbild, Hero-Elemente |
| `--shadow-sm` | weicher Doppel-Schatten | Karten (Ruhe) |
| `--shadow-md` | grösser | Karten (Hover) |

## 6. Komponenten (Auszug)

- **Button:** `.btn` + Variante (`--primary`, `--bright`, `--ghost`, `--light`), `--lg`, `--block`.
- **Produktkarte:** `.product-card` mit Media (4:3 SVG), Kategorie, Mono-Preis, „+"-Add-Button.
- **Cart:** Header-Button mit violettem Anzahl-Badge; Warenkorbseite mit Mengen-Steppern.
- **Spec-Chip:** Mono-Datenwert (Reinheit/MW/Charge) – „Instrument-Readout".
- **Pill/Badge:** `.pill` (`--accent`, `--violet`, `--bright`) für „Neu"/„inkl. CoA".
- **Formularfeld:** `.field` mit Label, Pflicht-Marker `.req`, Fokus-Ring in Akzentfarbe.
- **FAQ-Accordion:** natives `<details>/<summary>` (funktioniert ohne JS).
- **Toast:** kurze Bestätigung beim Hinzufügen zum Warenkorb.
- **Disclaimer:** gelbes Hinweis-Banner „Research Use Only".

## 7. Breakpoints

| Gerät | Breite | Layout-Verhalten |
|-------|--------|------------------|
| **Mobile** | ≤ 680px | 1 Spalte, Hamburger-Menü, Formularzeilen einspaltig |
| **Tablet** | 681–960px | Hero/Detail einspaltig, Footer 2 Spalten |
| **Desktop** | > 960px | Volles Grid, Hero 2-spaltig, Footer 4-spaltig |

Produktraster: `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))` –
passt sich automatisch an jede Breite an.
