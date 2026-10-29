#!/usr/bin/env python3
"""Build repository-owned profile SVGs with Python's standard library."""

import argparse
from collections import Counter
from html import escape
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG, RED, TEXT, MUTED, LINE = "#07080D", "#FA2A29", "#F7F4E8", "#A6ADB6", "#3D3E41"
FONT = json.loads((ROOT / "scripts/atlas/typeface.json").read_text())
SANS = "'GeosansLight-NMS','Futura PT','Avenir Next',sans-serif"


def text(x, y, value, size=24, color=TEXT, mono=False, **attrs):
    value = str(value)
    if all(char in FONT["glyphs"] for char in value):
        scale = size / FONT["unitsPerEm"]
        tracking = float(attrs.get("letter_spacing", size * .08))
        width = sum(FONT["glyphs"][char]["advance"] * scale for char in value) + max(0, len(value)-1) * tracking
        if attrs.get("text_anchor") == "end":
            x -= width
        elif attrs.get("text_anchor") == "middle":
            x -= width / 2
        paths = []
        for char in value:
            glyph = FONT["glyphs"][char]
            if glyph["path"]:
                paths.append(f'<path transform="translate({x:.3f} {y}) scale({scale:.6f} {-scale:.6f})" d="{glyph["path"]}"/>')
            x += glyph["advance"] * scale + tracking
        return f'<g fill="{color}" aria-label="{escape(value, quote=True)}">' + ''.join(paths) + '</g>'
    extra = " ".join(f'{key.replace("_", "-")}="{escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="300" fill="{color}" {extra}>{escape(value)}</text>'


def svg(title, body, width=840, height=240, frame=True):
    border = ""
    if frame:
        corners = f"M1 29V1H29 M{width-30} {height-1}H{width-1}V{height-30}"
        border = f'''<defs><filter id="edge" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter></defs>
<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" fill="{BG}" stroke="{LINE}"/>
<path d="{corners}" fill="none" stroke="{RED}" stroke-width="4" opacity=".65" filter="url(#edge)"/>
<path d="{corners}" fill="none" stroke="#FFFDF4" stroke-width="1"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
{border}
{body}
</svg>\n'''


def write_assets(outputs):
    # Emit both GitHub appearance variants from one canonical drawing.
    light_palette = {"#07080D": "#FCFCFA", "#FA2A29": "#BD292B", "#F7F4E8": "#21242B",
                     "#A6ADB6": "#59616C", "#3D3E41": "#CFD0CF", "#FFFDF4": "#BD292B"}
    outputs = dict(outputs)
    for name, content in list(outputs.items()):
        light = re.sub("|".join(re.escape(color) for color in light_palette),
                       lambda match: light_palette[match.group()], content)
        outputs[name.replace(".svg", "-light.svg")] = light
    # Validate the complete batch before touching any successful previous assets.
    for content in outputs.values():
        ET.fromstring(content)
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        target = ASSETS / name
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            temporary = target.with_suffix(".tmp")
            temporary.write_text(content, encoding="utf-8")
            temporary.replace(target)
            print(f"Updated assets/{name}")


def render_design():
    body = text(38, 158, "JIKO", 104, TEXT, letter_spacing="14")
    body += text(38, 213, "Building tools. Exploring design.", 26, TEXT)
    outputs = {"header.svg": svg("Jiko — Building tools. Exploring design.", body, height=320)}

    for number, label, slug in [("01", "STACK", "stack"), ("02", "PROJECTS", "projects"), ("03", "ACTIVITY", "activity")]:
        body = text(0, 40, number, 24, RED, letter_spacing="3.4")
        body += text(70, 41, label, 36, TEXT, letter_spacing="5")
        outputs[f"section-{slug}.svg"] = svg(f"{number} {label}", body, height=58, frame=False)

    projects = [
        ("harmonica", "01", "HARMONICA DECK", "MIDI and notation tools"),
        ("atlas", "02", "ATLAS DESIGN", "Atlas interface components"),
        ("gallery", "03", "DESIGN GALLERY", "Web design experiments"),
        ("airfare", "04", "AIRFARE RADAR", "Low-fare flight discovery"),
    ]
    for slug, number, title, desc in projects:
        body = text(28, 64, number, 26, RED, letter_spacing="3.4")
        body += text(102, 68, title, 46, TEXT, letter_spacing="3")
        body += f'<path d="M776 68L792 52M780 52H792V64" fill="none" stroke="{TEXT}" stroke-width="1.2"/>'
        outputs[f"project-{slug}.svg"] = svg(f"{number} {title} — {desc}", body, height=110)

    badges = [("python", "PYTHON", 130), ("javascript", "JAVASCRIPT", 180), ("typescript", "TYPESCRIPT", 180), ("vue", "VUE", 110), ("html-css", "HTML / CSS", 180)]
    for slug, label, width in badges:
        body = text(width / 2, 29, label, 21, TEXT, text_anchor="middle", letter_spacing="1.6")
        outputs[f"badge-{slug}.svg"] = svg(label, body, width=width, height=46)
    write_assets(outputs)


def github(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "JikoSchnee-profile", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=30) as response:
        return json.load(response)


def collect_stats(username):
    repos = []
    for page in range(1, 1000):
        batch = github(f"/users/{username}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Expected a repository list")
        repos.extend(repo for repo in batch if not repo["fork"] and not repo["private"])
        if len(batch) < 100:
            break
    else:
        raise ValueError("Repository pagination did not finish")
    languages = Counter()
    for repo in repos:
        languages.update(github(f'/repos/{username}/{repo["name"]}/languages'))
    return {"repositories": len(repos), "stars": sum(repo["stargazers_count"] for repo in repos), "languages": dict(languages)}


def render_stats(data):
    body = f'<path d="M420 24V166" stroke="{LINE}"/>'
    for x, number, label in [(30, data["repositories"], "REPOSITORIES"), (454, data["stars"], "STARS")]:
        body += text(x, 103, f"{number:,}", 84, TEXT, letter_spacing="4")
        body += text(x, 155, label, 28, MUTED, letter_spacing="3")
    overview = svg("Public non-fork repositories and total stars", body, height=190)

    ordered = sorted(data["languages"].items(), key=lambda item: (-item[1], item[0]))
    shown = ordered[:5]
    if len(ordered) > 5:
        shown.append(("Other", sum(value for _, value in ordered[5:])))
    total = sum(data["languages"].values())
    colors = [RED, "#EB6976", "#C98C94", "#A8AEB8", "#788698", "#515D6D"]
    body, left = "", 30
    for i, (_, amount) in enumerate(shown):
        width = 780 * amount / total
        body += f'<rect x="{left:.3f}" y="28" width="{width:.3f}" height="5" fill="{colors[i]}"/>'
        left += width
    for i, (language, amount) in enumerate(shown):
        y = 78 + i * 43
        body += f'<circle cx="34" cy="{y-8}" r="3" fill="{colors[i]}"/>'
        body += text(52, y, language, 32, TEXT, letter_spacing="1.4")
        body += text(808, y, f"{amount / total:.1%}", 32, TEXT, text_anchor="end", letter_spacing="1.4")
    if not shown:
        body += text(28, 78, "No public language data", 26)
    height = 68 + max(len(shown), 1) * 43
    # Complete every request and render before replacing either theme's assets.
    write_assets({"stats-overview.svg": overview, "stats-languages.svg": svg("Language distribution across public non-fork repositories, by bytes", body, height=height)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["design", "stats"])
    parser.add_argument("--username", default="JikoSchnee")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.username):
        parser.error("Invalid GitHub username")
    if args.command == "design":
        render_design()
    else:
        render_stats(collect_stats(args.username))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Profile generation failed ({type(error).__name__}): {error}", file=sys.stderr)
        sys.exit(1)
