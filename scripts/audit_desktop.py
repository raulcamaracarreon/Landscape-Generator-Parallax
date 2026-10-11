"""Audit packed Windows applications and test physical Qt DLL replacement.

This confirms file-system replaceability, not compatibility with a modified Qt DLL.
"""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from importlib.metadata import version

root = Path("release/Desktop").resolve()
dest = root / "LICENSE_COMPLIANCE"
dest.mkdir(exist_ok=True)
apps = sorted(p for p in (root / "apps").iterdir() if p.is_dir())
if len(apps) != 10:
    raise SystemExit(f"Expected 10 application directories, got {len(apps)}")
results = []
for app in apps:
    exe = app / (app.name + ".exe")
    if not exe.is_file():
        raise SystemExit(f"Missing {exe}")
    dlls = list(app.rglob("Qt6Core.dll"))
    if not dlls:
        raise SystemExit(f"Missing Qt6Core.dll in {app}")
    dll = dlls[0]
    expected = hashlib.sha256(dll.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as folder:
        saved = Path(folder) / dll.name
        shutil.copy2(dll, saved)
        dll.unlink()
        shutil.copy2(saved, dll)
    if hashlib.sha256(dll.read_bytes()).hexdigest() != expected:
        raise SystemExit(f"Qt DLL physical replacement failed in {app.name}")
    results.append({"app": app.name, "exe": str(exe.relative_to(root)), "qt_core": str(dll.relative_to(root)), "sha256": expected, "replacement_test": "identical DLL restored"})
if not (root / "Landscape-Generator-Launcher.exe").is_file():
    raise SystemExit("Missing launcher")
(dest / "QT_DLL_REPLACEMENT_CHECK.json").write_text(
    json.dumps({"Qt_version": version("PySide6_Essentials"), "results": results,
                "limitation": "A byte-identical replacement was tested. Compatibility with a modified Qt DLL is NOT verified."},
               indent=2), encoding="utf-8")
print(f"Verified ten apps and filesystem replacement for {len(results)} Qt DLLs.")
