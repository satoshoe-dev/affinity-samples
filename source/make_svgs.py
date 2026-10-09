#!/usr/bin/env python3
"""Writes the SVGs the Affinity sample files were started from (photocraft#1606).

Each SVG is only the starting point. The feature itself (effect, adjustment,
special shape ...) was added in Affinity, see README.md.
"""
import struct
import zlib
from pathlib import Path

ZIEL = Path(__file__).parent
B, H = 1200, 800
SCHRIFT = "Fira Sans"  # unquoted, Affinity's SVG import falls back to Arial for quoted names
FARBEN = ["#e4572e", "#f3a712", "#29335c", "#669bbc", "#17bebb", "#8f2d56",
          "#76b041", "#ffc914", "#2e282a", "#c05746", "#4c6085", "#e0a890"]


def kopf(titel, rest=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{B}" height="{H}" '
            f'viewBox="0 0 {B} {H}">\n<title>{titel}</title>\n{rest}'
            f'<rect id="background" width="{B}" height="{H}" fill="#f4f1ea"/>\n')


def text(x, y, s, groesse=18, anker="middle", farbe="#2e282a", extra="", gewicht=400):
    return (f'<text x="{x}" y="{y}" font-family="{SCHRIFT}" font-size="{groesse}" font-weight="{gewicht}" '
            f'text-anchor="{anker}" fill="{farbe}"{extra}>{s}</text>\n')


def raster(namen, spalten, zeilen, oben=40):
    """Yields (x, y, w, h, name) per cell."""
    w = B / spalten
    h = (H - oben) / zeilen
    for i, n in enumerate(namen):
        yield (i % spalten) * w, oben + (i // spalten) * h, w, h, n


def speichern(name, inhalt):
    (ZIEL / name).write_text(inhalt + "</svg>\n", encoding="utf-8")


def zellen_mit_form(datei, titel, namen, spalten, zeilen, form="kreis"):
    s = kopf(titel) + text(B / 2, 30, titel, 22)
    for i, (x, y, w, h, n) in enumerate(raster(namen, spalten, zeilen)):
        cx, cy = x + w / 2, y + h / 2 - 12
        r = min(w, h) * 0.3
        f = FARBEN[i % len(FARBEN)]
        gid = n.lower().replace(" ", "-").replace("/", "-").replace("&", "and")
        s += f'<g id="{gid}">\n'
        if form == "kreis":
            s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{f}"/>\n'
        else:
            s += (f'<rect x="{cx - r:.1f}" y="{cy - r * 0.8:.1f}" width="{2 * r:.1f}" '
                  f'height="{1.6 * r:.1f}" fill="{f}"/>\n')
        s += text(cx, y + h - 14, n, 17)
        s += "</g>\n"
    speichern(datei, s)


def png(pfad, breite, hoehe, pixel):
    zeilen = []
    for y in range(hoehe):
        z = bytearray(b"\x00")
        for x in range(breite):
            z += bytes(pixel(x, y))
        zeilen.append(bytes(z))
    roh = b"".join(zeilen)

    def block(art, daten):
        return (struct.pack(">I", len(daten)) + art + daten
                + struct.pack(">I", zlib.crc32(art + daten) & 0xFFFFFFFF))
    ihdr = struct.pack(">IIBBBBB", breite, hoehe, 8, 2, 0, 0, 0)
    pfad.write_bytes(b"\x89PNG\r\n\x1a\n" + block(b"IHDR", ihdr)
                     + block(b"IDAT", zlib.compress(roh, 9)) + block(b"IEND", b""))


def main():
    ZIEL.mkdir(exist_ok=True)

    zellen_mit_form("01-layer-effects.svg", "Layer effects and live filters", [
        "Outer shadow", "Inner shadow", "Outer glow", "Inner glow",
        "Outline", "Bevel/Emboss", "3D", "Gaussian blur",
        "Colour overlay", "Gradient overlay", "Live Gaussian blur", "Live noise"], 4, 3)

    # Adjustment layers: one group per cell with a colour and a grey ramp
    titel = "Adjustment layers"
    s = kopf(titel, '<defs>\n<linearGradient id="regenbogen" x1="0" x2="1">'
             + "".join(f'<stop offset="{i / 6:.3f}" stop-color="{c}"/>' for i, c in enumerate(
                 ["#ff0000", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#ff00ff", "#ff0000"]))
             + '</linearGradient>\n<linearGradient id="grau" x1="0" x2="1">'
             '<stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/>'
             '</linearGradient>\n</defs>\n')
    s += text(B / 2, 30, titel, 22)
    for x, y, w, h, n in raster(["Levels", "Curves", "HSL", "Brightness/Contrast",
                                 "Black and White", "Invert", "Recolour", "Selective colour"], 4, 2):
        gid = n.lower().replace(" ", "-").replace("/", "-")
        s += f'<g id="{gid}">\n'
        s += f'<rect x="{x + 20:.1f}" y="{y + 20:.1f}" width="{w - 40:.1f}" height="{(h - 80) * 0.6:.1f}" fill="url(#regenbogen)"/>\n'
        s += f'<rect x="{x + 20:.1f}" y="{y + 20 + (h - 80) * 0.6:.1f}" width="{w - 40:.1f}" height="{(h - 80) * 0.4:.1f}" fill="url(#grau)"/>\n'
        s += "</g>\n" + text(x + w / 2, y + h - 30, n, 17)
    speichern("02-adjustment-layers.svg", s)

    # Brush strokes: grey guides to trace
    titel = "Brush strokes"
    s = kopf(titel) + text(B / 2, 30, titel, 22)
    for i, n in enumerate(["Pixel brush, pressure", "Vector brush, pressure", "Vector brush, no pressure",
                           "Pixel eraser over a stroke"]):
        y = 140 + i * 170
        s += (f'<path id="guide-{i + 1}" d="M 120 {y} C 350 {y - 90}, 600 {y + 90}, 850 {y} '
              f'S 1050 {y - 40}, 1100 {y}" fill="none" stroke="#bbb" stroke-width="2" stroke-dasharray="8 6"/>\n')
        s += text(120, y - 40, n, 17, "start")
    speichern("03-brush-strokes.svg", s)

    # Master page: header and footer, A4 portrait in points
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="595" height="842" viewBox="0 0 595 842">\n'
         '<title>Master page elements</title>\n')
    s += '<g id="header"><circle cx="70" cy="60" r="18" fill="#e4572e"/>'
    s += f'<line x1="100" y1="60" x2="545" y2="60" stroke="#29335c" stroke-width="1.5"/>'
    s += text(545, 50, "Sample document", 11, "end", extra="").rstrip() + "</g>\n"
    s += '<g id="footer"><line x1="50" y1="790" x2="545" y2="790" stroke="#29335c" stroke-width="1"/>'
    s += text(50, 808, "CC0 sample for photocraft#1606", 9, "start").rstrip()
    s += text(545, 808, "Page #", 9, "end").rstrip() + "</g>\n"
    (ZIEL / "04-master-page.svg").write_text(s + "</svg>\n", encoding="utf-8")

    # Symbol: a small flower
    blatt = "".join(
        f'<ellipse cx="0" cy="-34" rx="14" ry="30" fill="#f3a712" transform="rotate({a})"/>'
        for a in range(0, 360, 45))
    titel = "Symbols and embedded documents"
    s = kopf(titel) + text(B / 2, 30, titel, 22)
    s += f'<g id="flower" transform="translate(220 260)">{blatt}<circle r="16" fill="#8f2d56"/></g>\n'
    s += text(220, 380, "Make this a symbol, place 3 instances", 17)
    s += text(800, 380, "Place 05b-embedded.svg here as embedded document", 17)
    s += '<rect x="560" y="120" width="480" height="220" fill="none" stroke="#bbb" stroke-dasharray="8 6"/>\n'
    s += text(B / 2, 560, "Instance 2: recolour centre (override)   Instance 3: scale 150 %", 17)
    speichern("05-symbols.svg", s)

    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">\n'
         '<title>Embedded</title><rect width="400" height="200" rx="16" fill="#29335c"/>\n'
         '<circle cx="100" cy="100" r="60" fill="#17bebb"/><rect x="190" y="50" width="160" height="100" fill="#ffc914"/>\n')
    (ZIEL / "05b-embedded.svg").write_text(s + "</svg>\n", encoding="utf-8")

    # Special shapes: labelled grid only
    titel = "Special shapes (draw with Affinity's shape tools in each cell)"
    s = kopf(titel) + text(B / 2, 30, titel, 22)
    for x, y, w, h, n in raster(["Cloud", "Heart", "Cog", "Callout rounded", "Callout ellipse",
                                 "Arrow", "Double star", "Tear", "Crescent", "Donut", "Pie",
                                 "Segment", "Diamond", "Trapezoid", "Square star", "Polygon"], 4, 4):
        s += f'<rect x="{x + 8:.1f}" y="{y + 6:.1f}" width="{w - 16:.1f}" height="{h - 12:.1f}" fill="none" stroke="#ccc"/>\n'
        s += text(x + w / 2, y + h - 16, n, 16)
    speichern("06-special-shapes.svg", s)

    # Transparency: opacity, gradient with alpha, pattern fill
    titel = "Transparency"
    s = kopf(titel, '<defs><linearGradient id="alpha" x1="0" x2="1">'
             '<stop offset="0" stop-color="#29335c" stop-opacity="1"/>'
             '<stop offset="1" stop-color="#29335c" stop-opacity="0"/></linearGradient>'
             '<pattern id="muster" width="32" height="32" patternUnits="userSpaceOnUse">'
             '<image href="07-texture.png" xlink:href="07-texture.png" width="32" height="32"/></pattern></defs>\n')
    s += text(B / 2, 30, titel, 22)
    # Stripes behind, so transparency shows
    for i in range(12):
        s += f'<rect x="{i * 100}" y="40" width="50" height="{H - 40}" fill="#ddd"/>\n'
    for x, y, w, h, n in raster(["Fill opacity 50 %", "Layer opacity 50 %", "Gradient fill with alpha",
                                 "Transparency tool (linear)", "Transparency tool (radial)",
                                 "Bitmap fill (07-texture.png)"], 3, 2):
        cx, cy = x + w / 2, y + h / 2 - 15
        nid = n.split(" (")[0].lower().replace(" ", "-").replace("%", "pc")
        if n.startswith("Fill opacity"):
            f = 'fill="#e4572e" fill-opacity="0.5"'
        elif n.startswith("Layer opacity"):
            f = 'fill="#e4572e" opacity="0.5"'
        elif n.startswith("Gradient"):
            f = 'fill="url(#alpha)"'
        elif n.startswith("Bitmap"):
            f = 'fill="url(#muster)"'
        else:
            f = 'fill="#e4572e"'
        s += f'<rect id="{nid}" x="{cx - 130:.1f}" y="{cy - 90:.1f}" width="260" height="180" {f}/>\n'
        s += text(cx, y + h - 20, n, 17)
    speichern("07-transparency.svg", s)

    def textur(x, y):
        a = ((x // 8) + (y // 8)) % 2
        return (228, 87, 46) if a else (255, 201, 20)
    png(ZIEL / "07-texture.png", 32, 32, textur)

    # Gradients
    titel = "Gradients"
    s = kopf(titel, '<defs><linearGradient id="lin"><stop offset="0" stop-color="#e4572e"/>'
             '<stop offset="1" stop-color="#29335c"/></linearGradient>'
             '<radialGradient id="rad"><stop offset="0" stop-color="#ffc914"/>'
             '<stop offset="1" stop-color="#8f2d56"/></radialGradient></defs>\n')
    s += text(B / 2, 30, titel, 22)
    for i, (x, y, w, h, n) in enumerate(raster(["Linear (reference)", "Radial (reference)",
                                                "Elliptical", "Conical", "Conical, 3 stops",
                                                "Conical, off-centre"], 3, 2)):
        cx, cy = x + w / 2, y + h / 2 - 15
        f = "url(#lin)" if i == 0 else "url(#rad)" if i == 1 else "#cccccc"
        s += f'<circle id="g{i + 1}" cx="{cx:.1f}" cy="{cy:.1f}" r="120" fill="{f}"/>\n'
        s += text(cx, y + h - 20, n, 17)
    speichern("08-gradients.svg", s)

    zellen_mit_form("09-corners-stars.svg", "Corner types and stars", [
        "Rounded (reference)", "Straight", "Concave", "Inset",
        "Mixed per corner", "Smooth", "Star, rounded points", "Star, rounded inner"], 4, 2, "rechteck")

    zellen_mit_form("10-multiple-fills.svg", "Several fills and strokes on one object", [
        "2 fills", "2 strokes", "Fill + 2 strokes", "Gradient over solid fill",
        "Stroke inside + outside", "3 fills, middle hidden"], 3, 2, "rechteck")

    # Text
    absatz = ("PhotoCraft reads Affinity documents. This frame has two columns and a gutter "
              "of twelve points, so the text flows from the left column into the right one. "
              "It is long enough to fill both columns at this size. Kerning, tracking and "
              "leading stay at their defaults. The last line ends here.")
    titel = "Text"
    s = kopf(titel, '<defs><path id="bogen" d="M 640 300 A 220 140 0 0 1 1080 300"/></defs>\n')
    s += text(B / 2, 30, titel, 22)
    s += text(80, 120, "Outlined text", 48, "start", "#29335c", ' id="outlined"', 700)
    s += text(80, 150, "convert to curves", 14, "start")
    s += text(80, 260, "Scaled text", 48, "start", "#8f2d56", ' id="scaled" transform="matrix(0.6 0 0 1 32 0)"')
    s += text(80, 290, "horizontal scale 60 %", 14, "start")
    s += (f'<text id="on-path" font-family="{SCHRIFT}" font-size="28" font-weight="400" fill="#e4572e">'
          f'<textPath href="#bogen" xlink:href="#bogen">Text on a curved path</textPath></text>\n')
    s += '<use href="#bogen" xlink:href="#bogen" fill="none" stroke="#ccc"/>\n'
    s += text(860, 330, "text on path", 14)
    s += f'<text id="columns" font-family="{SCHRIFT}" font-size="15" font-weight="400" fill="#2e282a">\n'
    woerter, zeile, zeilen = absatz.split(), "", []
    for wd in woerter:
        if len(zeile) + len(wd) > 70:
            zeilen.append(zeile)
            zeile = ""
        zeile += wd + " "
    zeilen.append(zeile)
    for i, z in enumerate(zeilen):
        s += f'<tspan x="80" y="{420 + i * 22}">{z.strip()}</tspan>\n'
    s += "</text>\n"
    s += text(80, 400, "paste into a frame with 2 columns", 14, "start")
    s += text(700, 420, "Field: page number", 14, "start")
    s += text(700, 480, "Field: file name", 14, "start")
    s += text(700, 540, "Frame with an elliptical outline", 14, "start")
    s += '<ellipse cx="900" cy="660" rx="200" ry="100" fill="none" stroke="#ccc" stroke-dasharray="6 4"/>\n'
    speichern("11-text.svg", s)

    # Test chart for the colour formats
    titel = "Colour formats test chart"
    s = kopf(titel, '<defs><linearGradient id="verlauf" x1="0" x2="1">'
             '<stop offset="0" stop-color="#00ffff"/><stop offset="0.5" stop-color="#ff00ff"/>'
             '<stop offset="1" stop-color="#ffff00"/></linearGradient></defs>\n')
    s += text(B / 2, 30, titel, 22)
    felder = ["#ff0000", "#00ff00", "#0000ff", "#00ffff", "#ff00ff", "#ffff00", "#000000", "#ffffff"]
    for i, c in enumerate(felder):
        s += f'<rect x="{60 + i * 135}" y="80" width="120" height="120" fill="{c}" stroke="#999"/>\n'
        s += text(120 + i * 135, 225, c, 14)
    for i in range(21):
        g = round(i * 255 / 20)
        s += f'<rect x="{60 + i * 51.4:.1f}" y="270" width="51.4" height="100" fill="rgb({g},{g},{g})"/>\n'
    s += f'<rect x="60" y="420" width="1080" height="140" fill="url(#verlauf)"/>\n'
    s += text(B / 2, 640, "Save as: RGB 16-bit, RGB 32-bit, CMYK 8-bit, Lab 16-bit, Grey 8-bit", 18)
    speichern("12-colour-formats.svg", s)

    # Blend modes
    titel = "Affinity-only blend modes"
    s = kopf(titel, '<defs><linearGradient id="unten" x1="0" x2="1">'
             '<stop offset="0" stop-color="#29335c"/><stop offset="0.5" stop-color="#17bebb"/>'
             '<stop offset="1" stop-color="#f4f1ea"/></linearGradient></defs>\n')
    s += text(B / 2, 30, titel, 22)
    for i, (x, y, w, h, n) in enumerate(raster(["Normal (reference)", "Average", "Negation",
                                                "Reflect", "Glow", "Erase"], 3, 2)):
        cx, cy = x + w / 2, y + h / 2 - 15
        s += f'<g id="{n.split(" ")[0].lower()}">\n'
        s += f'<rect x="{cx - 150:.1f}" y="{cy - 100:.1f}" width="300" height="200" fill="url(#unten)"/>\n'
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="80" fill="#e4572e"/>\n</g>\n'
        s += text(cx, y + h - 20, n + ("" if i == 0 else ": set on the circle"), 17)
    speichern("13-blend-modes.svg", s)


if __name__ == "__main__":
    main()
