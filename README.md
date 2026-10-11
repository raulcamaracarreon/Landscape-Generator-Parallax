# Landscape Generator — Parallax

Multilingual procedural mountain landscape generator for 2D games and parallax backgrounds.

**Ten languages:** Español, English, Français, Deutsch, Português, Italiano, Русский, 中文, 日本語, हिन्दी.

## Features

- Generate 2–10 layers of mountains with interpolated colors.
- Adjust image dimensions, mountain amplitude and detail.
- Export a composite PNG/JPEG or separate transparent PNG layers.
- Horizontally continuous mountain silhouettes for repeating backgrounds.

## Run from source

Requires Python 3.10+.

```powershell
python -m pip install -r requirements.txt
python launcher.py
```

The launcher searches beside itself for ten prebuilt Windows executables, or in `src/` for Python entry points.

## Project structure

- `landscape_core.py`: shared generator and ten-language UI strings
- `launcher.py`: language selection
- `src/*.py`: ten language entry points
- `requirements.txt`: PySide6 and NumPy

## Recovered project status

The previous project folder was lost. This repository is a **reconstruction based on an earlier conversation**, not an exact byte-for-byte recovery of the original sources. The shared landscape-generation logic and UI have been restored with ten translated interfaces. The former fully translated help pages have **not** been restored; the current help page is bilingual Spanish/English. Test the app before producing public releases.

## Build for Windows

The source launcher can run alongside source scripts. For a binary distribution, build the ten language-specific entry points and place their `.exe` files alongside the compiled launcher. Build launcher with:

```powershell
python -m PyInstaller --onefile --windowed launcher.py
```

The launcher does not itself embed the ten other executables. Do not distribute `launcher.exe` alone.

## Author

Raúl Cámara Carreón · https://github.com/raulcamaracarreon

## Licensing

No project-level license selected yet. Public repository visibility does not automatically authorize redistribution or modification. Review PySide6 (Qt/LGPL) and NumPy dependencies and their licenses before releasing packaged binaries.
