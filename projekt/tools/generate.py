# -*- coding: utf-8 -*-
"""
HELIX PEPTIDES – statischer Seiten-Generator (M293, Projektauftrag 3)
---------------------------------------------------------------------
Erzeugt aus EINER Produktdatenquelle:
  - SVG-Bilder (Logo, Produkte, Team)            -> assets/img/...
  - js/products.js  (Produktdaten für den Warenkorb)
  - Hauptseiten: index, produkte, kontakt
  - Detailseiten: produkt-<slug>.html  (1 je Produkt)
  - Zusatzseiten: faq, warenkorb, danke, impressum, datenschutz, agb

Header/Footer/Markup bleiben über alle Seiten konsistent (DRY).
Das ERZEUGTE HTML/CSS/JS ist die Abgabe – dieses Skript ist nur Build-Hilfe.
Ausführen:  python tools/generate.py
"""
import os, html, json

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
     "purity":"0.9 % BnOH","mw":"—","badge":"","color":"#0ea5b7",
     "short":"Steriles Wasser mit Benzylalkohol zur Rekonstitution.",
     "long":["Bakteriostatisches Wasser (30 ml) dient zum Auflösen lyophilisierter Peptide im Labor. "
             "Der Zusatz von 0,9 % Benzylalkohol hemmt Keimwachstum bei mehrfacher Entnahme.",
             "Geliefert im verschlossenen Mehrdosen-Vial."]},

    {"slug":"vials","name":"Sterile Glasvials (10 Stk.)","cat":"zubehor","price":"12.90","size":"10 ml",
     "purity":"Typ-1-Glas","mw":"—","badge":"","color":"#0891b2",
     "short":"Leere, sterile Borosilikat-Vials mit Bördelkappe.",
     "long":["Set aus 10 sterilen Borosilikat-Vials (10 ml) mit Gummiseptum und Aluminium-Bördelkappe. "
             "Für die Lagerung rekonstituierter Lösungen im Labor.",
             "Autoklavierbar und chemisch beständig."]},

    {"slug":"misch-kit","name":"Rekonstitutions-Kit","cat":"zubehor","price":"19.90","size":"Set",
     "purity":"steril","mw":"—","badge":"Neu","color":"#0284c7",
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
    clamp = lambda v: max(0, min(255, int(v)))
    return "#%02x%02x%02x" % (clamp(r*f), clamp(g*f), clamp(b*f))

def product_svg(p):
    """Stilisiertes Vial + Molekül-Ring in der Produktfarbe (bolder)."""
    c = p["color"]; cd = darken(c, .68)
    # Hexagon-Ring (Molekül) oben links
    import math
    ring = ""
    cx, cy, r = 96, 96, 34
    pts = []
    for i in range(6):
        a = math.radians(60*i - 90)
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    for i in range(6):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%6]
        ring += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="2.4" opacity="0.65"/>'
    for x,y in pts:
        ring += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" opacity="0.92"/>'
    # Peptid-Kette unten
    chain = ""
    x0, yb = 120, 250
    for i in range(6):
        x = x0 + i*28
        y = yb + (9 if i%2 else -9)
        chain += f'<circle cx="{x}" cy="{y}" r="8" fill="#fff" opacity="0.9"/>'
        if i < 5:
            x2 = x0 + (i+1)*28; y2 = yb + (9 if (i+1)%2 else -9)
            chain += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="3" opacity="0.6"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img" aria-label="{html.escape(p['name'])} – {html.escape(p['size'])} Vial">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{cd}"/></linearGradient>
    <linearGradient id="liq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".12"/></linearGradient>
  </defs>
  <rect width="400" height="300" fill="url(#bg)"/>
  <circle cx="330" cy="64" r="120" fill="#fff" opacity="0.06"/>
  <circle cx="60" cy="250" r="90" fill="#fff" opacity="0.05"/>
  {ring}{chain}
  <g transform="translate(232,68)">
    <rect x="14" y="-14" width="22" height="16" rx="3" fill="#e7edf2"/>
    <rect x="10" y="0" width="30" height="10" rx="2" fill="#c1cdd9"/>
    <rect x="6" y="10" width="38" height="150" rx="12" fill="#fff" opacity="0.92"/>
    <rect x="6" y="74" width="38" height="86" rx="12" fill="url(#liq)"/>
    <rect x="13" y="16" width="6" height="40" rx="3" fill="#fff" opacity="0.85"/>
  </g>
  <text x="20" y="280" font-family="'Spline Sans Mono', monospace" font-size="14" fill="#fff" opacity="0.85" letter-spacing="0.5">{html.escape(p['size'])}</text>
</svg>'''

def logo_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-label="HELIX Logo">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0fa3a3"/><stop offset="1" stop-color="#5b54d6"/></linearGradient></defs>
  <rect width="48" height="48" rx="13" fill="url(#g)"/>
  <path d="M15 12c0 9 18 9 18 24M33 12c0 9-18 9-18 24" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <line x1="17" y1="18" x2="31" y2="18" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="17" y1="30" x2="31" y2="30" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
</svg>'''

def avatar_svg(t):
    c = t["color"]; cd = darken(c, .7)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{html.escape(t['name'])}">
  <defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{cd}"/></linearGradient></defs>
  <rect width="100" height="100" rx="50" fill="url(#a)"/>
  <text x="50" y="63" text-anchor="middle" font-family="'Archivo', sans-serif" font-size="36" font-weight="700" fill="#fff">{t['ini']}</text>
</svg>'''

# ----------------------------------------------------------------------------
# 3. HTML-BAUSTEINE
# ----------------------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@400;500;600;700&'
         'family=Archivo+Expanded:wght@600;700;800&'
         'family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')

CART_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
             '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/>'
             '<path d="M2 3h3l2.4 12.2a1.6 1.6 0 0 0 1.6 1.3h8.2a1.6 1.6 0 0 0 1.6-1.3L22 7H6"/></svg>')

PLUS_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M12 5v14M5 12h14"/></svg>')

NAV = [("index.html","Start"),("produkte.html","Produkte"),("faq.html","FAQ"),("kontakt.html","Kontakt")]

def head(title, desc, active):
    nav = ""
    for href, label in NAV:
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
  {FONTS}
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
        <a class="cart-btn" href="warenkorb.html" aria-label="Warenkorb">
          {CART_ICON}<span class="cart-count" data-cart-count data-empty="true">0</span>
        </a>
        <button class="nav-toggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="nav-links"><span></span></button>
      </div>
    </div>
  </header>
  <main id="main">
'''

def footer():
    shop_links = "".join(f'<li><a href="produkte.html#{k}">{html.escape(v)}</a></li>' for k,v in CATEGORIES.items())
    return f'''  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="assets/img/logo.svg" alt="HELIX PEPTIDES">
          <p>Peptide und Laborbedarf in dokumentierter Forschungsqualität. Jede Charge mit Analysezertifikat (CoA).</p>
          <p style="color:#fff"><strong>Nur für Forschungs- und Laborzwecke.</strong><br><span style="color:#aebccb">Nicht für den menschlichen oder tierischen Gebrauch.</span></p>
        </div>
        <div>
          <h4>Shop</h4>
          <ul>{shop_links}<li><a href="produkte.html">Alle Produkte</a></li><li><a href="warenkorb.html">Warenkorb</a></li></ul>
        </div>
        <div>
          <h4>Service</h4>
          <ul>
            <li><a href="kontakt.html">Kontakt</a></li>
            <li><a href="faq.html">FAQ</a></li>
            <li><a href="faq.html#versand">Versand &amp; Lieferung</a></li>
          </ul>
        </div>
        <div>
          <h4>Rechtliches</h4>
          <ul>
            <li><a href="impressum.html">Impressum</a></li>
            <li><a href="datenschutz.html">Datenschutz</a></li>
            <li><a href="agb.html">AGB</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; <span data-year>2026</span> HELIX PEPTIDES &mdash; Fiktiver Webshop für das Modul M293 (Schulprojekt).</span>
        <span class="mono">Bottighofen, Schweiz</span>
      </div>
    </div>
  </footer>
  <script src="js/products.js"></script>
  <script src="js/cart.js"></script>
  <script src="js/main.js"></script>
</body>
</html>'''

def disclaimer():
    return ('<div class="disclaimer" role="note">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>'
            '<div><strong>Wichtiger Hinweis:</strong> Alle Produkte sind ausschliesslich für Forschungs- und Laborzwecke '
            'bestimmt (Research Use Only). Sie sind <strong>nicht</strong> für den menschlichen oder tierischen Gebrauch, '
            'zur Diagnose oder Therapie zugelassen.</div></div>')

def product_card(p):
    badge = f'<span class="pill pill--violet product-card__tag">{p["badge"]}</span>' if p["badge"] else ""
    return f'''      <article class="product-card" data-category="{p['cat']}">
        <a class="product-card__media" href="produkt-{p['slug']}.html" aria-label="{html.escape(p['name'])} ansehen">
          <img src="assets/img/products/{p['slug']}.svg" alt="{html.escape(p['name'])} – {html.escape(p['size'])} Vial" loading="lazy">{badge}
        </a>
        <div class="product-card__body">
          <span class="product-card__cat">{CATEGORIES[p['cat']]}</span>
          <h3 class="product-card__title"><a href="produkt-{p['slug']}.html">{html.escape(p['name'])}</a></h3>
          <p class="product-card__desc">{html.escape(p['short'])}</p>
          <div class="product-card__foot">
            <span class="price">CHF&nbsp;{p['price']}</span>
            <button class="add-btn" type="button" data-add="{p['slug']}" aria-label="{html.escape(p['name'])} in den Warenkorb">{PLUS_ICON}</button>
          </div>
        </div>
      </article>'''

# ----------------------------------------------------------------------------
# 4. SEITEN
# ----------------------------------------------------------------------------
def build_products_js():
    data = {p["slug"]: {
        "name": p["name"], "price": float(p["price"]), "size": p["size"],
        "cat": p["cat"], "img": f"assets/img/products/{p['slug']}.svg"
    } for p in PRODUCTS}
    js = "/* Auto-generiert aus tools/generate.py – Produktdaten für den Warenkorb. */\n"
    js += "window.HELIX_PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    write("js/products.js", js)

def build_index():
    featured = [p for p in PRODUCTS if p["badge"] in ("Bestseller","Neu")][:4]
    if len(featured) < 4: featured = PRODUCTS[:4]
    cards = "\n".join(product_card(p) for p in featured)

    cat_tiles = ""
    for k,v in CATEGORIES.items():
        count = sum(1 for p in PRODUCTS if p["cat"] == k)
        cat_tiles += f'''        <a class="cat-tile" href="produkte.html#{k}">
          <svg class="cat-tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M9 3h6v4l4 11a2 2 0 0 1-1.9 2.6H6.9A2 2 0 0 1 5 18L9 7V3Z"/><path d="M8 14h8"/></svg>
          <strong>{html.escape(v)}</strong>
          <span>{html.escape(CAT_DESC[k])}</span>
          <span class="cat-tile__count">{count} Produkte &rarr;</span>
        </a>'''

    usps = [
        ("HPLC / MS", "Geprüfte Reinheit", "Jede Charge analytisch geprüft – Analysezertifikat (CoA) liegt bei."),
        ("2–8 °C", "Kühlversand", "Temperaturkontrollierter Versand mit Trockeneis bei sensiblen Produkten."),
        ("≥ 98 %", "Laborqualität", "Lyophilisierte Peptide in versiegelten Borosilikat-Vials."),
        ("CH-Team", "Fachsupport", "Fragen zu Sequenz, Lagerung oder Handling? Wir antworten fachkundig."),
    ]
    usp_html = ""
    for tag, t, d in usps:
        usp_html += f'<div class="usp"><span class="usp__num mono">{tag}</span><h3>{t}</h3><p>{d}</p></div>'

    body = f'''    <section class="hero">
      <div class="container hero__grid">
        <div>
          <p class="kicker" data-reveal>Research Peptides · Made in Switzerland</p>
          <h1 data-reveal>Peptide in <em>dokumentierter</em> Laborqualität.</h1>
          <p data-reveal>Lyophilisierte Forschungs- und Kosmetik-Peptide mit über 98&nbsp;% Reinheit – jede Charge mit Analysezertifikat. Schnell von der Charge zur Bestellung.</p>
          <div class="hero__cta" data-reveal>
            <a class="btn btn--bright btn--lg" href="produkte.html">Produkte entdecken</a>
            <a class="btn btn--light btn--lg" href="#newsletter">Newsletter abonnieren</a>
          </div>
          <div class="trust-ticker" data-reveal>
            <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 13 4 4L19 7"/></svg>≥ 98 % Reinheit</span>
            <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 13 4 4L19 7"/></svg>CoA pro Charge</span>
            <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 13 4 4L19 7"/></svg>Kühlversand 24–48 h CH</span>
          </div>
        </div>
        <div class="hero__art" data-reveal>
          <img src="assets/img/products/ghk-cu.svg" alt="GHK-Cu Peptid-Vial, 50 mg" width="440">
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">{disclaimer()}</div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section__head">
          <p class="kicker">Sortiment</p>
          <h2>Drei Kategorien, ein Standard</h2>
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
          <h2>Beliebt &amp; neu</h2>
          <p class="lead">Unsere meistbestellten und neusten Artikel auf einen Blick.</p>
        </div>
        <div class="card-grid">
{cards}
        </div>
        <p class="mt-4"><a class="btn btn--ghost" href="produkte.html">Alle Produkte ansehen &rarr;</a></p>
      </div>
    </section>

    <section class="section section--dark">
      <div class="container">
        <div class="section__head">
          <p class="kicker">Warum HELIX</p>
          <h2>Worauf Sie sich verlassen können</h2>
        </div>
        <div class="usp-grid">{usp_html}</div>
      </div>
    </section>

    <section class="section" id="newsletter">
      <div class="container">
        <div class="section__head">
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
          <p class="kicker">Sortiment · {len(PRODUCTS)} Artikel</p>
          <h1>Alle Produkte</h1>
          <p class="lead">Filtere nach Kategorie. Jeder Artikel mit Bild, Beschreibung, Video und Bestellformular auf der Detailseite.</p>
        </div>
        {disclaimer()}
        <div class="filter-bar mt-3" data-filter-bar role="group" aria-label="Nach Kategorie filtern">{filters}</div>
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
    pname = f"{p['name']} ({p['size']})"

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
          <li><strong>Reinheit</strong><span>{p['purity']}</span></li>
          <li><strong>Menge</strong><span>{html.escape(p['size'])}</span></li>
          <li><strong>Mol-Gewicht</strong><span>{p['mw']}</span></li>
          <li><strong>Form</strong><span>Lyophilisiert</span></li>
        </ul>
      </div>

      <div class="product__info">
        <span class="product-card__cat">{CATEGORIES[p['cat']]}</span> {badge}
        <h1>{html.escape(p['name'])}</h1>
        <p class="lead">{html.escape(p['short'])}</p>
        <div class="product__price">
          <span class="price">CHF&nbsp;{p['price']}</span>
          <span class="pill pill--bright">inkl. CoA</span>
        </div>

        <div class="product__buy" data-buy>
          <label class="qty" aria-label="Menge">
            <select name="menge" aria-label="Menge" style="border:none;background:transparent;padding:.5rem .6rem">
              <option>1</option><option>2</option><option>3</option><option>5</option><option>10</option>
            </select>
          </label>
          <button class="btn btn--bright btn--lg add-to-cart" type="button" data-add="{p['slug']}">In den Warenkorb</button>
        </div>

        <div class="order-box">
          <h3>Oder direkt per Formular bestellen</h3>
          <p class="form-note">Nach dem Absenden erhältst du eine Bestellbestätigung. (Demo – es werden keine Daten gespeichert.)</p>
          <form class="form" data-order-form action="danke.html" method="get" novalidate>
            <input type="hidden" name="type" value="order">
            <input type="hidden" name="produkt" value="{html.escape(pname)}">
            <div class="form__row">
              <div class="field"><label>Name <span class="req">*</span></label><input type="text" name="name" autocomplete="name" required></div>
              <div class="field"><label>E-Mail <span class="req">*</span></label><input type="email" name="email" autocomplete="email" required></div>
            </div>
            <div class="form__row">
              <div class="field"><label>Firma / Labor</label><input type="text" name="labor" autocomplete="organization"></div>
              <div class="field"><label>Menge <span class="req">*</span></label>
                <select name="menge" required><option>1 Vial</option><option>2 Vials</option><option>3 Vials</option><option>5 Vials</option><option>10 Vials</option></select>
              </div>
            </div>
            <button class="btn btn--primary btn--block btn--lg" type="submit">Bestellung anfragen · CHF&nbsp;{p['price']}</button>
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
        <div class="section__head"><h2>Ähnliche Produkte</h2></div>
        <div class="card-grid">
{rel_cards}
        </div>
      </div>
    </section>
'''
    write(f"produkt-{p['slug']}.html",
          head(f"{p['name']} – HELIX PEPTIDES", p["short"] + " Nur für Forschungszwecke.",
               "produkte.html") + body + footer())

def build_contact():
    options = ["Bestellung & Versand","Produktfrage","Reklamation","Grosshandel / B2B","Sonstiges"]
    opt_html = "".join(f'<option>{html.escape(o)}</option>' for o in options)
    team_html = ""
    for t in TEAM:
        team_html += f'''        <div class="team-card">
          <img src="assets/img/team/{t['ini'].lower()}.svg" alt="{html.escape(t['name'])}">
          <strong>{html.escape(t['name'])}</strong><span>{html.escape(t['role'])}</span>
        </div>'''
    body = f'''    <div class="container breadcrumb"><a href="index.html">Start</a> / Kontakt</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head">
          <p class="kicker">Kontakt</p>
          <h1>Wir sind für dich da</h1>
          <p class="lead">Fragen zu Produkten, Bestellungen oder Analysezertifikaten? Wähle ein Betreff – deine Anfrage wird automatisch dem richtigen Team zugeordnet.</p>
        </div>
        <div class="contact-grid">
          <form class="form" data-contact-form novalidate>
            <div class="form__row">
              <div class="field"><label>Name <span class="req">*</span></label><input type="text" name="name" autocomplete="name" required></div>
              <div class="field"><label>E-Mail <span class="req">*</span></label><input type="email" name="email" autocomplete="email" required></div>
            </div>
            <div class="field">
              <label>Betreff <span class="req">*</span></label>
              <select name="betreff" required><option value="">Bitte wählen …</option>{opt_html}</select>
              <span class="field__hint">Das gewählte Betreff bestimmt, welches Team deine E-Mail erhält.</span>
            </div>
            <div class="field"><label>Nachricht <span class="req">*</span></label><textarea name="nachricht" required placeholder="Wie können wir helfen?"></textarea></div>
            <button class="btn btn--primary btn--lg" type="submit">Nachricht senden</button>
            <p class="form-feedback" role="status" aria-live="polite"></p>
          </form>
          <aside>
            <div class="order-box" id="versand">
              <h3>Direktkontakt</h3>
              <ul class="info-list">
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg><span class="mono">info@helix-peptides.example</span></li>
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2Z"/></svg><span class="mono">+41 71 000 00 00</span></li>
                <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg><span>Seestrasse 1, 8598 Bottighofen, CH</span></li>
              </ul>
              <p class="form-note"><strong>Versand:</strong> Mo–Fr, 24–48&nbsp;h innerhalb der Schweiz. Details unter <a href="faq.html#versand">Versand &amp; Lieferung</a>.</p>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="container">
        <div class="section__head"><p class="kicker">Team</p><h2>Die Menschen hinter HELIX</h2><p class="lead">Ein kleines, spezialisiertes Team aus Wissenschaft, Qualitätssicherung und Logistik.</p></div>
        <div class="team-grid">
{team_html}
        </div>
      </div>
    </section>
'''
    write("kontakt.html", head("Kontakt – HELIX PEPTIDES",
          "Kontaktiere das HELIX-Team. Betreffauswahl mit automatischer Zuordnung zum richtigen Ansprechpartner.",
          "kontakt.html") + body + footer())

def prose_page(filename, active, title, desc, h1, kicker, inner):
    body = f'''    <div class="container breadcrumb"><a href="index.html">Start</a> / {html.escape(h1)}</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head"><p class="kicker">{html.escape(kicker)}</p><h1>{html.escape(h1)}</h1></div>
        <div class="prose">
{inner}
        </div>
      </div>
    </section>
'''
    write(filename, head(title, desc, active) + body + footer())

def build_impressum():
    inner = '''          <p class="muted">Angaben gemäss Schweizer Recht. Fiktive Daten – Schulprojekt M293.</p>
          <h2>Betreiber</h2>
          <p>HELIX PEPTIDES GmbH (fiktiv)<br>Seestrasse 1<br>8598 Bottighofen, Schweiz</p>
          <h2>Kontakt</h2>
          <p class="mono">info@helix-peptides.example<br>+41 71 000 00 00</p>
          <h2>Handelsregister</h2>
          <p>UID: CHE-000.000.000 (fiktiv)<br>Eingetragen im Handelsregister des Kantons Thurgau.</p>
          <h2>Vertretungsberechtigte Person</h2>
          <p>Dr. Lena Brunner, Geschäftsführung</p>
          <h2>Haftungsausschluss</h2>
          <p>Dies ist ein nicht-kommerzielles Schulprojekt. Alle Produkte, Preise und Firmenangaben
          sind erfunden. Es findet kein realer Verkauf statt. Alle Produkte werden ausschliesslich
          zu Forschungs- und Laborzwecken dargestellt (Research Use Only).</p>'''
    prose_page("impressum.html","impressum.html","Impressum – HELIX PEPTIDES",
               "Impressum des HELIX-PEPTIDES-Shops (fiktives Schulprojekt M293).","Impressum","Rechtliches",inner)

def build_datenschutz():
    inner = '''          <p class="muted">Diese Datenschutzerklärung erläutert den Umgang mit Daten in diesem
          Schulprojekt. Da es sich um eine statische Demo-Seite handelt, werden keine personenbezogenen
          Daten an einen Server übertragen oder gespeichert.</p>
          <h2>1. Verantwortliche Stelle</h2>
          <p>HELIX PEPTIDES GmbH (fiktiv), Seestrasse 1, 8598 Bottighofen, CH.</p>
          <h2>2. Welche Daten werden verarbeitet?</h2>
          <p>Formulareingaben (Newsletter, Kontakt, Bestellung) werden <strong>ausschliesslich lokal
          im Browser</strong> verarbeitet. Das Kontaktformular öffnet dein eigenes E-Mail-Programm;
          es erfolgt keine automatische Übertragung an uns.</p>
          <h2>3. Warenkorb (Web Storage)</h2>
          <p>Der Warenkorb nutzt die <span class="mono">localStorage</span>-Funktion deines Browsers,
          um die ausgewählten Produkte zwischen den Seiten zu merken. Diese Daten bleiben auf deinem
          Gerät und werden nicht an Dritte übermittelt. Du kannst sie jederzeit löschen, indem du den
          Warenkorb leerst oder den Browser-Speicher leerst.</p>
          <h2>4. Cookies & Tracking</h2>
          <p>Diese Seite setzt keine Tracking-Cookies und bindet keine Analyse-Dienste ein.
          Schriftarten werden von Google Fonts geladen.</p>
          <h2>5. Deine Rechte</h2>
          <p>Da keine Daten serverseitig gespeichert werden, entfällt eine Auskunft, Berichtigung oder
          Löschung. Für ein reales Angebot würden hier die Rechte nach DSG/DSGVO erläutert.</p>'''
    prose_page("datenschutz.html","datenschutz.html","Datenschutz – HELIX PEPTIDES",
               "Datenschutzerklärung des HELIX-PEPTIDES-Shops (Schulprojekt, keine Datenspeicherung).","Datenschutz","Rechtliches",inner)

def build_agb():
    inner = '''          <p class="muted">Allgemeine Geschäftsbedingungen (fiktiv, Schulprojekt M293).</p>
          <h2>1. Geltungsbereich</h2>
          <p>Diese AGB gelten für alle (fiktiven) Bestellungen über den HELIX-PEPTIDES-Shop.
          Es handelt sich um ein Schulprojekt ohne realen Geschäftsbetrieb.</p>
          <h2>2. Research Use Only</h2>
          <p>Alle Produkte sind ausschliesslich für Forschungs- und Laborzwecke bestimmt. Sie sind
          <strong>nicht</strong> für den menschlichen oder tierischen Gebrauch, zur Diagnose oder
          Therapie zugelassen. Mit der Bestellung bestätigt die Käuferin/der Käufer, die Produkte
          ausschliesslich sach- und fachgerecht im Labor einzusetzen.</p>
          <h2>3. Bestellung & Vertragsschluss</h2>
          <p>Eine Bestellung über das Formular gilt als unverbindliche Anfrage. Ein Vertrag käme
          (im realen Betrieb) erst mit unserer Bestätigung zustande.</p>
          <h2>4. Preise & Versand</h2>
          <p>Alle Preise verstehen sich in CHF inkl. MwSt. Versandkosten und -fristen sind in der
          <a href="faq.html#versand">FAQ</a> beschrieben.</p>
          <h2>5. Widerruf & Rückgabe</h2>
          <p>Aus Qualitäts- und Sicherheitsgründen sind geöffnete oder rekonstituierte Vials vom
          Umtausch ausgeschlossen. Bei Transportschäden bitte innert 7 Tagen melden.</p>
          <h2>6. Gewährleistung</h2>
          <p>Wir gewährleisten die auf dem Analysezertifikat (CoA) angegebene Reinheit zum Zeitpunkt
          des Versands bei sachgerechter Lagerung.</p>
          <h2>7. Anwendbares Recht</h2>
          <p>Es gilt Schweizer Recht; Gerichtsstand ist Bottighofen (fiktiv).</p>'''
    prose_page("agb.html","agb.html","AGB – HELIX PEPTIDES",
               "Allgemeine Geschäftsbedingungen des HELIX-PEPTIDES-Shops (Schulprojekt).","AGB","Rechtliches",inner)

def build_faq():
    faqs = [
        ("Was bedeutet „Research Use Only“?",
         "Alle Produkte sind ausschliesslich für Forschungs- und Laborzwecke bestimmt und nicht für den menschlichen oder tierischen Gebrauch, zur Diagnose oder Therapie zugelassen. Mit der Bestellung bestätigst du die fachgerechte Verwendung im Labor."),
        ("Erhalte ich ein Analysezertifikat (CoA)?",
         "Ja. Jede Charge wird per HPLC und Massenspektrometrie geprüft; das CoA mit Reinheit und Identität liegt jeder Lieferung bei und kann auf Wunsch vorab zugesendet werden."),
        ("Wie lagere ich lyophilisierte Peptide richtig?",
         "Lyophilisiert bei −20 °C, vor Licht und Feuchtigkeit geschützt. Nach der Rekonstitution gekühlt (2–8 °C) aufbewahren und zeitnah verwenden."),
        ("Wie funktioniert die Bestellung?",
         "Du kannst Produkte in den Warenkorb legen und zentral bestellen oder direkt auf der Produktseite das Bestellformular nutzen. Beides löst eine unverbindliche Anfrage aus."),
        ("Bezahlung",
         "Im realen Betrieb per Rechnung, Kreditkarte oder TWINT. In dieser Demo wird keine Zahlung ausgelöst."),
    ]
    items = ""
    for q,a in faqs:
        items += f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
    ship = ('<details open id="versand"><summary>Versand &amp; Lieferung</summary>'
            '<p>Versand Mo–Fr innerhalb der Schweiz in 24–48 h. Sensible Produkte werden '
            'temperaturkontrolliert mit Trockeneis versandt. Ab CHF 100 Bestellwert ist der '
            'Versand gratis, darunter CHF 8.50.</p></details>')
    body = f'''    <div class="container breadcrumb"><a href="index.html">Start</a> / FAQ</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head"><p class="kicker">Hilfe</p><h1>Häufige Fragen</h1>
        <p class="lead">Antworten zu Qualität, Lagerung, Bestellung und Versand.</p></div>
        <div class="faq">
          {ship}
          {items}
        </div>
        <p class="mt-4">Noch Fragen? <a href="kontakt.html">Schreib uns &rarr;</a></p>
      </div>
    </section>
'''
    write("faq.html", head("FAQ – HELIX PEPTIDES",
          "Häufige Fragen zu Research-Peptiden: Qualität, CoA, Lagerung, Bestellung und Versand.",
          "faq.html") + body + footer())

def build_warenkorb():
    body = '''    <div class="container breadcrumb"><a href="index.html">Start</a> / Warenkorb</div>
    <section class="section" style="padding-top:var(--sp-3)">
      <div class="container">
        <div class="section__head"><p class="kicker">Warenkorb</p><h1>Dein Warenkorb</h1></div>

        <div class="cart-empty hidden" data-cart-empty>
          <p>Dein Warenkorb ist noch leer.</p>
          <a class="btn btn--primary" href="produkte.html">Produkte entdecken</a>
        </div>

        <div class="cart-layout hidden" data-cart-body>
          <div class="cart-list" data-cart-list></div>
          <aside class="cart-summary">
            <h3>Zusammenfassung</h3>
            <dl>
              <dt>Zwischensumme</dt><dd data-sum-items>CHF 0.00</dd>
              <dt>Versand</dt><dd data-sum-ship>CHF 0.00</dd>
            </dl>
            <dl><dt class="total">Total</dt><dd class="total" data-sum-total>CHF 0.00</dd></dl>
            <form class="form" data-cart-order action="danke.html" method="get" novalidate style="margin-top:var(--sp-2)">
              <input type="hidden" name="type" value="order">
              <input type="hidden" name="bestellung" value="">
              <div class="field"><label>Name <span class="req">*</span></label><input type="text" name="name" autocomplete="name" required></div>
              <div class="field"><label>E-Mail <span class="req">*</span></label><input type="email" name="email" autocomplete="email" required></div>
              <button class="btn btn--bright btn--block btn--lg" type="submit">Bestellung abschliessen</button>
              <p class="form-feedback" role="status" aria-live="polite"></p>
              <p class="form-note">Unverbindliche Anfrage · Demo, keine Datenspeicherung.</p>
            </form>
          </aside>
        </div>
      </div>
    </section>
'''
    write("warenkorb.html", head("Warenkorb – HELIX PEPTIDES",
          "Dein Warenkorb bei HELIX PEPTIDES.", "warenkorb.html") + body + footer())

def build_danke():
    body = '''    <section class="container">
      <div class="thanks" data-thanks>
        <div class="thanks__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 13 4 4L19 7"/></svg></div>
        <h1 data-thanks-headline>Vielen Dank!</h1>
        <p class="lead">Deine Anfrage ist eingegangen. Wir melden uns in Kürze per E-Mail mit der Bestätigung und dem Analysezertifikat.</p>
        <p class="mono" data-thanks-detail style="color:var(--c-accent-dark)"></p>
        <p class="form-note">Hinweis: Dies ist ein Schulprojekt (Demo). Es wurde keine echte Bestellung ausgelöst und keine Daten gespeichert.</p>
        <p class="mt-3"><a class="btn btn--primary" href="produkte.html">Weiter einkaufen</a> <a class="btn btn--ghost" href="index.html">Zur Startseite</a></p>
      </div>
    </section>
'''
    write("danke.html", head("Danke – HELIX PEPTIDES",
          "Bestellbestätigung – vielen Dank für deine Anfrage.", "danke.html") + body + footer())

# ----------------------------------------------------------------------------
# 5. BUILD
# ----------------------------------------------------------------------------
def main():
    write("assets/img/logo.svg", logo_svg())
    for p in PRODUCTS:
        write(f"assets/img/products/{p['slug']}.svg", product_svg(p))
    for t in TEAM:
        write(f"assets/img/team/{t['ini'].lower()}.svg", avatar_svg(t))
    build_products_js()
    build_index()
    build_products()
    build_contact()
    for p in PRODUCTS:
        build_detail(p)
    build_faq()
    build_warenkorb()
    build_danke()
    build_impressum()
    build_datenschutz()
    build_agb()
    n_html = 3 + len(PRODUCTS) + 6  # index/produkte/kontakt + details + faq/warenkorb/danke/impressum/datenschutz/agb
    print(f"OK: {len(PRODUCTS)} Produkte, {n_html} HTML-Seiten, "
          f"{1 + len(PRODUCTS) + len(TEAM)} SVG-Grafiken, products.js erzeugt.")

if __name__ == "__main__":
    main()
