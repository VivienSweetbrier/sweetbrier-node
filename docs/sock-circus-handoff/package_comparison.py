from pathlib import Path
import zipfile,json,hashlib
r=Path("C:/Users/Vivian/AppData/Local/hermes/artifacts/sock-dash-face-study")
expected="0227259bdf619a9b56963d9e4a30568c05da961509952e03a1358d2a91a98591"
assert hashlib.sha256((r/"output/sock_head_64.png").read_bytes()).hexdigest()==expected
files=[r/n for n in ["COMPARISON.md","compare_resolutions.py","build_study.py","head_model.json","test_comparison.py","comparison-test-results.json","output/sock_head_64.png"]]+sorted((r/"comparison-64-128").glob("*"))
p=r/"sock-dash-64-vs-128.zip"
with zipfile.ZipFile(p,"w",compression=zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(f,f.relative_to(r))
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    assert hashlib.sha256(z.read("output/sock_head_64.png")).hexdigest()==expected
    assert z.read("comparison-64-128/comparison.png")== (r/"comparison-64-128/comparison.png").read_bytes()
m=json.loads((r/"comparison-64-128/comparison.json").read_text())
print(json.dumps({"native_palette_entries":[m["native_64_palette_entries"],m["native_128_palette_entries"]],"changed_native_pixels_versus_bitmap_enlargement":m["native_pixels_different_from_2x_enlargement"],"panels":m["panels"],"approved_64_preserved":True,"zip":str(p),"zip_members":len(files),"zip_bytes":p.stat().st_size},indent=2))
