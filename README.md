# Portfolio Generator

A minimal static site generator for personal portfolio sites. Write your content in Markdown, run one script, and deploy to GitHub Pages.

## Quick start

1. Fork or clone this repo
2. Edit `content/profile.md` with your info
3. Push to `main` — GitHub Actions builds and deploys automatically

## Requirements

Python 3.10+ with:

```
pip install python-frontmatter markdown Pillow
```

To build locally:

```
python generate_site.py
```

Then open `index.html`.

## Content

Everything you need to edit is in the `content/` folder.

### `content/profile.md` (required)

The only file you must create. Controls the index page.

```yaml
---
name: Your Name
bio: >
  A short paragraph about yourself.
portrait: headshot.jpg           # photo in content/, shown on index page
skills:                          # optional — shown as tags on index page
  - Skill 1
  - Skill 2
links:                           # optional — external links shown below bio
  - label: Email
    url: mailto:you@example.com
  - label: GitHub
    url: https://github.com/yourname
section: Projects                # optional — heading above project list
background: "#f7f7f2"            # optional — page background color 
accent: "#899878"                # optional — button/link color
---
```

Navigation links for Resume and Photography are generated automatically when the corresponding content exists:
- Resume: a PDF in `content/`
- Photography: images in `content/photography/`

### Projects (`content/projects/*.md`)

Each `.md` file becomes a project card on the index page and its own detail page. Frontmatter fields:

```yaml
---
title: Project Name              # required
description: >                   # required — shown on index card
  One or two sentences.
order: 1                         # optional — lower numbers appear first
thumbnail: photos/photo.jpg      # optional
thumbnail_alt: Alt text          # optional
thumbnail_class: contain         # optional — adds CSS class to thumbnail
redirect: https://example.com    # optional — link to external URL instead of detail page
---

Markdown body content goes here. This becomes the project detail page.
If `redirect` is set, the index card links to that URL and no detail page is generated.
If no body is defined, the project will just exist on the home page
```

Images and links in project markdown use paths relative to `content/projects/`:

```markdown
<img src="photos/my-photo.jpg" alt="...">
<a href="articles/saved-article.html">link</a>
```

The generator rewrites these to the correct output paths automatically.

### Photography (`content/photography/`)

Drop images (jpg, png, webp, gif, avif) into this folder. The generator creates a two-column gallery page, sorted by dominant color with grayscale images at the end.

If the folder is missing or empty, the photography page and nav link are skipped.

### Resume (`content/*.pdf`)

Place a single PDF in `content/`. The generator creates a resume page with an embedded viewer and download link.

If there's no PDF, the resume page and nav link are skipped.

### Project assets

You can create any subfolder under `content/projects/` to organize assets:

```
content/projects/
  photos/         # project images and thumbnails
  articles/       # saved article backups
  diagrams/       # or whatever you need
```

Reference them from project markdown with simple relative paths like `photos/image.jpg`.

## Styling

Edit `style.css` to change the look. The site uses IBM Plex Mono loaded from `fonts/`. The layout is a centered single column (600px max width) with responsive breakpoints for mobile.

## Deployment

The included GitHub Actions workflow (`.github/workflows/deploy.yml`) runs on every push to `main`:

1. Installs Python dependencies
2. Runs `generate_site.py`
3. Deploys the repo root to GitHub Pages

Make sure GitHub Pages is enabled in your repo settings with the source set to **GitHub Actions**.

## File structure

```
content/                  # your content (edit this)
  profile.md
  portrait.jpg
  resume.pdf
  projects/
    *.md
    photos/
  photography/

fonts/                    # web fonts
style.css                 # site styles
generate_site.py          # build script
index.html                # generated
site/                     # generated subpages
.github/workflows/        # deployment config
```
