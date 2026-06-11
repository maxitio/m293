/* =========================================================================
   HELIX PEPTIDES – cart.js
   Optionaler Warenkorb über die Web Storage API (localStorage).
   Speichert nur { slug: menge }. Produktdaten kommen aus js/products.js
   (window.HELIX_PRODUCTS). Funktioniert seitenübergreifend.
   ========================================================================= */
(function () {
    "use strict";

    var KEY = "helix_cart";
    var PRODUCTS = window.HELIX_PRODUCTS || {};

    /* ---------- Speicher ---------- */
    function read() {
        try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
        catch (e) { return {}; }
    }
    function write(cart) {
        try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {}
        updateBadge();
    }
    function count(cart) {
        cart = cart || read();
        return Object.keys(cart).reduce(function (n, k) { return n + cart[k]; }, 0);
    }
    function total(cart) {
        cart = cart || read();
        return Object.keys(cart).reduce(function (sum, slug) {
            var p = PRODUCTS[slug];
            return p ? sum + p.price * cart[slug] : sum;
        }, 0);
    }
    function chf(n) { return "CHF " + n.toFixed(2); }

    /* ---------- Badge im Header ---------- */
    function updateBadge() {
        var n = count();
        document.querySelectorAll("[data-cart-count]").forEach(function (el) {
            el.textContent = n;
            el.setAttribute("data-empty", n === 0 ? "true" : "false");
        });
    }

    /* ---------- Toast ---------- */
    var toastEl;
    function toast(msg) {
        if (!toastEl) {
            toastEl = document.createElement("div");
            toastEl.className = "toast";
            toastEl.setAttribute("role", "status");
            document.body.appendChild(toastEl);
        }
        toastEl.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 13 4 4L19 7"/></svg><span></span>';
        toastEl.querySelector("span").textContent = msg;
        // erzwinge Reflow für Transition
        void toastEl.offsetWidth;
        toastEl.classList.add("is-show");
        clearTimeout(toastEl._t);
        toastEl._t = setTimeout(function () { toastEl.classList.remove("is-show"); }, 2200);
    }

    /* ---------- Öffentliche Aktionen ---------- */
    function add(slug, qty) {
        qty = qty || 1;
        var cart = read();
        cart[slug] = (cart[slug] || 0) + qty;
        write(cart);
        var p = PRODUCTS[slug];
        toast((p ? p.name : "Produkt") + " in den Warenkorb gelegt");
    }
    function setQty(slug, qty) {
        var cart = read();
        if (qty <= 0) delete cart[slug]; else cart[slug] = qty;
        write(cart);
    }
    function remove(slug) { var c = read(); delete c[slug]; write(c); }

    /* ---------- Add-Buttons (Karten + Detailseite) ---------- */
    document.addEventListener("click", function (e) {
        var btn = e.target.closest("[data-add]");
        if (!btn) return;
        e.preventDefault();
        var slug = btn.getAttribute("data-add");
        var qtyEl = btn.closest("[data-buy]") ? btn.closest("[data-buy]").querySelector('[name="menge"]') : null;
        var qty = qtyEl ? parseInt(qtyEl.value, 10) || 1 : 1;
        add(slug, qty);
        // kurze visuelle Bestätigung an Icon-Buttons
        if (btn.classList.contains("add-btn")) {
            btn.classList.add("is-added");
            setTimeout(function () { btn.classList.remove("is-added"); }, 1200);
        }
    });

    /* ---------- Warenkorbseite ---------- */
    var listEl = document.querySelector("[data-cart-list]");
    if (listEl) {
        var emptyEl = document.querySelector("[data-cart-empty]");
        var bodyEl = document.querySelector("[data-cart-body]");
        var sumItems = document.querySelector("[data-sum-items]");
        var sumShip = document.querySelector("[data-sum-ship]");
        var sumTotal = document.querySelector("[data-sum-total]");
        var orderForm = document.querySelector("[data-cart-order]");

        function render() {
            var cart = read();
            var slugs = Object.keys(cart);
            if (slugs.length === 0) {
                if (bodyEl) bodyEl.classList.add("hidden");
                if (emptyEl) emptyEl.classList.remove("hidden");
                return;
            }
            if (bodyEl) bodyEl.classList.remove("hidden");
            if (emptyEl) emptyEl.classList.add("hidden");

            listEl.innerHTML = slugs.map(function (slug) {
                var p = PRODUCTS[slug]; if (!p) return "";
                var line = p.price * cart[slug];
                return '' +
                '<div class="cart-row" data-row="' + slug + '">' +
                  '<img src="' + p.img + '" alt="' + p.name + '">' +
                  '<div>' +
                    '<div class="cart-row__title">' + p.name + '</div>' +
                    '<div class="cart-row__meta">' + p.size + ' · ' + chf(p.price) + '</div>' +
                    '<div class="qty">' +
                      '<button type="button" data-dec="' + slug + '" aria-label="weniger">−</button>' +
                      '<input type="number" min="1" value="' + cart[slug] + '" data-qty="' + slug + '" aria-label="Menge">' +
                      '<button type="button" data-inc="' + slug + '" aria-label="mehr">+</button>' +
                    '</div>' +
                  '</div>' +
                  '<div class="cart-row__right">' +
                    '<span class="price">' + chf(line) + '</span>' +
                    '<button type="button" class="link-remove" data-remove="' + slug + '">entfernen</button>' +
                  '</div>' +
                '</div>';
            }).join("");

            var t = total(cart);
            if (sumItems) sumItems.textContent = chf(t);
            if (sumShip) sumShip.textContent = t > 0 ? (t >= 100 ? "gratis" : chf(8.50)) : chf(0);
            if (sumTotal) sumTotal.textContent = chf(t > 0 && t < 100 ? t + 8.5 : t);
        }

        listEl.addEventListener("click", function (e) {
            var inc = e.target.closest("[data-inc]");
            var dec = e.target.closest("[data-dec]");
            var rem = e.target.closest("[data-remove]");
            var cart = read();
            if (inc) { var s = inc.getAttribute("data-inc"); setQty(s, (cart[s] || 0) + 1); render(); }
            else if (dec) { var d = dec.getAttribute("data-dec"); setQty(d, (cart[d] || 0) - 1); render(); }
            else if (rem) { remove(rem.getAttribute("data-remove")); render(); }
        });
        listEl.addEventListener("change", function (e) {
            var q = e.target.closest("[data-qty]");
            if (q) { setQty(q.getAttribute("data-qty"), parseInt(q.value, 10) || 1); render(); }
        });

        // Bestellung absenden: Inhalt in verstecktes Feld, Korb leeren, dann
        // native Navigation zu danke.html (GET).
        if (orderForm) {
            orderForm.addEventListener("submit", function (e) {
                var cart = read();
                if (Object.keys(cart).length === 0) { e.preventDefault(); return; }
                var name = (orderForm.querySelector('[name="name"]') || {}).value || "";
                var email = (orderForm.querySelector('[name="email"]') || {}).value || "";
                if (name.trim().length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
                    e.preventDefault();
                    var fb = orderForm.querySelector(".form-feedback");
                    if (fb) { fb.textContent = "Bitte Name und gültige E-Mail angeben."; fb.className = "form-feedback is-err"; }
                    return;
                }
                var summary = Object.keys(cart).map(function (s) {
                    var p = PRODUCTS[s]; return cart[s] + "× " + (p ? p.name : s);
                }).join(", ");
                var hidden = orderForm.querySelector('[name="bestellung"]');
                if (hidden) hidden.value = summary + " | Total " + chf(total(cart));
                localStorage.removeItem(KEY); // Korb leeren
                // native Submit folgt -> danke.html
            });
        }

        render();
    }

    updateBadge();
})();
