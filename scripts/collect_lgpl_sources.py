"""Collect version-matched Qt and PySide source archives, failing closed."""
import hashlib,json,urllib.request
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile
root=Path("release/Desktop/LGPL_SOURCE");root.mkdir(parents=True,exist_ok=True)
qt_version=version("PySide6_Essentials")
if version("shiboken6")!=qt_version or version("PySide6")!=qt_version:
    raise SystemExit("Qt for Python component versions differ; inspect manually")
# Identify the Qt modules actually bundled, not just the pip packages.
bundled={p.name.lower() for p in Path("release/Desktop").rglob("Qt6*.dll")}
modules={"qtbase"}
prefix_map={"qt6svg":"qtsvg","qt6qml":"qtdeclarative","qt6quick":"qtdeclarative","qt6shader":"qtshadertools","qt6multimedia":"qtmultimedia","qt6websockets":"qtwebsockets","qt6serialport":"qtserialport","qt6positioning":"qtpositioning","qt6charts":"qtcharts","qt6pdf":"qtwebengine","qt6virtualkeyboard":"qtvirtualkeyboard"}
core=("qt6core","qt6gui","qt6widgets","qt6network","qt6opengl","qt6printsupport","qt6test","qt6sql","qt6xml","qt6dbus","qt6concurrent")
unknown=[]
for dll in bundled:
    if dll.startswith(core):continue
    matches=[module for prefix,module in prefix_map.items() if dll.startswith(prefix)]
    if not matches:unknown.append(dll)
    else:modules.update(matches)
if unknown:raise SystemExit("STOP: Unmapped Qt DLLs: "+", ".join(sorted(unknown)))
archives={
    **{name:f"https://github.com/qt/{name}/archive/refs/tags/v{qt_version}.tar.gz" for name in sorted(modules)},
    "pyside-setup":f"https://github.com/qtproject/pyside-pyside-setup/archive/refs/tags/v{qt_version}.tar.gz",
}
manifest={"Qt_PySide_version":qt_version,"bundled_qt_dlls":sorted(bundled),"qt_source_modules":sorted(modules),"sources":[],"notes":"Inspect bundled plugins and third-party libraries separately before certifying compliance."}
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
