from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel


class EditCellDialog(QDialog):
    def __init__(self, current_value, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar celda")

        # Layout del cuadro de diálogo
        self.layout = QVBoxLayout()

        # Etiqueta para mostrar el valor actual
        self.label = QLabel(f"Valor actual: {current_value}", self)
        self.layout.addWidget(self.label)

        # Campo de texto para editar
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(current_value)
        self.layout.addWidget(self.line_edit)

        # Botones de aceptar y cancelar
        self.accept_button = QPushButton("Aceptar", self)
        self.accept_button.clicked.connect(self.accept)
        self.layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def get_new_value(self):
        return self.line_edit.text()
