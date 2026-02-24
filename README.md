# Portfolio Generator

A minimal static site generator for personal portfolio sites. Write your content in Markdown, run one script, and get a clean site ready for GitHub Pages.

## Quick start

1. Fork or clone this repo
2. Edit `content/profile.md` with your info
3. Add projects as `.md` files in `content/projects/`
4. Push to `main` — GitHub Actions builds and deploys automatically

To build locally:

```
pip install python-frontmatter markdown Pillow
python generate_site.py
open index.html
```

## Content

Everything lives in the `content/` folder.

### Profile (`content/profile.md`)

Controls the index page. Only `name` and `bio` are required — everything else is optional.

```yaml
---
name: Your Name
bio: >
  A short paragraph about yourself.
portrait: headshot.jpg        # photo in content/
background: "#f7f7f2"         # page background color
accent: "#899878"             # button/link color
skills:
  - Skill 1
  - Skill 2
links:
  - label: GitHub
    url: https://github.com/yourname
gallery: photography          # folder in content/ to use as photo gallery
sections: [projects, writing] # order sections appear on index page
---
```

### Sections

Any subfolder in `content/` with `.md` files automatically becomes a section on the index page (title derived from folder name). For example:

```
content/
  projects/    → "Projects" section
  writing/     → "Writing" section
```

Use `sections` in your profile to control the order. Unlisted folders appear alphabetically after the listed ones.

Each `.md` file in a section needs at minimum:

```yaml
---
title: Project Name
description: >
  One or two sentences shown on the index card.
---

Markdown body here — becomes the detail page.
```

Other optional fields:

| Field | Description |
|-------|-------------|
| `order` | Sort position within the section (lower = first) |
| `thumbnail` | Image path relative to `content/` |
| `thumbnail_alt` | Alt text for thumbnail |
| `thumbnail_class` | CSS class on thumbnail (e.g. `contain`) |
| `redirect` | Link to external URL instead of generating a detail page |

Images and links in your markdown use paths relative to `content/` — the generator rewrites them automatically.

### Gallery

Set `gallery: photography` in your profile to turn a content folder into a photo gallery page. The folder name becomes the page title and nav link (e.g. `gallery: artwork` → "Artwork"). Drop images (jpg, png, webp, gif, avif) into that folder and the generator creates a color-sorted two-column gallery.

If the folder is missing or empty, the gallery page is skipped.

### Resume

Place a PDF in `content/`. The generator creates a resume page with an embedded viewer and download link. No PDF = no resume page.

## `.genignore`

Exclude files from generation with glob patterns, one per line:

```
*draft*
*template*
```

## Styling

Edit `style.css` to change the look. The layout is a centered single column with responsive breakpoints.

## Deployment

The included GitHub Actions workflow runs `generate_site.py` on every push to `main` and deploys to GitHub Pages. Enable GitHub Pages in your repo settings with the source set to **GitHub Actions**.

## File structure

```
content/
  profile.md              # your info (required)
  portrait.jpg            # optional portrait
  resume.pdf              # optional resume
  projects/*.md           # sections with markdown content
  photography/            # gallery images
.genignore                # optional ignore patterns
style.css                 # site styles
generate_site.py          # build script
```

## Using with Obsidian

The entire site can be managed from [Obsidian](https://obsidian.md/) by pointing it at the `content/` folder as a vault. Each section folder becomes a subfolder in the vault, and new pages are just markdown files with frontmatter.

Use Obsidian's Templates to scaffold new section pages with the required `title` and `description` fields. Add your template files to `.genignore` so they aren't included in the build:

```
*template*
```

A few tips:
- Turn off **Settings > Files & Links > Use [[Wikilinks]]** so links stay as standard markdown
- Use a `*draft*` naming convention and add it to `.genignore` to keep work-in-progress pages out of the build
