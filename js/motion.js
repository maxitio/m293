/* =========================================================================
   HELIX PEPTIDES – motion.js
   Bewegungssystem der Seite ("Lab instrument readout, committed"):
     1. Header-Zustand beim Scrollen
     2. Hero-Entrance-Choreografie (Web Animations API)
     3. Molekül-Netzwerk-Canvas im Hero (Peptidketten-Metapher)
     4. Hero-Parallax beim Scrollen
     5. Scroll-Reveals via IntersectionObserver + WAAPI
     6. "Instrument-Readout"-Scramble für Mono-Datenwerte
     7. Pointer-Glow auf Produktkarten/Kategorie-Kacheln

   Grundsätze: Inhalt ist IMMER ohne JS sichtbar (WAAPI statt CSS-Gating).
   Reveals starten BEVOR ein Element sichtbar wird (positiver rootMargin)
   und sind kurz – nichts wartet, nichts "erscheint mit Verspätung".
   Alles respektiert prefers-reduced-motion; Canvas pausiert ausserhalb
   des Viewports und in versteckten Tabs.
   ========================================================================= */
(function () {
    "use strict";

    var REDUCE = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var WAAPI = typeof Element !== "undefined" && "animate" in Element.prototype;
    var EASE = "cubic-bezier(.16, 1, .3, 1)"; /* ease-out-expo */

    /* ---------- 1. Header-Zustand ---------- */
    var header = document.querySelector(".site-header");
    if (header) {
        var onHeaderScroll = function () {
            header.classList.toggle("is-scrolled", window.scrollY > 8);
        };
        window.addEventListener("scroll", onHeaderScroll, { passive: true });
        onHeaderScroll();
    }

    /* ---------- 2. Hero-Entrance ----------
       Kurz und dicht gestaffelt: Gesamtdauer < 0.8 s, erste Elemente
       praktisch sofort da. */
    if (!REDUCE && WAAPI) {
        document.querySelectorAll(".hero [data-reveal]").forEach(function (el, i) {
            el.animate([
                { opacity: 0, transform: "translateY(16px)", filter: "blur(5px)" },
                { opacity: 1, transform: "none", filter: "blur(0px)" }
            ], { duration: 520, delay: 40 + i * 65, easing: EASE, fill: "backwards" });
        });
    }

    /* ---------- 2b. Glassy Orb: statischer Fallback ----------
       Wenn das Video nicht lädt oder Autoplay blockiert ist, zeigt
       .orb--static den CSS-Farbverlaufs-Orb (siehe style.css). */
    var orb = document.querySelector("[data-orb]");
    if (orb) {
        var orbVideo = orb.querySelector("video");
        if (!orbVideo || REDUCE) {
            orb.classList.add("orb--static");
        } else {
            orbVideo.addEventListener("error", function () { orb.classList.add("orb--static"); }, true);
            var playing = orbVideo.play && orbVideo.play();
            if (playing && playing.catch) playing.catch(function () { orb.classList.add("orb--static"); });
        }
    }

    /* ---------- 3. Molekül-Netzwerk-Canvas ---------- */
    var canvas = document.querySelector("[data-molecule-canvas]");
    if (canvas && canvas.getContext) {
        var ctx = canvas.getContext("2d");
        var host = canvas.parentElement;
        var nodes = [];
        var raf = 0;
        var inView = true;
        var W = 0, H = 0, DPR = 1;
        var LINK = 130;                       /* max. Bindungslänge in px */
        var pointer = { x: .5, y: .5, tx: .5, ty: .5 };

        var COLORS = [
            "rgba(25, 227, 196, .9)",         /* Teal vivid  */
            "rgba(25, 227, 196, .55)",
            "rgba(106, 92, 240, .8)",         /* Violett     */
            "rgba(199, 214, 229, .7)"         /* kühles Weiss */
        ];

        function resize() {
            DPR = Math.min(window.devicePixelRatio || 1, 2);
            W = host.clientWidth;
            H = host.clientHeight;
            canvas.width = Math.round(W * DPR);
            canvas.height = Math.round(H * DPR);
            ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
            seed();
        }

        function seed() {
            var count = Math.min(Math.round(W * H / 16000), 95);
            nodes = [];
            for (var i = 0; i < count; i++) {
                nodes.push({
                    x: Math.random() * W,
                    y: Math.random() * H,
                    vx: (Math.random() - .5) * .28,
                    vy: (Math.random() - .5) * .28,
                    r: 1.2 + Math.random() * 1.6,
                    depth: .25 + Math.random() * .75,   /* für Pointer-Parallax */
                    color: COLORS[Math.floor(Math.random() * COLORS.length)]
                });
            }
        }

        function frame() {
            /* Pointer weich nachziehen (Lerp) */
            pointer.x += (pointer.tx - pointer.x) * .04;
            pointer.y += (pointer.ty - pointer.y) * .04;
            var px = (pointer.x - .5) * 26;
            var py = (pointer.y - .5) * 18;

            ctx.clearRect(0, 0, W, H);

            var i, j, n, m;
            for (i = 0; i < nodes.length; i++) {
                n = nodes[i];
                n.x += n.vx; n.y += n.vy;
                if (n.x < -20) n.x = W + 20; else if (n.x > W + 20) n.x = -20;
                if (n.y < -20) n.y = H + 20; else if (n.y > H + 20) n.y = -20;
                n.rx = n.x + px * n.depth;   /* gerenderte Position inkl. Parallax */
                n.ry = n.y + py * n.depth;
            }

            /* Bindungen */
            ctx.lineWidth = 1;
            for (i = 0; i < nodes.length; i++) {
                n = nodes[i];
                for (j = i + 1; j < nodes.length; j++) {
                    m = nodes[j];
                    var dx = n.rx - m.rx, dy = n.ry - m.ry;
                    var d2 = dx * dx + dy * dy;
                    if (d2 > LINK * LINK) continue;
                    var a = (1 - Math.sqrt(d2) / LINK) * .34;
                    ctx.strokeStyle = "rgba(25, 227, 196, " + a.toFixed(3) + ")";
                    ctx.beginPath();
                    ctx.moveTo(n.rx, n.ry);
                    ctx.lineTo(m.rx, m.ry);
                    ctx.stroke();
                }
            }

            /* Atome */
            for (i = 0; i < nodes.length; i++) {
                n = nodes[i];
                ctx.fillStyle = n.color;
                ctx.beginPath();
                ctx.arc(n.rx, n.ry, n.r, 0, 6.2832);
                ctx.fill();
            }
        }

        function loop() {
            frame();
            raf = requestAnimationFrame(loop);
        }
        function start() {
            if (!raf && inView && !document.hidden && !REDUCE) raf = requestAnimationFrame(loop);
        }
        function stop() {
            if (raf) { cancelAnimationFrame(raf); raf = 0; }
        }

        resize();
        if (REDUCE) {
            frame();                          /* ein statisches Bild, keine Bewegung */
        } else {
            window.addEventListener("resize", function () { resize(); frame(); });
            host.addEventListener("pointermove", function (e) {
                var r = host.getBoundingClientRect();
                pointer.tx = (e.clientX - r.left) / r.width;
                pointer.ty = (e.clientY - r.top) / r.height;
            });
            document.addEventListener("visibilitychange", function () {
                if (document.hidden) stop(); else start();
            });
            if ("IntersectionObserver" in window) {
                new IntersectionObserver(function (entries) {
                    inView = entries[0].isIntersecting;
                    if (inView) start(); else stop();
                }).observe(host);
            }
            start();
        }
    }

    /* ---------- 4. Hero-Parallax beim Scrollen (dezent) ---------- */
    var heroGrid = document.querySelector(".hero__grid");
    if (heroGrid && !REDUCE) {
        var heroEl = heroGrid.closest(".hero");
        var ticking = false;
        var onHeroScroll = function () {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () {
                ticking = false;
                var y = window.scrollY;
                var h = heroEl.offsetHeight || 1;
                if (y > h) return;
                heroGrid.style.transform = "translate3d(0," + (y * .12).toFixed(1) + "px,0)";
                heroGrid.style.opacity = Math.max(1 - y / (h * 1.4), .55).toFixed(3);
            });
        };
        window.addEventListener("scroll", onHeroScroll, { passive: true });
    }

    /* ---------- 5. Scroll-Reveals (nur unterhalb des Folds) ----------
       Wichtig gegen "erscheint mit Verspätung": der Observer feuert schon
       12 % UNTERHALB des Viewports (positiver rootMargin). Wenn das Element
       in Sicht kommt, läuft seine kurze Animation bereits. */
    if (!REDUCE && WAAPI && "IntersectionObserver" in window) {
        var candidates = document.querySelectorAll(
            ".section__head, .card-grid > *, .cat-grid > *, .proto__row, " +
            ".team-grid > *, .faq details, .product__specs li, " +
            ".order-box, .contact-grid > *, .step, .coa"
        );
        var below = Array.prototype.filter.call(candidates, function (el) {
            return el.getBoundingClientRect().top > window.innerHeight;
        });
        if (below.length) {
            var io = new IntersectionObserver(function (entries) {
                var batch = 0;
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    io.unobserve(entry.target);
                    entry.target.animate([
                        { opacity: 0, transform: "translateY(14px)" },
                        { opacity: 1, transform: "none" }
                    ], {
                        duration: 440,
                        delay: Math.min(batch * 55, 220),
                        easing: EASE,
                        fill: "backwards"
                    });
                    /* Mono-Datenwerte "messen sich ein" */
                    entry.target.querySelectorAll(".proto__key, .product__specs span").forEach(scramble);
                    batch++;
                });
            }, { threshold: 0, rootMargin: "0px 0px 12% 0px" });
            below.forEach(function (el) { io.observe(el); });
        }
    }

    /* ---------- 6. Instrument-Readout-Scramble ---------- */
    function scramble(el) {
        if (REDUCE || el._scrambled) return;
        el._scrambled = true;
        var final = el.textContent;
        if (!final || final.length > 24) return;
        var glyphs = "0123456789≥%·—/ABCDEFHX";
        var t0 = performance.now();
        var dur = 450;
        (function tick(now) {
            var p = Math.min((now - t0) / dur, 1);
            if (p === 1) { el.textContent = final; return; }
            var settled = Math.floor(final.length * p);
            var out = final.slice(0, settled);
            for (var i = settled; i < final.length; i++) {
                var c = final[i];
                out += (c === " " || c === " ") ? c : glyphs[Math.floor(Math.random() * glyphs.length)];
            }
            el.textContent = out;
            requestAnimationFrame(tick);
        })(t0);
    }

    /* ---------- 7. Pointer-Glow auf Karten ---------- */
    if (window.matchMedia && window.matchMedia("(hover: hover)").matches) {
        document.addEventListener("pointermove", function (e) {
            var card = e.target.closest && e.target.closest(".product-card, .cat-tile");
            if (!card) return;
            var r = card.getBoundingClientRect();
            card.style.setProperty("--mx", (e.clientX - r.left).toFixed(0) + "px");
            card.style.setProperty("--my", (e.clientY - r.top).toFixed(0) + "px");
        }, { passive: true });
    }
})();
