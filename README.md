# Affinity sample files

Small Affinity documents for testing importers, made for
[storytold/photocraft#1606](https://github.com/storytold/photocraft/issues/1606). Each file
covers one item from that issue. Next to every `.af` there is a PNG exported by Affinity
from the same document, to compare an importer's render against.

- Made with Affinity 3.1.0 (Windows build, running under Wine on Linux).
- Drawn from scratch for this repo. No stock images, no assets from Affinity's libraries, no
  brush packs. Only Affinity's basic round brushes were used.
- Text is set in Fira Sans (SIL Open Font License). The font is not embedded in the files.
- Released under CC0 1.0, see `LICENSE`.

## Files

| File | #1606 item | What is in it |
|---|---|---|
| `01-layer-effects` | Layer effects and live filters | One circle per effect: outer shadow, inner shadow, outer glow (red, blend mode Normal), inner glow, outline, bevel/emboss, 3D, Gaussian blur, colour overlay, gradient overlay. The last two circles have a live filter layer as a child instead (Gaussian blur, add noise). |
| `02-adjustment-layers` | Adjustment layers | Eight groups, each with a colour and a grey ramp and one adjustment inside the group: Levels (master black 20 %, white 80 %, gamma 1.5, output 10–90 %; red gamma 0.7), Curves (master 0.25→0.15 and 0.75→0.85; blue 0.5→0.6), HSL (hue +90°, saturation −30 %, luminosity +10 %), Brightness/Contrast (+20 %, +40 %), Black and White (reds +80 %, blues −40 %), Invert, Recolour (hue 200°, saturation 70 %), Selective Colour (relative; reds cyan −50 %, yellow +50 %; neutrals black +20 %). |
| `03-brush-strokes` | Brush and pressure strokes | Row 1: stroke rasterised with "Rasterize & Trim". Row 2: vector brush on a curve with a pressure profile rising from 0 to 100 %. Row 3: vector brush, no pressure profile. Row 4: stroke rasterised with "Rasterize", then erased at 100, 75, 50 and 25 % from left to right. The four dashed guide curves are hidden layers. |
| `04-master-page` | Master pages | A4, three pages, master A with header and footer. The footer holds a page number field. Page 3 edits the master detached (header circle recoloured). PNG per page. |
| `05-symbols` | Symbols and embedded documents | A symbol with three instances: one unchanged, one with the centre recoloured while sync was off, one scaled to 150 %. `source/05b-embedded.svg` is placed as an embedded document. |
| `06-special-shapes` | Special shapes | Sixteen shapes drawn with Affinity's shape tools and kept as shapes: cloud, heart, cog, two callouts, arrow, double star, tear, crescent, donut, pie, segment, diamond, trapezoid, square star, polygon. Most have their parameters moved away from the defaults. |
| `07-transparency` | Transparency gradients, fill opacity, bitmap fills | Fill opacity 50 %, layer opacity 50 %, gradient fill with an alpha stop, linear and radial transparency tool, bitmap fill with `source/07-texture.png`. |
| `08-gradients` | Conical gradients | Linear and radial for reference, one elliptical (its axes ended up equal, so it looks round), conical with two stops, conical with three stops, conical with the centre moved off the shape centre. |
| `09-corners-stars` | Corner types, stars with rounded points | Corner tool: rounded, straight, concave, cutout (labelled "Inset"), mixed per corner, large rounded radius (labelled "Smooth", Affinity 3 has no corner type of that name). Two stars: rounded points, rounded inner corners. |
| `10-multiple-fills` | Several fills or strokes on one object | Made in the Appearance panel: two fills, two strokes, fill with two strokes (one dashed), gradient fill at 50 % over a solid fill, strokes aligned inside and outside, three fills with the middle one hidden. |
| `11-text` | Outlined or scaled text, fields, columns, curved frames | Text converted to curves, artistic text with 60 % horizontal scale, text on a path, frame text with two columns (12 pt gutter, balanced), a page number field as its own text, a file name field inside a line of text, frame text in an elliptical frame. |
| `12-*` | CMYK, Lab, grey, 16/32-bit | One test chart saved in six formats: RGB/8, RGB/16, RGB/32, CMYK/8, LAB/16, Gray/8, each converted from RGB/8 with Affinity's default profile for that format. |
| `13-blend-modes` | Affinity-only blend modes | A circle over a gradient, blend mode Normal for reference, then Average, Negation, Reflect, Glow and Erase. |

## Source

`source/` has the SVGs the documents were started from and `make_svgs.py`, which writes
them. They are the starting point only, everything listed above was added in Affinity.
A few things in the SVGs did not survive Affinity's SVG import and were redone by hand: the
text on a path, the pattern fill and the paragraph in `11-text`, which came in as one
artistic text per line.

## Not covered

Files from Affinity 2 (`.afdesign`, `.afphoto`, `.afpub`), and anything that needs macOS.
