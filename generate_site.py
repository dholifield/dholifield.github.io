import frontmatter
import markdown
import glob
import math
import os
import sys
import re
from colorsys import rgb_to_hsv
from datetime import date
from PIL import Image


def rewrite_project_paths(html):
    """Rewrite relative src/href values to be relative to the projects/ folder."""
    def rewrite(m):
        attr, path = m.group(1), m.group(2)
        if re.match(r'https?://|/|#|mailto:', path):
            return m.group(0)
        return f'{attr}="../../content/projects/{path}"'
    return re.sub(r'(src|href)="([^"]*)"', rewrite, html)


def page_head(title, css_path, bg, accent):
    return f"""\
<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css_path}">
<style>:root{{--bg:{bg};--accent:{accent}}}</style>"""


def page_footer(name, year):
    return f'  <footer><p>{name} · {year}</p><a href="https://github.com/dholifield/portfolio-generator">generate</a></footer>'

def color_sort_key(pixels):
    """
    Sort key for color ordering.
    Chromatic images sort first (0, hue), achromatic sort after (1, brightness).
    This keeps B&W/grayscale images grouped at the end rather than
    collapsing them all to position 0 (the red end of the hue wheel).
    """
    sum_x = 0.0
    sum_y = 0.0
    total_weight = 0.0
    total_v = 0.0

    for r, g, b in pixels:
        h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
        total_v += v

        # Ignore near-black pixels
        if v < 0.1 or s < 0.1:
            continue

        # Weight: emphasize bright + saturated colors
        weight = s * (v ** 2)  # v^2 boosts bright pixels strongly

        if weight > 0:
            angle = 2 * math.pi * h
            sum_x += math.cos(angle) * weight
            sum_y += math.sin(angle) * weight
            total_weight += weight

    if total_weight > 0:
        avg_angle = math.atan2(sum_y, sum_x)
        avg_hue = (avg_angle / (2 * math.pi)) % 1.0
        return (0, avg_hue)

    # Achromatic case
    return (1, total_v / len(pixels))

# open profile.md with frontmatter
if not os.path.exists("content/profile.md"):
    raise FileNotFoundError("content/profile.md not found - cannot generate site")
profile = frontmatter.load("content/profile.md")

# look through all .md files in the projects folder
projects = []
for path in glob.glob("content/projects/*.md"):
    project = frontmatter.load(path)
    if "title" not in project or "description" not in project:
        print(f"Warning: skipping {path} (missing title or description)")
        continue
    projects.append((path, project))
projects.sort(key=lambda x: x[1].get("order", 999))

year = date.today().year

# detect optional features
_photo_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
has_photography = os.path.isdir("content/photography") and any(
    os.path.splitext(f)[1].lower() in _photo_exts
    for f in os.listdir("content/photography")
)
has_resume = bool(glob.glob("content/*.pdf"))

if not has_photography:
    print("Note: no photography folder or images found, skipping photography page")
if not has_resume:
    print("Note: no PDF found, skipping resume page")

# clean and set up output directory
for f in glob.glob("site/*.html"):
    os.remove(f)
for f in glob.glob("site/projects/*.html"):
    os.remove(f)
os.makedirs("site/projects", exist_ok=True)

# --- index.html generation ---

print("Generating index.html ... ", end="", flush=True)
if "name" not in profile:
    sys.exit("Error: profile.md is missing required field 'name'")
if "bio" not in profile:
    sys.exit("Error: profile.md is missing required field 'bio'")
name = profile["name"]
bio = profile["bio"].strip()
portrait = profile.get("portrait")
bg = profile.get("background") or "f7f7f2"
accent = profile.get("accent") or "899878"
bg = bg if bg.startswith("#") else f"#{bg}"
accent = accent if accent.startswith("#") else f"#{accent}"
section_label = profile.get("section", "Projects")

INDEX_TEMPLATE = """\
{head}

<body style="max-width:600px">
  <header>
    <h1>{name}</h1>
    <nav>
{nav_links}
    </nav>
  </header>

  <main>
    <div class="intro">
{portrait_img}
      <p>{bio}</p>
    </div>

{skills_section}
{links_section}
    <hr>

    <h2>{section_label}</h2>
    <ul class="projects">
{project_items}
    </ul>
  </main>

{footer}
</body>
"""


def build_project_item(slug, project):
    """Build a single <li> for the project list on the index page."""
    title = project["title"]
    desc = project["description"].strip()

    thumbnail = project.get("thumbnail")
    thumbnail_alt = project.get("thumbnail_alt", title)
    thumbnail_class = project.get("thumbnail_class")

    img = ""
    if thumbnail:
        cls = f' class="{thumbnail_class}"' if thumbnail_class else ""
        img = f'\n        <img src="content/projects/{thumbnail}" alt="{thumbnail_alt}"{cls}>'

    link = ""
    redirect = project.get("redirect")
    if redirect:
        if project.content.strip():
            print(f"Warning: {slug}.md has a redirect and body content; body will be ignored")
        link = f'\n          <a href="{redirect}">read more ↝</a>'
    elif project.content.strip():
        link = f'\n          <a href="site/projects/{slug}.html">read more ↝</a>'

    return f"""\
      <li>
        <div class="info">
          <h3>{title}</h3>
          <p>{desc}</p>{link}
        </div>{img}
      </li>"""


_nav = []
if has_resume:
    _nav.append(("site/resume.html", "Resume"))
if has_photography:
    _nav.append(("site/photography.html", "Photography"))
nav_links = "\n".join(
    f'      <a href="{url}">{label}</a>' for url, label in _nav
)
skills = profile.get("skills") or []
links = profile.get("links") or []
skills_section = ""
if skills:
    spans = "\n".join(f"      <span>{s}</span>" for s in skills)
    skills_section = f'    <div class="skills">\n{spans}\n    </div>'
portrait_img = ""
if portrait:
    portrait_img = f'      <img src="content/{portrait}" alt="{name}" class="portrait">'
links_section = ""
if links:
    anchors = "\n".join(f'      <a href="{l["url"]}">{l["label"]}</a>' for l in links)
    links_section = f'    <p class="links">\n{anchors}\n    </p>'
project_items = "\n".join(
    build_project_item(os.path.splitext(os.path.basename(p))[0], proj)
    for p, proj in projects
)

index_html = INDEX_TEMPLATE.format(
    head=page_head(name, "style.css", bg, accent),
    footer=page_footer(name, year),
    name=name,
    bio=bio,
    portrait_img=portrait_img,
    nav_links=nav_links,
    skills_section=skills_section,
    links_section=links_section,
    project_items=project_items,
    section_label=section_label,
    year=year,
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("done")

# --- photography.html generation ---

if has_photography:
    print("Generating site/photography.html ... ", end="", flush=True)
    PHOTOGRAPHY_TEMPLATE = """\
{head}
<body style="max-width:1500px;">
  <header>
    <nav><a href="../index.html">↜ {name}</a></nav>
    <h1>Photography</h1>
  </header>

  <main>
    <div class="grid">
{photo_imgs}
    </div>
  </main>

{footer}
</body>
"""

    photo_files = [
        f for f in os.listdir("content/photography")
        if os.path.splitext(f)[1].lower() in _photo_exts
    ]

    # read aspect ratios and compute color sort keys in one pass
    ratios = {}
    sort_keys = {}
    for f in photo_files:
        with Image.open(f"content/photography/{f}") as img:
            w, h = img.size
            ratios[f] = h / w  # height relative to width (all rendered same width)
            pixels = list(img.convert("RGB").resize((50, 50)).get_flattened_data())
        sort_keys[f] = color_sort_key(pixels)

    # sort by dominant hue, then greedily assign to two columns to balance height
    photo_files.sort(key=lambda f: sort_keys[f])
    col1, col2 = [], []
    h1, h2 = 0, 0
    for f in photo_files:
        if h1 <= h2:
            col1.append(f)
            h1 += ratios[f]
        else:
            col2.append(f)
            h2 += ratios[f]

    # CSS columns: 2 fills top-to-bottom in col1, then col2
    ordered = col1 + col2
    photo_imgs = "\n".join(
        f'      <img src="../content/photography/{f}" alt="">' for f in ordered
    )

    photography_html = PHOTOGRAPHY_TEMPLATE.format(
        head=page_head(f"Photography - {name}", "../style.css", bg, accent),
        footer=page_footer(name, year),
        name=name,
        photo_imgs=photo_imgs,
        year=year,
    )
    with open("site/photography.html", "w", encoding="utf-8") as f:
        f.write(photography_html)
    print("done")

# --- resume.html generation ---

if has_resume:
    print("Generating site/resume.html ... ", end="", flush=True)
    resume_pdf = glob.glob("content/*.pdf")[0]

    RESUME_TEMPLATE = """\
{head}
<body>
  <header>
    <nav>
      <a href="../index.html">↜ {name}</a>
      <a href="../{resume_pdf}" download>Download</a>
    </nav>
    <h1>Resume</h1>
  </header>

  <main>
    <iframe class="resume" src="../{resume_pdf}"></iframe>
  </main>

{footer}
</body>"""

    resume_html = RESUME_TEMPLATE.format(
        head=page_head(f"Resume - {name}", "../style.css", bg, accent),
        footer=page_footer(name, year),
        name=name,
        resume_pdf=resume_pdf,
        year=year,
    )
    with open("site/resume.html", "w", encoding="utf-8") as f:
        f.write(resume_html)
    print("done")

# --- project page generation ---

PROJECT_TEMPLATE = """\
{head}

<body>
  <header>
    <nav><a href="../../index.html">↜ {name}</a></nav>
    <h1>{title}</h1>
    <p>{description}</p>
  </header>

  <main>
    {body}
  </main>

{footer}
</body>"""

# generate html for each project with markdown content
for path, project in projects:
    if not project.content.strip():
        continue
    if project.get("redirect"):
        continue
    slug = os.path.splitext(os.path.basename(path))[0]
    output_path = f"site/projects/{slug}.html"
    print(f"Generating {output_path} ... ", end="", flush=True)
    body = markdown.markdown(project.content, extensions=["fenced_code"])
    body = rewrite_project_paths(body)
    html = PROJECT_TEMPLATE.format(
        head=page_head(f"{project['title']} - {name}", "../../style.css", bg, accent),
        footer=page_footer(name, year),
        name=name,
        title=project["title"],
        description=project["description"].strip(),
        body=body,
        year=year,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("done")
