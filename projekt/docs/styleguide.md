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
| Text (primär) | `--c-ink` | `#14181f` | Fliesstext, Überschriften |
| Text (sekundär) | `--c-muted` | `#5b6573` | Hilfetexte, Captions |
| Hintergrund | `--c-bg` | `#ffffff` | Seite |
| Fläche | `--c-surface` | `#f4f7fa` | Karten, getönte Sektionen |
| Linien | `--c-line` | `#dce3ec` | Rahmen, Trenner |
| **Akzent (primär)** | `--c-accent` | `#0fa3a3` | Buttons, Links, Icons |
| Akzent dunkel | `--c-accent-dark` | `#0b7e7e` | Hover, Linktext |
| **Akzent (sekundär)** | `--c-accent-2` | `#5b54d6` | Verläufe, „Neu"-Badge |
| Dunkel | `--c-deep` | `#0e1622` | Hero, Footer |
| Erfolg | `--c-ok` | `#1f9d57` | Formular-Feedback |
| Warnung | `--c-warn` | `#c98a00` | Disclaimer-Banner |

**Kontrast:** Text (`#14181f`) auf Weiss erreicht ca. 15:1, Akzent-Buttons (weisser
Text auf `#0fa3a3`) ca. 3.4:1 für grosse/fette Schrift → erfüllt WCAG AA.

### Farbverlauf (Hero)
```
radial-gradient(rgba(91,84,214,.55)) + radial-gradient(rgba(15,163,163,.55)) auf #0e1622
```

---

## 3. Typografie

| Einsatz | Font | Gewichte | Beispiel |
|---------|------|----------|----------|
| Überschriften / UI | **Space Grotesk** | 500 / 600 / 700 | H1–H4, Buttons, Preise |
| Fliesstext | **Inter** | 400 / 500 / 600 | Absätze, Formulare |

Eingebunden über Google Fonts. Fallback-Stack: `system-ui, "Segoe UI", sans-serif`.

### Typo-Skala (responsive via `clamp()`)

| Element | Grösse | Zeilenhöhe |
|---------|--------|-----------|
| H1 | `clamp(2rem, 5vw, 3.1rem)` | 1.15 |
| H2 | `clamp(1.5rem, 3.5vw, 2.2rem)` | 1.15 |
| H3 | `1.25rem` | 1.15 |
| Lead | `1.1rem` | 1.65 |
| Body | `1rem` (16px) | 1.65 |
| Eyebrow / Caption | `0.78rem`, `letter-spacing .14em`, UPPERCASE | – |

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

- **Button:** `.btn` + Variante (`--primary`, `--ghost`, `--light`), `--lg`, `--block`.
- **Produktkarte:** `.product-card` mit Media (4:3), Kategorie, Titel, Preis, CTA.
- **Pill/Badge:** `.pill` (`--accent`, `--violet`) für Status wie „Neu" oder „inkl. CoA".
- **Formularfeld:** `.field` mit Label, Pflicht-Marker `.req`, Fokus-Ring in Akzentfarbe.
- **Disclaimer:** gelbes Hinweis-Banner „Research Use Only".

## 7. Breakpoints

| Gerät | Breite | Layout-Verhalten |
|-------|--------|------------------|
| **Mobile** | ≤ 680px | 1 Spalte, Hamburger-Menü, Formularzeilen einspaltig |
| **Tablet** | 681–960px | Hero/Detail einspaltig, Footer 2 Spalten |
| **Desktop** | > 960px | Volles Grid, Hero 2-spaltig, Footer 4-spaltig |

Produktraster: `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))` –
passt sich automatisch an jede Breite an.
