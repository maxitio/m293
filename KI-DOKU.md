# KI-Dokumentation: Evaluation und Reflexion

Dieses Dokument dokumentiert den Einsatz von künstlicher Intelligenz (KI) während der Entwicklung des Webshops **HELIX PEPTIDES** für das Modul **M293 – Webauftritt erstellen und veröffentlichen** (Projektauftrag 3).

---

## 1. Einleitung & Ziele

Im Rahmen dieses Projekts wurde KI zielgerichtet eingesetzt, um:
1. Geeignete KI-Werkzeuge für die moderne Web-Entwicklung zu evaluieren.
2. Die KI direkt in der lokalen Entwicklungsumgebung (IDE & Terminal) zu nutzen.
3. Die gemachten Erfahrungen kritisch zu reflektieren und den Lerneffekt bei CSS- und JS-Konzepten zu maximieren.

Der Webshop wurde ohne vorgefertigte Frameworks (wie Bootstrap oder Tailwind) vollständig mit eigenem, semantischem HTML5, modernem CSS3 und Vanilla JavaScript umgesetzt. Die KI diente dabei als Assistent, Code-Reviewer und Lern-Tutor.

---

## 2. Nutzwertanalyse der KI-Tools

Um das am besten geeignete Werkzeug für das Projekt zu bestimmen, wurden zwei unterschiedliche KI-Tools evaluiert:
*   **Tool A: Claude Code** (Anthropic) – Ein agentisches CLI-Tool, das direkt im Terminal läuft und projektweiten Kontext versteht.
*   **Tool B: GitHub Copilot** (Microsoft/GitHub) – Ein klassischer Editor-Assistent für VS Code zur Inline-Autovervollständigung und für Chat-Fragen.

### Kriterienkatalog & Gewichtung
Die Kriterien wurden basierend auf den Anforderungen der Modulabgabe und der Entwicklungs-Effizienz gewichtet (Summe = 100 %):
1.  **Kontextverständnis (25 %)**: Fähigkeit, das gesamte Projektverzeichnis zu durchsuchen, Abhängigkeiten zu verstehen und konsistente Anpassungen über mehrere Dateien hinweg vorzunehmen.
2.  **Codequalität & Standardtreue (20 %)**: Erzeugung von sauberem, semantischem HTML5 und modernem CSS3 gemäss gängigen Web-Richtlinien (z. B. Vermeidung von Code-Verschlammung/Slop, Barrierefreiheit).
3.  **Makro-Geschwindigkeit (15 %)**: Zeitersparnis bei der Erstellung komplexer, neuer Dateien oder Skripte (z. B. Automatisierungen).
4.  **Workflow-Integration / Mikro-Speed (15 %)**: Nahtlose Integration direkt beim Tippen im Editor (Inline-Vervollständigungen, Hotkeys).
5.  **Lerneffekt & Erklärungsqualität (15 %)**: Qualität der Erklärungen von Webtechnologien (z. B. CSS Grid, responsive Typografie).
6.  **Kontrolle & Reviewsicherheit (10 %)**: Übersichtlichkeit der vorgeschlagenen Änderungen (z. B. Diffs) vor dem Speichern.

### Nutzwert-Matrix (Skala 1 bis 10 Punkte)

| Kriterium | Gewichtung | Tool A: Claude Code (Punkte) | Tool A: Claude Code (Nutzwert) | Tool B: GitHub Copilot (Punkte) | Tool B: GitHub Copilot (Nutzwert) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 1. Kontextverständnis | 25 % | 10 | 2.50 | 6 | 1.50 |
| 2. Codequalität | 20 % | 9 | 1.80 | 7 | 1.40 |
| 3. Makro-Geschwindigkeit | 15 % | 10 | 1.50 | 6 | 0.90 |
| 4. Workflow-Integration | 15 % | 6 | 0.90 | 10 | 1.50 |
| 5. Lerneffekt | 15 % | 9 | 1.35 | 6 | 0.90 |
| 6. Kontrolle (Review-Diffs) | 10 % | 9 | 0.90 | 8 | 0.80 |
| **Summe** | **100 %** | | **8.95** | | **7.00** |

**Ergebnis:** **Claude Code** erreicht einen Gesamtnutzwert von **8.95**, während **GitHub Copilot** bei **7.00** liegt.

---

## 3. Begründung der Werkzeugwahl

Die Nutzwertanalyse zeigt eine klare Überlegenheit von **Claude Code (Tool A)** bei komplexen, projektweiten Aufgaben. 

**Begründung für die primäre Wahl von Claude Code:**
*   **Projektweiter Kontext:** Da der Webshop aus mehreren miteinander verknüpften HTML-Seiten, einem CSS-System und mehreren JS-Dateien besteht, war das tiefe Kontextverständnis von Claude Code entscheidend. Es konnte analysieren, wie Header und Footer auf allen 21 HTML-Seiten strukturiert sind, und diese konsistent anpassen.
*   **Agentische Fähigkeiten:** Claude Code konnte eigenständig Suchvorgänge im Projekt durchführen, Fehler in Pfaden korrigieren und das Python-Generator-Skript (`tools/generate.py`) in einem Schritt erstellen und testen.
*   **Lerneffekt:** Die Antworten von Claude Code gingen tiefer auf moderne Best Practices (wie Barrierefreiheit, CSS custom properties und fluid typography) ein.

**Ergänzende Nutzung von GitHub Copilot:**
Obwohl Claude Code das primäre Werkzeug war, wurde **GitHub Copilot** als Ergänzung im Editor genutzt. Für das schnelle Schreiben von Standardzeilen, das automatische Schliessen von Klammern und Mikro-Tweaks im CSS ist die direkte Inline-Vervollständigung im Editor unschlagbar, da hierfür kein Wechsel ins Terminal nötig ist.

---

## 4. Einsatz der KI im Projekt

Die KI wurde in verschiedenen Phasen des Projekts strukturiert eingesetzt:

1.  **Konzeption & Generierung des Build-Tools (`tools/generate.py`)**:
    *   Um doppelten HTML-Code (DRY-Prinzip) für die 12 Produkt-Detailseiten zu vermeiden, wurde die KI beauftragt, ein Python-Skript zu entwerfen. Das Skript liest die Produktdaten (Namen, Preise, Beschreibungen, Reinheiten) aus einer zentralen Liste und generiert konsistente HTML-Seiten sowie die passenden Vektor-Grafiken (SVGs) und die JSON-Datenquelle für den Warenkorb (`js/products.js`).
2.  **Design-System & CSS-Tokens (`css/style.css`)**:
    *   Die KI half bei der Definition der CSS-Variablen für Farben, Abstände, Radien und Schriftarten gemäss den Richtlinien in `DESIGN.md`.
    *   Optimierung der Responsiveness über fluide Abstände und Schriftgrössen mittels `clamp()`.
3.  **JavaScript-Interaktionen (`js/main.js` & `js/cart.js`)**:
    *   **Kategoriefilter:** Entwicklung eines Vanilla-JS-Filters für die Produktübersicht, der den Zustand über den URL-Hash (`produkte.html#forschung`) teilt.
    *   **Warenkorb-Logik:** Entwicklung einer seitenübergreifenden Warenkorb-Speicherung über die `localStorage`-API mit dynamischer Berechnung von Preisen, Mengen-Steppern und Gratisversand ab CHF 100.
    *   **Kontakt-Routing:** Implementierung einer Betreff-Dropdown-Auswahl im Kontaktformular, die dynamisch die passende E-Mail-Adresse für das `mailto:`-Routing wählt (z. B. „Produktfrage“ an `lab@helix-peptides.example`).
4.  **Barrierefreiheit (Accessibility)**:
    *   Die KI gab Ratschläge für semantisches HTML (z. B. `<main id="main">`, `skip-link` für Tastaturnavigation) und die Einhaltung des WCAG-2.1-AA-Kontrastverhältnisses.
    *   Einrichtung eines reduzierten Bewegungsmodus über Media Queries (`@media (prefers-reduced-motion: reduce)`) für alle CSS-Animationen und das Deaktivieren des interaktiven Hero-Canvas.

---

## 5. Reflexion: Chancen & Grenzen

### Stärken & Chancen
*   **Zeitersparnis:** Repetitives Markup (wie das Erstellen von 12 fast identischen Detailseiten) wurde durch das von der KI generierte Python-Generator-Skript komplett automatisiert.
*   **Interaktiver Tutor:** Konzepte wie der `IntersectionObserver` für Scroll-Reveals, das Mischen von RGB-Werten für weiche Schatten und CSS Grid `auto-fill` wurden durch die KI-Erklärungen verständlich vermittelt.
*   **Fehlerdiagnose:** Syntaxfehler (wie falsch gesetzte Z-Indizes oder unvollständige Pfade) wurden durch das Übergeben von Fehlermeldungen an die KI in Sekunden behoben.

### Schwächen & Grenzen
*   **Veralteter oder unvollständiger Code:** Copilot schlug gelegentlich veraltete CSS-Eigenschaften (z. B. unnötige Vendor-Prefixes wie `-webkit-box-shadow`) vor oder erfand nicht existierende HTML-Attribute.
*   **Verlust des roten Fadens:** Bei zu langen Prompts neigt die KI dazu, unvollständige Codeblöcke auszugeben („// hier restlicher Code...“), was zu Syntaxfehlern führen kann, wenn man blind kopiert.
*   **Kritischer Umgang:** Jeder Codevorschlag der KI wurde manuell geprüft, an das visuelle Konzept des Styleguides angepasst und lokal getestet. Die inhaltliche Verantwortung (z. B. der gesetzliche Hinweis „Research Use Only“ oder die korrekten Schweizer Währungsschreibweisen „CHF 44.90“) lag vollständig beim Entwickler.

---

## 6. Konkrete Anwendungsbeispiele

Hier sind drei konkrete Beispiele dokumentiert, wie die KI im Projekt zur Code-Erstellung genutzt wurde:

### Beispiel 1: Responsives Produktraster mit CSS Grid
*   **Ziel:** Ein modernes, flexibles Raster für Produktkarten, das sich ohne feste Media Queries automatisch an alle Bildschirmgrössen anpasst.
*   **Prompt an die KI:**
    > „Schreibe eine CSS-Klasse `.card-grid` mit CSS Grid. Die Karten sollen mindestens 250px breit sein und den verbleibenden Platz gleichmässig füllen (`auto-fill`). Nutze ein flexibles Gap aus dem Design-Token `--sp-3`.“
*   **Erzeugter CSS-Code (Auszug aus `css/style.css`):**
    ```css
    .card-grid {
        display: grid;
        gap: var(--sp-3);
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
    ```
*   **Lerneffekt:** Die KI erklärte den Unterschied zwischen `auto-fill` (erstellt leere Grid-Spalten, wenn Platz vorhanden ist) und `auto-fit` (streckt vorhandene Karten, um den Platz auszufüllen). Für einen Webshop ist `auto-fill` besser geeignet, um einheitliche Kartengrössen zu wahren.

---

### Beispiel 2: Statischer Generator in Python
*   **Ziel:** Automatisches Erzeugen der HTML-Dateien aus einer zentralen Produktdatenliste, um Konsistenz zu wahren.
*   **Prompt an Claude Code:**
    > „Schreibe ein Python-Skript `tools/generate.py`, das eine Liste von Produkt-Objekten (mit slug, name, price, size, color) einliest. Generiere für jedes Produkt eine HTML-Datei mit dem Namen `produkt-<slug>.html`. Verwende ein einheitliches HTML-Template mit Header und Footer, binde ein Poster-Bild (SVG) und ein `<video>`-Element ein. Schreibe auch die Produktdaten in ein JavaScript-File `js/products.js`.“
*   **Erzeugter Code (Auszug aus `tools/generate.py`):**
    ```python
    def build_products_js():
        data = {p["slug"]: {
            "name": p["name"], "price": float(p["price"]), "size": p["size"],
            "cat": p["cat"], "img": f"assets/img/products/{p['slug']}.svg"
        } for p in PRODUCTS}
        js = "/* Auto-generiert aus tools/generate.py – Produktdaten für den Warenkorb. */\n"
        js += "window.HELIX_PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
        write("js/products.js", js)
    ```
*   **Ergebnis:** Das Skript erzeugt zuverlässig alle statischen Seiten und die SVG-Produktbilder. Dies spart Stunden an manuellem Copy-Paste-Aufwand.

---

### Beispiel 3: JavaScript-Kategoriefilter mit URL-Hash
*   **Ziel:** Die Produkte auf `produkte.html` dynamisch filtern und den Filterzustand in der URL speichern, damit Links (z. B. aus dem Footer) direkt auf die gefilterte Kategorie verweisen.
*   **Prompt an die KI:**
    > „Schreibe eine Vanilla-JS-Funktion für einen Kategoriefilter. Lies beim Laden der Seite den Hash aus `location.hash` aus. Wenn ein Filter-Button geklickt wird, blende die Artikel mit passendem `data-category` ein und die anderen aus (`hidden`-Klasse). Aktualisiere den URL-Hash, ohne die Seite neu zu laden.“
*   **Erzeugter JS-Code (Auszug aus `js/main.js`):**
    ```javascript
    var filterBar = document.querySelector("[data-filter-bar]");
    if (filterBar) {
        var cards = Array.prototype.slice.call(document.querySelectorAll("[data-category]"));
        var emptyMsg = document.querySelector("[data-filter-empty]");
        function applyFilter(cat) {
            var visible = 0;
            cards.forEach(function (card) {
                var match = cat === "all" || card.getAttribute("data-category") === cat;
                card.classList.toggle("hidden", !match);
                if (match) visible++;
            });
            if (emptyMsg) emptyMsg.classList.toggle("hidden", visible !== 0);
            filterBar.querySelectorAll(".filter-btn").forEach(function (b) {
                var on = b.getAttribute("data-cat") === cat;
                b.classList.toggle("is-active", on);
                b.setAttribute("aria-pressed", on ? "true" : "false");
            });
        }
        filterBar.addEventListener("click", function (e) {
            var btn = e.target.closest(".filter-btn");
            if (!btn) return;
            var cat = btn.getAttribute("data-cat");
            applyFilter(cat);
            history.replaceState(null, "", cat === "all" ? "#" : "#" + cat);
        });
        var initial = (location.hash || "").replace("#", "");
        var known = Array.prototype.map.call(filterBar.querySelectorAll(".filter-btn"),
            function (b) { return b.getAttribute("data-cat"); });
        applyFilter(known.indexOf(initial) > -1 ? initial : "all");
    }
    ```
*   **Ergebnis:** Wenn man auf `produkte.html#kosmetik` navigiert, filtert die Seite die Produkte direkt beim Laden. Das teilt sich nahtlos über den Browserverlauf mittels `history.replaceState`.
