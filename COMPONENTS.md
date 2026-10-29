# README Components

The profile uses the original Atlas typeface, a rendered Atlas globe, square hairline frames and two-digit indices. Dark and light variants follow GitHub’s active theme.

## Profile design

| Element | Treatment |
| --- | --- |
| Typography | GeosansLight-NMS outlines, light weight, generous tracking |
| Indices | Two digits in signal red |
| Frames | Square hairlines; warm-white edges with a narrow red bloom |
| Dark | `#07080D` canvas, `#FA2A29` accent, `#F7F4E8` text |
| Light | `#FCFCFA` canvas, `#BD292B` accent, `#21242B` text |
| Content | English only; one introduction, project names, direct card links |

Project cards open their repositories. Separate Demo links open the live projects. Statistical methodology stays inside a collapsed details section.

## Optional components

These external examples are alternatives to the repository-owned assets. They use a neutral black background with red or gold accents. Public services may cache responses, impose rate limits or become unavailable.

| Component | Use | Notes |
| --- | --- | --- |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | Headers and footers | Explicit colors should not be combined with a theme override. |
| [Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) | Animated introduction | Keep lines short and avoid competing animations. |
| [Shields.io](https://shields.io/badges/static-badge) | Technology and social badges | Use valid Simple Icons slugs and URL-encode labels. |
| [Readme Stats](https://github.com/anuraghazra/github-readme-stats) | Statistics and language cards | Repository generation or self-hosting is more reliable than a shared endpoint. |
| [Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats) | Contribution streaks | Time zone and caching affect day boundaries. |

Examples are filled in for JikoSchnee. Replace the account name when reusing them. Never include access tokens in image URLs.

## 1. Capsule Render

Black / red:

```markdown
![Jiko](https://capsule-render.vercel.app/api?type=rect&color=0D1117&height=200&text=Jiko%20%2F%20JikoSchnee&fontColor=FF3B4E&fontSize=44&animation=fadeIn)
```

Black / gold:

```markdown
![Jiko](https://capsule-render.vercel.app/api?type=rect&color=0D1117&height=200&text=Jiko%20%2F%20JikoSchnee&fontColor=D4AF37&fontSize=44&animation=fadeIn)
```

## 2. Typing SVG

Black / red:

```markdown
![Introduction](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3200&pause=1500&color=FF3B4E&background=0D1117&center=true&vCenter=true&width=650&height=70&lines=Build+tools.+Explore+design.;Python+%2F+TypeScript+%2F+Vue)
```

Black / gold:

```markdown
![Introduction](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3200&pause=1500&color=D4AF37&background=0D1117&center=true&vCenter=true&width=650&height=70&lines=Build+tools.+Explore+design.;Python+%2F+TypeScript+%2F+Vue)
```

## 3. Shields.io

Black / red:

```markdown
![Python](https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=FF3B4E)
![TypeScript](https://img.shields.io/badge/TypeScript-0D1117?style=for-the-badge&logo=typescript&logoColor=FF3B4E)
![Vue](https://img.shields.io/badge/Vue-0D1117?style=for-the-badge&logo=vuedotjs&logoColor=FF3B4E)
```

Black / gold:

```markdown
![Python](https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=D4AF37)
![TypeScript](https://img.shields.io/badge/TypeScript-0D1117?style=for-the-badge&logo=typescript&logoColor=D4AF37)
![Vue](https://img.shields.io/badge/Vue-0D1117?style=for-the-badge&logo=vuedotjs&logoColor=D4AF37)
```

## 4. GitHub Readme Stats

Black / red:

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=JikoSchnee&show_icons=true&hide_rank=true&bg_color=0D1117&title_color=FF3B4E&icon_color=FF3B4E&text_color=C9D1D9&border_color=30363D)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=JikoSchnee&layout=compact&bg_color=0D1117&title_color=FF3B4E&text_color=C9D1D9&border_color=30363D)
```

Black / gold:

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=JikoSchnee&show_icons=true&hide_rank=true&bg_color=0D1117&title_color=D4AF37&icon_color=D4AF37&text_color=C9D1D9&border_color=30363D)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=JikoSchnee&layout=compact&bg_color=0D1117&title_color=D4AF37&text_color=C9D1D9&border_color=30363D)
```

## 5. Streak Stats

Black / red:

```markdown
![GitHub Streak](https://streak-stats.demolab.com/?user=JikoSchnee&background=0D1117&border=30363D&stroke=30363D&ring=FF3B4E&fire=FF3B4E&currStreakNum=C9D1D9&sideNums=C9D1D9&currStreakLabel=FF3B4E&sideLabels=C9D1D9&dates=96A0AE&timezone=Asia%2FShanghai)
```

Black / gold:

```markdown
![GitHub Streak](https://streak-stats.demolab.com/?user=JikoSchnee&background=0D1117&border=30363D&stroke=30363D&ring=D4AF37&fire=D4AF37&currStreakNum=C9D1D9&sideNums=C9D1D9&currStreakLabel=D4AF37&sideLabels=C9D1D9&dates=96A0AE&timezone=Asia%2FShanghai)
```

## Theme and motion

Paired images and links use `#gh-dark-mode-only` and `#gh-light-mode-only` to follow the active GitHub appearance. See the [theme-context examples](https://github.com/anuraghazra/github-readme-stats#use-githubs-theme-context-tag). Light SVGs use the `-light.svg` suffix.

The header uses the actual Atlas geometry and shaders rendered into a looping GIF. Its picture element selects a static PNG for reduced-motion preferences. Clicking the header opens the interactive Atlas project. The sphere retains its original dark shell and red interior in both themes.

## Maintenance

Regenerate static artwork and statistics from the repository root:

```sh
python3 scripts/profile.py design
python3 scripts/profile.py stats
```

Both commands use Python’s standard library. `scripts/atlas/typeface.json` supplies the original font contours, so SVG viewers do not need to fetch fonts. See [Atlas rendering instructions](scripts/atlas/README.md) for the animation export process and source attribution.

Statistics include all public non-fork repositories owned by JikoSchnee, including archived repositories and this profile repository. Stars are summed across that set. Languages are aggregated from the Languages API by byte count; the top five are shown individually and the remainder becomes Other. Byte counts do not measure proficiency.

The [workflow](.github/workflows/update-profile.yml) updates both themes daily at 08:17 Asia/Shanghai and supports manual runs. GitHub scheduling may be delayed or paused after prolonged inactivity. It uses the repository-provided `GITHUB_TOKEN` with `contents: write`; no personal token is needed.

All requests and SVG validation must finish before any statistics file is replaced. Failures preserve the last successful images. Files contain no timestamps, and unchanged images do not create commits.

Only smoke checks are required: validate assets and links, inspect mobile rendering and both GitHub appearances, and confirm the statistics workflow succeeds.
