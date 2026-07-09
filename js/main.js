/* =========================================================================
   HELIX PEPTIDES – main.js
   Progressive Enhancement: Seite funktioniert auch ohne JavaScript.
   Ergänzt: mobile Navigation, Kategoriefilter, Formular-Validierung,
   Newsletter-Feedback, Kontakt-Betreff-Routing (mailto), Reveal-Motion.
   Warenkorb-Logik liegt in cart.js.
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
        links.addEventListener("click", function (e) {
            if (e.target.tagName === "A") {
                links.classList.remove("is-open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });
    }

    /* ---------- 2. Jahr im Footer ---------- */
    var year = new Date().getFullYear();
    document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = year; });

    /* ---------- 3. Kategoriefilter ---------- */
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

    /* ---------- 4. Validierungs-Helfer ---------- */
    function showFeedback(form, message, ok) {
        // Feedback-Element kann im Formular ODER direkt daneben stehen
        var box = form.querySelector(".form-feedback") ||
            (form.parentElement && form.parentElement.querySelector(".form-feedback"));
        if (!box) return;
        box.textContent = message;
        box.className = "form-feedback " + (ok ? "is-ok" : "is-err");
    }
    function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }

    /* ---------- 5. Newsletter (Demo – keine Datenspeicherung) ---------- */
    document.querySelectorAll("[data-newsletter]").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            var email = form.querySelector('input[type="email"]');
            if (!email || !isEmail(email.value.trim())) {
                showFeedback(form, "Bitte gib eine gültige E-Mail-Adresse ein.", false);
                if (email) email.focus();
                return;
            }
            showFeedback(form, "Danke! Du bist für den Newsletter angemeldet. ✓", true);
            form.reset();
        });
    });

    /* ---------- 6. Bestellformular (Detailseite) ----------
       Validierung; gültig -> native GET-Navigation zu danke.html. */
    document.querySelectorAll("[data-order-form]").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            var data = new FormData(form);
            var name = (data.get("name") || "").toString().trim();
            var email = (data.get("email") || "").toString().trim();
            if (name.length < 2) { e.preventDefault(); showFeedback(form, "Bitte Namen angeben.", false); return; }
            if (!isEmail(email)) { e.preventDefault(); showFeedback(form, "Bitte gültige E-Mail-Adresse angeben.", false); return; }
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

            var routing = {
                "Bestellung & Versand": "bestellung@helix-peptides.example",
                "Produktfrage": "lab@helix-peptides.example",
                "Reklamation": "support@helix-peptides.example",
                "Grosshandel / B2B": "b2b@helix-peptides.example",
                "Sonstiges": "info@helix-peptides.example"
            };
            var to = routing[betreff] || "info@helix-peptides.example";
            var body = "Name:  " + name + "\nE-Mail: " + email + "\n\n" + nachricht + "\n";
            window.location.href = "mailto:" + to + "?subject=" +
                encodeURIComponent("[" + betreff + "] Anfrage von " + name) +
                "&body=" + encodeURIComponent(body);
            showFeedback(contact, "Danke! Dein E-Mail-Programm öffnet sich – die Anfrage wird an „" + betreff + "“ geleitet. ✓", true);
        });
    }

    /* ---------- 8. Danke-Seite: Bestelldetails aus URL anzeigen ---------- */
    var thanks = document.querySelector("[data-thanks]");
    if (thanks) {
        var params = new URLSearchParams(location.search);
        var detail = thanks.querySelector("[data-thanks-detail]");
        var headline = thanks.querySelector("[data-thanks-headline]");
        var type = params.get("type") || "order";
        if (headline && type === "contact") headline.textContent = "Nachricht erhalten!";
        if (detail) {
            var produkt = params.get("produkt");
            var bestellung = params.get("bestellung");
            var menge = params.get("menge");
            if (bestellung) detail.textContent = "Deine Bestellung: " + bestellung;
            else if (produkt) detail.textContent = "Deine Anfrage: " + (menge ? menge + "× " : "") + produkt;
            else detail.textContent = "";
        }
    }

    /* ---------- 9. Reveal-Motion ----------
       Entrance- und Scroll-Animationen liegen zentral in js/motion.js
       (Web Animations API, respektiert prefers-reduced-motion). */
})();
