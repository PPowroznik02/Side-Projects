from PyQt5.QtWidgets import QMainWindow, QLabel, QToolBar, QAction, QDockWidget, QStackedWidget
from PyQt5.QtCore import Qt
from gui.tool_panels import ToolOptionsPanel
from tools.palette_tools import PaletteTools
from tools.morphology_tools import MorphologyTools
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QAction
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from PyQt5.QtGui import QImage
from tools.palette_tools import PaletteTools
from tools.morphology_tools import MorphologyTools


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edytor Obrazów")
        self.resize(1000, 700)

        self.image_label = QLabel("Brak zdjęcia")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        self.init_toolbar()
        self.init_side_panel()
        
        self.current_image = None
        self.setAcceptDrops(True)

    def init_toolbar(self):
        toolbar = QToolBar("Narzędzia")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # === Przycisk: Wybierz obraz ===
        load_action = QAction("📂 Wczytaj obraz", self)
        load_action.triggered.connect(self.load_image)
        toolbar.addAction(load_action)


        # === Przycisk: Zapisz obraz ===
        save_action = QAction("💾 Zapisz obraz", self)
        save_action.triggered.connect(self.save_image)
        toolbar.addAction(save_action)


        # === Grupa: Konwersja palety ===
        palette_menu = QMenu("Konwersja palety", self)
        for tool_name in PaletteTools.available_tools():
            action = QAction(tool_name, self)
            action.triggered.connect(lambda _, name=tool_name: self.show_tool(name))
            palette_menu.addAction(action)

        palette_button = QToolButton()
        palette_button.setText("🎨 Konwersja")
        palette_button.setPopupMode(QToolButton.InstantPopup)
        palette_button.setMenu(palette_menu)
        toolbar.addWidget(palette_button)


        # === Grupa: Operacje morfologiczne ===
        morph_menu = QMenu("Operacje morfologiczne", self)
        for tool_name in MorphologyTools.available_tools():
            action = QAction(tool_name, self)
            action.triggered.connect(lambda _, name=tool_name: self.apply_palette_tool(name))
            action.triggered.connect(lambda _, name=tool_name: self.show_tool(name))
            morph_menu.addAction(action)

        morph_button = QToolButton()
        morph_button.setText("🔧 Morfologia")
        morph_button.setPopupMode(QToolButton.InstantPopup)
        morph_button.setMenu(morph_menu)
        toolbar.addWidget(morph_button)



    def init_side_panel(self):
        self.side_dock = QDockWidget("Opcje narzędzia", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.side_dock)
        self.panel_stack = QStackedWidget()
        self.tool_panels = {}

        # Dodajemy panele z wywołaniem callbacka
        for name in PaletteTools.available_tools() + MorphologyTools.available_tools():
            panel = ToolOptionsPanel(name, self.apply_tool)
            self.tool_panels[name] = panel
            self.panel_stack.addWidget(panel)

        self.side_dock.setWidget(self.panel_stack)


    def show_tool(self, name):
        panel = self.tool_panels.get(name)
        if panel:
            self.panel_stack.setCurrentWidget(panel)
            
    def apply_palette_tool(self, tool_name):
        if self.current_image is None:
            print("Brak obrazu do przetworzenia.")
            return

        from tools.palette_tools import PaletteTools
        result = PaletteTools.apply(tool_name, self.current_image)
        self.current_image = result
        self.display_image(result)


    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            image = cv2.imread(file_name)
            if image is not None:
                self.current_image = image
                self.display_image(image)
            else:
                print("Nie udało się załadować obrazu.")
                
    def display_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    def resizeEvent(self, event):
        if self.current_image is not None:
            self.display_image(self.current_image)
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_image_from_path(file_path)

    def load_image_from_path(self, path):
        image = cv2.imread(path)
        if image is not None:
            self.current_image = image
            self.display_image(image)
            
    def save_image(self):
        if self.current_image is None:
            print("Brak obrazu do zapisania.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz obraz jako", "", "Obrazy (*.png *.jpg *.bmp)")
        if file_name:
            cv2.imwrite(file_name, self.current_image)
            
    def apply_tool(self, tool_name, params):
        if self.current_image is None:
            print("Brak obrazu do przetworzenia.")
            return

        if tool_name in PaletteTools.available_tools():
            result = PaletteTools.apply(tool_name, self.current_image.copy(), params)
            self.current_image = result
            self.display_image(result)
