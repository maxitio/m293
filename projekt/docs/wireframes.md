# Wireframes – HELIX PEPTIDES

Low-Fidelity-Skizzen (ASCII) für **Mobile**, **Tablet** und **Desktop**.
Sie zeigen die Struktur *vor* dem Visual Design und begründen die Grid-Entscheidungen.
Die umgesetzten Seiten folgen diesen Wireframes.

Legende: `[ ]` Box/Bild · `___` Eingabefeld · `(btn)` Button · `≡` Hamburger

---

## 1. Startseite (`index.html`)

### Mobile (≤ 680px) – 1 Spalte
```
+--------------------------+
| Logo            ≡  (Shop)|  <- Header sticky
+--------------------------+
|        HERO              |
|  H1 Titel               |
|  Lead-Text              |
|  (Produkte)(Newsletter) |
|  12+ | >98% | 24h       |
|        [ Vial-Bild ]    |
+--------------------------+
| ⚠ Research-Use-Hinweis  |
+--------------------------+
| Kategorien (gestapelt)  |
|  [ Forschung   ]        |
|  [ Kosmetik    ]        |
|  [ Zubehör     ]        |
+--------------------------+
| Ausgewählte Produkte    |
|  [ Karte 1 ]            |
|  [ Karte 2 ]            |
|  ...                    |
+--------------------------+
| Warum HELIX (USP x4)    |
+--------------------------+
| Newsletter ___ (btn)    |
+--------------------------+
| Footer (1 Spalte)       |
+--------------------------+
```

### Tablet (681–960px) – 2 Spalten
```
+------------------------------------------+
| Logo        Start Produkte Kontakt (Shop)|
+------------------------------------------+
|   HERO (Text)        |   [ Vial-Bild ]   |
+------------------------------------------+
| ⚠ Research-Use-Hinweis                   |
+------------------------------------------+
| Kategorien:  [ Forsch ] [ Kosm ] [ Zub ] |
+------------------------------------------+
| Produkte:   [ K1 ] [ K2 ] [ K3 ]         |
+------------------------------------------+
| USP:        [ ] [ ]  /  [ ] [ ]          |
+------------------------------------------+
| Newsletter ______________ (btn)          |
+------------------------------------------+
| Footer (2 Spalten)                       |
+------------------------------------------+
```

### Desktop (> 960px) – Hero 2-spaltig, Raster auto-fill
```
+------------------------------------------------------------+
| Logo            Start  Produkte  Kontakt          (Shop)   |
+------------------------------------------------------------+
|  HERO Text + CTA + Stats        |        [ Vial-Bild ]     |
+------------------------------------------------------------+
| ⚠ Research-Use-Hinweis                                     |
+------------------------------------------------------------+
| Kategorien:   [ Forschung ]  [ Kosmetik ]  [ Zubehör ]     |
+------------------------------------------------------------+
| Produkte:   [ K1 ] [ K2 ] [ K3 ] [ K4 ]                    |
+------------------------------------------------------------+
| USP:        [ ] [ ] [ ] [ ]                                |
+------------------------------------------------------------+
| Newsletter ________________________ (btn)                  |
+------------------------------------------------------------+
| Footer:  Brand  |  Shop  |  Service  |  Rechtliches        |
+------------------------------------------------------------+
```

---

## 2. Produktübersicht (`produkte.html`)

### Mobile
```
| Logo  ≡            |
| Breadcrumb         |
| H1 Alle Produkte   |
| ⚠ Hinweis          |
| [Alle][Forsch]..   |  <- Filter (umbrechend)
| [ Karte ]          |
| [ Karte ]          |
| ...                |
| Footer             |
```

### Desktop
```
| Breadcrumb: Start / Produkte                       |
| H1 + Lead                                          |
| ⚠ Hinweis                                          |
| Filter:  (Alle) (Forschung) (Kosmetik) (Zubehör)   |
| [ K1 ] [ K2 ] [ K3 ] [ K4 ]                        |
| [ K5 ] [ K6 ] [ K7 ] [ K8 ]   <- auto-fill Grid    |
| ...                                                |
```
Filter-Logik: Buttons blenden Karten per `data-category` ein/aus (JS).
Ohne JS werden alle Produkte angezeigt (Fallback).

---

## 3. Produktdetail (`produkt-<slug>.html`)

### Mobile (gestapelt)
```
| Breadcrumb            |
| [ Produktbild ]       |
| Specs (1 Spalte)      |
| Kategorie + Titel     |
| Preis  [inkl. CoA]    |
| +-- Bestellbox ----+  |
| | Name ___ Mail ___|  |
| | Labor ___ Menge ▾|  |
| | Anmerkung _______|  |
| | (Bestellen)      |  |
| +------------------+  |
| Beschreibung          |
| [ Video ]             |
| Lagerung & Handling   |
| Ähnliche Produkte     |
```

### Desktop (2-spaltig, Bild sticky)
```
| Breadcrumb: Start / Produkte / Kategorie / Name           |
+-----------------------------+-----------------------------+
| [ Produktbild ] (sticky)    | Kategorie + Badge           |
| Specs: [Reinheit][Menge]    | H1 Produktname              |
|        [MW]     [Form]      | Lead                        |
|                             | Preis (gross) [inkl. CoA]   |
|                             | +-- Bestellbox ----------+  |
|                             | | Name | E-Mail          |  |
|                             | | Labor| Menge ▾         |  |
|                             | | Anmerkung             |  |
|                             | | (Bestellung anfragen) |  |
|                             | +-----------------------+  |
|                             | Beschreibung / Video /     |
|                             | Lagerung & Handling        |
+-----------------------------+-----------------------------+
| Ähnliche Produkte:  [ ] [ ] [ ]                           |
```

---

## 4. Kontakt (`kontakt.html`)

### Desktop (2-spaltig)
```
| Breadcrumb: Start / Kontakt                     |
| H1 + Lead                                       |
+----------------------------+--------------------+
| Kontaktformular            | Direktkontakt      |
|  Name ___  E-Mail ___      |  ✉ info@...        |
|  Betreff [ Dropdown ▾ ]    |  ☎ +41 ...         |
|  Nachricht ____________    |  📍 Adresse        |
|  (Senden)                  |  Versand-Infos     |
+----------------------------+--------------------+
| Team:  [ LB ] [ MI ] [ SK ] [ DR ]              |
+-------------------------------------------------+
```
Betreff-Dropdown steuert per `mailto:` die Empfängeradresse → automatische
Zuordnung im E-Mail-Programm (Auftrags-Anforderung).

### Mobile
Formular und Direktkontakt gestapelt, Team-Karten untereinander.
