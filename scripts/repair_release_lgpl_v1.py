#!/usr/bin/env python3
"""Repair v1.0.0 license source coverage and third-party notices, without rebuilding an EXE."""
import hashlib
import io
import json
import shutil
import tarfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

base = Path("release_audit")
dest = Path("patched")
dest.mkdir(exist_ok=True)
win = base/"Landscape-Generator-Desktop-Windows.zip"
src = base/"Landscape-Generator-Qt-LGPL-Sources.zip"
additional = base/"qtimageformats-6.11.0.tar.gz"
assert win.is_file() and src.is_file() and additional.is_file()

base_plugins = {
 "qcertonlybackend.dll", "qdirect2d.dll", "qgif.dll", "qico.dll",
 "qjpeg.dll", "qminimal.dll", "qmodernwindowsstyle.dll",
 "qnetworklistmanager.dll", "qoffscreen.dll", "qopensslbackend.dll",
 "qschannelbackend.dll", "qtuiotouchplugin.dll", "qwindows.dll"
}
svg_plugins = {"qsvg.dll","qsvgicon.dll"}
image_plugins = {"qicns.dll","qtga.dll","qtiff.dll","qwbmp.dll","qwebp.dll"}
plugin_to_module = {n:"qtbase" for n in base_plugins}
plugin_to_module.update({n:"qtsvg" for n in svg_plugins})
plugin_to_module.update({n:"qtimageformats" for n in image_plugins})

with ZipFile(win) as w:
    binaries = [n for n in w.namelist() if n.lower().endswith((".dll",".pyd",".exe"))]
    plugins = {Path(n).name.lower() for n in binaries if "/plugins/" in n.lower()}
    unaccounted = plugins-set(plugin_to_module)
    assert not unaccounted, f"Unknown Qt plugins requiring separate module source: {unaccounted}"
    assert image_plugins <= plugins, "Expected Qt ImageFormats plugins not all present: audit mismatch"
    dlls = {Path(n).name.lower() for n in binaries if Path(n).name.lower().startswith("qt6")}
    assert dlls == {"qt6core.dll","qt6gui.dll","qt6network.dll","qt6svg.dll","qt6widgets.dll"}, dlls
    bin_manifest = {n:(w.getinfo(n).CRC,w.getinfo(n).file_size) for n in binaries}
    old_info = json.loads(w.read("LICENSE_COMPLIANCE/QT_DLL_REPLACEMENT_CHECK.json"))
    assert old_info["Qt_version"]=="6.11.0"

with ZipFile(src) as s:
    m = json.loads(s.read("MANIFEST.json"))
    assert m["Qt_PySide_version"] == "6.11.0"
    assert {"qtbase","qtsvg","pyside-setup"} <= {x["module"] for x in m["sources"]}
    assert set(m["bundled_qt_dlls"]) == dlls
    sha=hashlib.sha256(additional.read_bytes()).hexdigest()
    with tarfile.open(additional,"r:gz") as t:
        names=t.getnames()
        assert any("/src/plugins/imageformats/webp/" in n for n in names), "Unexpected QtImageFormats source"
        assert any("/src/plugins/imageformats/tiff/" in n for n in names), "Missing QtImageFormats TIFF source"
    m["qt_source_modules"]=sorted(set(m["qt_source_modules"])|{"qtimageformats"})
    m["sources"].append({"module":"qtimageformats","url":"https://github.com/qt/qtimageformats/archive/refs/tags/v6.11.0.tar.gz",
                         "filename":additional.name,"sha256":sha})
    m["bundled_qt_plugins"] = [{"name":name,"source_module":plugin_to_module[name]} for name in sorted(plugins)]
    m["notes"] = "Includes qtbase, qtsvg, qtimageformats and PySide/Shiboken 6.11.0 source archives. Review runtime third-party licenses in Windows THIRD_PARTY_NOTICES.md."
    fixed_source=dest/src.name
    with ZipFile(fixed_source,"w",compression=ZIP_DEFLATED,allowZip64=True) as out:
        for info in s.infolist():
            if info.filename=="MANIFEST.json":continue
            with s.open(info) as inp,out.open(info,"w") as output:
                shutil.copyfileobj(inp,output,1024*1024)
        out.writestr(additional.name,additional.read_bytes())
        out.writestr("MANIFEST.json",json.dumps(m,indent=2,ensure_ascii=False).encode("utf-8"))

notices = """# Landscape Generator Parallax v1.0.0 — Third-party notices and LGPL information

The application source code is licensed under MIT (see LICENSE-MIT.txt).
The separately distributed desktop binary includes additional software
under its own licenses. This notice does not relicense those libraries.

## Qt / PySide6 / Shiboken 6.11.0

QtBase (Core, Gui, Widgets, Network and plugins), QtSvg, QtImageFormats,
PySide6 Essentials and Shiboken are included as separately replaceable
dynamic libraries. Copyright belongs to The Qt Company Ltd. and other
respective contributors, as stated in each source file.

These components are available under LGPLv3 or other applicable licenses.
They are not being relicensed under MIT. Read LGPL-3.0.txt and GPL-3.0.txt
and the additional license texts under LICENSE_COMPLIANCE/THIRD_PARTY_LICENSES.

The complete corresponding version-matched sources for QtBase, QtSvg,
QtImageFormats and PySide/Shiboken 6.11.0 are distributed separately in
Landscape-Generator-Qt-LGPL-Sources.zip at the same GitHub Release v1.0.0.
The source archive includes SHA-256 hashes and a manifest of Qt DLLs and plugins.

You are permitted to modify or replace the LGPL libraries, and to reverse
engineer the application as needed to debug modifications to the LGPL libraries,
consistent with LGPLv3. There is no DRM or binary-signature enforcement in this
portable ZIP. Installation and replacement instructions are in
LICENSE_COMPLIANCE/README_RELINKING.txt.

## Qt Image Formats codec plugins and third-party software

The image format plugins include libtiff (libtiff license) and libwebp
(BSD-3-Clause), where applicable. The complete QtImageFormats 6.11.0 source
is included in the corresponding LGPL source ZIP, including its LICENSES
directory. Its bundled license texts are also copied under
LICENSE_COMPLIANCE/THIRD_PARTY_LICENSES/qtimageformats/.

QtBase can use OpenSSL 3 shared libraries (Apache-2.0); license text is
included in the QtBase source archive and additional licensing texts folder.
OpenSSL is copyright the OpenSSL Project authors and contributors.

NumPy 2.5.4 is under BSD-3-Clause and may bundle OpenBLAS/scipy-openblas
(BSD-style license). Review copyright and bundled notices from its package.
https://numpy.org/doc/stable/license.html

Python 3.12 is under the PSF License and other component notices:
https://docs.python.org/3/license.html

PyInstaller is under GPL with an exception for applications it bundles:
https://pyinstaller.org/en/stable/license.html

Microsoft Visual C++ runtime DLLs may be included and are subject to
Microsoft's redistribution terms. These runtimes are not LGPL libraries.

## Source, modifications and distribution

The author has not modified Qt/PySide/Shiboken sources. If you redistribute
a modified covered library, comply with the corresponding license terms.
The full MIT-licensed application source is publicly available at:
https://github.com/raulcamaracarreon/Landscape-Generator-Parallax

Licensing documentation describes distribution obligations; it is not a
legal certification. Consult the complete LGPLv3 text and Qt's guidance:
https://www.qt.io/development/open-source-lgpl-obligations
"""

instructions = """LANDSCAPE GENERATOR PARALLAX — REPLACING Qt/PySide6 DLLs (LGPLv3)

1. Download and fully extract Landscape-Generator-Desktop-Windows.zip
   to a writable folder on Windows. Do not use the launcher inside a ZIP viewer.
2. Back up the whole extracted application folder.
3. For each language application under apps/<language>/, locate the Qt runtime
   in its _internal folder. Qt6Core.dll, Qt6Gui.dll, Qt6Widgets.dll,
   Qt6Network.dll and Qt6Svg.dll and associated plugins are normal files.
   Their exact nested locations vary by PyInstaller layout.
4. Compile or obtain an ABI-compatible modified LGPL Qt 6.11.0 DLL/plugin
   and replace the corresponding file(s) in the backed-up extracted copy.
   If a plugin depends on additional DLLs, replace its compatible dependencies.
5. Run apps/<language>/<language>.exe from the extracted folder, or use
   Landscape-Generator-Launcher.exe to choose a language.
   If a binary is incompatible, restore the backup; the LGPL does not require
   the distributor to support arbitrary incompatible modified binaries.
6. No keys, cryptographic signatures, installers or DRM prevent file replacement.
   The user may reverse engineer the app for debugging a modification to LGPL
   library components, consistent with LGPLv3.

This build uses PyInstaller --onedir: shared Qt DLL files are neither
statically linked into the EXE nor locked inside a --onefile executable.
The previous automated audit restored an identical Qt6Core.dll only; it did
not run the application with a user-modified ABI-compatible library.
Version-matched LGPL source archives are available at the same v1.0.0 release.

Copyright and license notices: THIRD_PARTY_NOTICES.md, LGPL-3.0.txt,
GPL-3.0.txt and LICENSE_COMPLIANCE/THIRD_PARTY_LICENSES/.
"""

def tar_licenses(source_name, blob):
    licenses = {}
    with tarfile.open(fileobj=io.BytesIO(blob),mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and "/LICENSES/" in member.name and member.size < 1024*1024:
                name=member.name.split("/LICENSES/",1)[1]
                if name and ".." not in Path(name).parts:
                    f=tar.extractfile(member)
                    if f:licenses[f"LICENSE_COMPLIANCE/THIRD_PARTY_LICENSES/{source_name}/{name}"]=f.read()
    return licenses

licenses={}
with ZipFile(src) as s:
    for mod in ("qtbase","qtsvg"):
        licenses.update(tar_licenses(mod,s.read(f"{mod}-6.11.0.tar.gz")))
    licenses.update(tar_licenses("pyside-setup",s.read("pyside-setup-6.11.0.tar.gz")))
licenses.update(tar_licenses("qtimageformats",additional.read_bytes()))
assert licenses and any("Apache-2.0" in k for k in licenses) and any("BSD-3-Clause" in k for k in licenses), "Missing required third-party license texts"

component_info = {
 "qt_version":"6.11.0","pyinstaller_mode":"onedir",
 "qt_dlls":sorted(dlls),"qt_plugins":m["bundled_qt_plugins"],
 "source_manifest_sha256":hashlib.sha256(fixed_source.read_bytes()).hexdigest(),
 "dynamic_replacement_note":"All DLLs distributed as accessible files; a modified DLL runtime smoke test has not been performed.",
 "other_binaries_requiring_licenses":["OpenSSL 3","NumPy 2.5.4 / OpenBLAS","Python 3.12","PyInstaller 6.22.3","Microsoft VC runtime"]
}

fixed_win = dest/win.name
with ZipFile(win) as w, ZipFile(fixed_win,"w",compression=ZIP_DEFLATED,allowZip64=True) as out:
    updates={"THIRD_PARTY_NOTICES.md",
             "LICENSE_COMPLIANCE/README_RELINKING.txt",
             "LICENSE_COMPLIANCE/COMPONENT_MANIFEST.json"}
    for info in w.infolist():
        if info.filename in updates or info.filename in licenses:continue
        if info.is_dir(): out.writestr(info,b"")
        else:
            with w.open(info) as inp,out.open(info,"w") as op:
                shutil.copyfileobj(inp,op,1024*1024)
    out.writestr("THIRD_PARTY_NOTICES.md",notices)
    out.writestr("LICENSE_COMPLIANCE/README_RELINKING.txt",instructions)
    out.writestr("LICENSE_COMPLIANCE/COMPONENT_MANIFEST.json",json.dumps(component_info,indent=2))
    for filename,data in licenses.items():out.writestr(filename,data)

with ZipFile(fixed_win) as w:
    assert w.testzip() is None, "Patched desktop ZIP failed CRC integrity"
    for name,(crc,size) in bin_manifest.items():
        b=w.getinfo(name)
        assert (b.CRC,b.file_size)==(crc,size),f"Binary changed unintentionally: {name}"
    assert "qtimageformats" in w.read("THIRD_PARTY_NOTICES.md").decode().lower()
with ZipFile(fixed_source) as s:
    assert s.testzip() is None
    newer=json.loads(s.read("MANIFEST.json"))
    assert {"qtbase","qtsvg","pyside-setup","qtimageformats"} == {x["module"] for x in newer["sources"]}
    with s.open(additional.name) as f:
        digest=hashlib.sha256()
        for block in iter(lambda:f.read(1024*1024),b""):digest.update(block)
    assert digest.hexdigest()==sha

print(json.dumps({
 "status":"PASSED","qt_plugins":len(plugins),"source_modules":sorted({x["module"] for x in m["sources"]}),
 "license_documents_added":len(licenses),
 "unmodified_binaries":len(bin_manifest),
 "desktop_zip_size":fixed_win.stat().st_size,
 "sources_zip_size":fixed_source.stat().st_size
},indent=2))
