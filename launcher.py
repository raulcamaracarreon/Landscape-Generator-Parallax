import sys
import subprocess
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMessageBox

LANGUAGES = [
    ("Español", "es", "generador_paisajes_es"),
    ("English", "en", "landscape_generator_en"),
    ("Français", "fr", "generateur_paysages_fr"),
    ("Deutsch", "de", "landschaftsgenerator_de"),
    ("Português", "pt", "Gerador_de_Paisagens_pt"),
    ("Italiano", "it", "generatore_paesaggi_it"),
    ("Русский", "ru", "generator_peyzazhey_ru"),
    ("中文", "zh", "landscape_generator_zh"),
    ("日本語", "ja", "landscape_generator_ja"),
    ("हिन्दी", "hi", "landscape_generator_hi"),
]

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar idioma / Select language")
        self.resize(450, 320)
        layout = QVBoxLayout(self)
        heading = QLabel("Selecciona un idioma / Select a language:")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)
        grid = QGridLayout()
        for index, (label, language, filename) in enumerate(LANGUAGES):
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, name=filename: self.launch(name))
            grid.addWidget(button, index // 2, index % 2)
        layout.addLayout(grid)

    def launch(self, filename):
        # Check next to the launcher first; support both compiled programs and source.
        base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        candidates = [base / (filename + ".exe"), base / "src" / (filename + ".py"), base / (filename + ".py")]
        target = next((p for p in candidates if p.is_file()), None)
        if target is None:
            QMessageBox.warning(self, "File not found / Archivo no encontrado",
                                "Missing / Falta: " + filename + "\nFolder / Carpeta: " + str(base))
            return
        try:
            if target.suffix.lower() == ".exe":
                subprocess.Popen([str(target)], cwd=str(target.parent))
            else:
                subprocess.Popen([sys.executable, str(target)], cwd=str(target.parent))
            self.close()
        except OSError as exc:
            QMessageBox.critical(self, "Launch error / Error al abrir", str(exc))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())
