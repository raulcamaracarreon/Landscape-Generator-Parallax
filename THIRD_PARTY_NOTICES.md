# Third-party software and LGPL review

This project source is MIT licensed. The desktop distribution includes **PySide6 / Qt 6**, Shiboken, Python, NumPy, and packaging runtime components under their own respective licenses.

## Qt and PySide6
Qt for Python community packages use LGPLv3/GPLv3 licensing for covered modules; see https://doc.qt.io/qtforpython-6/ and https://www.qt.io/development/open-source-lgpl-obligations.

The desktop archive includes copies of the GNU LGPLv3 and GPLv3 texts downloaded from GNU as part of packaging. This information does **not** on its own establish that the archive satisfies all applicable LGPLv3 obligations.

This build uses PyInstaller **--onedir**, so Qt runtime DLLs and plugins are distributed as files in each application folder (`apps/<language>/_internal/`) rather than hidden inside a one-file extraction bundle. Recipients must remain free to modify or replace covered Qt libraries, subject to interface/ABI compatibility. Keep each application's complete folder intact. The author should validate a replacement with a compatible user-built library before treating the package as compliant.

Additional distributor responsibilities include providing the exact corresponding source for LGPL-covered libraries (including any changes) or a valid written offer for that source, as well as the necessary installation/relink information and clear license notices. Merely linking to the Qt vendor's public website may be insufficient. Check all bundled Qt libraries/plugins and other dependencies against their exact versions and licenses.

Qt LGPL compliance reference: https://www.qt.io/faq/qt-open-source-licensing

## Other dependencies
- NumPy: BSD 3-Clause — https://numpy.org/doc/stable/license.html
- Python: PSF — https://docs.python.org/3/license.html
- PyInstaller: GPL with an exception for distributing frozen applications — https://pyinstaller.org/en/stable/license.html

**Before public distribution:** Verify the real content of the built ZIP, exact Qt/PySide versions, full license texts, library replacement, and corresponding source / written offer arrangements. If these cannot be completed, do not publish the Windows binary; the MIT-licensed source and standalone web version are still distributable.

## Publication status (v1.0.0)

The **web application can be publicly released under MIT**. The Windows archive is currently made available as a build artifact for verification, but **is deliberately not attached to automated public GitHub Releases** until the following steps are demonstrably completed:

1. Identify the exact versions and license of each Qt/PySide6/Shiboken DLL/plugin bundled by the Windows workflow. Check `DEPENDENCY_VERSIONS.txt` created during packaging and inspect the generated `_internal/PySide6/Qt/` directories.
2. Supply the **complete corresponding source** for the distributed LGPL components, under the distributor's own control (or a legally sufficient written offer), including modifications and applicable build scripts. A bare link to Qt's site does not satisfy Qt's stated guidance.
3. Verify and document the procedure for replacing LGPL shared libraries and plugins with modified, binary-compatible builds, and confirm that the application continues to run.
4. Include all appropriate copyright/license notices for the **actual** packaged components; consider third-party Qt plugins and libraries as well as NumPy, Python and PyInstaller.
5. Document the installation information required under LGPLv3, insofar as applicable, and check for restrictions that could prevent using a modified library.

The open-source Qt references are:
- https://www.qt.io/development/open-source-lgpl-obligations
- https://www.qt.io/faq/qt-open-source-licensing
- https://doc.qt.io/qtforpython-6/

This checklist is engineering guidance, **not a legal compliance certification**. Consult a qualified attorney if uncertainty remains.
