#!/usr/bin/env python3
"""Read-only audit of the EXACT v1.0.0 Windows and source ZIPs published to GitHub.
Does not rebuild binaries or claim legal certification.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

desktop = Path("release_audit/Landscape-Generator-Desktop-Windows.zip")
sources = Path("release_audit/Landscape-Generator-Qt-LGPL-Sources.zip")
apps = [
    "generador_paisajes_es", "landscape_generator_en", "generateur_paysages_fr",
    "landschaftsgenerator_de", "Gerador_de_Paisagens_pt",
    "generatore_paesaggi_it", "generator_peyzazhey_ru",
    "landscape_generator_zh", "landscape_generator_ja", "landscape_generator_hi"
]
results = {"passed": [], "failed": [], "requires_review": [], "inventory": {}}

def check(condition, description):
    results["passed" if condition else "failed"].append(description)
    return bool(condition)

def review(description):
    results["requires_review"].append(description)

with ZipFile(desktop) as w, ZipFile(sources) as s:
    wnames = set(w.namelist())
    snames = set(s.namelist())
    check(w.testzip() is None, "Windows archive ZIP integrity")
    check(s.testzip() is None, "Qt/PySide source ZIP integrity")
    needed = ["Landscape-Generator-Launcher.exe", "LICENSE-MIT.txt",
              "LGPL-3.0.txt", "GPL-3.0.txt", "THIRD_PARTY_NOTICES.md",
              "DEPENDENCY_VERSIONS.txt",
              "LICENSE_COMPLIANCE/QT_DLL_REPLACEMENT_CHECK.json"]
    for app in apps:
        needed.append(f"apps/{app}/{app}.exe")
        check(any(n.startswith(f"apps/{app}/") and n.lower().endswith("qt6core.dll") for n in wnames),
              f"Qt6Core.dll is present and replaceable in {app}")
    check(not (set(needed)-wnames), "All ten language EXEs, launcher, and licensing documents")
    manifest = json.loads(s.read("MANIFEST.json"))
    audit = json.loads(w.read("LICENSE_COMPLIANCE/QT_DLL_REPLACEMENT_CHECK.json"))
    versions = w.read("DEPENDENCY_VERSIONS.txt").decode("utf-8-sig", errors="replace")
    actual_qt_dlls = {Path(n).name.lower() for n in wnames if Path(n).name.lower().startswith("qt6") and n.lower().endswith(".dll")}
    check(set(manifest["bundled_qt_dlls"]) == actual_qt_dlls, "All Qt6 DLL names accounted for by source manifest")
    check(str(manifest["Qt_PySide_version"]) == str(audit["Qt_version"]) == "6.11.0",
          "Same Qt version in source manifest and DLL audit")
    packages = dict((line.split("==",1)[0].strip().lower().replace("_","-"),line.split("==",1)[1].strip()) for line in versions.splitlines() if "==" in line)
    for name in ["pyside6-essentials","shiboken6"]:
        check(packages.get(name) == "6.11.0", f"Packaged {name} version is 6.11.0")
    modules = {p["module"] for p in manifest["sources"]}
    check({"qtbase","qtsvg","pyside-setup"} <= modules, "Bundled Qt base, SVG and Python binding sources listed")
    for source in manifest["sources"]:
        fname=source["filename"]
        check(fname in snames, f"Source archive present: {fname}")
        if fname in snames:
            h=hashlib.sha256()
            with s.open(fname) as f:
                for block in iter(lambda:f.read(4*1024*1024), b""):
                    h.update(block)
            check(h.hexdigest() == source["sha256"], f"Source archive SHA256 matches: {fname}")
    check(len(audit.get("results",[]))==10, "Ten DLL replacement copy tests reported")
    check(all(x.get("replacement_test")=="identical DLL restored" for x in audit["results"]),
          "Audit accurately describes its identical DLL replacement test")
    dlls=sorted(n for n in wnames if n.lower().endswith((".dll",".pyd")))
    plugins=sorted(n for n in dlls if "/plugins/" in n.lower() or "/qt/plugins/" in n.lower())
    thirdparty=sorted({Path(n).name.lower() for n in dlls
                       if any(x in n.lower() for x in ("numpy.libs","libcrypto","libssl","freetype","harfbuzz","libpng","zlib","jpeg"))})
    notices=w.read("THIRD_PARTY_NOTICES.md").decode("utf-8-sig",errors="replace")
    if "Windows binaries remain unreleased" in notices or "deliberately not attached" in notices:
        review("Published Windows ZIP includes outdated notice saying Windows is not publicly released.")
    review("Compatible MODIFIED Qt DLL behavior not yet tested on Windows: only byte-identical DLL replacement was tested.")
    if plugins:
        review(f"Qt plugins must have their licenses mapped to corresponding source modules: {len(plugins)} files ({len({Path(n).name for n in plugins})} distinct names).")
    if thirdparty:
        review("Check third-party redistributable license notices for: "+", ".join(thirdparty))
    review("Qt licensing requires allowing reverse engineering for debugging LGPL modifications; review all distributed notices and terms.")
    results["inventory"]={
        "desktop_archive_bytes":desktop.stat().st_size,
        "qt_sources_archive_bytes":sources.stat().st_size,
        "qt_dlls":sorted(actual_qt_dlls),
        "qt_source_modules":sorted(modules),
        "packaged_pyside6_essentials":packages.get("pyside6-essentials"),
        "packaged_shiboken6":packages.get("shiboken6"),
        "zip_dll_and_pyd_count":len(dlls),
        "qt_plugin_paths":plugins,
        "third_party_binary_names":thirdparty,
        "version_lines": [line for line in versions.splitlines() if any(x in line.lower() for x in ("pyside","shiboken","numpy","pyinstaller"))]
    }
Path("release_audit/audit_v1.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
summary=["# LGPL inventory for actual Windows v1.0.0 release",
        f"**PASS: {len(results['passed'])} · FAIL: {len(results['failed'])} · FOLLOW-UP: {len(results['requires_review'])}**",
        "## Failed checks",*(f"- {x}" for x in results["failed"]),
        "## Still requiring review",*(f"- {x}" for x in results["requires_review"]),
        "## Modules",", ".join(results["inventory"]["qt_dlls"])]
Path("release_audit/SUMMARY.md").write_text("\n".join(summary)+"\n",encoding="utf-8")
print("\n".join(summary))
if results["failed"]:
    raise SystemExit(1)
