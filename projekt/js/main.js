/* =========================================================================
   HELIX PEPTIDES – main.js
   Progressive Enhancement: Die Seite funktioniert auch ohne JavaScript.
   JS ergänzt: mobile Navigation, Kategoriefilter, Formular-Validierung,
   Bestell-/Kontakt-Mailto und Jahr im Footer.
   (JavaScript ist laut Auftrag für optionale Funktionen erlaubt.)
   ========================================================================= */
(function () {
    "use strict";

    /* ---------- 1. Mobile Navigation ---------- */
    var toggle = document.querySelector(".nav-toggle");
    var links = document.getElementById("nav-links");
    if (toggle && links) {
        toggle.addEventListener("click", function () {
            var open = links.classList.toggle("is-open");
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
        });
        // Menü schliessen, wenn ein Link geklickt wird
        links.addEventListener("click", function (e) {
            if (e.target.tagName === "A") {
                links.classList.remove("is-open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    /* ---------- 2. Aktuelles Jahr im Footer ---------- */
    var yearEls = document.querySelectorAll("[data-year]");
    var year = new Date().getFullYear();
    yearEls.forEach(function (el) { el.textContent = year; });

    /* ---------- 3. Kategoriefilter (Produktübersicht) ---------- */
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
            // Buttons-Status
            filterBar.querySelectorAll(".filter-btn").forEach(function (b) {
                b.classList.toggle("is-active", b.getAttribute("data-cat") === cat);
                b.setAttribute("aria-pressed", b.getAttribute("data-cat") === cat ? "true" : "false");
            });
        }

        filterBar.addEventListener("click", function (e) {
            var btn = e.target.closest(".filter-btn");
            if (!btn) return;
            var cat = btn.getAttribute("data-cat");
            applyFilter(cat);
            // URL-Hash aktualisieren, damit Links teilbar sind
            history.replaceState(null, "", cat === "all" ? "#" : "#" + cat);
        });

        // Beim Laden: Kategorie aus URL-Hash übernehmen (z.B. produkte.html#kosmetik)
        var initial = (location.hash || "").replace("#", "");
        var known = Array.prototype.map.call(
            filterBar.querySelectorAll(".filter-btn"),
            function (b) { return b.getAttribute("data-cat"); }
        );
        applyFilter(known.indexOf(initial) > -1 ? initial : "all");
    }

    /* ---------- 4. Hilfsfunktionen Validierung ---------- */
    function showFeedback(form, message, ok) {
        var box = form.querySelector(".form-feedback");
        if (!box) return;
        box.textContent = message;
        box.className = "form-feedback " + (ok ? "is-ok" : "is-err");
    }
    function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }

    /* ---------- 5. Newsletter-Formulare ---------- */
    document.querySelectorAll("[data-newsletter]").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            var email = form.querySelector('input[type="email"]');
            if (!email || !isEmail(email.value.trim())) {
                showFeedback(form, "Bitte gib eine gültige E-Mail-Adresse ein.", false);
                if (email) email.focus();
                return;
            }
            showFeedback(form, "Danke! Du bist für den Newsletter angemeldet. ✅", true);
            form.reset();
        });
    });

    /* ---------- 6. Bestellformular (Produkt-Detailseite) ---------- */
    document.querySelectorAll("[data-order-form]").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            var data = new FormData(form);
            var name = (data.get("name") || "").toString().trim();
            var email = (data.get("email") || "").toString().trim();
            if (name.length < 2) { showFeedback(form, "Bitte Namen angeben.", false); return; }
            if (!isEmail(email)) { showFeedback(form, "Bitte gültige E-Mail-Adresse angeben.", false); return; }

            var produkt = form.getAttribute("data-product") || "Produkt";
            var menge = data.get("menge") || "1";
            var subject = "Bestellung: " + produkt;
            var body =
                "Bestellung über den HELIX-PEPTIDES-Shop\n" +
                "----------------------------------------\n" +
                "Produkt:  " + produkt + "\n" +
                "Menge:    " + menge + "\n" +
                "Name:     " + name + "\n" +
                "E-Mail:   " + email + "\n" +
                "Firma/Labor: " + (data.get("labor") || "-") + "\n" +
                "Anmerkung:\n" + (data.get("notiz") || "-") + "\n";
            // E-Mail-Programm öffnen, damit die Anfrage zugeordnet werden kann
            window.location.href =
                "mailto:bestellung@helix-peptides.example?subject=" +
                encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
            showFeedback(form, "Dein E-Mail-Programm öffnet sich mit der vorausgefüllten Bestellung. ✅", true);
        });
    });

    /* ---------- 7. Kontaktformular (Betreff-Routing per mailto) ---------- */
    var contact = document.querySelector("[data-contact-form]");
    if (contact) {
        contact.addEventListener("submit", function (e) {
            e.preventDefault();
            var data = new FormData(contact);
            var name = (data.get("name") || "").toString().trim();
            var email = (data.get("email") || "").toString().trim();
            var betreff = (data.get("betreff") || "").toString();
            var nachricht = (data.get("nachricht") || "").toString().trim();

            if (name.length < 2) { showFeedback(contact, "Bitte Namen angeben.", false); return; }
            if (!isEmail(email)) { showFeedback(contact, "Bitte gültige E-Mail-Adresse angeben.", false); return; }
            if (!betreff) { showFeedback(contact, "Bitte ein Betreff auswählen.", false); return; }
            if (nachricht.length < 10) { showFeedback(contact, "Bitte eine etwas längere Nachricht schreiben.", false); return; }

            // Betreff-Auswahl steuert die Empfängeradresse -> automatische Zuordnung
            var routing = {
                "Bestellung & Versand": "bestellung@helix-peptides.example",
                "Produktfrage": "lab@helix-peptides.example",
                "Reklamation": "support@helix-peptides.example",
                "Grosshandel / B2B": "b2b@helix-peptides.example",
                "Sonstiges": "info@helix-peptides.example"
            };
            var to = routing[betreff] || "info@helix-peptides.example";
            var body = "Name:  " + name + "\nE-Mail: " + email + "\n\n" + nachricht + "\n";
            window.location.href =
                "mailto:" + to + "?subject=" + encodeURIComponent("[" + betreff + "] Anfrage von " + name) +
                "&body=" + encodeURIComponent(body);
            showFeedback(contact, "Danke! Dein E-Mail-Programm öffnet sich – die Anfrage wird an „" + betreff + "“ geleitet. ✅", true);
        });
    }
})();
