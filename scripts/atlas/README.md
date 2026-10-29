# Atlas header renderer

The README globe uses the actual two-layer geometry and shaders from [JikoSchnee/Atlas-Design](https://github.com/JikoSchnee/Atlas-Design/tree/f26271e5056ae663584510e7c8e82afce984064f/components/atlas-core), snapshot `f26271e5056ae663584510e7c8e82afce984064f`.

`atlas-core.js` preserves the source renderer and adds an optional `capturePhase` for deterministic export: a full Y-axis turn, fixed X angle and frozen shader noise. There is no audio input in the profile. `three.min.js` is the original project's vendored Three.js r160; its MIT license is included beside it.

GitHub READMEs cannot run WebGL/JavaScript, so the published header is a looping GIF. The 96 rendered frames play at 120 ms per frame. Daily statistics updates do not render the animation and need no additional packages.

## Regeneration

1. Run `python3 scripts/profile.py design` from the repository root to update both SVG header backgrounds and the static component themes.
2. Serve the repository with a local HTTP server.
3. In a browser with WebGL enabled, visit `scripts/atlas/render.html?theme=dark&frame=0`. Wait for `Ready: dark / 0` below the header, then capture the top-left 840 × 320 pixels at 1× scale.
4. Repeat for frame indices 0–95 and both `dark` and `light`. Save them outside the repository as `dark-000.png` through `light-095.png`.
5. Run `python3 scripts/atlas/assemble.py /path/to/frames` with Pillow installed. This writes two GIFs and their static PNG fallback images into `assets/`.

The `<picture>` fallback uses the static frame for visitors who request reduced motion. Theme context fragments on the surrounding links follow the active GitHub appearance, including when it differs from the operating system theme.

## Typography and borders

`typeface.json` contains printable ASCII outlines extracted from the original project's [GeosansLight-NMS Regular.ttf](https://github.com/JikoSchnee/Atlas-Design/blob/f26271e5056ae663584510e7c8e82afce984064f/GeosansLight-NMS%20Regular/GeosansLight-NMS%20Regular.ttf). The SVG generator uses the original contours, advance widths and explicit letter spacing. No browser font download or additional dependency is needed for statistics updates. All visible profile copy is English.

Section indices, project indices, labels and statistics all use this typeface. Panels use complete square white outlines and layered red bloom, based on the illuminated hover state of the Atlas boundary study. The effect is static, with internal clearance around every frame to protect the glow. Light mode preserves white outlines and softens the glow. Secondary category labels, repeated slogans and redundant repository links are omitted; the three project cards themselves open the live project pages.
