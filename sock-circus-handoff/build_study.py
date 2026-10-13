"""Reference-guided Sock/Dash study. Pillow only; originals are read-only."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent


def render_head(model, detailed=True):
    """Rasterize named construction shapes directly on the native pixel grid."""
    size = tuple(model["canvas"])
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    colours = {key: tuple(value) for key, value in model["palette"].items()}
    x0, y0, x1, y1 = model["viewport_in_local_coordinates"]

    def point(p):
        return (round((p[0] - x0) * size[0] / (x1 - x0)),
                round((p[1] - y0) * size[1] / (y1 - y0)))

    def polygon(points, role):
        d.polygon([point(p) for p in points], fill=colours[role])

    polygon(model["silhouette"], "ink")
    silhouette = image.copy()
    if detailed:
        for lock in model["hair_locks"]:
            polygon(lock["polygon"], lock["colour"])
    polygon(model["face_outline"], "face_shadow" if detailed else "ivory")
    if detailed:
        polygon(model["face_inner"], "ivory")
    planes = image.copy()
    if detailed:
        for seam in model["seams"]:
            d.line([point(p) for p in seam], fill=colours["seam"], width=1)
    for eye in model["eyes"]:
        a, b, c, e = eye["bbox"]
        d.ellipse((*point((a, b)), *point((c, e))), fill=colours["ink"])
        d.point(point(eye["glint"]), fill=colours["ivory"])
    for stitch in model["eye_stitches"]:
        d.point(point(stitch), fill=colours["ink"])
    polygon(model["nose"], "nose_shadow")
    polygon([[239, 295], [252, 320], [232, 322]], "nose_red")
    d.point(point((235, 312)), fill=colours["nose_light"])
    d.line([point(p) for p in model["mouth"]], fill=colours["ink"], width=1)
    for bang in model["bangs"]:
        if detailed or bang["colour"] == "ink":
            polygon(bang["polygon"], bang["colour"])
    # Native polygons only: no resampled source pixels, blur, or partial alpha.
    return image, silhouette, planes


def write_review_package(model, image, silhouette, planes, out):
    """Keep annotations inspectable and present each drawing stage separately."""
    source = Path(model["primary_source"])
    origin = model["coordinate_origin_in_primary"]
    x0, y0, x1, y1 = model["viewport_in_local_coordinates"]
    landmarks = {}
    for name, (x, y) in model["landmarks"].items():
        u, v = (x-x0)/(x1-x0), (y-y0)/(y1-y0)
        landmarks[name] = {"source_pixel": [x+origin[0], y+origin[1]],
                           "normalized_in_draft_frame": [u, v],
                           "native_pixel": [round(u*64), round(v*64)]}
    record = {"annotation_method": "Manual approximate tracing, followed by deterministic native-grid snapping",
              "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "secondary_source": model["secondary_source"],
              "secondary_source_sha256": hashlib.sha256(Path(model["secondary_source"]).read_bytes()).hexdigest(),
              "canvas": [64, 64], "landmarks": landmarks,
              "colours_used_including_transparency": len(image.getcolors(4097)),
              "palette_limit_including_transparency": 16, "palette": model["palette"],
              "palette_measurements": model["palette_measurements"],
              "status": "Unapproved face-and-hair study; no animation or body"}
    (out / "construction.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    silhouette.save(out / "silhouette_64.png")
    planes.save(out / "planes_64.png")
    crop = model["reference_display_crop"]
    with Image.open(source) as original:
        guide = original.convert("RGB").crop(crop)
    gd = ImageDraw.Draw(guide)
    def ref(p):
        return p[0]+origin[0]-crop[0], p[1]+origin[1]-crop[1]
    for field, colour in [("silhouette", "#60edcf"), ("face_outline", "#ffb4c8")]:
        points = [ref(p) for p in model[field]]
        gd.line(points+[points[0]], fill=colour, width=2)
    gd.line([ref(model["landmarks"]["eye_viewer_left"]), ref(model["landmarks"]["eye_viewer_right"])], fill="#fddb64", width=2)
    for p in model["landmarks"].values():
        x, y = ref(p)
        gd.ellipse((x-4,y-4,x+4,y+4), fill="#fddb64", outline="#181823", width=1)
    guide.save(out / "reference-guide.png")

    def font(size, bold=False):
        path = Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf")
        return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)
    def checker(size):
        b = Image.new("RGBA", size, "#d9d5cd")
        bd = ImageDraw.Draw(b)
        for y in range(0, size[1], 16):
            for x in range(0, size[0], 16):
                if (x//16+y//16)%2:
                    bd.rectangle((x,y,x+15,y+15), fill="#cbc8c1")
        return b
    def pixel_panel(sprite, x, y, scale):
        b = checker((64*scale,64*scale))
        b.alpha_composite(sprite.resize(b.size, Image.Resampling.NEAREST))
        board.paste(b.convert("RGB"), (x,y))

    board = Image.new("RGB", (1200, 720), "#f0ece4")
    bd = ImageDraw.Draw(board)
    ink, muted = "#242333", "#605e69"
    bd.text((24,20), "SOCK / DASH  -  HEAD STUDY 01", font=font(28,True), fill=ink)
    bd.text((24,58), "Reference-guided construction. Face + hair only. Your likeness check comes before animation.", font=font(17), fill=muted)
    bd.text((24,96), "01  REFERENCE + HAND ANNOTATIONS", font=font(15,True), fill=ink)
    bd.text((432,96), "02  SILHOUETTE", font=font(15,True), fill=ink)
    bd.text((660,96), "04  NATIVE 64 x 64 DRAFT / 8x DISPLAY", font=font(15,True), fill=ink)
    board.paste(guide.resize((384,384), Image.Resampling.LANCZOS), (24,124))
    pixel_panel(silhouette,432,124,3)
    bd.text((432,336), "03  FLAT SHAPES", font=font(15,True), fill=ink)
    pixel_panel(planes,432,360,3)
    pixel_panel(image,660,124,8)
    bd.text((24,524), "Mint: hair contour   Pink: face contour", font=font(15), fill=muted)
    bd.text((24,548), "Gold: eye line + editable facial landmarks", font=font(15), fill=muted)
    bd.text((24,586), "SAMPLED CHARACTER PALETTE", font=font(15,True), fill=ink)
    used = [tuple(c) for c in model["palette"].values() if c[3]]
    for i, colour in enumerate(used):
        x = 24+i*34
        bd.rectangle((x,614,x+27,641), fill=colour[:3], outline="#89838c", width=1)
    bd.text((24,657), f"{record['colours_used_including_transparency']} entries used including transparency / 16 allowed. No antialiasing on sprite.", font=font(16), fill=ink)
    bd.text((24,683), "Study, not final: keep or change her expression and proportions before adding the body.", font=font(16), fill=muted)
    board.save(out / "study-board.png")
    # Export the raster as ASCII only AFTER drawing; the geometry is the source of truth.
    alphabet = ".Kabcdefghij"
    colour_to_char = {tuple(c): alphabet[i] for i,c in enumerate(model["palette"].values())}
    rows = ["".join(colour_to_char[image.getpixel((x,y))] for x in range(64)) for y in range(64)]
    (out / "head-grid.txt").write_text("\n".join(rows)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    model = json.loads((ROOT / "head_model.json").read_text(encoding="utf-8"))
    image, silhouette, planes = render_head(model)
    args.out.mkdir(parents=True, exist_ok=True)
    image.save(args.out / "sock_head_64.png")
    image.resize((512, 512), Image.Resampling.NEAREST).save(args.out / "sock_head_8x.png")
    flat, _, _ = render_head(model, detailed=False)
    write_review_package(model, image, silhouette, flat, args.out)
    print(json.dumps({"file": str(args.out / "sock_head_64.png"),
                      "size": image.size, "colour_entries_used": len(image.getcolors(4097))}))


if __name__ == "__main__":
    main()
