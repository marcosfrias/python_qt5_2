import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QSizePolicy, QLabel
from qtpy import uic


class DropButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('temp_btn.ui', self)
        self.setAcceptDrops(True)
        self.main_window = parent  # Asume que el parent es MainWindow directamente
        self.setFont(QFont('Verdana', 16))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Agregar texto al botón
        self.setText("Arrastra un archivo o presiona")  # Texto del botón
        # Estilo del botón
        self.setStyleSheet("""QPushButton {
                        border: none;
                        background-color: transparent; /* Fondo transparente */
                        color: black; /* Color del texto */
                        font: 16px 'Verdana';
                        }
                        QPushButton:hover {
                            background-color: transparent; /* Sin cambio al pasar el mouse */
                        }
                        QPushButton:pressed {
                            background-color: transparent; /* Sin cambio al presionar */
                        }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith(('.xls', '.xlsx')):
                self.main_window.load_excel(file_path)
            else:
                self.setText("Archivo no válido. Arrastra un archivo Excel.")
        else:
            self.setText("No se arrastró un archivo válido.")
