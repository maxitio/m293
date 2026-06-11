# -*- coding: utf-8 -*-
"""
HELIX PEPTIDES – statischer Seiten-Generator (M293, Projektauftrag 3)
---------------------------------------------------------------------
Erzeugt aus EINER Produktdatenquelle:
  - SVG-Produktbilder + Logo + Team-Avatare  (assets/img/...)
  - index.html, produkte.html, kontakt.html
  - eine Detailseite je Produkt (produkt-<slug>.html)

Damit bleibt Header/Footer/Markup über alle Seiten konsistent (DRY).
Das ERZEUGTE HTML/CSS ist die Abgabe – dieses Skript ist nur Build-Hilfe.
Ausführen:  python tools/generate.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# 1. DATEN
# ----------------------------------------------------------------------------
CATEGORIES = {
    "forschung": "Forschungspeptide",
    "kosmetik":  "Kosmetik-Peptide",
    "zubehor":   "Laborzubehör",
}
CAT_DESC = {
    "forschung": "Lyophilisierte Peptide für In-vitro- und Laborforschung.",
    "kosmetik":  "Aktive Peptide für kosmetische Formulierungsforschung.",
    "zubehor":   "Wasser, Vials & Kits für die Rekonstitution im Labor.",
}

# color = Hauptfarbe des SVG-Bildes
PRODUCTS = [
    {"slug":"bpc-157","name":"BPC-157","cat":"forschung","price":"44.90","size":"5 mg",
     "purity":"99.1 %","mw":"1419.5 g/mol","badge":"Bestseller","color":"#0fa3a3",
     "short":"Synthetisches 15-Aminosäuren-Peptidfragment, lyophilisiert.",
     "long":["BPC-157 ist ein stabiles, synthetisch hergestelltes Peptid aus 15 Aminosäuren. "
             "Es wird als weisses, gefriergetrocknetes (lyophilisiertes) Pulver in einem versiegelten "
             "Vial geliefert und ist ausschliesslich für die In-vitro-Forschung bestimmt.",
             "Jede Charge wird per HPLC und Massenspektrometrie auf Reinheit und Identität geprüft. "
             "Das Analysezertifikat (CoA) liegt jeder Lieferung bei."]},

    {"slug":"tb-500","name":"TB-500 (Thymosin β4)","cat":"forschung","price":"49.90","size":"5 mg",
     "purity":"98.7 %","mw":"4963.4 g/mol","badge":"","color":"#1597a0",
     "short":"Synthetisches Thymosin-Beta-4-Fragment für die Laborforschung.",
     "long":["TB-500 entspricht der aktiven Region des natürlich vorkommenden Proteins Thymosin Beta-4. "
             "Geliefert als lyophilisiertes Pulver im Borosilikat-Vial.",
             "Reinheit und Sequenz werden chargenweise dokumentiert. Nur für Forschungszwecke – "
             "nicht zum menschlichen oder tierischen Gebrauch."]},

    {"slug":"ipamorelin","name":"Ipamorelin","cat":"forschung","price":"39.90","size":"5 mg",
     "purity":"99.0 %","mw":"711.9 g/mol","badge":"","color":"#138f86",
     "short":"Pentapeptid, häufig in Rezeptorbindungs-Studien eingesetzt.",
     "long":["Ipamorelin ist ein selektives Pentapeptid, das in der Grundlagenforschung zu "
             "Sekretagoga untersucht wird. Lyophilisiert, hochrein.",
             "Lagerung kühl und trocken; nach Rekonstitution gekühlt aufbewahren. CoA inklusive."]},

    {"slug":"epitalon","name":"Epitalon","cat":"forschung","price":"42.50","size":"10 mg",
     "purity":"98.5 %","mw":"390.3 g/mol","badge":"Neu","color":"#2b8ad6",
     "short":"Synthetisches Tetrapeptid (Ala-Glu-Asp-Gly) für Zellforschung.",
     "long":["Epitalon ist ein kurzes Tetrapeptid, das in Telomer- und Zellalterungsstudien "
             "als Forschungsreagenz verwendet wird.",
             "Geliefert als lyophilisiertes Pulver mit beiliegendem Analysezertifikat."]},

    {"slug":"glutathion","name":"Glutathion (reduziert)","cat":"forschung","price":"28.90","size":"600 mg",
     "purity":"99.4 %","mw":"307.3 g/mol","badge":"","color":"#0d9488",
     "short":"Tripeptid-Antioxidans (GSH) in Laborqualität.",
     "long":["Reduziertes L-Glutathion (GSH) ist ein Tripeptid aus Glutamat, Cystein und Glycin "
             "und ein häufig genutztes Reagenz in Redox- und Zellkulturstudien.",
             "Hohe Reinheit, chargengeprüft. Vor Licht und Feuchtigkeit geschützt lagern."]},

    {"slug":"ghk-cu","name":"GHK-Cu (Kupferpeptid)","cat":"kosmetik","price":"34.90","size":"50 mg",
     "purity":"99.2 %","mw":"403.9 g/mol","badge":"Bestseller","color":"#5b54d6",
     "short":"Kupferkomplex des Tripeptids GHK für Formulierungsforschung.",
     "long":["GHK-Cu ist ein blauer Kupfer-Tripeptid-Komplex, der in der kosmetischen "
             "Formulierungsforschung breit untersucht wird. Geliefert als feines Pulver.",
             "Ideal für die Entwicklung von Seren und Emulsionen im Labormassstab. CoA inklusive."]},

    {"slug":"matrixyl","name":"Matrixyl (Pal-KTTKS)","cat":"kosmetik","price":"37.90","size":"10 mg",
     "purity":"98.9 %","mw":"802.0 g/mol","badge":"","color":"#7a5cf0",
     "short":"Palmitoyl-Pentapeptid für die kosmetische Wirkstoffforschung.",
     "long":["Matrixyl (Palmitoyl Pentapeptide-4) ist ein lipidiertes Peptid, das in Studien zu "
             "Kollagen-Modellsystemen verwendet wird.",
             "Lyophilisiert, hochrein, mit beiliegendem Analysezertifikat."]},

    {"slug":"argireline","name":"Argireline (Acetyl-Hexapeptid-8)","cat":"kosmetik","price":"32.90","size":"10 mg",
     "purity":"98.6 %","mw":"888.0 g/mol","badge":"","color":"#6d28d9",
     "short":"Acetyliertes Hexapeptid – Klassiker der Kosmetik-Forschung.",
     "long":["Argireline ist ein synthetisches Hexapeptid, das in der kosmetischen "
             "Forschung als Modellwirkstoff dient.",
             "Geliefert als lyophilisiertes Pulver in versiegeltem Vial."]},

    {"slug":"snap-8","name":"SNAP-8 Peptid","cat":"kosmetik","price":"36.50","size":"10 mg",
     "purity":"98.4 %","mw":"1075.2 g/mol","badge":"Neu","color":"#8b5cf6",
     "short":"Octapeptid, Weiterentwicklung des Argireline-Konzepts.",
     "long":["SNAP-8 ist ein Octapeptid, das in der kosmetischen Formulierungsforschung "
             "als verlängerte Variante klassischer Hexapeptide untersucht wird.",
             "Hochrein und chargengeprüft, inkl. CoA."]},

    {"slug":"bac-wasser","name":"Bakteriostatisches Wasser","cat":"zubehor","price":"9.90","size":"30 ml",
     "purity":"0.9 % Benzylalkohol","mw":"—","badge":"","color":"#0ea5b7",
     "short":"Steriles Wasser mit Benzylalkohol zur Rekonstitution.",
     "long":["Bakteriostatisches Wasser (30 ml) dient zum Auflösen lyophilisierter Peptide im Labor. "
             "Der Zusatz von 0,9 % Benzylalkohol hemmt Keimwachstum bei mehrfacher Entnahme.",
             "Geliefert im verschlossenen Mehrdosen-Vial."]},

    {"slug":"vials","name":"Sterile Glasvials (10 Stk.)","cat":"zubehor","price":"12.90","size":"10 ml",
     "purity":"Typ-1-Borosilikat","mw":"—","badge":"","color":"#0891b2",
     "short":"Leere, sterile Borosilikat-Vials mit Bördelkappe.",
     "long":["Set aus 10 sterilen Borosilikat-Vials (10 ml) mit Gummiseptum und Aluminium-Bördelkappe. "
             "Für die Lagerung rekonstituierter Lösungen im Labor.",
             "Autoklavierbar und chemisch beständig."]},

    {"slug":"misch-kit","name":"Rekonstitutions-Kit","cat":"zubehor","price":"19.90","size":"Set",
     "purity":"—","mw":"—","badge":"Neu","color":"#0284c7",
     "short":"Kit aus Spritzen, Kanülen, Tupfern und Vial-Adapter.",
     "long":["Praktisches Labor-Kit für die saubere Rekonstitution lyophilisierter Peptide: "
             "enthält Einwegspritzen, Filterkanülen, Alkoholtupfer und einen Vial-Adapter.",
             "Steril verpackt, für den einmaligen Gebrauch."]},
]

TEAM = [
    {"name":"Dr. Lena Brunner","role":"Wissenschaftliche Leitung","ini":"LB","color":"#0fa3a3"},
    {"name":"Marco Iten","role":"Qualitätssicherung (HPLC/QC)","ini":"MI","color":"#5b54d6"},
    {"name":"Sophie Keller","role":"Kundenservice & Versand","ini":"SK","color":"#0ea5b7"},
    {"name":"David Roth","role":"Logistik & Lager","ini":"DR","color":"#7a5cf0"},
]

# Stabiles, frei nutzbares Demo-Video (Platzhalter für eigenes Produktvideo)
VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"

# ----------------------------------------------------------------------------
# 2. SVG-GRAFIKEN
# ----------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def darken(hexcol, f=0.7):
    h = hexcol.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return "#%02x%02x%02x" % (int(r*f), int(g*f), int(b*f))

def product_svg(p):
    """Stilisiertes Vial mit Peptidkette in der Produktfarbe."""
    c = p["color"]; cd = darken(c, .72); cl = darken(c, 1.0)
    chain = ""
    cx0, cy = 150, 250
    for i in range(6):
        x = cx0 + i*30
        chain += f'<circle cx="{x}" cy="{cy + (8 if i%2 else -8)}" r="9" fill="#fff" opacity="0.9"/>'
        if i < 5:
            x2 = cx0 + (i+1)*30
            y1 = cy + (8 if i%2 else -8); y2 = cy + (8 if (i+1)%2 else -8)
            chain += f'<line x1="{x}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="3" opacity="0.7"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="{html.escape(p['name'])}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{cd}"/>
    </linearGradient>
    <linearGradient id="liq" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity=".15"/>
    </linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg)"/>
  <circle cx="320" cy="70" r="120" fill="#ffffff" opacity="0.06"/>
  <circle cx="70" cy="250" r="90" fill="#ffffff" opacity="0.06"/>
  {chain}
  <!-- Vial -->
  <g transform="translate(175,70)">
    <rect x="14" y="-14" width="22" height="16" rx="3" fill="#dfe7ee"/>
    <rect x="10" y="0" width="30" height="10" rx="2" fill="#b9c6d4"/>
    <rect x="6" y="10" width="38" height="150" rx="12" fill="#ffffff" opacity="0.9"/>
    <rect x="6" y="70" width="38" height="90" rx="12" fill="url(#liq)"/>
    <rect x="13" y="16" width="6" height="40" rx="3" fill="#ffffff" opacity="0.8"/>
  </g>
  <text x="200" y="285" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-size="15" fill="#ffffff" opacity="0.85" letter-spacing="1">{html.escape(p['size'])}</text>
</svg>'''

def logo_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="HELIX Logo">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0fa3a3"/><stop offset="1" stop-color="#5b54d6"/></linearGradient></defs>
  <rect width="48" height="48" rx="12" fill="url(#g)"/>
  <path d="M15 12c0 9 18 9 18 24M33 12c0 9-18 9-18 24" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <line x1="17" y1="18" x2="31" y2="18" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="17" y1="30" x2="31" y2="30" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
</svg>'''

def avatar_svg(t):
    c = t["color"]; cd = darken(c, .7)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{html.escape(t['name'])}">
  <defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{cd}"/></linearGradient></defs>
  <rect width="100" height="100" rx="50" fill="url(#a)"/>
  <text x="50" y="62" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-size="38" font-weight="700" fill="#fff">{t['ini']}</text>
</svg>'''

# ----------------------------------------------------------------------------
# 3. HTML-BAUSTEINE
# ----------------------------------------------------------------------------
def head(title, desc, active):
    nav = ""
    pages = [("index.html","Start"),("produkte.html","Produkte"),("kontakt.html","Kontakt")]
    for href, label in pages:
        cur = ' aria-current="page"' if href == active else ""
        nav += f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <a class="skip-link" href="#main">Zum Inhalt springen</a>
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="index.html">
        <img src="assets/img/logo.svg" alt="">
        <span>HELIX PEPTIDES<small>Research Grade</small></span>
      </a>
      <nav aria-label="Hauptnavigation">
        <ul class="nav__links" id="nav-links">{nav}</ul>
      </nav>
      <div class="nav__actions">
        <a class="btn btn--primary" href="produkte.html">Shop</a>
        <button class="nav-toggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="nav-links"><span></span></button>
      </div>
    </div>
  </header>
  <main id="main">
'''

def footer():
    shop_links = "".join(
        f'<li><a href="produkte.html#{k}">{html.escape(v)}</a></li>' for k,v in CATEGORIES.items())
    return f'''  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="assets/img/logo.svg" alt="HELIX PEPTIDES">
          <p>Peptide und Laborbedarf in dokumentierter Forschungsqualität. Jede Charge mit Analysezertifikat (CoA).</p>
          <p><strong style="color:#fff">Nur für Forschungs- und Laborzwecke.</strong><br>Nicht für den menschlichen oder tierischen Gebrauch.</p>
        </div>
        <div>
          <h4>Shop</h4>
          <ul>{shop_links}<li><a href="produkte.html">Alle Produkte</a></li></ul>
        </div>
        <div>
          <h4>Service</h4>
          <ul>
            <li><a href="kontakt.html">Kontakt</a></li>
            <li><a href="kontakt.html#versand">Versand &amp; Lieferung</a></li>
            <li><a href="kontakt.html">CoA anfordern</a></li>
          </ul>
        </div>
        <div>
          <h4>Rechtliches</h4>
          <ul>
            <li><a href="#">Impressum</a></li>
            <li><a href="#">Datenschutz</a></li>
            <li><a href="#">AGB</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>2026</span> HELIX PEPTIDES &mdash; Fiktiver Webshop für das Modul M293 (Schulprojekt).</span>
        <span>Bottighofen, Schweiz</span>
      </div>
    </div>
  </footer>
  <script src="js/main.js"></script>
</body>
</html>'''

def disclaimer():
    return '''<div class="disclaimer" role="note">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>
  <div><strong>Wichtiger Hinweis:</strong> Alle Produkte sind ausschliesslich für Forschungs- und Laborzwecke bestimmt (Research Use Only). Sie sind <strong>nicht</strong> für den menschlichen oder tierischen Gebrauch, zur Diagnose oder zur Therapie zugelassen.</div>
</div>'''

def product_card(p):
    badge = f'<span class="pill pill--violet product-card__tag">{p["badge"]}</span>' if p["badge"] else ""
    return f'''      <article class="product-card" data-category="{p['cat']}">
        <a class="product-card__media" href="produkt-{p['slug']}.html" aria-label="{html.escape(p['name'])} ansehen">
          <img src="assets/img/products/{p['slug']}.svg" alt="{html.escape(p['name'])} – {html.escape(p['size'])} Vial" loading="lazy">
          {badge}
        </a>
        <div class="product-card__body">
          <span class="product-card__cat">{CATEGORIES[p['cat']]}</span>
          <h3 class="product-card__title"><a href="produkt-{p['slug']}.html">{html.escape(p['name'])}</a></h3>
          <p class="product-card__desc">{html.escape(p['short'])}</p>
          <div class="product-card__foot">
            <span class="price">CHF&nbsp;{p['price']}</span>
            <a class="btn btn--ghost" href="produkt-{p['slug']}.html">Details</a>
          </div>
        </div>
      </article>'''

# ----------------------------------------------------------------------------
# 4. SEITEN
# ----------------------------------------------------------------------------
def build_index():
    featured = [p for p in PRODUCTS if p["badge"] in ("Bestseller","Neu")][:4]
    if len(featured) < 4:
        featured = PRODUCTS[:4]
    cards = "\n".join(product_card(p) for p in featured)

    cat_tiles = ""
    for k,v in CATEGORIES.items():
        count = sum(1 for p in PRODUCTS if p["cat"] == k)
        cat_tiles += f'''        <a class="cat-tile" href="produkte.html#{k}">
          <svg class="cat-tile__icon" viewBox="0 0 24 24" fill="none" stroke="#0fa3a3" stroke-width="1.8"><path d="M9 3h6v4l4 11a2 2 0 0 1-1.9 2.6H6.9A2 2 0 0 1 5 18L9 7V3Z"/><path d="M8 14h8"/></svg>
          <strong>{html.escape(v)}</strong>
          <span>{html.escape(CAT_DESC[k])}</span>
          <span class="cat-tile__count">{count} Produkte &rarr;</span>
        </a>'''

    usps = [
        ("Geprüfte Reinheit", "HPLC &amp; MS pro Charge", "Jede Charge wird analytisch geprüft – Analysezertifikat (CoA) inklusive."),
        ("Kühlversand", "24–48 h in der Schweiz", "Temperaturkontrollierter Versand mit Trockeneis bei sensiblen Produkten."),
        ("Laborqualität", "&gt; 98 % Reinheit", "Lyophilisierte Peptide in versiegelten Borosilikat-Vials."),
        ("Support", "Wissenschaftliches Team", "Fragen zu Sequenz, Lagerung oder Handling? Wir antworten fachkundig."),
    ]
    usp_html = ""
    for t, s, d in usps:
        usp_html += f'''        <div class="usp">
          <svg class="usp__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m9 12 2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg>
          <h3>{t}</h3><p><strong>{s}</strong><br>{d}</p>
        </div>'''

    body = f'''    <section class="hero">
      <div class="container hero__grid">
        <div>
          <span class="eyebrow" style="color:#7ee3e3">Research Peptides &middot; Made in Switzerland</span>
          <h1>Peptide in dokumentierter Laborqualität.</h1>
          <p>Lyophilisierte Forschungs- und Kosmetik-Peptide mit über 98&nbsp;% Reinheit – jede Charge mit Analysezertifikat.</p>
          <div class="hero__cta">
            <a class="btn btn--primary btn--lg" href="produkte.html">Produkte entdecken</a>
            <a class="btn btn--light btn--lg" href="#newsletter">Newsletter abonnieren</a>
          </div>
          <div class="hero__stats">
            <div><strong>12+</strong><span>Produkte</span></div>
            <div><strong>&gt;98%</strong><span>Reinheit</span></div>
            <div><strong>24h</strong><span>Versand</span></div>
          </div>
        </div>
        <div class="hero__art">
          <img src="assets/img/products/ghk-cu.svg" alt="Peptid-Vial" width="420">
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        {disclaimer()}
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Sortiment</p>
          <h2>Kategorien</h2>
          <p class="lead">Vom Forschungspeptid bis zum Rekonstitutions-Kit – alles aus einer Hand.</p>
        </div>
        <div class="cat-grid">
{cat_tiles}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Beliebt &amp; neu</p>
          <h2>Ausgewählte Produkte</h2>
          <p class="lead">Unsere meistbestellten und neusten Artikel auf einen Blick.</p>
        </div>
        <div class="card-grid">
{cards}
        </div>
        <p class="mt-3"><a class="btn btn--ghost" href="produkte.html">Alle Produkte ansehen &rarr;</a></p>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section__head section__head--center">
          <p class="eyebrow">Warum HELIX</p>
          <h2>Worauf Sie sich verlassen können</h2>
        </div>
        <div class="usp-grid">
{usp_html}
        </div>
      </div>
    </section>

    <section class="section" id="newsletter">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Newsletter</p>
          <h2>Aktionen &amp; neue Peptide zuerst erfahren</h2>
          <p class="lead">Ein- bis zweimal pro Monat: neue Chargen, Forschungs-News und Rabatte. Jederzeit abbestellbar.</p>
        </div>
        <form class="newsletter" data-newsletter novalidate>
          <input type="email" name="email" placeholder="dein.name@labor.ch" aria-label="E-Mail-Adresse" required>
          <button class="btn btn--primary" type="submit">Abonnieren</button>
        </form>
        <p class="form-feedback" role="status" aria-live="polite"></p>
        <p class="form-note">Mit dem Abonnieren stimmst du dem Erhalt von E-Mails zu. (Demo – es werden keine Daten gespeichert.)</p>
      </div>
    </section>
'''
    write("index.html", head("HELIX PEPTIDES – Peptide in Laborqualität",
          "Webshop für Forschungs- und Kosmetik-Peptide in dokumentierter Laborqualität. Nur für Forschungszwecke.",
          "index.html") + body + footer())

def build_products():
    cards = "\n".join(product_card(p) for p in PRODUCTS)
    filters = '<button class="filter-btn is-active" data-cat="all" aria-pressed="true">Alle</button>'
    for k,v in CATEGORIES.items():
        filters += f'<button class="filter-btn" data-cat="{k}" aria-pressed="false">{html.escape(v)}</button>'

    body = f'''    <div class="container breadcrumb"><a href="index.html">Start</a> / Produkte</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Sortiment</p>
          <h1>Alle Produkte</h1>
          <p class="lead">{len(PRODUCTS)} Artikel – filtere nach Kategorie. Jeder Artikel mit Bild, Beschreibung, Video und Bestellformular auf der Detailseite.</p>
        </div>
        {disclaimer()}
        <div class="filter-bar mt-3" data-filter-bar role="group" aria-label="Nach Kategorie filtern">
          {filters}
        </div>
        <div class="card-grid">
{cards}
        </div>
        <p class="filter-empty hidden" data-filter-empty>Keine Produkte in dieser Kategorie.</p>
      </div>
    </section>
'''
    write("produkte.html", head("Produkte – HELIX PEPTIDES",
          "Alle Forschungs- und Kosmetik-Peptide sowie Laborzubehör im Überblick, filterbar nach Kategorie.",
          "produkte.html") + body + footer())

def build_detail(p):
    related = [x for x in PRODUCTS if x["cat"] == p["cat"] and x["slug"] != p["slug"]][:3]
    if len(related) < 3:
        related += [x for x in PRODUCTS if x["slug"] != p["slug"] and x not in related][:3-len(related)]
    rel_cards = "\n".join(product_card(x) for x in related)
    long_html = "".join(f"<p>{html.escape(par)}</p>" for par in p["long"])
    badge = f'<span class="pill pill--violet">{p["badge"]}</span>' if p["badge"] else ""

    body = f'''    <div class="container breadcrumb">
      <a href="index.html">Start</a> / <a href="produkte.html">Produkte</a> /
      <a href="produkte.html#{p['cat']}">{CATEGORIES[p['cat']]}</a> / {html.escape(p['name'])}
    </div>
    <section class="container product">
      <div class="product__media">
        <div class="product__image">
          <img src="assets/img/products/{p['slug']}.svg" alt="{html.escape(p['name'])} – {html.escape(p['size'])} Vial" width="600">
        </div>
        <ul class="product__specs">
          <li><strong>Reinheit</strong>{p['purity']}</li>
          <li><strong>Menge</strong>{html.escape(p['size'])}</li>
          <li><strong>Molekulargewicht</strong>{p['mw']}</li>
          <li><strong>Form</strong>Lyophilisiert</li>
        </ul>
      </div>

      <div class="product__info">
        <span class="product-card__cat">{CATEGORIES[p['cat']]}</span> {badge}
        <h1>{html.escape(p['name'])}</h1>
        <p class="lead">{html.escape(p['short'])}</p>
        <div class="product__price">
          <span class="price">CHF&nbsp;{p['price']}</span>
          <span class="pill pill--accent">inkl. CoA</span>
        </div>

        <div class="order-box">
          <h3>Online bestellen</h3>
          <p class="form-note">Bestellung per Formular – nach dem Absenden öffnet sich dein E-Mail-Programm mit der vorausgefüllten Anfrage.</p>
          <form class="form" data-order-form data-product="{html.escape(p['name'])} ({html.escape(p['size'])})" novalidate>
            <div class="form__row">
              <div class="field">
                <label>Name <span class="req">*</span></label>
                <input type="text" name="name" autocomplete="name" required>
              </div>
              <div class="field">
                <label>E-Mail <span class="req">*</span></label>
                <input type="email" name="email" autocomplete="email" required>
              </div>
            </div>
            <div class="form__row">
              <div class="field">
                <label>Firma / Labor</label>
                <input type="text" name="labor" autocomplete="organization">
              </div>
              <div class="field">
                <label>Menge <span class="req">*</span></label>
                <select name="menge" required>
                  <option value="1">1 Vial</option>
                  <option value="2">2 Vials</option>
                  <option value="3">3 Vials</option>
                  <option value="5">5 Vials</option>
                  <option value="10">10 Vials</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label>Anmerkung</label>
              <textarea name="notiz" rows="3" placeholder="z. B. gewünschtes Lieferdatum oder Chargen-Anforderung"></textarea>
            </div>
            <button class="btn btn--primary btn--block btn--lg" type="submit">Bestellung anfragen &middot; CHF&nbsp;{p['price']}</button>
            <p class="form-feedback" role="status" aria-live="polite"></p>
          </form>
        </div>

        <div class="product__longdesc">
          <h2>Produktbeschreibung</h2>
          {long_html}
          <h2>Produktvideo</h2>
          <p>Kurzer Einblick in Handling und Lagerung im Labor. <em>(Platzhalter-Demovideo.)</em></p>
          <div class="video-wrap">
            <video controls preload="none" poster="assets/img/products/{p['slug']}.svg">
              <source src="{VIDEO_URL}" type="video/mp4">
              Dein Browser unterstützt das Video-Element nicht.
            </video>
          </div>
          <h2>Lagerung &amp; Handling</h2>
          <ul>
            <li>Lyophilisiert bei &minus;20&nbsp;°C lagern, vor Licht und Feuchtigkeit geschützt.</li>
            <li>Nach Rekonstitution gekühlt (2–8&nbsp;°C) aufbewahren und zeitnah verwenden.</li>
            <li>Ausschliesslich durch geschultes Laborpersonal handhaben.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--tint related">
      <div class="container">
        <div class="section__head"><p class="eyebrow">Passend dazu</p><h2>Ähnliche Produkte</h2></div>
        <div class="card-grid">
{rel_cards}
        </div>
      </div>
    </section>
'''
    write(f"produkt-{p['slug']}.html",
          head(f"{p['name']} – HELIX PEPTIDES",
               p["short"] + " Nur für Forschungszwecke.",
               "produkte.html") + body + footer())

def build_contact():
    options = ["Bestellung & Versand","Produktfrage","Reklamation","Grosshandel / B2B","Sonstiges"]
    opt_html = "".join(f'<option>{html.escape(o)}</option>' for o in options)
    team_html = ""
    for t in TEAM:
        team_html += f'''        <div class="team-card">
          <img src="assets/img/team/{t['ini'].lower()}.svg" alt="{html.escape(t['name'])}">
          <strong>{html.escape(t['name'])}</strong>
          <span>{html.escape(t['role'])}</span>
        </div>'''

    body = f'''    <div class="container breadcrumb"><a href="index.html">Start</a> / Kontakt</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head">
          <p class="eyebrow">Kontakt</p>
          <h1>Wir sind für dich da</h1>
          <p class="lead">Fragen zu Produkten, Bestellungen oder Analysezertifikaten? Wähle ein Betreff – deine Anfrage wird automatisch dem richtigen Team zugeordnet.</p>
        </div>

        <div class="contact-grid">
          <form class="form" data-contact-form novalidate>
            <div class="form__row">
              <div class="field">
                <label>Name <span class="req">*</span></label>
                <input type="text" name="name" autocomplete="name" required>
              </div>
              <div class="field">
                <label>E-Mail <span class="req">*</span></label>
                <input type="email" name="email" autocomplete="email" required>
              </div>
            </div>
            <div class="field">
              <label>Betreff <span class="req">*</span></label>
              <select name="betreff" required>
                <option value="">Bitte wählen …</option>
                {opt_html}
              </select>
              <span class="field__hint">Das gewählte Betreff bestimmt, welches Team deine E-Mail erhält.</span>
            </div>
            <div class="field">
              <label>Nachricht <span class="req">*</span></label>
              <textarea name="nachricht" required placeholder="Wie können wir helfen?"></textarea>
            </div>
            <button class="btn btn--primary btn--lg" type="submit">Nachricht senden</button>
            <p class="form-feedback" role="status" aria-live="polite"></p>
          </form>

          <aside>
            <div class="order-box" id="versand">
              <h3>Direktkontakt</h3>
              <ul class="info-list">
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg><span>info@helix-peptides.example</span></li>
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2Z"/></svg><span>+41 71 000 00 00</span></li>
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span>Seestrasse 1, 8598 Bottighofen, CH</span></li>
              </ul>
              <p class="form-note"><strong>Versand:</strong> Mo–Fr, 24–48&nbsp;h innerhalb der Schweiz. Kühlversand mit Trockeneis bei sensiblen Produkten.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section__head"><p class="eyebrow">Team</p><h2>Die Menschen hinter HELIX</h2><p class="lead">Ein kleines, spezialisiertes Team aus Wissenschaft, Qualitätssicherung und Logistik.</p></div>
        <div class="team-grid">
{team_html}
        </div>
      </div>
    </section>
'''
    write("kontakt.html", head("Kontakt – HELIX PEPTIDES",
          "Kontaktiere das HELIX-Team. Betreffauswahl mit automatischer Zuordnung zum richtigen Ansprechpartner.",
          "kontakt.html") + body + footer())

# ----------------------------------------------------------------------------
# 5. BUILD
# ----------------------------------------------------------------------------
def main():
    write("assets/img/logo.svg", logo_svg())
    for p in PRODUCTS:
        write(f"assets/img/products/{p['slug']}.svg", product_svg(p))
    for t in TEAM:
        write(f"assets/img/team/{t['ini'].lower()}.svg", avatar_svg(t))
    build_index()
    build_products()
    build_contact()
    for p in PRODUCTS:
        build_detail(p)
    print(f"OK: {len(PRODUCTS)} Produkte, "
          f"{3 + len(PRODUCTS)} HTML-Seiten, "
          f"{1 + len(PRODUCTS) + len(TEAM)} SVG-Grafiken erzeugt.")

if __name__ == "__main__":
    main()
