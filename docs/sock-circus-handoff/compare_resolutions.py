"""Native-resolution comparison. Never edits the approved 64-pixel asset."""
import argparse
import hashlib
import shutil
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from build_study import render_head

ROOT = Path(__file__).resolve().parent


def write_comparison(model, native128, out):
    approved = ROOT / "output" / "sock_head_64.png"
    approved_hash = hashlib.sha256(approved.read_bytes()).hexdigest()
    shutil.copyfile(approved, out / "sock_head_64.png")
    with Image.open(approved) as original:
        native64 = original.convert("RGBA")
    display_size = (512,512)
    margin, gap, panel_top = 24,24,132
    width = margin*2 + display_size[0]*2 + gap
    height = panel_top + display_size[1] + 94
    board = Image.new("RGB",(width,height),"#f0ece4")
    d = ImageDraw.Draw(board)
    def font(size, bold=False):
        name = "arialbd.ttf" if bold else "arial.ttf"
        path = Path("C:/Windows/Fonts") / name
        return ImageFont.truetype(str(path),size) if path.exists() else ImageFont.load_default(size=size)
    def checker():
        panel = Image.new("RGBA",display_size,"#d9d5cd")
        pd = ImageDraw.Draw(panel)
        for y in range(0,512,16):
            for x in range(0,512,16):
                if (x//16+y//16)%2:
                    pd.rectangle((x,y,x+15,y+15),fill="#cbc8c1")
        return panel
    d.text((24,20),"SOCK / DASH - SAME FACE, MORE ROOM",fill="#242333",font=font(28,True))
    d.text((24,60),"A native-grid comparison. Same framing, expression and palette; no body or animation yet.",fill="#605e69",font=font(17))
    panels = []
    for i,(im,n,title) in enumerate([(native64,64,"64 x 64 / APPROVED FIRST STUDY"),(native128,128,"128 x 128 / NATIVE REDRAW")]):
        x = margin + i*(512+gap)
        d.text((x,100),title,fill="#242333",font=font(20,True))
        enlarged = im.resize(display_size,Image.Resampling.NEAREST)
        enlarged.save(out / f"sock_head_{n}_display.png")
        bg = checker()
        bg.alpha_composite(enlarged)
        board.paste(bg.convert("RGB"),(x,panel_top))
        panels.append({"native_file":f"sock_head_{n}.png","native_size":[n,n],"top_left":[x,panel_top],"display_scale":512//n})
    d.text((24,668),"Both heads occupy the same display area. The right-hand version is NOT an enlarged 64-pixel PNG.",fill="#242333",font=font(17))
    d.text((24,700),"Look at the eye shapes, triangular nose, cheek seams and hair tips. Same 16-entry palette budget.",fill="#605e69",font=font(17))
    board.save(out / "comparison.png")
    doubled64 = native64.resize((128,128),Image.Resampling.NEAREST)
    changed = sum(a!=b for a,b in zip(doubled64.get_flattened_data(),native128.get_flattened_data()))
    manifest = {"approved_64_sha256":approved_hash,
                "source_model_sha256":hashlib.sha256((ROOT / "head_model.json").read_bytes()).hexdigest(),
                "rendering_method":"128x128 rasterized directly from source-space shape data; never resized from 64x64",
                "display_panel_size":list(display_size),"board_size":[width,height],"panels":panels,
                "native_pixels_different_from_2x_enlargement":changed,
                "native_64_palette_entries":len(native64.getcolors(16385)),
                "native_128_palette_entries":len(native128.getcolors(16385)),
                "palette_limit_including_transparency":16,
                "palette":model["palette"],"antialiasing":False,
                "approval":"64x64 likeness accepted by user; 128x128 awaiting comparison feedback"}
    (out / "comparison.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    (out / "head_model_128.json").write_text(json.dumps(model,indent=2),encoding="utf-8")
    assert hashlib.sha256(approved.read_bytes()).hexdigest()==approved_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "comparison-64-128")
    args = parser.parse_args()
    model = json.loads((ROOT / "head_model.json").read_text(encoding="utf-8"))
    model["canvas"] = [128,128]
    image, _, _ = render_head(model)
    args.out.mkdir(parents=True, exist_ok=True)
    image.save(args.out / "sock_head_128.png")
    write_comparison(model,image,args.out)
    print(json.dumps({"native_size":image.size,"palette_entries":len(image.getcolors(16385)),"file":str(args.out / "sock_head_128.png")}))


if __name__ == "__main__":
    main()
