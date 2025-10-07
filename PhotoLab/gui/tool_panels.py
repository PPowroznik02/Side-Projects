from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PyQt5.QtCore import Qt

class ToolOptionsPanel(QWidget):
    def __init__(self, tool_name, apply_callback):
        super().__init__()
        self.tool_name = tool_name
        self.apply_callback = apply_callback
        self.params = {}

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Narzędzie: {tool_name}"))

        if tool_name == "Sepia":
            layout.addWidget(QLabel("Intensywność:"))
            self.intensity_slider = QSlider(Qt.Horizontal)
            self.intensity_slider.setRange(0, 100)
            self.intensity_slider.setValue(100)
            layout.addWidget(self.intensity_slider)
            self.params["intensity_slider"] = self.intensity_slider

        self.apply_button = QPushButton("Zastosuj")
        self.apply_button.clicked.connect(self.apply_tool)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def get_params(self):
        if self.tool_name == "Sepia":
            return {"intensity": self.params["intensity_slider"].value()}
        return {}

    def apply_tool(self):
        self.apply_callback(self.tool_name, self.get_params())
