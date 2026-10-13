"""Sock expression patches. Only approved eye/mouth regions may change."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from build_study import render_head

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "comparison-64-128" / "sock_head_128.png"


def build_states():
    model = json.loads((ROOT / "comparison-64-128/head_model_128.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "expression_model_128.json").read_text(encoding="utf-8"))
    selection = json.loads((ROOT / "CURRENT_DRAFT.json").read_text(encoding="utf-8"))
    if hashlib.sha256(BASE.read_bytes()).hexdigest() != selection["selected"]["sha256"]:
        raise ValueError("Approved baseline changed; select it explicitly before animating")
    with Image.open(BASE) as source:
        baseline = source.convert("RGBA")
    rendered, _, plate = render_head(model)
    if rendered.tobytes() != baseline.tobytes():
        raise ValueError("Construction no longer reproduces the approved baseline")
    colours = {key:tuple(value) for key,value in model["palette"].items()}
    x0,y0,x1,y1 = model["viewport_in_local_coordinates"]
    def point(p):
        return round((p[0]-x0)*128/(x1-x0)),round((p[1]-y0)*128/(y1-y0))
    pd = ImageDraw.Draw(plate)
    for seam in model["seams"]:
        pd.line([point(p) for p in seam],fill=colours["seam"],width=1)
    for stitch in model["eye_stitches"]:
        pd.point(point(stitch),fill=colours["ink"])
    # Protect fringe and nose even where the rectangular mouth patch overlaps them.
    protected = Image.new("L",(128,128),0)
    protect_draw = ImageDraw.Draw(protected)
    for bang in model["bangs"]:
        points = [point(p) for p in bang["polygon"]]
        pd.polygon(points,fill=colours[bang["colour"]])
        protect_draw.polygon(points,fill=255)
    nose_mask = Image.new("L",(128,128),0)
    ImageDraw.Draw(nose_mask).polygon([point(p) for p in model["nose"]],fill=255)
    protected = ImageChops.lighter(protected,nose_mask.filter(ImageFilter.MaxFilter(3)))
    face_mask = Image.new("L",(128,128),0)
    ImageDraw.Draw(face_mask).polygon([point(p) for p in model["face_outline"]],fill=255)
    allowed = ImageChops.subtract(face_mask,protected)
    boxes = [(*point(eye["bbox"][:2]),*point(eye["bbox"][2:])) for eye in model["eyes"]]
    areas = {}
    for name,box in zip(("left_eye","right_eye"),boxes):
        a,b,c,d = box
        mask = Image.new("L",(128,128),0)
        ImageDraw.Draw(mask).rectangle((a-1,b-1,c+1,d+1),fill=255)
        areas[name] = ImageChops.multiply(mask,allowed)
    mask = Image.new("L",(128,128),0)
    ImageDraw.Draw(mask).rectangle(config["mouth_box"],fill=255)
    areas["mouth"] = ImageChops.multiply(mask,allowed)
    movement = ImageChops.lighter(ImageChops.lighter(areas["left_eye"],areas["right_eye"]),areas["mouth"])
    frames = {}
    for name,spec in config["states"].items():
        if name=="neutral":
            frames[name]=baseline.copy()
            continue
        work = plate.copy()
        d = ImageDraw.Draw(work)
        active = Image.new("L",(128,128),0)
        if spec["eyes"] in ("half","closed"):
            for box in boxes:
                a,b,c,e = box
                cx,cy = (a+c)//2,(b+e)//2
                if spec["eyes"]=="half":
                    d.ellipse((a,cy-1,c,e),fill=colours["ink"])
                    d.line((a,cy-1,c,cy-1),fill=colours["seam"],width=1)
                else:
                    d.line([(a,cy),(a+2,cy+1),(cx,cy+2),(c-2,cy+1),(c,cy-1)],fill=colours["ink"],width=1)
            active = ImageChops.lighter(areas["left_eye"],areas["right_eye"])
        elif spec["eyes"]=="right_cross":
            a,b,c,e = boxes[1]
            d.line((a+1,b+1,c-1,e-1),fill=colours["ink"],width=1)
            d.line((a+1,e-1,c-1,b+1),fill=colours["ink"],width=1)
            d.point(((a+c)//2,(b+e)//2),fill=colours["hair_glint"])
            active = areas["right_eye"].copy()
        if spec["mouth"]!="original":
            active = ImageChops.lighter(active,areas["mouth"])
            if spec["mouth"] in ("small","open"):
                d.polygon([tuple(p) for p in spec["polygon"]],fill=colours["ink"])
                if "tongue" in spec:
                    d.polygon([tuple(p) for p in spec["tongue"]],fill=colours["nose_red"])
            elif spec["mouth"]=="round":
                d.ellipse(spec["bbox"],fill=colours["ink"])
            elif spec["mouth"]=="jagged":
                d.line([tuple(p) for p in spec["line"]],fill=colours["ink"],width=1)
        frames[name] = Image.composite(work,baseline,active)
    return frames,movement,model,config


def save_animations(frames,model,config,out):
    palette = [tuple(c) for c in model["palette"].values()]
    backgrounds = [(217,213,205,255),(203,200,193,255)]
    preview_palette = palette + backgrounds
    def indexed(image,colours):
        lookup = {c:i for i,c in enumerate(colours)}
        p = Image.new("P",image.size)
        flat = [channel for colour in colours for channel in colour[:3]]
        p.putpalette(flat+[0]*(16*3-len(flat)))
        # Explicit RGBA lookup keeps transparent black and opaque black distinct.
        p.frombytes(bytes(lookup[c] for c in image.get_flattened_data()))
        return p
    native = {name:indexed(image,palette) for name,image in frames.items()}
    checker = Image.new("RGBA",(512,512),backgrounds[0])
    cd = ImageDraw.Draw(checker)
    for y in range(0,512,16):
        for x in range(0,512,16):
            if (x//16+y//16)%2:
                cd.rectangle((x,y,x+15,y+15),fill=backgrounds[1])
    previews = {}
    for name,image in frames.items():
        panel = checker.copy()
        panel.alpha_composite(image.resize((512,512),Image.Resampling.NEAREST))
        previews[name] = indexed(panel,preview_palette)
    sequence = [step["state"] for step in config["timeline"]]
    durations = [step["ms"] for step in config["timeline"]]
    ordered = [native[name] for name in sequence]
    ordered[0].save(out / "sock_alive_128.gif",save_all=True,append_images=ordered[1:],
                    duration=durations,loop=0,disposal=2,transparency=0,background=0,optimize=False)
    ordered = [previews[name] for name in sequence]
    ordered[0].save(out / "sock_alive_preview.gif",save_all=True,append_images=ordered[1:],
                    duration=durations,loop=0,disposal=2,background=len(palette),optimize=False)
    return {"native_gif_frames":len(sequence),"preview":{"size":[512,512],"background_colours":backgrounds,
            "note":"Checkerboard adds two display-only colours; native sprites use only the approved palette."}}


def save_expression_sheet(frames,config,out):
    strip=Image.new("RGBA",(128*len(frames),128),(0,0,0,0))
    layout=[]
    columns,scale,margin,gap,top=4,2,24,24,112
    cell=128*scale
    row_height=cell+48
    rows=(len(frames)+columns-1)//columns
    board=Image.new("RGB",(margin*2+columns*cell+(columns-1)*gap,top+rows*row_height+24),"#f0ece4")
    d=ImageDraw.Draw(board)
    def font(size,bold=False):
        p=Path("C:/Windows/Fonts")/("arialbd.ttf" if bold else "arial.ttf")
        return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default(size=size)
    d.text((margin,22),"SOCK / THE EXPRESSION LAB",font=font(30,True),fill="#242333")
    d.text((margin,64),f"{len(frames)} native 128 x 128 states. Same doll; only her eyes and mouth change.",font=font(18),fill="#605e69")
    for i,(name,image) in enumerate(frames.items()):
        strip.paste(image,(i*128,0))
        layout.append({"state":name,"rect":[i*128,0,128,128]})
        x=margin+(i%columns)*(cell+gap)
        y=top+(i//columns)*row_height
        d.text((x,y),config["states"][name]["label"].upper(),font=font(18,True),fill="#242333")
        panel=Image.new("RGBA",(cell,cell),(217,213,205,255))
        pd=ImageDraw.Draw(panel)
        for py in range(0,cell,16):
            for px in range(0,cell,16):
                if (px//16+py//16)%2:
                    pd.rectangle((px,py,px+15,py+15),fill=(203,200,193,255))
        panel.alpha_composite(image.resize((cell,cell),Image.Resampling.NEAREST))
        board.paste(panel.convert("RGB"),(x,y+28))
    x=margin+3*(cell+gap)
    y=top+row_height+36
    d.text((x,y),"STAYS FIXED",font=font(17,True),fill="#242333")
    d.text((x,y+30),"Hair, nose and head position",font=font(16),fill="#605e69")
    d.text((x,y+80),"GETS TO PLAY",font=font(17,True),fill="#242333")
    d.text((x,y+110),"Eyelids, mouth and one X-eye",font=font(16),fill="#605e69")
    d.text((x,y+158),"Silent visual test.",font=font(16),fill="#605e69")
    d.text((x,y+184),"No audio-driven lip sync yet.",font=font(16),fill="#605e69")
    strip.save(out / "sock_expressions_128.png")
    board.save(out / "expression-sheet.png")
    return {"frame_layout":layout,"sheet_size":list(strip.size)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=ROOT / "expressions-128-soft-v2")
    args = parser.parse_args()
    frames,movement,model,config = build_states()
    args.out.mkdir(parents=True,exist_ok=True)
    for name,image in frames.items():
        image.save(args.out / (name+".png"))
    movement.save(args.out / "movement-mask.png")
    manifest = {"native_size":[128,128],"states":list(frames),"palette":model["palette"],
                "baseline_sha256":hashlib.sha256(BASE.read_bytes()).hexdigest(),
                "timeline":config["timeline"],"scope":config["scope"],
                "total_ms":sum(item["ms"] for item in config["timeline"]),
                "changed_pixels":{name:sum(a!=b for a,b in zip(image.get_flattened_data(),frames["neutral"].get_flattened_data())) for name,image in frames.items()}}
    manifest.update(save_animations(frames,model,config,args.out))
    manifest.update(save_expression_sheet(frames,config,args.out))
    (args.out / "expressions.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps({"states":len(frames),"output":str(args.out),"total_ms":manifest["total_ms"]}))


if __name__=="__main__":
    main()
