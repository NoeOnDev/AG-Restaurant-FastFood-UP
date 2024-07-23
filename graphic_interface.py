from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
import sys
import qtawesome as qta
from data_processing import algoritmo_genetico, graficar_resultados

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
        button.clicked.connect(self.run_algorithm)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        self.mode_button = QPushButton(self)
        self.mode_button.setIcon(qta.icon('fa5s.sun', color='black'))
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
            self.mode_button.setIcon(qta.icon('fa5s.moon', color='white'))
        else:
            self.set_light_mode()
            self.mode_button.setIcon(qta.icon('fa5s.sun', color='black'))
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
                border-radius: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: lightgray;
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
                border-radius: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        
    def run_algorithm(self):
        try:
            for input_field in self.inputs:
                if input_field.text() == "":
                    raise ValueError("Todos los campos deben estar llenos.")
            
            tamano_poblacion = int(self.inputs[0].text())
            tamano_maximo_poblacion = int(self.inputs[1].text())
            probabilidad_mutacion = float(self.inputs[2].text())
            probabilidad_mutacion_gen = float(self.inputs[3].text())
            num_generaciones = int(self.inputs[4].text())

            if tamano_poblacion < 2 or tamano_maximo_poblacion <= 0 or num_generaciones <= 0:
                raise ValueError("El tamaño de la población debe ser 2 o más. La población máxima y el número de generaciones deben ser enteros positivos.")
            if not (0 < probabilidad_mutacion < 1):
                raise ValueError("La probabilidad de mutación debe estar entre 0 y 1 (excluyendo 0 y 1).")
            if not (0 < probabilidad_mutacion_gen < 1):
                raise ValueError("La probabilidad de mutación por gen debe estar entre 0 y 1 (excluyendo 0 y 1).")
            
            mejor_combo, fitness_max, fitness_avg, fitness_min = algoritmo_genetico(
                tamano_poblacion, num_generaciones, tamano_maximo_poblacion,
                probabilidad_mutacion, probabilidad_mutacion_gen
            )

            graficar_resultados(fitness_max, fitness_avg, fitness_min)

            print(f"Mejor Combo: {mejor_combo[0]}")
            print(f"Fitness: {mejor_combo[1]}")
            print(f"Venta Combo: {mejor_combo[2]}")
            print(f"Costo Total: {mejor_combo[3]}")

        except ValueError as e:
            self.show_error_message(str(e))

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Error")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
