# Dokumentation des KI-Einsatzes

> Projektauftrag 3 (M293) verlangt: KI zielgerichtet zur Codegenerierung,
> Problemlösung und Weiterbildung einsetzen, **mindestens zwei KI-Tools**
> nutzen und sie anhand **selbst definierter Kriterien** vergleichen.

---

## 1. Eingesetzte KI-Tools

| # | Tool | Art | Rolle im Projekt |
|---|------|-----|------------------|
| **A** | **Claude Code** (Anthropic, Modell Opus) | Agentisches CLI-Tool im Terminal | Gerüst, Generator-Skript, Struktur, Refactoring ganzer Dateien |
| **B** | **GitHub Copilot** (in VS Code) | Inline-Autovervollständigung + Chat | Schnelle Zeilen-Vervollständigung, kleine CSS-Tweaks, Erklärungen |

Beide sind KI-gestützte Entwicklungsumgebungen im Sinne des Auftrags
(z. B. „VS-Code mit GitHub-Copilot" ist dort explizit genannt).

---

## 2. Selbst definierte Vergleichskriterien

1. **Codequalität & Konsistenz** – Wie sauber/wartbar ist das Ergebnis?
2. **Geschwindigkeit** – Wie schnell vom Wunsch zum lauffähigen Code?
3. **Kontextverständnis** – Versteht das Tool das ganze Projekt oder nur die offene Datei?
4. **Lerneffekt** – Wie gut erklärt es, *warum* etwas so gemacht wird?
5. **Kontrolle** – Wie gut bleibe ich Herr über den Code (Review, Nachvollziehbarkeit)?
6. **Einstieg** – Wie hoch ist die Einstiegshürde?

Bewertung: ★ (schwach) bis ★★★★★ (stark).

---

## 3. Bewertung

| Kriterium | Claude Code (A) | GitHub Copilot (B) |
|-----------|:---------------:|:------------------:|
| Codequalität & Konsistenz | ★★★★★ | ★★★☆☆ |
| Geschwindigkeit (grosse Tasks) | ★★★★★ | ★★★☆☆ |
| Geschwindigkeit (kleine Tasks) | ★★★☆☆ | ★★★★★ |
| Kontextverständnis (Projekt) | ★★★★★ | ★★★☆☆ |
| Lerneffekt | ★★★★☆ | ★★★☆☆ |
| Kontrolle | ★★★★☆ | ★★★★★ |
| Einstieg | ★★★☆☆ | ★★★★★ |

### Fazit der Bewertung
- **Claude Code** glänzt bei *ganzheitlichen* Aufgaben: Es kennt alle Dateien,
  erzeugt konsistente Header/Footer über 15 Seiten und schreibt das
  Generator-Skript (`tools/generate.py`) in einem Rutsch. Stärke = Architektur & Konsistenz.
- **GitHub Copilot** ist unschlagbar beim *Tippen*: eine halbfertige CSS-Regel oder
  Media-Query wird sofort sinnvoll ergänzt. Stärke = Mikro-Tempo direkt im Editor.

**Arbeitsweise im Projekt:** Grobstruktur und sich wiederholende Teile (Produktkarten,
Detailseiten) mit **Claude Code**; Feinschliff einzelner CSS-Zeilen und schnelle
Experimente mit **Copilot**. Die Kombination war effizienter als jedes Tool allein.

---

## 4. Konkrete Einsätze (Beispiele)

### a) Layout & UI-Optimierung
- **Prompt an Claude Code:** „Baue ein responsives Produktraster mit
  `auto-fill, minmax()` und Hover-Effekt." → lieferte die `.card-grid`/`.product-card`-Regeln.
- **Copilot:** Beim Schreiben von `@media (max-width: 680px)` automatisch die
  Hamburger-Menü-Regeln vorgeschlagen, die ich angepasst habe.

### b) Codevorschläge / Problemlösung
- **Problem:** Kategoriefilter ohne Framework. **Claude Code** schlug die
  `data-category` + `classList.toggle('hidden')`-Lösung mit URL-Hash vor
  (`js/main.js`), sodass `produkte.html#kosmetik` direkt filtert.
- **Problem:** Kontaktformular soll Anfragen „automatisch zuordnen".
  Lösung: Betreff-Dropdown steuert per `mailto:` die Empfängeradresse.

### c) Weiterbildung / Erklärungen
- Per Copilot-Chat „Was macht `aspect-ratio` und `object-fit: cover`?" gefragt
  und die Antwort genutzt, um Produktbilder ohne Verzerrung darzustellen.
- Claude Code erklärte `prefers-reduced-motion` und Fokus-Sichtbarkeit
  (`:focus-visible`) → in das Stylesheet übernommen (Barrierefreiheit).

---

## 5. Reflexion: Chancen & Grenzen

**Was gut lief**
- Enormer Zeitgewinn bei repetitivem Markup (12 Detailseiten aus einer Datenquelle).
- KI als „Tutor": Konzepte wie Grid-`auto-fill`, `clamp()`-Typografie und ARIA
  wurden nebenbei verständlich.

**Grenzen / kritischer Umgang**
- KI macht **Fehler** (z. B. veraltete Eigenschaften, zu generische Texte) –
  ich habe jeden Vorschlag gelesen, getestet und angepasst, nicht blind übernommen.
- **Inhaltliche Verantwortung** bleibt bei mir: Produkttexte, der „Research Use Only"-
  Hinweis und die Datenstruktur wurden bewusst gesetzt, nicht von der KI „erfunden".
- Der Auftrag verlangt **100 % eigenen** HTML/CSS-Code – KI war Werkzeug und
  Sparringspartner, die Entscheidungen (Struktur, Design, Inhalte) traf ich selbst.

**Erkenntnis:** KI ersetzt nicht das Verständnis, sondern beschleunigt es. Wer das
Ergebnis nicht prüfen kann, kann es auch nicht verantworten. Am produktivsten war
der Mix aus agentischem Tool (grosse Würfe) und Inline-Assistent (Feinschliff).
