import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
APPROVED = ROOT / "output" / "sock_head_64.png"

class ResolutionComparisonTests(unittest.TestCase):
    def test_native_128_is_new_raster_not_an_enlarged_64(self):
        before = hashlib.sha256(APPROVED.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            run = subprocess.run([sys.executable, str(ROOT / "compare_resolutions.py"), "--out", directory], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            with Image.open(APPROVED) as old, Image.open(out / "sock_head_128.png") as new:
                self.assertEqual(new.size, (128,128))
                self.assertEqual(new.mode, "RGBA")
                colours = set(new.get_flattened_data())
                self.assertLessEqual(len(colours),16)
                self.assertLessEqual(colours, set(old.get_flattened_data()))
                self.assertEqual(set(new.getchannel("A").get_flattened_data()), {0,255})
                self.assertNotEqual(new.tobytes(),old.resize((128,128),Image.Resampling.NEAREST).tobytes())
            self.assertEqual(hashlib.sha256(APPROVED.read_bytes()).hexdigest(),before)

    def test_comparison_shows_both_native_rasters_at_equal_display_size(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            run = subprocess.run([sys.executable, str(ROOT / "compare_resolutions.py"), "--out", directory], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((out / "comparison.png").exists(), "Missing same-display-size comparison")
            manifest = json.loads((out / "comparison.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["display_panel_size"],[512,512])
            self.assertEqual(manifest["approved_64_sha256"],hashlib.sha256(APPROVED.read_bytes()).hexdigest())
            self.assertGreater(manifest["native_pixels_different_from_2x_enlargement"],0)
            self.assertEqual((out / "sock_head_64.png").read_bytes(),APPROVED.read_bytes())
            for filename, preview in [(APPROVED, "sock_head_64_display.png"),(out / "sock_head_128.png","sock_head_128_display.png")]:
                with Image.open(filename) as im, Image.open(out / preview) as shown:
                    self.assertEqual(shown.size,(512,512))
                    self.assertEqual(shown.tobytes(),im.resize((512,512),Image.Resampling.NEAREST).tobytes())
            with Image.open(out / "comparison.png") as board:
                self.assertEqual(board.size,tuple(manifest["board_size"]))
                for panel in manifest["panels"]:
                    with Image.open(out / panel["native_file"]) as source:
                        enlarged = source.resize((512,512),Image.Resampling.NEAREST).convert("RGBA")
                    x,y = panel["top_left"]
                    for py in range(512):
                        for px in range(512):
                            rgb = enlarged.getpixel((px,py))
                            if rgb[3]:
                                self.assertEqual(board.getpixel((x+px,y+py)),rgb[:3])

if __name__ == "__main__":
    unittest.main(verbosity=2)
