"""Builds index.html and companies/*.html from the data below.

Edit company info in COMPANIES, then run from the project folder:
    python3 tools/build.py
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EVENT = {
    "name": "Techstars Future of Food",
    "eyebrow": "Demo Day · December 2026",
    "headline": "Meet the companies",
    "intro": "Eight startups building the future of food. Tap a logo to meet the founders and learn what they’re working on.",
}

# Leave a field out (or empty) to show a placeholder on the page.
# colors: (brand, dark ink for text/borders, soft tint for backgrounds) — sampled from each logo.
COMPANIES = [
    dict(slug="shelflife", name="ShelfLife", colors=("#D4694B", "#8F3B24", "#FCEEE8")),
    dict(slug="2daloop", name="2DaLoop", colors=("#2E4A9A", "#0B0B3D", "#E9EDF8"),
         about=("Frontline workers shouldn’t have to guess. We started on high-entropy recycling floors — "
                "the hardest visual environment to train on — and we’re expanding the same engine into "
                "retail loss prevention. 2DaLoop is building the visual identification infrastructure for the "
                "physical economy."),
         team=[("George Mitri", "Co-Founder & CEO"), ("Miquel Ortiz", "Co-Founder")],
         email="Info@2Daloop.com"),
    dict(slug="greazly", name="Greazly", colors=("#2B2B2B", "#111111", "#F0EFEC")),
    dict(slug="skyacres", name="SkyAcres", colors=("#5E9443", "#355D22", "#EEF5E8")),
    dict(slug="verde", name="Verde Biomaterials", colors=("#1F4D25", "#122E17", "#E7F0E8")),
    dict(slug="nanofreeze", name="NanoFreeze", colors=("#22385C", "#142338", "#E8EDF4"),
         # Company page uses the exact supplied file (square, lots of empty canvas), shown 3x larger.
         page_logo="home/nanofreeze.png", page_logo_scale=3),
    dict(slug="pinto", name="Pinto Robotics", colors=("#C42020", "#2E2E2E", "#FBEAEA")),
    dict(slug="oscar", name="Oscar", colors=("#1F3F72", "#152C52", "#E6EFF8")),
]

e = html.escape

LINKEDIN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 '
                '2.5 2.5 0 0 1 0-5zM3 9.75h4v11H3zM9.5 9.75h3.8v1.6h.06c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.77 '
                '2.5 4.77 5.75v5.6h-4v-4.96c0-1.18-.02-2.7-1.7-2.7-1.7 0-1.96 1.28-1.96 2.6v5.06h-4z"/></svg>')
MAIL_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" d="M3 6.5h18v11H3zM3.5 7l8.5 6 8.5-6"/></svg>')
ARROW = '<span class="arrow" aria-hidden="true">→</span>'


def head(title, desc, up):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
</head>
"""


def topbar(up, current):
    links = "\n".join(
        f'      <li><a href="{up}companies/{c["slug"]}.html"{" aria-current=" + chr(34) + "page" + chr(34) if c["slug"] == current else ""}>'
        f'<img src="{up}assets/logos/{c["slug"]}.png" alt="">{e(c["name"])}</a></li>'
        for c in COMPANIES)
    home_cur = ' aria-current="page"' if current == "home" else ""
    return f"""<header class="topbar">
  <a class="wordmark" href="{up}index.html">
    <span class="wm-main">techstars<span class="wm-us">_</span></span>
    <span class="wm-sub">Future of Food</span>
  </a>
  <span class="pill">Demo Day</span>
  <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
</header>
<div class="menu-scrim"></div>
<nav class="menu" id="menu" aria-label="Site">
  <div class="menu-head">
    <span class="menu-title">Demo Day</span>
    <button class="close" aria-label="Close menu">&times;</button>
  </div>
  <ul class="menu-home"><li><a href="{up}index.html"{home_cur}>All companies</a></li></ul>
  <p class="menu-label">Companies</p>
  <ul class="menu-list">
{links}
  </ul>
</nav>
"""


def footer(up):
    links = "\n".join(f'        <li><a href="{up}companies/{c["slug"]}.html">{e(c["name"])}</a></li>' for c in COMPANIES)
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="f-brand">techstars<span class="wm-us">_</span> Future of Food</p>
      <p class="f-sub">Demo Day · Powered by Ecolab</p>
    </div>
    <nav aria-label="Companies">
      <ul class="f-links">
{links}
      </ul>
    </nav>
  </div>
</footer>
<script src="{up}menu.js"></script>
</body>
</html>
"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def initials(name):
    return "".join(p[0] for p in name.split()[:2]).upper()


# ---------- Landing page ----------
# Home page logo boxes use the companies' original files exactly as supplied (assets/logos/home/).
HOME_LOGOS = {
    "shelflife": "shelflife.png", "2daloop": "2daloop.png", "greazly": "greazly.png",
    "skyacres": "skyacres.png", "verde": "verde.png", "nanofreeze": "nanofreeze.png",
    "pinto": "pinto.png", "oscar": "oscar.webp",
}
cards = "\n".join(
    f"""    <li class="logo-box logo-{c['slug']}" style="--i:{i}">
      <a href="companies/{c['slug']}.html" style="--brand-soft:{c['colors'][2]}">
        <img src="assets/logos/home/{HOME_LOGOS[c['slug']]}" alt="{e(c['name'])}">
      </a>
    </li>"""
    for i, c in enumerate(COMPANIES))

# Hero: clean photo with the white Techstars / Ecolab lockup on top.
HERO = """  <figure class="hero hero-layered">
    <img class="hero-photo" src="assets/hero-photo.jpg" alt="">
    <img class="hero-lockup" src="assets/hero-lockup.png" alt="Techstars Future of Food, powered by Ecolab">
  </figure>"""

index = head(f"{EVENT['name']} Demo Day", e(EVENT["intro"]), "")
index += '<body class="home">\n' + topbar("", "home")
index += f"""<main>
{HERO}

  <section class="intro wrap">
    <p class="eyebrow">{e(EVENT['eyebrow'])}</p>
    <h1>{e(EVENT['headline'])}</h1>
    <p class="lede">{e(EVENT['intro'])}</p>
  </section>

  <section class="wrap" aria-label="Companies">
    <ul class="logo-grid">
{cards}
    </ul>
  </section>
</main>
"""
index += footer("")
write(os.path.join(ROOT, "index.html"), index)

# ---------- Company pages ----------
for i, c in enumerate(COMPANIES):
    name = e(c["name"])
    up = "../"

    about = (f'<p>{e(c["about"])}</p>' if c.get("about") else
             f'<p class="placeholder">Add a 2–4 sentence description of what {name} does.</p>')

    team = c.get("team") or []
    if team:
        people = "\n".join(
            f"""      <li class="person">
        <span class="avatar" aria-hidden="true">{e(initials(n))}</span>
        <span><span class="p-name">{e(n)}</span><span class="p-role">{e(r)}</span></span>
      </li>""" for n, r in team)
    else:
        people = "\n".join(
            """      <li class="person is-placeholder">
        <span class="avatar" aria-hidden="true">?</span>
        <span><span class="p-name">Founder Name</span><span class="p-role">Title</span></span>
      </li>""" for _ in range(2))

    btns = []
    if c.get("linkedin"):
        btns.append(f'<a class="btn btn-li" href="{e(c["linkedin"])}" target="_blank" rel="noopener">{LINKEDIN_SVG}LinkedIn</a>')
    else:
        btns.append(f'<span class="btn btn-li is-placeholder" title="LinkedIn link coming soon">{LINKEDIN_SVG}LinkedIn</span>')
    if c.get("email"):
        btns.append(f'<a class="btn btn-mail" href="mailto:{e(c["email"])}">{MAIL_SVG}{e(c["email"])}</a>')
    else:
        btns.append(f'<span class="btn btn-mail is-placeholder">{MAIL_SVG}contact@company.com</span>')

    prev_c = COMPANIES[i - 1]
    next_c = COMPANIES[(i + 1) % len(COMPANIES)]

    def pager_card(p, label, cls):
        return (f'<a class="pager-card {cls}" href="{p["slug"]}.html"><span class="pager-label">{label}</span>'
                f'<span class="pager-name">{e(p["name"])}</span></a>')

    if c.get("page_logo"):
        brand_img = (f'<img class="scaled" src="../assets/logos/{c["page_logo"]}" alt="" '
                     f'style="--k:{c.get("page_logo_scale", 1)}">')
    else:
        brand_img = f'<img src="../assets/logos/{c["slug"]}.png" alt="">'

    prev_html = pager_card(prev_c, "← Previous", "prev")
    next_html = pager_card(next_c, "Next →", "next")

    page = head(f"{name} · {EVENT['name']}", f"{name} at {EVENT['name']} Demo Day.", up)
    brand, brand_ink, brand_soft = c["colors"]
    page += (f'<body class="company-page" style="--brand:{brand};--brand-ink:{brand_ink};--brand-soft:{brand_soft}">\n'
             + topbar(up, c["slug"]))
    page += f"""<div class="company-bar">
  <div class="wrap narrow bar-inner">
    <a class="bar-back" href="../index.html"><span aria-hidden="true">←</span> All companies</a>
    <h1 class="bar-name">{name}</h1>
  </div>
</div>
<main>
  <section class="company-hero">
    <div class="wrap narrow">
      <div class="brand-logo" role="img" aria-label="{name} logo">
        {brand_img}
      </div>
    </div>
  </section>

  <div class="wrap narrow company-body">
    <section class="block what">
      <h2>What We Do</h2>
      <div class="what-card">
        {about}
      </div>
    </section>

    <section class="block who">
      <h2>Who We Are</h2>
      <ul class="team">
{people}
      </ul>
    </section>

    <section class="block connect">
      <h2>Connect With Us</h2>
      <div class="btn-row">
        {btns[0]}
        {btns[1]}
      </div>
    </section>

    <nav class="pager" aria-label="More companies">
      {prev_html}
      {next_html}
    </nav>
  </div>
</main>
"""
    page += footer(up)
    write(os.path.join(ROOT, "companies", c["slug"] + ".html"), page)

print("Built index.html and", len(COMPANIES), "company pages")
