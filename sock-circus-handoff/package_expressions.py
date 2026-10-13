from pathlib import Path
import hashlib,json,zipfile,tempfile,subprocess,sys
from PIL import Image
r=Path("C:/Users/Vivian/AppData/Local/hermes/artifacts/sock-dash-face-study")
expected128="71170b8088336bfc1974c123faa8472d6e2746c127413dd339113195d959cb00"
expected64="0227259bdf619a9b56963d9e4a30568c05da961509952e03a1358d2a91a98591"
assert hashlib.sha256((r/"comparison-64-128/sock_head_128.png").read_bytes()).hexdigest()==expected128
assert hashlib.sha256((r/"output/sock_head_64.png").read_bytes()).hexdigest()==expected64
names=["EXPRESSIONS.md","CURRENT_DRAFT.json","animate_sock.py","expression_model_128.json","build_study.py","test_expressions.py","expressions-test-results.json","comparison-64-128/head_model_128.json","comparison-64-128/sock_head_128.png"]
files=[r/n for n in names]+sorted((r/"expressions-128").glob("*"))
package=r/"sock-face-alive-128.zip"
with zipfile.ZipFile(package,"w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p,p.relative_to(r))
with zipfile.ZipFile(package) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    with tempfile.TemporaryDirectory() as tmp:
        z.extractall(tmp)
        test=subprocess.run([sys.executable,"-B",str(Path(tmp)/"test_expressions.py")],capture_output=True,text=True)
        print("PORTABLE PACKAGE TEST:\n"+test.stdout+test.stderr)
        assert test.returncode==0
m=json.loads((r/"expressions-128/expressions.json").read_text())
with Image.open(r/"expressions-128/sock_alive_128.gif") as gif:
    metadata={"native_size":gif.size,"frames":gif.n_frames,"loop":gif.info["loop"]}
print(json.dumps({"animation":metadata,"unique_states":len(m["states"]),"duration_seconds":m["total_ms"]/1000,"changed_pixels":m["changed_pixels"],"originals_preserved":True,"portable_tests_passed":True,"package":str(package),"package_members":len(files),"package_bytes":package.stat().st_size},indent=2))
