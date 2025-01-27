from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
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
        button_layout.setContentsMargins(0, 20, 0, 20)

        main_layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mejor Combo", "Fitness", "Venta Combo", "Precio Individual Total", "Costo Total"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        main_layout.addWidget(self.table)

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
            if tamano_poblacion > tamano_maximo_poblacion:
                raise ValueError("El tamaño de la población no puede ser mayor que el tamaño de la población máxima.")
            
            _, fitness_max, fitness_avg, fitness_min, _, mejores_individuos = algoritmo_genetico(
                tamano_poblacion,
                num_generaciones, 
                tamano_maximo_poblacion, 
                probabilidad_mutacion,
                probabilidad_mutacion_gen)

            graficar_resultados(fitness_max, fitness_avg, fitness_min)

            self.update_table(mejores_individuos)

        except ValueError as e:
            self.show_error_message(str(e))

    def update_table(self, mejores_individuos):
        self.table.setRowCount(0)

        for i, combo in enumerate(mejores_individuos):
            self.table.insertRow(i)

            combo_item = QTableWidgetItem(str(combo[0]))
            fitness_item = QTableWidgetItem(str(combo[1]))

            venta_combo = f"${combo[2]:.2f} pesos"
            costo_total = f"${combo[3]:.2f} pesos"
            precio_individual_total = f"${combo[4]:.2f} pesos"

            combo_item.setTextAlignment(Qt.AlignCenter)
            fitness_item.setTextAlignment(Qt.AlignCenter)
            venta_combo_item = QTableWidgetItem(venta_combo)
            costo_total_item = QTableWidgetItem(costo_total)
            precio_individual_total_item = QTableWidgetItem(precio_individual_total)
            venta_combo_item.setTextAlignment(Qt.AlignCenter)
            costo_total_item.setTextAlignment(Qt.AlignCenter)
            precio_individual_total_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(i, 0, combo_item)
            self.table.setItem(i, 1, fitness_item)
            self.table.setItem(i, 2, venta_combo_item)
            self.table.setItem(i, 3, costo_total_item)
            self.table.setItem(i, 4, precio_individual_total_item)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)

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
