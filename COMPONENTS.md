# README Components · Black / Red / Gold

一套可复用的 GitHub 个人页组件清单。当前个人页使用仓库内的黑红 SVG；以下第三方组件可按需替换，黑金版本使用同样的深色背景。

## Palette

| 用途 | 黑红 | 黑金 |
| --- | --- | --- |
| 背景 | `#0D1117` | `#0D1117` |
| 强调色 | `#FF3B4E` | `#D4AF37` |
| 正文 | `#C9D1D9` | `#C9D1D9` |
| 次要文字 | `#96A0AE` | `#96A0AE` |
| 边框 | `#30363D` | `#30363D` |

README 无法覆盖 GitHub 页面本身的背景；这套配色用于嵌入图片。不要依赖页面级 CSS、JavaScript、iframe 或外部字体来实现个人页。

## Component index

| 组件与源码 | 适合用途 | 本页使用方式 | 维护注意 |
| --- | --- | --- | --- |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | 顶部横幅、页尾 | 本页使用自有 `header.svg` | 公共服务可能缓存或不可用；显式颜色不要与 `theme` 混用 |
| [Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) | 动态打字介绍 | 备选；当前仅标题入场动画 | 英文更容易控制宽度；长句和中文需检查实际字体与换行 |
| [Shields.io](https://shields.io/badges/static-badge) | 技术栈、社交与状态徽章 | 本页使用自有文字徽章 | logo 名称使用 Simple Icons slug；URL 文本需要编码 |
| [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats) | 综合数据、语言、仓库卡 | 本页使用 Actions 生成两张 SVG | 公共实例有缓存及限流；高可靠场景采用仓库生成或自托管 |
| [Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats) | 连续贡献记录 | 可选扩展 | 时区会影响连续天数；日期边界、缓存和上游服务影响显示 |

下面的示例已填写 `JikoSchnee`，可直接复制到 README。替其他账号使用时，替换 `username`、`user` 和展示名称。外部服务示例依赖各自部署，不承诺持续可用。

## 1. Capsule Render — header

黑红：

```markdown
![Jiko](https://capsule-render.vercel.app/api?type=rect&color=0D1117&height=200&text=Jiko%20%2F%20JikoSchnee&fontColor=FF3B4E&fontSize=44&animation=fadeIn)
```

黑金：

```markdown
![Jiko](https://capsule-render.vercel.app/api?type=rect&color=0D1117&height=200&text=Jiko%20%2F%20JikoSchnee&fontColor=D4AF37&fontSize=44&animation=fadeIn)
```

使用明确的 `color` 和 `fontColor`。服务的 `theme` 参数优先级更高，因此这些示例不设置主题名。

## 2. Typing SVG — introduction

黑红：

```markdown
![Introduction](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3200&pause=1500&color=FF3B4E&background=0D1117&center=true&vCenter=true&width=650&height=70&lines=Build+tools.+Explore+design.;Python+%2F+TypeScript+%2F+Vue)
```

黑金：

```markdown
![Introduction](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3200&pause=1500&color=D4AF37&background=0D1117&center=true&vCenter=true&width=650&height=70&lines=Build+tools.+Explore+design.;Python+%2F+TypeScript+%2F+Vue)
```

保持短句，只安排一处主要动画。保留有意义的 alt 文本，以便图片不可用时仍能理解内容。

## 3. Shields.io — tech badges

黑红：

```markdown
![Python](https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=FF3B4E)
![TypeScript](https://img.shields.io/badge/TypeScript-0D1117?style=for-the-badge&logo=typescript&logoColor=FF3B4E)
![Vue](https://img.shields.io/badge/Vue-0D1117?style=for-the-badge&logo=vuedotjs&logoColor=FF3B4E)
```

黑金：

```markdown
![Python](https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=D4AF37)
![TypeScript](https://img.shields.io/badge/TypeScript-0D1117?style=for-the-badge&logo=typescript&logoColor=D4AF37)
![Vue](https://img.shields.io/badge/Vue-0D1117?style=for-the-badge&logo=vuedotjs&logoColor=D4AF37)
```

徽章只表示项目中使用的技术，不表达未经说明的熟练度。当前页面的徽章由脚本直接绘制，使用文字缩写，不依赖外部 logo 服务。

## 4. GitHub Readme Stats — statistics

黑红：

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=JikoSchnee&show_icons=true&hide_rank=true&bg_color=0D1117&title_color=FF3B4E&icon_color=FF3B4E&text_color=C9D1D9&border_color=30363D)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=JikoSchnee&layout=compact&bg_color=0D1117&title_color=FF3B4E&text_color=C9D1D9&border_color=30363D)
```

黑金：

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=JikoSchnee&show_icons=true&hide_rank=true&bg_color=0D1117&title_color=D4AF37&icon_color=D4AF37&text_color=C9D1D9&border_color=30363D)
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=JikoSchnee&layout=compact&bg_color=0D1117&title_color=D4AF37&text_color=C9D1D9&border_color=30363D)
```

不要把访问令牌放进图片 URL。第三方卡片与本仓库生成卡的统计范围可能不同；切换组件时，应一并调整页面的统计口径说明。语言字节数不等于代码能力或投入时间。

## 5. Streak Stats — contribution streak

黑红：

```markdown
![GitHub Streak](https://streak-stats.demolab.com/?user=JikoSchnee&background=0D1117&border=30363D&stroke=30363D&ring=FF3B4E&fire=FF3B4E&currStreakNum=C9D1D9&sideNums=C9D1D9&currStreakLabel=FF3B4E&sideLabels=C9D1D9&dates=96A0AE&timezone=Asia%2FShanghai)
```

黑金：

```markdown
![GitHub Streak](https://streak-stats.demolab.com/?user=JikoSchnee&background=0D1117&border=30363D&stroke=30363D&ring=D4AF37&fire=D4AF37&currStreakNum=C9D1D9&sideNums=C9D1D9&currStreakLabel=D4AF37&sideLabels=C9D1D9&dates=96A0AE&timezone=Asia%2FShanghai)
```

该组件作为可选扩展，不在默认个人页堆叠展示。检查服务版本对 `timezone` 的支持，并以实际返回内容为准。

## Maintaining this profile

### Static artwork

运行以下命令重新生成横幅、项目卡和技术徽章，无需网络或额外 Python 包：

```sh
python3 scripts/profile.py design
```

在 `scripts/profile.py` 中维护项目文案和图形。页面中的仓库、演示链接在 `README.md` 中维护。SVG 不包含脚本、外部字体或远程图片，仅横幅标题有一次性 CSS 入场动画，并遵循减少动态效果设置。

### GitHub statistics

```sh
python3 scripts/profile.py stats
```

脚本默认使用公开 API；若环境中已有 `GITHUB_TOKEN`，会用于认证以提高请求额度。无需为此创建个人令牌，也不要把令牌提交到仓库。

- 范围：账号拥有的全部公开非 fork 仓库，包括归档仓库及本仓库。
- Stars：上述仓库的 `stargazers_count` 之和。
- 语言：逐仓库读取 Languages API，合并字节数，展示前五种，其余归入 `Other`。
- 图片不包含时间戳，数据不变时不会产生无意义提交。
- 全部 API 请求和 SVG 校验成功后才写入统计图；请求失败时退出失败，保留原有图片。
- [Actions 工作流](.github/workflows/update-profile.yml) 每天北京时间 08:17 尝试更新（GitHub 调度可能延迟），也可在 Actions 页面选择 **Run workflow** 手动刷新。
- 工作流仅授予生成任务 `contents: write`，使用 GitHub 自动提供的仓库令牌；无第三方统计服务依赖。
- 长期无活动的公共仓库可能被 GitHub 暂停定时工作流，届时在 Actions 中重新启用。

### Smoke checks

检查 README 图片与目标链接、手机宽度的可读性、GitHub 明暗主题显示，并确认更新工作流成功。无需额外框架或完整测试套件。
