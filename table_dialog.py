from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout


class TableDialog(QDialog):
    # Señal que envía el valor seleccionado y la columna
    category_selected = pyqtSignal(str, str)

    def __init__(self, data, headers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Categorías del Archivo")
        self.setMinimumSize(400, 300)

        # Crear el QTableWidget
        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        # Rellenar la tabla con los datos
        for col, value in enumerate(data):
            self.table_widget.setItem(0, col, QTableWidgetItem(str(value)))

        # Diseño del diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Conectar el evento de clic en una celda
        self.table_widget.cellClicked.connect(self.cell_selected)

    def cell_selected(self, row, column):
        """Evento que detecta cuando se selecciona una celda en la tabla."""
        selected_value = self.table_widget.item(row, column).text()
        selected_header = self.table_widget.horizontalHeaderItem(column).text()

        # Emitir la señal con el valor seleccionado y el encabezado
        self.category_selected.emit(selected_header, selected_value)
        self.close()  # Cerrar el diálogo después de seleccionar