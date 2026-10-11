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
