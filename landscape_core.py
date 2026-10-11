import sys
import random
from pathlib import Path
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QPainter, QPixmap, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QColorDialog, QMessageBox, QSpinBox, QFileDialog, QSlider,
    QSizePolicy, QLineEdit, QDialog, QTextEdit
)

TRANSLATIONS = {
 "es": ["Generador de Paisajes","Color del Cielo","Seleccionar Color del Cielo","Color de las Montañas","Seleccionar Color de las Montañas","Número de Capas (2-10):","Ancho (px):","Alto (px):","Amplitud Máxima (% del alto):","Cantidad de Picos:","Aleatorizar Parámetros","Generar Paisaje","Guardar Imagen Completa","Guardar Capas por Separado","Ayuda","Error","Introduce un ancho y alto válidos (mínimo 100 x 100).","Imagen guardada","La imagen se guardó en:","No hay ninguna imagen para guardar.","Capas guardadas","Las capas se guardaron en:","No se seleccionó una carpeta.","No hay capas para guardar.","Elegir carpeta para guardar capas"],
 "en": ["Landscape Generator","Sky Color","Select Sky Color","Mountain Color","Select Mountain Color","Number of Layers (2-10):","Width (px):","Height (px):","Maximum Amplitude (% of height):","Number of Peaks:","Randomize Parameters","Generate Landscape","Save Complete Image","Save Layers Separately","Help","Error","Enter valid width and height (minimum 100 x 100).","Image saved","Image saved to:","There is no image to save.","Layers saved","Layers saved to:","No folder selected.","There are no layers to save.","Choose folder to save layers"],
 "fr": ["Générateur de paysages","Couleur du ciel","Choisir la couleur du ciel","Couleur des montagnes","Choisir la couleur des montagnes","Nombre de couches (2-10) :","Largeur (px) :","Hauteur (px) :","Amplitude maximale (% de la hauteur) :","Nombre de sommets :","Paramètres aléatoires","Générer le paysage","Enregistrer l'image complète","Enregistrer les couches séparément","Aide","Erreur","Saisissez des dimensions valides (minimum 100 x 100).","Image enregistrée","Image enregistrée dans :","Aucune image à enregistrer.","Couches enregistrées","Couches enregistrées dans :","Aucun dossier sélectionné.","Aucune couche à enregistrer.","Choisir le dossier de destination"],
 "de": ["Landschaftsgenerator","Himmelsfarbe","Himmelsfarbe auswählen","Bergfarbe","Bergfarbe auswählen","Anzahl der Ebenen (2-10):","Breite (px):","Höhe (px):","Maximale Amplitude (% der Höhe):","Anzahl der Gipfel:","Parameter zufällig wählen","Landschaft erzeugen","Gesamtbild speichern","Ebenen einzeln speichern","Hilfe","Fehler","Gültige Maße eingeben (mindestens 100 x 100).","Bild gespeichert","Bild gespeichert unter:","Kein Bild zum Speichern vorhanden.","Ebenen gespeichert","Ebenen gespeichert unter:","Kein Ordner ausgewählt.","Keine Ebenen zum Speichern vorhanden.","Ordner für Ebenen auswählen"],
 "pt": ["Gerador de Paisagens","Cor do Céu","Selecionar Cor do Céu","Cor das Montanhas","Selecionar Cor das Montanhas","Número de Camadas (2-10):","Largura (px):","Altura (px):","Amplitude Máxima (% da altura):","Número de Picos:","Aleatorizar Parâmetros","Gerar Paisagem","Salvar Imagem Completa","Salvar Camadas Separadamente","Ajuda","Erro","Insira dimensões válidas (mínimo 100 x 100).","Imagem salva","Imagem salva em:","Não há imagem para salvar.","Camadas salvas","Camadas salvas em:","Nenhuma pasta selecionada.","Não há camadas para salvar.","Selecionar pasta para salvar camadas"],
 "it": ["Generatore di Paesaggi","Colore del Cielo","Seleziona Colore del Cielo","Colore delle Montagne","Seleziona Colore delle Montagne","Numero di Livelli (2-10):","Larghezza (px):","Altezza (px):","Ampiezza Massima (% dell'altezza):","Numero di Picchi:","Parametri Casuali","Genera Paesaggio","Salva Immagine Completa","Salva Livelli Separatamente","Aiuto","Errore","Inserisci dimensioni valide (minimo 100 x 100).","Immagine salvata","Immagine salvata in:","Nessuna immagine da salvare.","Livelli salvati","Livelli salvati in:","Nessuna cartella selezionata.","Nessun livello da salvare.","Seleziona cartella per i livelli"],
 "ru": ["Генератор пейзажей","Цвет неба","Выбрать цвет неба","Цвет гор","Выбрать цвет гор","Количество слоёв (2-10):","Ширина (пикс):","Высота (пикс):","Максимальная амплитуда (% высоты):","Количество вершин:","Случайные параметры","Создать пейзаж","Сохранить изображение","Сохранить слои отдельно","Справка","Ошибка","Введите корректные размеры (не менее 100 x 100).","Изображение сохранено","Изображение сохранено в:","Нет изображения для сохранения.","Слои сохранены","Слои сохранены в:","Папка не выбрана.","Нет слоёв для сохранения.","Выберите папку для слоёв"],
 "zh": ["风景生成器","天空颜色","选择天空颜色","山脉颜色","选择山脉颜色","图层数量（2-10）：","宽度（像素）：","高度（像素）：","最大振幅（高度百分比）：","山峰数量：","随机化参数","生成风景","保存完整图像","分别保存图层","帮助","错误","请输入有效尺寸（至少 100 x 100）。","图像已保存","图像保存至：","没有可保存的图像。","图层已保存","图层保存至：","未选择文件夹。","没有可保存的图层。","选择保存图层的文件夹"],
 "ja": ["風景ジェネレーター","空の色","空の色を選択","山の色","山の色を選択","レイヤー数（2-10）：","幅（px）：","高さ（px）：","最大振幅（高さの%）：","山頂の数：","パラメーターをランダム化","風景を生成","画像全体を保存","レイヤーを個別に保存","ヘルプ","エラー","有効なサイズを入力してください（最小 100 x 100）。","画像を保存しました","保存先：","保存する画像がありません。","レイヤーを保存しました","保存先：","フォルダーが選択されていません。","保存するレイヤーがありません。","レイヤーの保存先を選択"],
 "hi": ["परिदृश्य जनरेटर","आकाश का रंग","आकाश का रंग चुनें","पहाड़ों का रंग","पहाड़ों का रंग चुनें","परतों की संख्या (2-10):","चौड़ाई (px):","ऊँचाई (px):","अधिकतम आयाम (ऊँचाई का %):","चोटियों की संख्या:","मापदंड यादृच्छिक करें","परिदृश्य बनाएँ","पूरी छवि सहेजें","परतें अलग से सहेजें","सहायता","त्रुटि","मान्य आकार दर्ज करें (न्यूनतम 100 x 100)।","छवि सहेजी गई","छवि यहाँ सहेजी गई:","सहेजने के लिए छवि नहीं है।","परतें सहेजी गईं","परतें यहाँ सहेजी गईं:","कोई फ़ोल्डर नहीं चुना गया।","सहेजने के लिए परतें नहीं हैं।","परतों के लिए फ़ोल्डर चुनें"]
}

class HelpDialog(QDialog):
    def __init__(self, language, parent=None):
        super().__init__(parent)
        t = TRANSLATIONS[language]
        self.setWindowTitle(t[14] + " - " + t[0])
        self.resize(600, 550)
        layout = QVBoxLayout(self)
        editor = QTextEdit()
        editor.setReadOnly(True)
        # Bilingual documentation is used until all original localized help is restored.
        editor.setHtml("""<h1>Landscape Generator / Generador de Paisajes</h1>
        <p>Generate procedural mountain layers for parallax backgrounds.
        Genera capas de montañas para fondos con paralaje.</p>
        <p>Choose the sky and mountain colors, number of layers, output size,
        maximum amplitude and detail. Generate the landscape and export either
        the full image (PNG or JPEG) or transparent PNG layers.</p>
        <p>Elige colores, capas, dimensiones, amplitud y detalle.
        Genera el paisaje y guarda la imagen completa (PNG o JPEG)
        o cada capa por separado (PNG transparente).</p>
        <p>Developer / Desarrollador: Raúl Cámara Carreón<br>
        <a href="https://github.com/raulcamaracarreon">GitHub</a></p>""")
        layout.addWidget(editor)

class LandscapeGenerator(QWidget):
    def __init__(self, language="en"):
        super().__init__()
        self.language = language
        self.t = TRANSLATIONS[language]
        self.landscape_image = None
        self.layer_images = []
        self.layer_amplitudes = []
        self.layer_details = []
        self.init_ui()

    def init_ui(self):
        t = self.t
        self.setWindowTitle(t[0])
        self.resize(900, 620)
        root = QHBoxLayout(self)
        controls = QVBoxLayout()
        image_layout = QVBoxLayout()
        root.addLayout(controls, 1)
        root.addLayout(image_layout, 3)
        title = QLabel(t[0])
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px;font-weight:bold")
        controls.addWidget(title)

        self.sky_color = QColor(135, 206, 235)
        self.mountain_color = QColor(34, 139, 34)
        for label, button_label, attr, callback in [
            (t[1], t[2], "sky_display", self.select_sky_color),
            (t[3], t[4], "mountain_display", self.select_mountain_color)
        ]:
            controls.addWidget(QLabel(label))
            display = QLabel()
            display.setFixedSize(40, 40)
            display.setAutoFillBackground(True)
            setattr(self, attr, display)
            controls.addWidget(display)
            button = QPushButton(button_label)
            button.clicked.connect(callback)
            controls.addWidget(button)
        self.update_color_display(self.sky_display, self.sky_color)
        self.update_color_display(self.mountain_display, self.mountain_color)

        row = QHBoxLayout()
        row.addWidget(QLabel(t[5]))
        self.layers_input = QSpinBox()
        self.layers_input.setRange(2, 10)
        self.layers_input.setValue(5)
        row.addWidget(self.layers_input)
        controls.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel(t[6]))
        self.width_input = QLineEdit("800")
        self.width_input.setFixedWidth(65)
        row.addWidget(self.width_input)
        row.addWidget(QLabel(t[7]))
        self.height_input = QLineEdit("600")
        self.height_input.setFixedWidth(65)
        row.addWidget(self.height_input)
        controls.addLayout(row)

        controls.addWidget(QLabel(t[8]))
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setRange(5, 30)
        self.amplitude_slider.setValue(10)
        controls.addWidget(self.amplitude_slider)
        controls.addWidget(QLabel(t[9]))
        self.detail_slider = QSlider(Qt.Horizontal)
        self.detail_slider.setRange(1, 100)
        self.detail_slider.setValue(50)
        controls.addWidget(self.detail_slider)

        button = QPushButton(t[10])
        button.clicked.connect(self.randomize_parameters)
        controls.addWidget(button)
        controls.addStretch()
        button = QPushButton(t[11])
        button.clicked.connect(self.generate_landscape)
        controls.addWidget(button)
        self.save_button = QPushButton(t[12])
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        controls.addWidget(self.save_button)
        self.save_layers_button = QPushButton(t[13])
        self.save_layers_button.clicked.connect(self.save_layers)
        self.save_layers_button.setEnabled(False)
        controls.addWidget(self.save_layers_button)
        button = QPushButton(t[14])
        button.clicked.connect(lambda: HelpDialog(self.language, self).exec())
        controls.addWidget(button)

        self.landscape_label = QLabel()
        self.landscape_label.setAlignment(Qt.AlignCenter)
        self.landscape_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.landscape_label.setStyleSheet("background-color: skyblue")
        image_layout.addWidget(self.landscape_label)

    @staticmethod
    def update_color_display(label, color):
        p = label.palette()
        p.setColor(QPalette.Window, color)
        label.setPalette(p)
        label.setAutoFillBackground(True)

    def select_sky_color(self):
        color = QColorDialog.getColor(self.sky_color, self)
        if color.isValid():
            self.sky_color = color
            self.update_color_display(self.sky_display, color)

    def select_mountain_color(self):
        color = QColorDialog.getColor(self.mountain_color, self)
        if color.isValid():
            self.mountain_color = color
            self.update_color_display(self.mountain_display, color)

    def randomize_parameters(self):
        n = self.layers_input.value()
        self.layer_amplitudes = [random.uniform(5, self.amplitude_slider.value()) for _ in range(n)]
        self.layer_details = [random.randint(1, self.detail_slider.value()) for _ in range(n)]

    def generate_landscape(self):
        try:
            width, height = int(self.width_input.text()), int(self.height_input.text())
            if width < 100 or height < 100:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, self.t[15], self.t[16])
            return
        n = self.layers_input.value()
        if len(self.layer_amplitudes) != n:
            self.layer_amplitudes = [random.uniform(5, self.amplitude_slider.value()) for _ in range(n)]
        if len(self.layer_details) != n:
            self.layer_details = [random.randint(1, self.detail_slider.value()) for _ in range(n)]

        image = QPixmap(width, height)
        image.fill(self.sky_color)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.layer_images = []
        for i in range(n):
            ratio = i / (n - 1)
            color = QColor(*[
                int(getattr(self.sky_color, channel)() * (1 - ratio) +
                    getattr(self.mountain_color, channel)() * ratio)
                for channel in ("red", "green", "blue")
            ])
            base = height * (i + 1) / (n + 1)
            amplitude = height * self.layer_amplitudes[i] / 100.0
            point_count = max(self.layer_details[i] * 2, 10)
            x = np.linspace(0, width, point_count, endpoint=False)
            y = base + np.random.uniform(-amplitude, amplitude, point_count)
            # Periodic interpolation: horizontal edges match for tiling.
            xs = np.linspace(0, width, point_count * 10 + 1)
            ys = np.interp(xs, np.append(x, width), np.append(y, y[0]))
            path = QPainterPath()
            path.moveTo(float(xs[0]), float(ys[0]))
            for xx, yy in zip(xs[1:], ys[1:]):
                path.lineTo(float(xx), float(yy))
            path.lineTo(width, height)
            path.lineTo(0, height)
            path.closeSubpath()

            layer = QPixmap(width, height)
            layer.fill(Qt.transparent)
            layer_painter = QPainter(layer)
            layer_painter.setRenderHint(QPainter.Antialiasing)
            for p in (painter, layer_painter):
                p.setBrush(color)
                p.setPen(Qt.NoPen)
                p.drawPath(path)
            layer_painter.end()
            self.layer_images.append(layer)
        painter.end()
        self.landscape_image = image
        self.update_preview()
        self.save_button.setEnabled(True)
        self.save_layers_button.setEnabled(True)

    def update_preview(self):
        if self.landscape_image is not None:
            self.landscape_label.setPixmap(self.landscape_image.scaled(
                self.landscape_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()

    def save_image(self):
        if self.landscape_image is None:
            QMessageBox.warning(self, self.t[15], self.t[19])
            return
        path, selected_filter = QFileDialog.getSaveFileName(
            self, self.t[12], "", "PNG (*.png);;JPEG (*.jpg *.jpeg)")
        if path:
            target = Path(path)
            if not target.suffix:
                target = target.with_suffix(".jpg" if "JPEG" in selected_filter else ".png")
            if self.landscape_image.save(str(target)):
                QMessageBox.information(self, self.t[17], self.t[18] + "\n" + str(target))

    def save_layers(self):
        if not self.layer_images:
            QMessageBox.warning(self, self.t[15], self.t[23])
            return
        directory = QFileDialog.getExistingDirectory(self, self.t[24])
        if not directory:
            return
        for i, layer in enumerate(self.layer_images, 1):
            layer.save(str(Path(directory) / f"layer_{i:02d}.png"), "PNG")
        QMessageBox.information(self, self.t[20], self.t[21] + "\n" + directory)

def run(language="en"):
    app = QApplication(sys.argv)
    window = LandscapeGenerator(language)
    window.show()
    sys.exit(app.exec())
