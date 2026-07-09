# HELIX PEPTIDES – Webshop

Schulprojekt für das Modul **M293 – Webauftritt erstellen und veröffentlichen**,
Projektauftrag 3: *Webshop mit KI-gestützter Webentwicklung*.

Ein fiktiver Webshop für **Research-Peptide und Laborzubehör**.
100 % eigener **HTML- und CSS**-Code, **kein Framework**. JavaScript nur für
optionale Funktionen (Filter, Formular-Komfort, mobile Navigation).

> ⚠️ **Hinweis:** Alle Produkte und Texte sind erfunden und ausschliesslich für
> Forschungs-/Laborzwecke dargestellt (*Research Use Only*). Reiner Schul-Mockup –
> es findet kein echter Verkauf und keine Datenspeicherung statt.

---

## 🔗 Links

- **Live (GitHub Pages):** https://maxitio.github.io/m293/
- **Repository:** https://github.com/maxitio/m293

---

## ✅ Erfüllte Auftrags-Anforderungen

| Anforderung | Umsetzung |
|-------------|-----------|
| Mind. 3 Hauptseiten | Start, Produktübersicht, Kontakt (+ 12 Detailseiten) |
| Mind. 10 Produkte (Text, Bild, **Video**, Preis) | 12 Produkte mit SVG-Bild, Beschreibung, Video & Preis |
| Startseite: neu/beliebt, Kategorien, Newsletter | `index.html` |
| Artikelübersicht mit **Kategoriefilter** | `produkte.html` (JS-Filter + URL-Hash) |
| Detailseite mit Beschreibung, Bild, Video, **Bestellfunktion** | `produkt-*.html` |
| **Kontaktformular mit Betreffauswahl** | `kontakt.html` (mailto-Routing) |
| Header / Main / Footer | alle Seiten |
| **Grid-Layout** | Produktraster, Footer, Kategorien, Hero |
| Formulare (Newsletter + Kontakt) | mit JS-Validierung |
| **Responsive** (Mobile/Tablet/Desktop) | `@media`-Breakpoints 680px / 960px |
| Wireframes (Markdown) | [`docs/wireframes.md`](docs/wireframes.md) |
| Styleguide (Markdown) | [`docs/styleguide.md`](docs/styleguide.md) |
| KI-Doku, 2 Tools verglichen (Markdown) | [`KI-DOKU.md`](KI-DOKU.md) |

---

## 📁 Projektstruktur

```
├── index.html             # Startseite
├── produkte.html          # Produktübersicht mit Kategoriefilter
├── produkt-<slug>.html    # 12 Detailseiten (generiert)
├── kontakt.html           # Kontakt + Team
├── warenkorb.html         # Warenkorb (Web Storage)
├── danke.html             # Bestellbestätigung
├── faq.html               # FAQ inkl. Versand & Lieferung
├── impressum.html · datenschutz.html · agb.html   # Rechtliches
├── css/
│   └── style.css          # gesamtes Design (Design-Tokens, Grid, Responsive, Motion)
├── js/
│   ├── products.js        # Produktdaten für den Warenkorb (generiert)
│   ├── cart.js            # Warenkorb über localStorage + Header-Badge + Toast
│   └── main.js            # Nav, Filter, Formular-Validierung, mailto, Danke-Seite
├── assets/img/            # SVG-Logo, Produktbilder, Team-Avatare
├── tools/
│   └── generate.py        # Build-Hilfe: erzeugt SVGs + HTML + products.js aus 1 Datenquelle
├── PRODUCT.md · DESIGN.md # Design-Kontext (impeccable-Skill: Register, Marke, Visuals)
└── docs/                  # Wireframes, Styleguide, KI-Einsatz
```

**21 HTML-Seiten** insgesamt: 4 Hauptseiten + 12 Produkt-Detailseiten + 5 Zusatzseiten.

### Warum ein Generator-Skript?
Die 12 Detailseiten teilen sich Header, Footer und Aufbau. Statt 12-mal Code zu
kopieren, erzeugt `tools/generate.py` alle Seiten **konsistent aus einer
Produktdatenquelle**. Das ausgelieferte HTML/CSS ist die Abgabe; das Skript ist
nur Entwicklungs-Werkzeug (siehe `docs/ki-einsatz.md`).

---

## ▶️ Lokal starten

Reine statische Seite – einfach `index.html` im Browser öffnen.
Empfohlen (für korrekte Pfade) ein kleiner lokaler Server:

```bash
# im Hauptordner des Repositories
python -m http.server 8000
# dann http://localhost:8000 öffnen
```

### Neu generieren (nach Datenänderung in `tools/generate.py`)

```bash
python tools/generate.py
```

---

## 🚀 Veröffentlichung auf GitHub Pages

Da der Shop direkt im Hauptverzeichnis (Root) des Repos `m293` liegt:

1. GitHub → Repo **m293** → **Settings → Pages**
2. *Source:* **Deploy from a branch**, Branch **main**, Ordner **/ (root)**
3. Speichern. Nach ~1 Min. ist die Seite erreichbar unter
   `https://maxitio.github.io/m293/`
4. Diesen Link oben unter **Live** und in der Abgabe eintragen.

---

## 🧩 Optionale Features (laut Auftrag freiwillig)

- ✔️ **Warenkorb mit zentralem Bestellformular** (Web Storage API / `localStorage`):
  Produkte sammeln, Mengen ändern, Header-Badge, Versandlogik (ab CHF 100 gratis),
  Abschluss → Bestellbestätigung (`danke.html`).
- ✔️ JavaScript-Kategoriefilter mit teilbarem URL-Hash
- ✔️ Formular-Validierung, `mailto:`-Betreff-Routing im Kontaktformular
- ➖ Benutzerkonto / Login / Merkliste – nicht umgesetzt (optional, nicht Pflicht).

## 🎨 Design / KI-Workflow

Das Design wurde mit dem **impeccable**-Frontend-Skill verfeinert (Register „brand",
Slop-Vermeidung). Strategische und visuelle Entscheidungen sind in
[`PRODUCT.md`](PRODUCT.md) und [`DESIGN.md`](DESIGN.md) dokumentiert; der Vergleich
der KI-Tools steht in [`KI-DOKU.md`](KI-DOKU.md).
