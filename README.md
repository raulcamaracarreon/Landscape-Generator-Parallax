# Landscape Generator — Parallax

Multilingual procedural mountain landscape generator for 2D games and parallax backgrounds.

**Ten languages:** Español, English, Français, Deutsch, Português, Italiano, Русский, 中文, 日本語, हिन्दी.

## 🌐 Try the web app / Probar la aplicación web

**[▶ Open Landscape Generator online / Abrir el generador de paisajes](https://raulcamaracarreon.github.io/Landscape-Generator-Parallax/web/)**

No installation required / No requiere instalación.

## Features

- Generate 2–10 layers of mountains with interpolated colors.
- Adjust image dimensions, mountain amplitude and detail.
- Export a composite PNG/JPEG or separate transparent PNG layers.
- Horizontally continuous mountain silhouettes for repeating backgrounds.

## Downloads / Descargas

Two independent packages are produced by the [Windows packaging workflow](.github/workflows/package-releases.yml):

| Package | Contents | Requirements |
| --- | --- | --- |
| **Desktop for Windows** — `Landscape-Generator-Desktop-Windows.zip` | Language selector and ten standalone Windows executables | Windows 10/11; no Python installation |
| **Portable web app** — `Landscape-Generator-Web.zip` | `index.html`, `i18n.js`, instructions | Modern web browser; works offline |

**[View GitHub Releases / Ver versiones y descargas](https://github.com/raulcamaracarreon/Landscape-Generator-Parallax/releases)**

To build the ZIP archives, open **Actions → Package Desktop and Web → Run workflow**. The resulting packages appear in that run's Artifacts section. To publish downloadable release assets, create and push a version tag such as `v1.0.0`; the workflow packages both editions and publishes the ZIP files as release assets after the build succeeds.

**Build status:** The workflow has been configured but the Windows binaries are not yet verified. A GitHub Release will not appear until a successful tagged run completes.

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
- `web/index.html`: browser application with mountains, buildings and parallax preview
- `web/i18n.js`: translations for ten web interface languages

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

## Web version (HTML + Canvas)

Open [web/index.html](web/index.html) in a modern browser. This self-contained page needs no Python or external dependencies. It supports ten languages through a selector at the top of the page, with the preference retained in the browser. Features include configurable mountain/building layers, deterministic seeds, animated parallax preview, composite PNG export and a ZIP of transparent layer PNGs (including `capa_00_cielo.png`).

To publish via GitHub Pages, choose **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main → Folder: / (root)**, then open [the live web application](https://raulcamaracarreon.github.io/Landscape-Generator-Parallax/web/). Pages deployment must be enabled in repository settings; committing the HTML does not activate hosting automatically.

The web app is a reconstruction of the September 2025 single-file HTML generator, not the original recovered HTML. Test its exports and appearance before a public release.
