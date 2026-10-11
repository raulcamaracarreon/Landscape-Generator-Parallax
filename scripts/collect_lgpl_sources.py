"""Build a distributable LGPL source bundle for the exact installed Qt for Python wheels.

Fails closed if upstream source archives or package metadata cannot be resolved.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request
import hashlib

OUT = Path("release/Desktop/LGPL_SOURCE")
OUT.mkdir(parents=True, exist_ok=True)
packages = ["PySide6", "PySide6_Essentials", "PySide6_Addons", "shiboken6"]
index = "https://pypi.org/pypi/{name}/{version}/json"
manifest = []
for name in packages:
    try:
        from importlib.metadata import version, metadata
        v = version(name)
    except Exception as exc:
        raise SystemExit(f"Unable to identify {name}: {exc}")
    with urllib.request.urlopen(index.format(name=name, version=v), timeout=60) as response:
        release = json.load(response)
    source_candidates = [x for x in release["urls"] if x.get("packagetype") == "sdist"]
    if not source_candidates:
        raise SystemExit(f"STOP: No verified source distribution for {name} {v}. Do not publish Desktop.")
    item = source_candidates[0]
    filename = item["filename"]
    target = OUT / filename
    urllib.request.urlretrieve(item["url"], target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != item["digests"]["sha256"]:
        raise SystemExit(f"Checksum failed for {filename}")
    manifest.append({"name": name, "version": v, "file": filename, "sha256": digest, "source_url": item["url"]})
(OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("LGPL source package hashes verified")
