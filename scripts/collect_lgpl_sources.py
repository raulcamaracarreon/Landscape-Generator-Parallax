"""Collect version-matched Qt and PySide source archives, failing closed."""
import hashlib,json,urllib.request
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile
root=Path("release/Desktop/LGPL_SOURCE");root.mkdir(parents=True,exist_ok=True)
qt_version=version("PySide6_Essentials")
if version("shiboken6")!=qt_version or version("PySide6")!=qt_version:
    raise SystemExit("Qt for Python component versions differ; inspect manually")
archives={
    "qtbase":f"https://github.com/qt/qtbase/archive/refs/tags/v{qt_version}.tar.gz",
    "pyside-setup":f"https://github.com/qt/pyside-setup/archive/refs/tags/v{qt_version}.tar.gz",
}
manifest={"Qt_PySide_version":qt_version,"sources":[],"notes":"QtBase and Qt for Python source snapshots. Other bundled Qt modules require separate coverage if present."}
for name,url in archives.items():
    dest=root/(name+"-"+qt_version+".tar.gz")
    print("Fetching",url,flush=True)
    req=urllib.request.Request(url,headers={"User-Agent":"landscape-generator-release"})
    with urllib.request.urlopen(req,timeout=120) as response, dest.open("wb") as out:
        import shutil
        shutil.copyfileobj(response,out)
    checksum=hashlib.sha256(dest.read_bytes()).hexdigest()
    if dest.stat().st_size<10240:raise SystemExit("Source archive unexpectedly small: "+name)
    manifest["sources"].append({"module":name,"url":url,"filename":dest.name,"sha256":checksum})
(root/"MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
