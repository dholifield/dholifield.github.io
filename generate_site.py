import fnmatch
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


def load_genignore():
    """Load .genignore patterns and return an is_ignored(path) predicate."""
    if not os.path.exists(".genignore"):
        return lambda path: False
    with open(".genignore", encoding="utf-8") as f:
        patterns = [
            line.strip() for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    def is_ignored(path):
        name = os.path.basename(path)
        return any(fnmatch.fnmatch(name, p) for p in patterns)
    return is_ignored


def rewrite_project_paths(html):
    """Rewrite relative src/href values to be relative to the content folder."""
    def rewrite(m):
        attr, path = m.group(1), m.group(2)
        if re.match(r'https?://|/|#|mailto:', path):
            return m.group(0)
        return f'{attr}="../../content/{path}"'
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

# load .genignore patterns
is_ignored = load_genignore()

# open profile.md with frontmatter
if not os.path.exists("content/profile.md"):
    raise FileNotFoundError("content/profile.md not found - cannot generate site")
profile = frontmatter.load("content/profile.md")

year = date.today().year
gallery_folder = profile.get("gallery")

# discover content subdirectories dynamically
all_sections = {}  # folder_name -> sorted list of (path, project)
for entry in os.listdir("content"):
    folder_path = os.path.join("content", entry)
    if not os.path.isdir(folder_path):
        continue
    if entry.startswith("."):
        continue
    if entry == gallery_folder:
        continue
    items = []
    for path in glob.glob(os.path.join(folder_path, "*.md")):
        if is_ignored(path):
            print(f"Ignored: {path}")
            continue
        project = frontmatter.load(path)
        if "title" not in project or "description" not in project:
            print(f"Warning: skipping {path} (missing title or description)")
            continue
        items.append((path, project))
    if items:
        items.sort(key=lambda x: x[1].get("order") or 999)
        all_sections[entry] = items

# order sections: explicit list from profile first, then remaining alphabetically
section_order = profile.get("sections") or []
ordered_keys = [s for s in section_order if s in all_sections]
ordered_keys += sorted(k for k in all_sections if k not in ordered_keys)
sections = {k: all_sections[k] for k in ordered_keys}

# detect optional features
_photo_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
has_photography = gallery_folder and os.path.isdir(f"content/{gallery_folder}") and any(
    os.path.splitext(f)[1].lower() in _photo_exts
    and not is_ignored(f)
    for f in os.listdir(f"content/{gallery_folder}")
)
has_resume = bool(glob.glob("content/*.pdf"))

if not has_photography:
    print("Note: no photography folder or images found, skipping photography page")
if not has_resume:
    print("Note: no PDF found, skipping resume page")

# clean and set up output directory
os.makedirs("site", exist_ok=True)
for f in glob.glob("site/*.html"):
    os.remove(f)
for folder_name in sections:
    for f in glob.glob(f"site/{folder_name}/*.html"):
        os.remove(f)
    os.makedirs(f"site/{folder_name}", exist_ok=True)

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

{sections}
  </main>

{footer}
</body>
"""


def build_project_item(slug, project, folder):
    """Build a single <li> for the project list on the index page."""
    title = project["title"]
    desc = project["description"].strip()

    thumbnail = project.get("thumbnail")
    thumbnail_alt = project.get("thumbnail_alt", title)
    thumbnail_class = project.get("thumbnail_class")

    img = ""
    if thumbnail:
        cls = f' class="{thumbnail_class}"' if thumbnail_class else ""
        img = f'\n        <img src="content/{thumbnail}" alt="{thumbnail_alt}"{cls}>'

    link = ""
    redirect = project.get("redirect")
    if redirect:
        if project.content.strip():
            print(f"Warning: {slug}.md has a redirect and body content; body will be ignored")
        link = f'\n          <a href="{redirect}">read more ↝</a>'
    elif project.content.strip():
        link = f'\n          <a href="site/{folder}/{slug}.html">read more ↝</a>'

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
    gallery_title = gallery_folder.replace("-", " ").replace("_", " ").title()
    _nav.append((f"site/{gallery_folder}.html", gallery_title))
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
sections_html_parts = []
for folder_name, items in sections.items():
    section_title = folder_name.replace("-", " ").replace("_", " ").title()
    project_items = "\n".join(
        build_project_item(os.path.splitext(os.path.basename(p))[0], proj, folder_name)
        for p, proj in items
    )
    sections_html_parts.append(
        f"    <h2>{section_title}</h2>\n"
        f"    <ul class=\"projects\">\n"
        f"{project_items}\n"
        f"    </ul>"
    )
sections_html = "\n<hr>\n".join(sections_html_parts)

index_html = INDEX_TEMPLATE.format(
    head=page_head(name, "style.css", bg, accent),
    footer=page_footer(name, year),
    name=name,
    bio=bio,
    portrait_img=portrait_img,
    nav_links=nav_links,
    skills_section=skills_section,
    links_section=links_section,
    sections=sections_html,
    year=year,
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("done")

# --- photography.html generation ---

if has_photography:
    gallery_title = gallery_folder.replace("-", " ").replace("_", " ").title()
    gallery_output = f"site/{gallery_folder}.html"
    print(f"Generating {gallery_output} ... ", end="", flush=True)
    PHOTOGRAPHY_TEMPLATE = """\
{head}
<body style="max-width:1500px;">
  <header>
    <nav><a href="../index.html">↜ {name}</a></nav>
    <h1>{gallery_title}</h1>
  </header>

  <main>
    <div class="grid">
{photo_imgs}
    </div>
    <p class="license">&copy; {name} &middot; Licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a></p>
  </main>

{footer}
</body>
"""

    gallery_path = f"content/{gallery_folder}"
    photo_files = []
    for f in os.listdir(gallery_path):
        if os.path.splitext(f)[1].lower() not in _photo_exts:
            continue
        if is_ignored(f):
            print(f"Ignored: {gallery_path}/{f}")
            continue
        photo_files.append(f)

    # read aspect ratios and compute color sort keys in one pass
    ratios = {}
    sort_keys = {}
    for f in photo_files:
        with Image.open(f"{gallery_path}/{f}") as img:
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
        f'      <img src="../content/{gallery_folder}/{f}" alt="">' for f in ordered
    )

    photography_html = PHOTOGRAPHY_TEMPLATE.format(
        head=page_head(f"{gallery_title} - {name}", "../style.css", bg, accent),
        footer=page_footer(name, year),
        name=name,
        gallery_title=gallery_title,
        photo_imgs=photo_imgs,
        year=year,
    )
    with open(gallery_output, "w", encoding="utf-8") as f:
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
    <hr>
  </header>

  <main>
    {body}
  </main>

{footer}
</body>"""

# generate html for each project with markdown content
for folder_name, items in sections.items():
    for path, project in items:
        if not project.content.strip():
            continue
        if project.get("redirect"):
            continue
        slug = os.path.splitext(os.path.basename(path))[0]
        output_path = f"site/{folder_name}/{slug}.html"
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
