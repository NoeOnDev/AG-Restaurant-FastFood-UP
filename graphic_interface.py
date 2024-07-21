from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtGui import QIcon
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algoritmo Genético")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        labels = [
            "Población inicial: ", 
            "Población máxima: ", 
            "Probabilidad de mutación: ", 
            "Probabilidad de mutación por gen: ", 
            "Número de generaciones: "
        ]
        self.inputs = []
        for label_text in labels:
            label = QLabel(label_text, self)
            input_field = QLineEdit(self)
            form_layout.addRow(label, input_field)
            self.inputs.append(input_field)

        main_layout.addLayout(form_layout)

        button = QPushButton("Ejecutar", self)
        button.setFixedWidth(100)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        self.mode_button = QPushButton(self)
        self.mode_button.setIcon(QIcon("path/to/icon.png"))
        self.mode_button.setFixedSize(40, 40)
        self.mode_button.clicked.connect(self.toggle_mode)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.mode_button)

        main_layout.addLayout(bottom_layout)

        central_widget.setLayout(main_layout)

        self.light_mode = True
        self.set_light_mode()

    def toggle_mode(self):
        if self.light_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()
        self.light_mode = not self.light_mode

    def set_light_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QLineEdit, QLabel, QPushButton {
                background-color: white;
                color: black;
            }
            QPushButton {
                border: 1px solid black;
            }
        """)

    def set_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: white;
            }
            QLineEdit, QLabel, QPushButton {
                background-color: #2e2e2e;
                color: white;
            }
            QPushButton {
                border: 1px solid white;
            }
        """)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
