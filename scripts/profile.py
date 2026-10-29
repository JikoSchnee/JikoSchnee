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
BG, RED, TEXT, MUTED, LINE = "#0D1117", "#FF3B4E", "#C9D1D9", "#96A0AE", "#30363D"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "'PingFang SC','Microsoft YaHei','Noto Sans CJK SC',sans-serif"


def text(x, y, value, size=24, color=TEXT, mono=False, **attrs):
    extra = " ".join(f'{key.replace("_", "-")}="{escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def svg(title, body, width=840, height=240):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" fill="{BG}" stroke="{LINE}"/>
{body}
</svg>\n'''


def write_assets(outputs):
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
    body = '''<defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#30363D" stroke-opacity=".3"/></pattern></defs>
<rect x="540" y="1" width="299" height="318" rx="12" fill="url(#grid)"/>
<path d="M570 1L470 319" stroke="#FF3B4E" stroke-opacity=".35"/>
<g transform="translate(682 151)" fill="none" stroke="#FF3B4E">
<circle r="87" stroke-opacity=".25"/><circle r="63" stroke-opacity=".6"/>
<path d="M0-94V-75M0 75V94M-94 0H-75M75 0H94"/>
<path d="M0-50L43 25H-43ZM0 50L-43-25H43Z" stroke-width="2"/>
<path d="M0-50V50M-43-25L43 25M-43 25L43-25" stroke-opacity=".5"/>
<circle r="7" fill="#FF3B4E"/></g>
<path d="M32 32H65" stroke="#FF3B4E" stroke-width="3"/>
<style>@keyframes reveal{from{opacity:.25;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}.name{animation:reveal 1.2s ease-out both}@media(prefers-reduced-motion:reduce){.name{animation:none}}</style>'''
    body += text(80, 38, "JIKOSCHNEE / PERSONAL LAB", 16, MUTED, True, letter_spacing="1.2")
    body += '<g class="name">' + text(32, 150, "Jiko", 96, "#F0F3F6", True, font_weight="700", letter_spacing="-5") + text(275, 150, "_", 96, RED, True) + '</g>'
    body += text(36, 194, "BUILD TOOLS. EXPLORE DESIGN.", 19, RED, True, letter_spacing=".5")
    body += '<path d="M32 236H808" stroke="#30363D"/>'
    body += text(32, 284, "制作实用工具，探索网页设计与交互。", 28)
    outputs = {"header.svg": svg("Jiko / JikoSchnee — 制作实用工具，探索网页设计与交互。", body, height=320)}

    projects = [
        ("harmonica", "01", "Harmonica Deck", "简谱与 MIDI 处理、试听及鼠标宏导出", "MUSIC / TOOLS", "wave"),
        ("atlas", "02", "Atlas Design", "Atlas 风格视觉研究与网页组件", "VISUAL / WEBGL", "atlas"),
        ("gallery", "03", "Design Gallery", "网页设计作品集", "DESIGN / WEB", "grid"),
        ("airfare", "04", "AirFare Radar", "低价机票发现与探索型交互原型", "TRAVEL / PROTOTYPE", "radar"),
    ]
    for slug, number, title, desc, category, icon in projects:
        art = '<g transform="translate(746 87)" fill="none" stroke="#FF3B4E" stroke-width="2">'
        if icon == "wave":
            for i, h in enumerate([12, 28, 48, 34, 18, 40, 56, 28, 12]):
                art += f'<path d="M{-48+i*12} {-h/2}V{h/2}" stroke-linecap="round"/>'
        elif icon == "atlas":
            art += '<circle r="48" stroke-opacity=".3"/><path d="M0-45L40 0L0 45L-40 0ZM0-45V45M-40 0H40"/><path d="M0-25L22 0L0 25L-22 0Z" fill="#FF3B4E" fill-opacity=".12"/>'
        elif icon == "grid":
            art += '<rect x="-44" y="-35" width="38" height="70" rx="3"/><rect x="6" y="-35" width="38" height="28" rx="3"/><rect x="6" y="5" width="38" height="30" rx="3" fill="#FF3B4E" fill-opacity=".15"/>'
        else:
            art += '<circle r="44" stroke-opacity=".5"/><circle r="26" stroke-opacity=".3"/><path d="M-52 0H52M0-52V52" stroke-opacity=".3"/><path d="M0 0L32-31"/><circle cx="22" cy="-21" r="5" fill="#FF3B4E"/>'
        art += '</g>'
        body = '<path d="M1 24V166" stroke="#FF3B4E" stroke-width="2"/>'
        body += text(28, 34, number, 17, RED, True) + text(68, 34, category, 16, MUTED, True, letter_spacing="1")
        body += text(28, 88, title, 36, "#F0F3F6", True, font_weight="600")
        body += text(28, 139, desc, 26)
        body += '<path d="M28 166H650" stroke="#30363D"/>' + art
        outputs[f"project-{slug}.svg"] = svg(f"{title} — {desc}", body, height=190)

    badges = [("python", "Python", "Py", 146), ("javascript", "JavaScript", "JS", 188), ("typescript", "TypeScript", "TS", 188), ("vue", "Vue", "V", 122), ("html-css", "HTML / CSS", "<>", 188)]
    for slug, label, symbol, width in badges:
        body = '<path d="M46 9V33" stroke="#30363D"/>'
        body += text(24, 27, symbol, 15, RED, True, text_anchor="middle", font_weight="700")
        body += text(58, 27, label, 16, TEXT, True)
        outputs[f"badge-{slug}.svg"] = svg(label, body, width=width, height=42)
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
    body = text(28, 40, "PUBLIC / ORIGINAL", 19, RED, True, letter_spacing="1")
    body += '<path d="M420 65V192" stroke="#30363D"/>'
    for x, number, label in [(28, data["repositories"], "公开原创仓库"), (454, data["stars"], "获得的 Stars")]:
        body += text(x, 132, f"{number:,}", 70, "#F0F3F6", True, font_weight="700")
        body += text(x, 179, label, 26)
    body += text(28, 224, "全部公开非 fork 仓库 · 含归档仓库", 20, MUTED)
    overview = svg("公开原创仓库与获得的 Stars", body, height=250)

    ordered = sorted(data["languages"].items(), key=lambda item: (-item[1], item[0]))
    shown = ordered[:5]
    if len(ordered) > 5:
        shown.append(("Other", sum(value for _, value in ordered[5:])))
    total = sum(data["languages"].values())
    body = text(28, 40, "LANGUAGE DISTRIBUTION", 19, RED, True, letter_spacing="1")
    colors = ["#FF3B4E", "#EB6976", "#C98C94", "#A8AEB8", "#788698", "#515D6D"]
    left = 28
    for i, (_, amount) in enumerate(shown):
        width = 784 * amount / total
        body += f'<rect x="{left:.3f}" y="64" width="{width:.3f}" height="12" fill="{colors[i]}"/>'
        left += width
    for i, (language, amount) in enumerate(shown):
        y = 124 + i * 45
        body += f'<circle cx="34" cy="{y-8}" r="5" fill="{colors[i]}"/>'
        body += text(52, y, language, 27, TEXT, True)
        body += text(808, y, f"{amount / total:.1%}", 27, TEXT, True, text_anchor="end")
    if not shown:
        body += text(28, 124, "暂无公开语言数据", 26)
    height = 154 + max(len(shown), 1) * 45
    body += text(28, height-25, "按 GitHub 语言字节数统计 · 非熟练度", 20, MUTED)
    # Every API request and both renders finish before either asset is replaced.
    write_assets({"stats-overview.svg": overview, "stats-languages.svg": svg("公开原创仓库的语言分布，按代码字节数", body, height=height)})


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
