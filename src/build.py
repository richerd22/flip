#!/usr/bin/env python3
"""Build flip.cold.fyi - The Flip, a cited field guide to music sampling.

    python3 build.py            # writes the site to OUT
    STRICT=1 python3 build.py   # also fails on [[GAP:]] markers or unknown footnote keys

Inputs (R = the report folder):
  R/parts/NN-slug.md     one section each, starting "## Title"; footnotes as [^key]
  R/frag/*-sources.tsv   key <TAB> Publisher: Title <TAB> URL
  R/frag/*-glossary.json, *-timeline.json, *-faq.json, *-resources.json
  R/frag/*-breaks.json   {name, artist, year, player, what, used_by, count, paid, source_url}
  R/frag/*-cases.json    {case, court, year, place, about, holding, effect, source_url}
  R/frag/*-machines.json {name, maker, year, price, bits, time, known_for, source_url}
  R/quiz.json, R/seo.json, R/gaps.json, R/corrections.json (optional)
Outputs: hub, one page per section, /all/, /crate/, /docket/, /rack/, /glossary/, /sources/, /corrections/, 404,
sitemap.xml, robots.txt, llms.txt, CNAME, favicon, and JSON copies of every dataset (AX).
"""
import glob, html, json, os, re, sys, datetime
import markdown
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_pixel  # noqa: E402
META_PIXEL = "2368576097306858"  # cold.fyi Deep Dives pixel; footer note links thirdpolararch.com/privacy

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get("FLIP_REPORT", "/home/claude/reports/flip")
OUT = os.environ.get("FLIP_OUT", "/home/claude/flip")
DOMAIN = "flip.cold.fyi"
SITE = f"https://{DOMAIN}"
NAME = "The Flip"
NO = 11
PUBLISHED = "2026-11-19"
STRICT = os.environ.get("STRICT") == "1"
E = lambda s: html.escape(str(s), quote=True)


def J(p, default=None):
    p = os.path.join(R, p)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


# ------------------------------------------------------------ sources
src, clash = {}, []
for f in sorted(glob.glob(f"{R}/frag/*-sources.tsv")):
    for ln in open(f, encoding="utf-8"):
        parts = ln.rstrip("\n").split("\t")
        if len(parts) < 3 or not parts[0].strip():
            continue
        k, t, u = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if k in src and src[k][1] != u:
            clash.append(k)
        src.setdefault(k, (t, u))


def jl(pattern):
    out = []
    for f in sorted(glob.glob(f"{R}/frag/{pattern}")):
        try:
            out += json.load(open(f, encoding="utf-8"))
        except Exception as ex:
            sys.exit(f"bad json {f}: {ex}")
    return out


glossary = sorted({g["term"].lower(): g for g in jl("*-glossary.json")}.values(), key=lambda g: g["term"].lower())
timeline = sorted(jl("*-timeline.json"), key=lambda t: str(t.get("date", "")))
resources = jl("*-resources.json")
breaks = jl("*-breaks.json")
cases = sorted(jl("*-cases.json"), key=lambda r: str(r.get("year") or "9999"))
machines = sorted(jl("*-machines.json"), key=lambda r: str(r.get("year") or "9999"))
quiz = J("quiz.json", [])
seo = J("seo.json", {})
gaps = J("gaps.json", [])
corrections = J("corrections.json", [])

# ------------------------------------------------------------ parts
parts = sorted(glob.glob(f"{R}/parts/*.md"))
lede_md = open(parts[0], encoding="utf-8").read()
sections = []
for p in parts[1:]:
    md = open(p, encoding="utf-8").read()
    md = re.sub(r"^\[\[DIAGRAM-IDEA:.*?\]\]\s*$", "", md, flags=re.M)
    md = re.sub(r"^\[\^[^\]]+\]:.*$", "", md, flags=re.M)
    m = re.match(r"\s*##\s+(.+)", md)
    if not m:
        sys.exit(f"{p}: must start with '## Title'")
    slug = re.sub(r"^\d+-", "", os.path.basename(p)[:-3])
    sections.append({"slug": slug, "title": m.group(1).strip(), "md": md[m.end():].strip(), "file": os.path.basename(p)})
SLUGS = [s["slug"] for s in sections]
faq_by_slug = {}
for f in sorted(glob.glob(f"{R}/frag/*-faq.json")):
    for x in json.load(open(f, encoding="utf-8")):
        if x.get("section"):
            faq_by_slug.setdefault(x["section"], []).append(x)

# ------------------------------------------------------------ footnotes: numbered globally by first use
order, missing = {}, set()


def num(k):
    if k not in src:
        missing.add(k)
        return None
    u = src[k][1]
    if u not in order:
        order[u] = (len(order) + 1, k)
    return order[u][0]


def footnotes(md, page_refs):
    def rep(m):
        n = num(m.group(1))
        if n is None:
            return ""
        page_refs.add(n)
        return f'<sup class="fn"><a href="#src-{n}" data-n="{n}">{n}</a></sup>'
    return re.sub(r"\[\^([A-Za-z0-9_.:-]+)\]", rep, md)


MDX = markdown.Markdown(extensions=["tables", "sane_lists", "attr_list"])


def mdhtml(s):
    MDX.reset()
    return MDX.convert(s)


def heading_ids(h):
    used = set()

    def rep(m):
        lvl, txt = m.group(1), m.group(2)
        base = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", txt).lower()).strip("-")[:70] or "h"
        sid, i = base, 2
        while sid in used:
            sid, i = f"{base}-{i}", i + 1
        used.add(sid)
        return f'<h{lvl} id="{sid}">{txt}<a class="anchor" href="#{sid}" aria-label="Link to this">#</a></h{lvl}>'
    return re.sub(r"<h([34])>(.*?)</h\1>", rep, h)


SHORT_RE = re.compile(r"^\*\*The short version:\*\*\s*(.+?)\n\n", re.S)

# ------------------------------------------------------------ modules
def mod(kicker, title, intro, inner, id_=""):
    return (f'<section class="mod"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="mod-head"><p class="kick">{E(kicker)}</p><h3>{E(title)}</h3>'
            f'{f"<p>{E(intro)}</p>" if intro else ""}</div>{inner}</section>')


def js_json(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")


def srcu(u):
    return f' <a class="s" href="{E(u)}" rel="noopener" target="_blank">source</a>' if u else ""


def _tbl(id_, cols, rows, search, placeholder, chip_attr=None, chip_vals=None):
    chips = ""
    if chip_vals:
        chips = ('<div class="chips" role="group" aria-label="Filter"><button type="button" data-k="" aria-pressed="true">All</button>'
                 + "".join(f'<button type="button" data-k="{E(v)}" aria-pressed="false">{E(v)}</button>' for v in chip_vals) + "</div>")
    return (f'<div class="tools"><label class="sr" for="{id_}-q">Search</label><input id="{id_}-q" type="search" placeholder="{E(placeholder)}" autocomplete="off">{chips}<span class="cnt" id="{id_}-cnt"></span></div>'
            f'<div class="tbl"><table class="dc"><thead><tr>' + "".join(f"<th>{E(c)}</th>" for c in cols) + f'</tr></thead><tbody id="{id_}-list">{rows}</tbody></table></div>')


def m_breaks():
    if not breaks:
        return ""
    rows = "".join(
        f'<tr data-k="" data-s="{E(" ".join(str(r.get(k, "")) for k in ("name", "artist", "player", "used_by", "what")).lower())}"><td class="nm">{E(r.get("name", ""))}<br><span class="ex">{E(r.get("artist", ""))}{", " + E(r["year"]) if r.get("year") else ""}</span></td>'
        f'<td>{E(r.get("what", ""))}' + (f' <span class="ex">Played by {E(r["player"])}.</span>' if r.get("player") else "") + f'{srcu(r.get("source_url"))}</td>'
        f'<td>{E(r.get("used_by", ""))}</td><td>{E(r.get("paid", ""))}</td></tr>' for r in breaks)
    return mod("The crate", f"{len(breaks)} breaks and sources everyone uses", "", _tbl("bk", ["The break", "What gets sampled", "Heard in", "Did the players get paid?"], rows, True, "Amen, Funky Drummer, Apache, Think..."), "breaks")


def m_cases():
    if not cases:
        return ""
    places = []
    for r in cases:
        if r.get("place") and r["place"] not in places:
            places.append(r["place"])
    rows = "".join(
        f'<tr data-k="{E(r.get("place", ""))}" data-s="{E(" ".join(str(r.get(k, "")) for k in ("case", "about", "holding", "court")).lower())}"><td class="nm">{E(r.get("case", ""))}<br><span class="ex">{E(r.get("court", ""))}, {E(r.get("year", ""))}</span></td>'
        f'<td>{E(r.get("about", ""))}</td><td>{E(r.get("holding", ""))}{srcu(r.get("source_url"))}</td><td>{E(r.get("effect", ""))}</td></tr>' for r in cases)
    return mod("The docket", f"{len(cases)} cases that set the rules", "General information, not legal advice.", _tbl("cs", ["Case", "The sample", "What the court said", "What changed"], rows, True, "Bridgeport, Biz Markie, Kraftwerk, de minimis...", "k", places), "cases")


def m_machines():
    if not machines:
        return ""
    rows = "".join(
        f'<tr data-k="" data-s="{E(" ".join(str(r.get(k, "")) for k in ("name", "maker", "known_for")).lower())}"><td class="nm">{E(r.get("name", ""))}<br><span class="ex">{E(r.get("maker", ""))}{", " + E(r["year"]) if r.get("year") else ""}</span></td>'
        f'<td class="k">{E(r.get("bits", ""))}</td><td class="k">{E(r.get("time", ""))}</td><td class="k">{E(r.get("price", ""))}</td><td>{E(r.get("known_for", ""))}{srcu(r.get("source_url"))}</td></tr>' for r in machines)
    return mod("The rack", f"{len(machines)} samplers, by year", "", _tbl("mc", ["Machine", "Resolution", "Sample time", "Launch price", "Known for"], rows, True, "SP-1200, MPC60, Fairlight, SP-404..."), "machines")


def m_timeline():
    eras = []
    for t in timeline:
        if t.get("era") and t["era"] not in eras:
            eras.append(t["era"])
    items = "".join(f'<li data-era="{E(t.get("era", ""))}"><span class="d">{E(t["date"])}</span><b>{E(t["label"])}</b> {E(t.get("detail", ""))}{srcu(t.get("source_url"))}</li>' for t in timeline)
    seg = '<div class="chips" role="group" aria-label="Era"><button type="button" data-era="" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-era="{E(x)}" aria-pressed="false">{E(x)}</button>' for x in eras) + "</div>"
    return mod("Timeline", f"{len(timeline)} dates, tape splice to stem split", "", seg + f'<ol class="tl" id="tl-list">{items}</ol>', "timeline")


def m_glossary():
    items = "".join(f'<li id="term-{E(re.sub(r"[^a-z0-9]+", "-", g["term"].lower()).strip("-"))}" data-s="{E((g["term"] + " " + g.get("definition", "")).lower())}"><dfn>{E(g["term"])}</dfn> {E(g.get("definition", ""))}'
                    + (f' <a class="s" href="/{E(g["section"])}/">read more</a>' if g.get("section") in SLUGS else "") + "</li>" for g in glossary)
    return mod("Glossary", f"{len(glossary)} terms of art", "", f'<div class="tools"><label class="sr" for="gl-q">Search the glossary</label><input id="gl-q" type="search" placeholder="chop, interpolation, de minimis, master..." autocomplete="off"></div><ul class="gl" id="gl-list">{items}</ul>', "glossary")


def m_resources():
    items = "".join(f'<li><a href="{E(r["url"])}" rel="noopener" target="_blank">{E(r["title"])}</a> - {E(r.get("why", ""))}</li>' for r in resources)
    return mod("Further", "Where to go next", "", f'<ul class="res">{items}</ul>', "resources")


def m_quiz():
    if not quiz:
        return ""
    return mod("Test yourself", f"{len(quiz)} questions", "", f'<div id="quiz"></div><script type="application/json" id="quiz-data">{js_json(quiz)}</script>', "quiz")


def m_gaps():
    items = "".join(f"<li>{E(g)}</li>" for g in gaps) or "<li>None listed.</li>"
    return mod("Still unconfirmed", f"{len(gaps)} open questions", "Know the answer? hello@thirdpolararch.com", f"<ul>{items}</ul>", "gaps")


MODULES = {"breaks": m_breaks, "cases": m_cases, "machines": m_machines, "timeline": m_timeline, "glossary": m_glossary, "resources": m_resources, "quiz": m_quiz, "gaps": m_gaps}


def modules(h):
    def rep(m):
        k = m.group(1).strip()
        if k not in MODULES:
            sys.exit(f"unknown module {k}")
        return MODULES[k]()
    h = re.sub(r"<p>\[\[MODULE:([a-z]+)\]\]</p>", rep, h)
    return re.sub(r"\[\[MODULE:([a-z]+)\]\]", rep, h)


# ------------------------------------------------------------ render sections
gap_left = []
for s in sections:
    refs = set()
    md = s["md"]
    m = SHORT_RE.match(md + "\n\n")
    s["short"] = re.sub(r"\[\^[^\]]+\]", "", m.group(1)).strip() if m else ""
    for g in re.findall(r"\[\[GAP:(.*?)\]\]", md):
        gap_left.append((s["slug"], g))
    md = re.sub(r"^\[\[GAP:.*?\]\]\s*$", "", md, flags=re.M)
    md = footnotes(md, refs)
    h = mdhtml(md)
    h = h.replace("<p><strong>The short version:</strong>", '<p class="short"><strong>The short version:</strong>', 1)
    h = heading_ids(h)
    h = modules(h)
    s["html"], s["refs"] = h, sorted(refs)
    s["words"] = len(re.sub(r"<[^>]+>", " ", h).split())
    s["mins"] = max(1, round(s["words"] / 230))
    s["h3"] = re.findall(r'<h3 id="([^"]+)">(.*?)<a class="anchor"', h)
lede_refs = set()
lede_md = footnotes(re.sub(r"^#\s+.*\n", "", lede_md, count=1), lede_refs)
lede_html = modules(mdhtml(lede_md))
if missing:
    msg = "unknown footnote keys: " + ", ".join(sorted(missing))
    if STRICT:
        sys.exit(msg)
    print("WARN", msg)
if gap_left and STRICT:
    sys.exit("GAP markers left: " + "; ".join(f"{a}: {b}" for a, b in gap_left))
nsrc = {n: (k, src[k]) for u, (n, k) in order.items()}
WORDS = sum(s["words"] for s in sections) + len(re.sub(r"<[^>]+>", " ", lede_html).split())

# ------------------------------------------------------------ shell
CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()
FONTS = [("Archivo", 900, "italic", "archivo-latin-900-italic"), ("Source Serif 4", 400, "normal", "source-serif-4-latin-400-normal"),
         ("Source Serif 4", 400, "italic", "source-serif-4-latin-400-italic"), ("Source Serif 4", 600, "normal", "source-serif-4-latin-600-normal"),
         ("IBM Plex Mono", 400, "normal", "ibm-plex-mono-latin-400-normal"), ("IBM Plex Mono", 600, "normal", "ibm-plex-mono-latin-600-normal"),
         ("Silkscreen", 400, "normal", "silkscreen-latin-400-normal")]
FONT_CSS = "".join(f"@font-face{{font-family:'{f}';font-style:{st};font-weight:{w};font-display:swap;src:url(/fonts/{fn}.woff2) format('woff2')}}" for f, w, st, fn in FONTS)
STAMP = datetime.date.fromisoformat(os.environ.get("FLIP_UPDATED", PUBLISHED))
UPDATED = STAMP.strftime("%B %Y")


DB_PADS = [("crate", "Crate", "The crate"), ("docket", "Docket", "The docket"), ("rack", "Rack", "The rack"), ("glossary", "Terms", "Glossary"), ("all", "All", "Everything on one page")]


def pad_label(s):
    return {"what-sampling-is": "Basics", "history": "History", "machines": "Machines", "breaks": "Breaks", "making-a-flip": "The flip", "law": "Law", "clearing": "Clearing",
            "money": "Money", "world": "World", "ai": "AI", "next": "Quiz"}.get(s["slug"], s["slug"].replace("-", " ")[:9])


def waveform(n=96, chops=8, seed=7):
    """A sample drawn in code: a waveform with chop markers, the way a sampler screen shows a break."""
    import random
    rnd = random.Random(seed)
    bars, env = [], 0.0
    for i in range(n):
        hit = i % (n // chops) == 0
        env = 1.0 if hit else env * rnd.uniform(.78, .93)
        h = max(2, env * rnd.uniform(.55, 1) * 30)
        bars.append(f'<rect x="{i * 4 + 1}" y="{32 - h:.1f}" width="2.4" height="{2 * h:.1f}"/>')
    marks = "".join(f'<line x1="{k * (n // chops) * 4}" y1="0" x2="{k * (n // chops) * 4}" y2="64"/><text x="{k * (n // chops) * 4 + 3}" y="8">{k + 1}</text>' for k in range(chops))
    return f'<svg class="wave" viewBox="0 0 {n * 4} 64" preserveAspectRatio="none" role="img" aria-label="A drum break on a sampler screen, cut into {chops} slices"><g class="bars">{"".join(bars)}</g><g class="marks">{marks}</g></svg>'


def machine():
    """The hub's sampler: an LCD with a chopped break and sixteen pads that are the table of contents."""
    pads = [(f"/{s['slug']}/", pad_label(s), s["title"]) for s in sections][:12]
    for slug, lab, title in DB_PADS:
        if len(pads) < 16:
            pads.append((f"/{slug}/", lab, title))
    pads = pads[:16]
    ph = "".join(f'<a class="pad" href="{E(u)}" data-t="{E(t)}"><span class="pnum">PAD {i:02d}</span><b>{E(l)}</b></a>' for i, (u, l, t) in enumerate(pads, 1))
    return (f'<div class="mpc"><div class="mpc-top"><span class="brand">FLIP<i>60</i></span><span class="model">sampling field guide · 16 pads</span></div>'
            f'<div class="lcd"><div class="lcd-row"><span>SEQ 01</span><span id="lcd-t">AMEN, BROTHER</span><span>BAR 1-4</span></div>{waveform()}'
            f'<div class="lcd-row sm"><span>{WORDS:,} WORDS</span><span>{len(nsrc)} SOURCES</span><span>CHOP 8</span></div></div>'
            f'<nav class="pads" aria-label="Sections">{ph}</nav></div>')


def head(title, desc, path, ld=None, robots="index, follow, max-image-preview:large"):
    canon = SITE + path
    lds = "".join(f'<script type="application/ld+json">{js_json(x)}</script>' for x in (ld or []))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="{robots}">
<meta name="theme-color" content="#1e2024"><meta property="og:type" content="article"><meta property="og:site_name" content="cold.fyi">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
<link rel="preload" href="/fonts/archivo-latin-900-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/source-serif-4-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>try{{var t=localStorage.getItem('flip-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{lds}<style>{FONT_CSS}{CSS}</style></head><body><a class="skip" href="#main">Skip to the text</a><div class="progress" id="progress" aria-hidden="true"></div>
<header class="mast"><span><a href="https://cold.fyi">cold.fyi</a><span class="sep">/</span><a href="/">{NAME}</a></span><button class="theme-btn" id="theme-btn" type="button">Night</button></header>
"""


SISTERS = [("groove", "The Groove", "how a vinyl record is made"), ("radiowheel", "The Radio Wheel", "every GTA radio station, song and talk show"), ("polo", "Polo", "how Coachella works"), ("wristband", "The Wristband", "how music festivals work"), ("lastcall", "Last Call", "how nightlife works"),
           ("noise", "The Noise", "every sound in a city"), ("showfile", "The Show File", "how a dance music show is made"),
           ("tickets", "The Ticket", "how a concert ticket gets from artist to fan"), ("airwaves", "The Airwaves", "every radio signal over a city"),
           ("streetcode", "Street Code", "every mark on the street"), ("works", "How a City Works", "the systems under every street"),
           ("penamnesty", "The Pens Went Away", "pharma swag")]


def foot():
    sis = "".join(f'<li><a href="https://{h}.cold.fyi/">{E(n)}</a> <span>- {E(d)}</span></li>' for h, n, d in SISTERS)
    return f"""<footer class="foot"><div class="foot-in"><p class="k">More deep dives from cold.fyi</p><ul class="sis">{sis}</ul>
<p>made with &lt;3 in boston · <a href="https://thirdpolararch.com">Third Polar Arch</a> · Independent. Not affiliated with any artist, label, publisher, manufacturer or service named here. General information, not legal advice.
<a href="/corrections/">Corrections</a> · <a href="/sources/">All {len(nsrc)} sources</a> · <a href="/llms.txt">llms.txt</a> · <a href="mailto:hello@thirdpolararch.com?subject=flip.cold.fyi">hello@thirdpolararch.com</a></p></div></footer>
<script>{JS}</script></body></html>
"""


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items, 1)]}


def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in qas]}


def article_ld(title, desc, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "url": SITE + path, "inLanguage": "en",
            "datePublished": PUBLISHED, "dateModified": STAMP.isoformat(), "image": SITE + "/og.png",
            "author": {"@type": "Organization", "name": "Third Polar Arch", "url": "https://thirdpolararch.com"},
            "publisher": {"@type": "Organization", "name": "Third Polar Arch", "url": "https://thirdpolararch.com"},
            "isPartOf": {"@type": "CreativeWork", "name": f"{NAME}: how sampling works", "url": SITE + "/"}}


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p) or OUT, exist_ok=True)
    if str(rel).endswith(".html"):
        text = meta_pixel.inject(text, META_PIXEL)[0]
    open(p, "w", encoding="utf-8").write(text)


def refs_list(nums, title="Sources for this pad"):
    if not nums:
        return ""
    li = "".join(f'<li id="src-{n}" value="{n}"><a href="{E(nsrc[n][1][1])}" rel="noopener" target="_blank">{E(nsrc[n][1][0])}</a></li>' for n in nums)
    return f'<section class="refs"><h2>{E(title)}</h2><ol>{li}</ol></section>'


def tracklist(active=None):
    items = "".join(f'<li><a href="/{s["slug"]}/"{" aria-current=page class=on" if s["slug"] == active else ""}><span class="tn">{i:02d}</span><span class="tt">{E(s["title"])}</span><span class="td">{s["mins"]} min</span></a></li>' for i, s in enumerate(sections, 1))
    db = "".join(f'<li><a href="/{slug}/"><span class="tn">DB</span><span class="tt">{E(title)}</span><span class="td"></span></a></li>' for slug, lab, title in DB_PADS)
    return f'<nav class="tracks" aria-label="Sections"><p class="sl">Program A</p><ol>{items}{db}</ol></nav>'


# ------------------------------------------------------------ pages
def section_page(i, s):
    prev_s = sections[i - 1] if i else None
    next_s = sections[i + 1] if i + 1 < len(sections) else None
    qas = faq_by_slug.get(s["slug"], [])[:6]
    qa_html = ('<section class="qa"><h2>Quick answers</h2><dl>' + "".join(f'<dt>{E(q["q"])}</dt><dd>{E(q["a"])}</dd>' for q in qas) + "</dl></section>") if qas else ""
    toc = ("<nav class=\"intoc\" aria-label=\"On this page\"><p class=\"k\">On this pad</p><ol>" + "".join(f'<li><a href="#{a}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for a, t in s["h3"]) + "</ol></nav>") if len(s["h3"]) > 3 else ""
    pn = ('<nav class="pn">' + (f'<a href="/{prev_s["slug"]}/"><span>Previous pad</span>{E(prev_s["title"])}</a>' if prev_s else '<span></span>')
          + (f'<a class="nx" href="/{next_s["slug"]}/"><span>Next pad</span>{E(next_s["title"])}</a>' if next_s else '<a class="nx" href="/"><span>Back to</span>The front page</a>') + "</nav>")
    desc = s["short"][:300] or f"{s['title']} - from {NAME}, a cited field guide to music sampling."
    ld = [article_ld(s["title"], desc, f"/{s['slug']}/"), crumbs([(NAME, "/"), (s["title"], f"/{s['slug']}/")])] + ([faq_ld(qas)] if qas else [])
    body = f"""<div class="layout">{tracklist(s['slug'])}<main class="col" id="main">
<p class="readmeta"><span class="tn">PAD {i + 1:02d}</span> · about {s['mins']} min · updated {UPDATED}</p>
<h1>{E(s['title'])}</h1>
{toc}
<article>{s['html']}</article>
{qa_html}
<p class="fix"><a href="mailto:hello@thirdpolararch.com?subject=flip.cold.fyi%20-%20{E(s['slug'])}">Spot a mistake? Tell us.</a></p>
{pn}
{refs_list(s['refs'])}
</main></div>"""
    write(f"{s['slug']}/index.html", head(f"{s['title']} | {NAME}", desc, f"/{s['slug']}/", ld) + body + foot())


def hub():
    t = seo.get("title", f"{NAME}: how sampling works")
    d = seo.get("description", "")
    stats = (f'<p class="stats"><b>{WORDS:,}</b> words · <b>{len(sections)}</b> sections · <b>{len(nsrc)}</b> sources' + (f' · <b>{len(breaks)}</b> breaks' if breaks else "")
             + (f' · <b>{len(cases)}</b> cases' if cases else "") + (f' · <b>{len(machines)}</b> machines' if machines else "") + f' · updated {UPDATED}</p>')
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/", "description": d, "inLanguage": "en",
           "publisher": {"@type": "Organization", "name": "Third Polar Arch", "url": "https://thirdpolararch.com"}},
          article_ld(t, d, "/")] + ([faq_ld(seo["faq"])] if seo.get("faq") else [])
    paths = seo.get("paths", [])
    ph = ""
    if paths:
        ph = '<section class="paths"><h2>Pick your bank</h2><div class="pgrid">' + "".join(
            f'<div class="path"><p class="k">{E(p["who"])}</p><b>{E(p["title"])}</b><p>{E(p["blurb"])}</p>' + " ".join(f'<a href="/{x}/">{E(next((s["title"] for s in sections if s["slug"] == x), x))}</a>' for x in p["slugs"]) + "</div>" for p in paths) + "</div></section>"
    body = f"""<main id="main" class="hub">
<section class="hero"><div class="hero-in"><div class="hero-t"><p class="kicker">cold.fyi deep dive No. {NO} · an independent guide</p><h1 class="title">The <span>Flip</span></h1>
<p class="dek">How sampling works: the breaks everyone uses, the machines, the lawsuits, and what it costs to clear one.</p>{stats}
<div class="cta"><a class="primary" href="/{sections[0]['slug']}/">Start at pad 01</a><a href="/crate/">Dig the crate</a><a href="/docket/">Read the docket</a></div></div>
<div class="hero-v">{machine()}</div></div></section>
<section class="lede col">{lede_html}</section>
<section class="back">{tracklist()}</section>
{ph}
</main>"""
    write("index.html", head(t, d, "/", ld) + body + foot())


def all_page():
    allh = "".join(f'<section id="{s["slug"]}" class="allsec"><p class="readmeta">Pad {i + 1:02d}</p><h1>{E(s["title"])}</h1>{s["html"]}</section>' for i, s in enumerate(sections))
    refs = refs_list(sorted(nsrc), "Every source")
    write("all/index.html", head(f"Everything on one page | {NAME}", "The whole field guide to sampling on one page, with every source.", "/all/") +
          f'<div class="layout">{tracklist()}<main class="col" id="main"><h1>Everything on one page</h1><div class="lede">{lede_html}</div>{allh}{refs}</main></div>' + foot())


def simple(path, title, desc, inner, ld=None):
    write(path.strip("/") + "/index.html" if path != "/404.html" else "404.html",
          head(f"{title} | {NAME}", desc, path, ld, "noindex" if path == "/404.html" else "index, follow, max-image-preview:large") +
          f'<div class="layout">{tracklist()}<main class="col" id="main"><h1>{E(title)}</h1>{inner}</main></div>' + foot())


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, s in enumerate(sections):
        section_page(i, s)
    hub()
    all_page()
    def ds(name, desc, path, file):
        return [{"@context": "https://schema.org", "@type": "Dataset", "name": name, "description": desc, "url": SITE + path, "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True,
                 "creator": {"@type": "Organization", "name": "Third Polar Arch"}, "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": SITE + file}]},
                crumbs([(NAME, "/"), (name, path)])]
    if True:
        simple("/crate/", "The most sampled breaks, and who played them", f"{len(breaks)} drum breaks and sources that sampling is built on: who played them, what gets lifted, where you have heard them, and whether the players were paid.",
               m_breaks() + '<p>The stories behind them are in <a href="/breaks/">the breaks section</a>.</p>', ds("The most sampled breaks", "Drum breaks and other sources sampled again and again, each with a source.", "/crate/", "/breaks.json"))
    if True:
        simple("/docket/", "Sampling lawsuits: the cases that set the rules", f"{len(cases)} court decisions on music sampling from the US, UK and EU: what was sampled, what the court said and what changed.",
               m_cases() + '<p>What they add up to is in <a href="/law/">the law section</a>.</p>', ds("Sampling court cases", "Court decisions on music sampling, each with a source. General information, not legal advice.", "/docket/", "/cases.json"))
    if True:
        simple("/rack/", "Every classic sampler, by year", f"{len(machines)} samplers from the Fairlight to the SP-404: year, resolution, sample time, launch price and what each is known for.",
               m_machines() + '<p>How they work and who used them is in <a href="/machines/">the machines section</a>.</p>', ds("Classic samplers", "Hardware and software samplers with year, resolution, sample time and launch price, each with a source.", "/rack/", "/machines.json"))
    simple("/glossary/", "Glossary of sampling terms", f"{len(glossary)} sampling terms in plain words: chop, flip, interpolation, master, publishing, de minimis and more.", m_glossary(), [crumbs([(NAME, "/"), ("Glossary", "/glossary/")])])
    simple("/sources/", "Every source", "Every source behind the guide, numbered.", refs_list(sorted(nsrc), f"{len(nsrc)} sources"))
    cl = "".join(f"<li><b>{E(c['date'])}</b> · <a href=\"/{E(c['section'])}/\">{E(c['section'])}</a>: {E(c['what'])}</li>" for c in corrections) or "<li>None yet.</li>"
    simple("/corrections/", "Corrections and updates", "Every correction to a fact, dated.", f'<p>Every fix to a fact, dated. To report one: <a href="mailto:hello@thirdpolararch.com?subject=flip.cold.fyi%20correction">hello@thirdpolararch.com</a>.</p><ul>{cl}</ul>')
    simple("/404.html", "No sample loaded", "Page not found.", '<p>That pad is empty. <a href="/">Back to the front page</a>.</p>')
    # data
    write("sections.json", json.dumps([{"n": i + 1, "slug": s["slug"], "title": s["title"], "short": s["short"], "url": f"{SITE}/{s['slug']}/", "words": s["words"], "sources": s["refs"]} for i, s in enumerate(sections)], indent=1, ensure_ascii=False))
    write("sources.json", json.dumps([{"n": n, "key": k, "title": t, "url": u} for n, (k, (t, u)) in sorted(nsrc.items())], indent=1, ensure_ascii=False))
    for nm, data in (("breaks.json", breaks), ("cases.json", cases), ("machines.json", machines)):
        write(nm, json.dumps(data, indent=1, ensure_ascii=False))
    write("glossary.json", json.dumps(glossary, indent=1, ensure_ascii=False))
    write("timeline.json", json.dumps(timeline, indent=1, ensure_ascii=False))
    urls = ["/", "/all/"] + ["/crate/", "/docket/", "/rack/"] + ["/glossary/", "/sources/", "/corrections/"] + [f"/{s['slug']}/" for s in sections]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{STAMP.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = [f"# {seo.get('title', NAME)}", "", f"> {seo.get('description', '')}", "",
            f"Independent cited field guide, {WORDS:,} words, {len(nsrc)} sources, updated {UPDATED}. Not affiliated with any artist, label, publisher, manufacturer or service. General information, not legal advice.", "", "## Sections"]
    llms += [f"- [{s['title']}]({SITE}/{s['slug']}/): {s['short']}" for s in sections]
    llms += ["", "## Tools and data", f"- Breaks: {SITE}/crate/ (data {SITE}/breaks.json) · Cases: {SITE}/docket/ (data {SITE}/cases.json) · Machines: {SITE}/rack/ (data {SITE}/machines.json)", f"- Glossary: {SITE}/glossary/ (data {SITE}/glossary.json)",
             f"- {SITE}/sections.json, {SITE}/sources.json, {SITE}/timeline.json", f"- Everything on one page: {SITE}/all/", "",
             "## Sister guides"] + [f"- https://{h}.cold.fyi/ - {n}: {d}" for h, n, d in SISTERS]
    write("llms.txt", "\n".join(llms) + "\n")
    write("CNAME", DOMAIN + "\n")
    write(".nojekyll", "")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1e2024"/>' + "".join(f'<rect x="{9 + c * 12}" y="{9 + r * 12}" width="10" height="10" rx="2" fill="{"#e23a2c" if (r, c) == (1, 2) else "#8b8e96"}"/>' for r in range(4) for c in range(4)) + "</svg>")
    os.makedirs(f"{OUT}/fonts", exist_ok=True)
    for f in glob.glob(f"{HERE}/fonts/*.woff2"):
        open(f"{OUT}/fonts/{os.path.basename(f)}", "wb").write(open(f, "rb").read())
    print(f"built: {WORDS:,} words, {len(sections)} sections, {len(nsrc)} refs, {len(glossary)} terms, {len(breaks)} breaks, {len(cases)} cases, {len(machines)} machines, {len(timeline)} dates"
          + (f", {len(gap_left)} GAP left" if gap_left else "") + (f", clashes {clash}" if clash else ""))


main()
