# Retrospektive: Wie lief meine Projektarbeit?

**Name:** _[Dein Name eintragen]_
**Projekt:** HELIX PEPTIDES (Modul M293)

---

## 1. Was lief gut?

*   **Automatisierung (Statischer Generator):** Die Verwendung des Python-Skripts (`tools/generate.py`) zur automatischen Generierung der 12 Produkt-Detailseiten und SVG-Grafiken aus einer einzigen Datenquelle hat extrem viel Zeit gespart und Redundanz verhindert (DRY-Prinzip).
*   **Modernes Design & CSS-Tokens:** Die Umsetzung des Designs komplett ohne Frameworks (kein Bootstrap/Tailwind) durch den Einsatz von CSS-Variablen (Tokens) lief sehr gut. Das Styling ist extrem sauber, konsistent und nutzt moderne Features wie fluide Typografie (`clamp()`) und CSS Grid.
*   **KI als Lern- und Debugging-Partner:** Der gezielte Einsatz von Claude Code zur Klärung von CSS-Verhalten, Barrierefreiheit (z. B. `prefers-reduced-motion`) und Vanilla-JS-Filterlogiken hat das Verständnis für Webtechnologien stark verbessert.
*   **Responsive Umsetzung:** Das Layout passt sich dank CSS Grid (`auto-fill`) und flexibler Flexbox-Elemente nahtlos an alle Bildschirmgrössen (Mobile, Tablet, Desktop) an.

---

## 2. Was lief weniger gut?

*   **Repository-Struktur zu Beginn:** Das Projekt wurde anfangs in einem Unterordner (`projekt/`) innerhalb eines übergeordneten Repositories aufgesetzt. Das hat das automatische Deployment auf GitHub Pages anfangs verkompliziert.
*   **Reines CSS vs. Frameworks:** Das Schreiben von 100 % eigenem CSS war zu Beginn zeitaufwendiger als erwartet. Besondere Hürden waren die Umsetzung der voll funktionsfähigen mobilen Navigation (Hamburger-Menü) und das Erreichen guter Kontrastverhältnisse für Barrierefreiheit.
*   **Fehlerhafte Codevorschläge der KI:** Gelegentlich haben die KI-Assistenten veraltete CSS-Präfixe vorgeschlagen oder unvollständigen Code generiert (z. B. mit Platzhaltern wie `// Code hier einfügen`), was manuelle Nacharbeit und sorgfältiges Testen erforderte.

---

## 3. Was würde ich anders machen?

*   **Projekt direkt im Root-Ordner starten:** Bei zukünftigen Projekten würde ich das Repository von Anfang an flach aufbauen, um Probleme mit Pfaden und dem Deployment auf GitHub Pages zu vermeiden.
*   **Accessibility (Barrierefreiheit) von Beginn an einplanen:** Kontraste und Tastatursteuerung (`:focus-visible`) direkt beim Erstellen der ersten Elemente testen, statt erst am Ende des Projekts Korrekturen vorzunehmen.
*   **Häufigere, kleinere Commits:** Den Code in noch kleineren Schritten in Git sichern, um eine noch detailliertere Versionshistorie zu haben.
