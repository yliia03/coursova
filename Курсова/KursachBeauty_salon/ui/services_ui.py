from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QComboBox, QLineEdit, QLabel, QHeaderView
from PyQt5.QtCore import Qt
from models.database import DatabaseManager
from ui.service_details_ui import ServiceDetailsWindow
from ui.service_edit_ui import ServiceEditDialog

class ServicesWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Послуги та Товари Салону краси")
        self.setMinimumSize(700, 400)

        db = DatabaseManager()
        self.conn = db.connect()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton(" ⬅  Меню")
        self.btn_add = QPushButton(" ➕  Додати")
        self.btn_edit = QPushButton(" ✏️  Редагувати")
        self.btn_delete = QPushButton(" 🗑️  Видалити")
        self.btn_details = QPushButton(" ℹ️  Деталі")
        for btn in [self.back_btn, self.btn_add, self.btn_edit, self.btn_delete, self.btn_details]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        sort_layout = QHBoxLayout()
        self.sort_field = QComboBox()
        self.sort_field.addItems(["Назва", "Майстер", "Категорія", "Ціна ($)", "Тривалість", "Залишок"])
        self.sort_order = QComboBox()
        self.sort_order.addItems(["За зростанням", "За спаданням"])
        sort_layout.addWidget(QLabel("Сортування:"))
        sort_layout.addWidget(self.sort_field)
        sort_layout.addWidget(self.sort_order)
        sort_layout.addStretch()
        layout.addLayout(sort_layout)

        filter_layout = QHBoxLayout()
        self.filter_field = QComboBox()
        self.filter_field.addItems(["Назва", "Майстер", "Категорія"])
        self.filter_input1 = QLineEdit()
        self.filter_input1.setPlaceholderText("Введіть текст для пошуку...")
        self.btn_clear_filter = QPushButton(" ✖  Очистити")
        filter_layout.addWidget(QLabel("Фільтр:"))
        filter_layout.addWidget(self.filter_field)
        filter_layout.addWidget(self.filter_input1)
        filter_layout.addWidget(self.btn_clear_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.back_btn.clicked.connect(self.go_back)
        self.btn_add.clicked.connect(self.add_service)
        self.btn_edit.clicked.connect(self.edit_service)
        self.btn_delete.clicked.connect(self.delete_service)
        self.btn_details.clicked.connect(self.show_details)
        self.sort_field.currentIndexChanged.connect(self.apply_filter_and_sort)
        self.sort_order.currentIndexChanged.connect(self.apply_filter_and_sort)
        self.filter_input1.textChanged.connect(self.apply_filter_and_sort)
        self.btn_clear_filter.clicked.connect(self.clear_filter)
        self.filter_field.currentIndexChanged.connect(self.apply_filter_and_sort)

        self.all_rows = []
        self.current_rows = []
        self.load_data()

    def go_back(self):
        current_geometry = self.geometry()
        self.main_window.setGeometry(current_geometry)
        self.hide()
        self.main_window.show()

    def load_data(self):
        try:
            self.cursor.execute("SELECT s.id, s.name, m.name, c.name, s.duration_min, s.price_usd, s.stock_quantity FROM Services s LEFT JOIN Masters m ON s.master_id = m.id LEFT JOIN Categories c ON s.category_id = c.id")
            self.all_rows = self.cursor.fetchall()
            self.apply_filter_and_sort()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити дані: {e}")

    def apply_filter_and_sort(self):
        filter_text = self.filter_input1.text().lower()
        field_name = self.filter_field.currentText()
        field_idx = {"Назва": 1, "Майстер": 2, "Категорія": 3}.get(field_name, 1)
        if not filter_text:
            self.current_rows = self.all_rows[:]
        else:
            self.current_rows = [row for row in self.all_rows if filter_text in str(row[field_idx] or '').lower()]

        sort_key_name = self.sort_field.currentText()
        sort_col_idx = {"Назва": 1, "Майстер": 2, "Категорія": 3, "Тривалість": 4, "Ціна ($)": 5, "Залишок": 6}.get(sort_key_name, 1)
        is_numeric = sort_key_name in ["Тривалість", "Ціна ($)", "Залишок"]
        is_reverse = self.sort_order.currentText() == "За спаданням"

        def sort_key(row):
            val = row[sort_col_idx]
            if is_numeric:
                try: return float(val)
                except (ValueError, TypeError): return 0
            return str(val or '').lower()

        self.current_rows.sort(key=sort_key, reverse=is_reverse)
        self.display_data(self.current_rows)

    def clear_filter(self):
        self.filter_input1.clear()

    def display_data(self, rows):
        headers = ["ID", "Назва", "Майстер", "Категорія", "Тривалість (хв)", "Ціна ($)", "Залишок (шт)"]
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.hideColumn(0)
        self.table.setAlternatingRowColors(True)
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def show_details(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Увага", "Оберіть позицію для перегляду деталей.")
            return
        service_id = self.current_rows[selected_row][0]
        self.cursor.execute("SELECT s.id, s.name, m.name, c.name, s.duration_min, s.price_usd, s.stock_quantity FROM Services s LEFT JOIN Masters m ON s.master_id=m.id LEFT JOIN Categories c ON s.category_id=c.id WHERE s.id=?", (service_id,))
        details = self.cursor.fetchone()
        if details:
            self.details_window = ServiceDetailsWindow(details)
            self.details_window.show()

    def add_service(self):
        dialog = ServiceEditDialog()
        if dialog.exec_():
            self.load_data()

    def edit_service(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Увага", "Оберіть позицію для редагування.")
            return
        service_id = self.current_rows[selected_row][0]
        self.cursor.execute("SELECT * FROM Services WHERE id=?", (service_id,))
        row = self.cursor.fetchone()
        if row:
            service = {'id': row[0], 'name': row[1], 'master_id': row[2], 'category_id': row[3], 'duration_min': row[4], 'price_usd': row[5], 'stock_quantity': row[6]}
            dialog = ServiceEditDialog(service)
            if dialog.exec_():
                self.load_data()

    def delete_service(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Увага", "Оберіть позицію для видалення.")
            return
        service_id = self.current_rows[selected_row][0]
        reply = QMessageBox.question(self, "Підтвердження", f"Видалити послугу ID {service_id}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.cursor.execute("DELETE FROM Services WHERE id=?", (service_id,))
                self.conn.commit()
                self.load_data()
            except Exception as e:
                self.conn.rollback()
                QMessageBox.critical(self, "Помилка", f"Не вдалося видалити: {e}")