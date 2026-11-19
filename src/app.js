(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var all = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };
  var norm = function (s) { return (s || "").normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase(); };
  function readJSON(id) { try { return JSON.parse($(id).textContent); } catch (e) { return null; } }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* theme: system by default, remembered per viewer */
  var tb = $("theme-btn"), root = document.documentElement;
  function isDark() { var t = root.dataset.theme; return t ? t === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches; }
  function label() { if (tb) tb.textContent = isDark() ? "Day" : "Night"; }
  if (tb) { label(); tb.addEventListener("click", function () { var n = isDark() ? "light" : "dark"; root.dataset.theme = n; store("flip-theme", n); label(); }); }

  /* reading progress */
  var pr = $("progress");
  if (pr) window.addEventListener("scroll", function () {
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    pr.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
  }, { passive: true });

  /* footnotes: hover or focus shows the source title */
  all("sup.fn a").forEach(function (a) {
    var li = $("src-" + a.dataset.n); if (li) a.title = li.textContent.trim();
  });

  /* chip groups + search filter helper */
  function filter(input, chipsSel, items, attrS, attrK) {
    var q = $(input), k = "", chips = all(chipsSel);
    function go() {
      var t = norm(q ? q.value.trim() : ""), n = 0;
      items.forEach(function (el) {
        var m = (!t || norm(el.dataset[attrS] || el.textContent).indexOf(t) > -1) && (!k || el.dataset[attrK] === k);
        el.classList.toggle("hide", !m); if (m) n++;
      });
      return n;
    }
    chips.forEach(function (b) { b.addEventListener("click", function () { k = b.dataset[attrK]; chips.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); after(go()); }); });
    var cnt = null, after = function (n) { if (cnt) cnt.textContent = n + " of " + items.length; };
    if (q) q.addEventListener("input", function () { after(go()); });
    return function (c) { cnt = c; after(go()); };
  }
  [["bk", "#breaks"], ["cs", "#cases"], ["mc", "#machines"]].forEach(function (t) {
    var rows = all("#" + t[0] + "-list tr");
    if (rows.length) filter(t[0] + "-q", t[1] + " .chips button", rows, "s", "k")($(t[0] + "-cnt"));
  });
  var gl = all("#gl-list li");
  if (gl.length) filter("gl-q", "#glossary .chips button", gl, "s", "x")(null);
  var tl = all("#tl-list li");
  if (tl.length) filter(null, "#timeline .chips button", tl, "s", "era")(null);

  /* pads: the LCD names the section under your finger */
  var lt = $("lcd-t");
  if (lt) {
    var idle = lt.textContent;
    all(".pads .pad").forEach(function (p) {
      function on() { lt.textContent = p.dataset.t || idle; }
      function off() { lt.textContent = idle; }
      p.addEventListener("mouseenter", on); p.addEventListener("focus", on);
      p.addEventListener("mouseleave", off); p.addEventListener("blur", off);
    });
  }

  /* quiz */
  var qd = readJSON("quiz-data"), qz = $("quiz");
  if (qd && qz) {
    var score = 0, done = 0;
    qd.forEach(function (q, i) {
      var d = document.createElement("div"); d.className = "q";
      d.innerHTML = "<p><b>" + (i + 1) + ".</b> " + q.q.replace(/</g, "&lt;") + "</p>";
      q.options.forEach(function (o, j) {
        var b = document.createElement("button"); b.type = "button"; b.textContent = o;
        b.addEventListener("click", function () {
          if (d.dataset.done) return; d.dataset.done = 1; done++;
          if (j === q.answer) { score++; b.classList.add("right"); } else { b.classList.add("wrong"); d.querySelectorAll("button")[q.answer].classList.add("right"); }
          var w = document.createElement("p"); w.className = "why";
          w.innerHTML = q.why.replace(/</g, "&lt;") + (q.section ? ' <a href="/' + q.section + '/">Read more</a>' : "") + (done === qd.length ? " <b>Score: " + score + " of " + qd.length + ".</b>" : "");
          d.appendChild(w);
        });
        d.appendChild(b);
      });
      qz.appendChild(d);
    });
  }
})();
