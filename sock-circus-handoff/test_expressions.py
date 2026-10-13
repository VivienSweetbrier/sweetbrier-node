import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "comparison-64-128" / "sock_head_128.png"
EXPECTED = "71170b8088336bfc1974c123faa8472d6e2746c127413dd339113195d959cb00"

class ExpressionTests(unittest.TestCase):
    def test_expressions_change_only_the_eyes_and_mouth(self):
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),EXPECTED)
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            run = subprocess.run([sys.executable,str(ROOT / "animate_sock.py"),"--out",directory],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            manifest = json.loads((out / "expressions.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest["states"]),{"neutral","blink_half","blink_closed","talk_small","talk_open","talk_round","glitch"})
            with Image.open(BASE) as b:
                baseline = b.convert("RGBA")
            with Image.open(out / "movement-mask.png") as m:
                mask = m.convert("L")
            fingerprints = set()
            palette = set(baseline.get_flattened_data())
            for state in manifest["states"]:
                with Image.open(out / (state+".png")) as f:
                    frame = f.convert("RGBA")
                self.assertEqual(frame.size,(128,128))
                self.assertLessEqual(set(frame.get_flattened_data()),palette)
                self.assertEqual(frame.getchannel("A").tobytes(),baseline.getchannel("A").tobytes())
                if state=="neutral":
                    self.assertEqual(frame.tobytes(),baseline.tobytes())
                else:
                    self.assertNotEqual(frame.tobytes(),baseline.tobytes())
                fingerprints.add(hashlib.sha256(frame.tobytes()).hexdigest())
                for y in range(128):
                    for x in range(128):
                        if not mask.getpixel((x,y)):
                            self.assertEqual(frame.getpixel((x,y)),baseline.getpixel((x,y)),(state,x,y))
            self.assertEqual(len(fingerprints),len(manifest["states"]))
        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(),EXPECTED)

    def test_gifs_decode_to_the_exact_states_with_timing_and_transparency(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            run = subprocess.run([sys.executable,str(ROOT / "animate_sock.py"),"--out",directory],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue((out / "sock_alive_128.gif").exists(),"No real native animation produced")
            manifest = json.loads((out / "expressions.json").read_text(encoding="utf-8"))
            timeline = manifest["timeline"]
            checker = Image.new("RGBA",(512,512),tuple(manifest["preview"]["background_colours"][0]))
            d = ImageDraw.Draw(checker)
            for y in range(0,512,16):
                for x in range(0,512,16):
                    if (x//16+y//16)%2:
                        d.rectangle((x,y,x+15,y+15),fill=tuple(manifest["preview"]["background_colours"][1]))
            for filename,size in [("sock_alive_128.gif",(128,128)),("sock_alive_preview.gif",(512,512))]:
                with Image.open(out / filename) as gif:
                    self.assertEqual(gif.size,size)
                    self.assertEqual(gif.info["loop"],0)
                    self.assertEqual(gif.n_frames,len(timeline))
                    total = 0
                    union = set()
                    for i,item in enumerate(timeline):
                        gif.seek(i)
                        total += gif.info["duration"]
                        self.assertEqual(gif.info["duration"],item["ms"])
                        with Image.open(out / (item["state"]+".png")) as p:
                            expected=p.convert("RGBA")
                        if size==(512,512):
                            panel=checker.copy()
                            panel.alpha_composite(expected.resize(size,Image.Resampling.NEAREST))
                            expected=panel
                        actual=gif.convert("RGBA")
                        union.update(actual.get_flattened_data())
                        self.assertEqual(actual.tobytes(),expected.tobytes(),(filename,i,item))
                    self.assertEqual(total,manifest["total_ms"])
                    self.assertLessEqual(len(union),16)

    def test_spritesheet_cells_are_the_exported_native_states(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            run=subprocess.run([sys.executable,str(ROOT / "animate_sock.py"),"--out",directory],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue((out / "sock_expressions_128.png").exists(),"Missing native spritesheet")
            manifest=json.loads((out / "expressions.json").read_text(encoding="utf-8"))
            with Image.open(out / "sock_expressions_128.png") as strip:
                self.assertEqual(strip.size,(128*len(manifest["states"]),128))
                for entry in manifest["frame_layout"]:
                    x,y,w,h=entry["rect"]
                    with Image.open(out / (entry["state"]+".png")) as frame:
                        self.assertEqual(strip.crop((x,y,x+w,y+h)).tobytes(),frame.tobytes())
            with Image.open(out / "expression-sheet.png") as board:
                board.verify()

    def test_talking_revision_is_smaller_and_other_poses_are_unchanged(self):
        from animate_sock import build_states
        frames,_,_,_=build_states()
        for state in ("neutral","blink_half","blink_closed","glitch"):
            with Image.open(ROOT / "expressions-128" / (state+".png")) as previous:
                self.assertEqual(frames[state].tobytes(),previous.convert("RGBA").tobytes(),state)
        roi=(48,84,75,99)
        for state in ("talk_small","talk_open","talk_round"):
            with self.subTest(state=state):
                with Image.open(ROOT / "expressions-128" / (state+".png")) as previous:
                    old=sum(p==(0,0,0,255) for p in previous.convert("RGBA").crop(roi).get_flattened_data())
                new=sum(p==(0,0,0,255) for p in frames[state].crop(roi).get_flattened_data())
                self.assertLess(new,old,"Talking mouth did not become smaller")

if __name__=="__main__":
    unittest.main(verbosity=2)
