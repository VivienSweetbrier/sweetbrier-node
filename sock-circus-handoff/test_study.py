import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent

class SpriteTests(unittest.TestCase):
    def test_renders_a_transparent_64_pixel_head_within_16_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run([sys.executable, str(ROOT / "build_study.py"), "--out", directory], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            with Image.open(Path(directory) / "sock_head_64.png") as im:
                self.assertEqual(im.size, (64, 64))
                self.assertEqual(im.mode, "RGBA")
                self.assertLessEqual(len(im.getcolors(maxcolors=4097)), 16)
                self.assertEqual(im.getchannel("A").getextrema(), (0, 255))
                self.assertEqual(set(im.getchannel("A").get_flattened_data()), {0, 255})

    def test_preview_is_exact_integer_nearest_neighbour(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run([sys.executable, str(ROOT / "build_study.py"), "--out", directory], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            preview = Path(directory) / "sock_head_8x.png"
            self.assertTrue(preview.exists(), "Missing inspectable integer-scaled preview")
            with Image.open(Path(directory) / "sock_head_64.png") as native, Image.open(preview) as enlarged:
                self.assertEqual(enlarged.size, (512, 512))
                self.assertEqual(enlarged.tobytes(), native.resize((512, 512), Image.Resampling.NEAREST).tobytes())

    def test_review_board_retains_source_and_landmark_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            run = subprocess.run([sys.executable, str(ROOT / "build_study.py"), "--out", directory], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((out / "construction.json").exists(), "Missing reusable landmark/provenance record")
            record = json.loads((out / "construction.json").read_text(encoding="utf-8"))
            self.assertIn("manual", record["annotation_method"].lower())
            self.assertEqual(record["source_sha256"], hashlib.sha256(Path(record["source"]).read_bytes()).hexdigest())
            self.assertEqual(len(record["landmarks"]), 6)
            for data in record["landmarks"].values():
                self.assertTrue(all(0 <= c < 64 for c in data["native_pixel"]))
            for filename in ["study-board.png", "reference-guide.png", "silhouette_64.png", "planes_64.png"]:
                with Image.open(out / filename) as im:
                    im.verify()

    def test_button_eyes_stay_separate_from_the_fringe(self):
        from build_study import render_head
        model = json.loads((ROOT / "head_model.json").read_text(encoding="utf-8"))
        image, _, _ = render_head(model)
        x0, y0, x1, y1 = model["viewport_in_local_coordinates"]
        for eye in model["eyes"]:
            with self.subTest(eye=eye["name"]):
                a,b,c,d = eye["bbox"]
                x = round(((a+c)/2-x0)*64/(x1-x0))
                y = round((b-y0)*64/(y1-y0))-1
                self.assertEqual(image.getpixel((x,y)), tuple(model["palette"]["ivory"]), "Hair merged into the button eye after grid snapping")

if __name__ == "__main__":
    unittest.main(verbosity=2)
