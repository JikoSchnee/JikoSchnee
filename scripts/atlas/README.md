# Atlas SVG header

The profile header is generated entirely as SVG code by `svg_sphere.py` and `../profile.py`. It contains vector paths and declarative SMIL animation, with no GIF, PNG, embedded raster frames, browser capture, or JavaScript runtime. Clicking the header opens [Awesome Portfolio](https://jikoschnee.github.io/Awesome-Portfolio/).

## Regeneration

```sh
python3 scripts/profile.py design
```

Only Python’s standard library is required. The command generates animated and static SVG headers in both GitHub themes. The README uses the static variants when the visitor requests reduced motion. Without animation support, the SVG retains a complete first frame.

`svg_sphere.py` builds a detail-4 icosahedron with 500 triangles, projects it through a perspective camera, and emits 48 vector keyframes across an 18-second rotation. The lighting direction, camera, geometry and dark-shell/red-core color model follow the original [Atlas core](https://github.com/JikoSchnee/Atlas-Design/tree/f26271e5056ae663584510e7c8e82afce984064f/components/atlas-core). SVG uses flat triangle colors rather than WebGL’s per-pixel shading, so this is a vector adaptation of the original globe.

The original WebGL reference files and optional capture utilities remain here for reference; the README no longer uses their raster output.

## Typography and borders

`typeface.json` contains printable ASCII outlines extracted from the original [GeosansLight-NMS Regular.ttf](https://github.com/JikoSchnee/Atlas-Design/blob/f26271e5056ae663584510e7c8e82afce984064f/GeosansLight-NMS%20Regular/GeosansLight-NMS%20Regular.ttf). No font download is needed at display time.

Panels use complete white outlines with a static red glow and internal clearance to protect the bloom. Light mode preserves the white outlines and softens the glow. All profile copy is English.
