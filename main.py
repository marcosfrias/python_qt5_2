#import ctypes
import os
import sys
import res_rc
import res_btn_rc
import pandas as pd
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QPushButton, QMessageBox
from drop_button import DropButton
import qdarktheme
from table_dialog import TableDialog
from table_window import TableWindow



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('temp.ui', self)

        # Reemplazo de Widget clase personalizada
        self.pushButton_drop = DropButton(parent=self)
        self.frame_sub.layout().addWidget(self.pushButton_drop)

        # Configurar el tema oscuro
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))

        # Conecta el botón de subir archivo
        self.pushButton_drop.clicked.connect(self.open_file)

        # Conecta el search_btn con la función de búsqueda
        self.search_button = self.findChild(QtWidgets.QPushButton, "search_btn")
        self.search_button.clicked.connect(self.open_table_window)

        # Conecta el lineEdit con la función de búsqueda en tiempo real
        self.lineEdit.textChanged.connect(self.search_value)

        # Configurar ícono en la barra de tareas (Windows)
        #myappid = 'mi.aplicacion.id.version.1.0'  # Identificador único
        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Conecta el botón de reset
        self.btn_reset = self.findChild(QtWidgets.QPushButton, "btn_reset")
        self.btn_reset.clicked.connect(self.reset)

        # Conecta el botón de mostrar categorías
        self.btn_categories = self.findChild(QtWidgets.QPushButton, "btn_categories")
        self.btn_categories.clicked.connect(self.show_categories)

        # Variables para almacenar selección de categoría
        self.selected_column = None
        self.selected_value = None

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Abrir archivo Excel", "",
            "Archivos Excel (*.xls *.xlsx);;Todos los archivos (*)", options=options
        )
        if file_name:
            self.load_excel(file_name)

    def load_excel(self, file_name):
        try:
            print(f"Intentando leer el archivo Excel: {file_name}")  # Depuración
            self.df = pd.read_excel(file_name)
            print(f"Archivo Excel cargado: {file_name}")  # Depuración
            print(f"Estructura del DataFrame:\n{self.df.head()}")  # Depuración
            print("Columnas del DataFrame:", self.df.columns)
            print("Actualizando la tabla...")  # Depuración
            self.tableWidget.setRowCount(self.df.shape[0])
            self.tableWidget.setColumnCount(self.df.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

            for i in range(self.df.shape[0]):
                for j in range(self.df.shape[1]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))
                    print(f"Celda actualizada: ({i}, {j}) - {self.df.iat[i, j]}")  # Depuración

            file_name_only = os.path.basename(file_name)
            self.label_up.setText(f"{file_name_only}")

            # Oculta el DropButton después de cargar el archivo
            self.pushButton_drop.setVisible(False)

            # Establece un ancho específico para las columnas del tableWidget
            for column in range(self.tableWidget.columnCount()):
                self.tableWidget.setColumnWidth(column, 200)
        except Exception as e:
            self.label_up.setText(f"Error al cargar el archivo: {e}")
            print(f"Error: {e}")  # Depuración


    def update_table(self, df):
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
                print(f"Celda actualizada: ({i}, {j}) - {df.iat[i, j]}")  # Depuración

    def open_table_window(self):
        self.table_window = TableWindow(self.tableWidget)
        self.table_window.show()

    def reset(self):
        # Limpiar la tabla
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

        # Restaurar la visibilidad del DropButton
        self.pushButton_drop.setVisible(True)

        # Limpiar el texto del label_up
        self.label_up.setText("")

        # Limpiar el texto del lineEdit
        self.lineEdit.clear()

        # Eliminar cualquier DataFrame previamente cargado
        if hasattr(self, 'df'):
            del self.df
        print("Interfaz restaurada al estado inicial.")

    def show_categories(self):
        """Muestra las categorías (columnas o fila 0) en un diálogo de tabla."""
        if hasattr(self, 'df') and self.df is not None:
            if self.df.columns.isnull().any():  # Si alguna columna no tiene nombre
                categories = self.df.iloc[0].tolist()
                headers = ["Valores de la fila 0"] * len(categories)
            else:
                categories = self.df.columns.tolist()
                headers = categories  # Los encabezados son los nombres de las columnas

            # Crear y mostrar el diálogo con la tabla
            self.dialog = TableDialog(categories, headers, self)
            self.dialog.category_selected.connect(self.handle_category_selection)  # Conectar la señal
            self.dialog.exec_()
        else:
            # Si no hay DataFrame cargado, mostrar un mensaje de error
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error: El archivo no está cargado. Carga un archivo Excel primero.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

    def handle_category_selection(self, column, value):
        """Maneja la selección de categoría desde el diálogo."""
        self.selected_column = column
        self.selected_value = value

        # Actualizar el lineEdit con el valor seleccionado
        self.lineEdit.setText(value)

    def search_value(self):
        """Filtra los datos según el texto ingresado y la selección de categoría."""
        if hasattr(self, 'df') and self.selected_column is not None:  # Verifica si hay una columna seleccionada
            value = self.lineEdit.text()
            print(f"Buscando en la columna '{self.selected_column}' con el valor '{value}'")  # Depuración

            # Filtrar el DataFrame en la columna seleccionada
            filtered_df = self.df[self.df[self.selected_column].astype(str).str.contains(value, na=False, case=False)]

            if not filtered_df.empty:
                self.update_table(filtered_df)  # Actualiza la tabla principal con el DataFrame filtrado
            else:
                # Si no se encuentran resultados, limpiar la tabla
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(len(self.df.columns))
                self.tableWidget.setHorizontalHeaderLabels(self.df.columns)
        else:
            print("Seleccione una columna en la tabla de categorías antes de buscar.")

    def make_first_row_and_column_editable(self):
        """Hacer que la primera fila y la primera columna sean editables."""
        row_count = self.tableWidget.rowCount()
        column_count = self.tableWidget.columnCount()

        # Hacer editable la primera fila (encabezados de las columnas)
        for col in range(column_count):
            item = self.tableWidget.item(0, col)
            if item is None:
                item = QTableWidgetItem()  # Crear un item vacío si no existe
                self.tableWidget.setItem(0, col, item)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # Hacerlo editable

        # Hacer editable la primera columna (encabezados de las filas)
        for row in range(row_count):
            item = self.tableWidget.item(row, 0)
            if item is None:
                item = QTableWidgetItem()  # Crear un item vacío si no existe
                self.tableWidget.setItem(row, 0, item)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # Hacerlo editable

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
