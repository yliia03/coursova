from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
)
from models.database import DatabaseManager

class ServiceEditDialog(QDialog):
    def __init__(self, service=None):
        super().__init__()
        self.setWindowTitle("Редагування послуги" if service else "Додавання послуги")
        self.service = service
        self.resize(450, 350)

        self.db = DatabaseManager()
        self.conn = self.db.connect()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()
        form = QFormLayout()

        self.name_edit = QLineEdit()
        self.master_combo = QComboBox()
        self.category_combo = QComboBox()
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(0, 360)
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0, 10000)
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 1000)

        self.load_comboboxes()

        form.addRow("Назва:", self.name_edit)
        form.addRow("Майстер:", self.master_combo)
        form.addRow("Категорія:", self.category_combo)
        form.addRow("Тривалість (хв, 0 для товару):", self.duration_spin)
        form.addRow("Ціна ($):", self.price_spin)
        form.addRow("Залишок (шт):", self.stock_spin)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton(" 💾 Зберегти")
        self.btn_cancel = QPushButton(" ❌ Скасувати")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_service)
        self.btn_cancel.clicked.connect(self.reject)

        if self.service:
            self.load_data()

    def load_comboboxes(self):
        self.cursor.execute("SELECT id, name FROM Masters")
        for mid, name in self.cursor.fetchall():
            self.master_combo.addItem(name, mid)
        self.cursor.execute("SELECT id, name FROM Categories")
        for cid, name in self.cursor.fetchall():
            self.category_combo.addItem(name, cid)

    def load_data(self):
        self.name_edit.setText(self.service['name'])
        self.duration_spin.setValue(self.service['duration_min'])
        self.price_spin.setValue(self.service['price_usd'])
        self.stock_spin.setValue(self.service['stock_quantity'])

        master_index = self.master_combo.findData(self.service['master_id'])
        if master_index >= 0: self.master_combo.setCurrentIndex(master_index)

        category_index = self.category_combo.findData(self.service['category_id'])
        if category_index >= 0: self.category_combo.setCurrentIndex(category_index)

    def save_service(self):
        name = self.name_edit.text().strip()
        master_id = self.master_combo.currentData()
        category_id = self.category_combo.currentData()
        duration_min = self.duration_spin.value()
        price = self.price_spin.value()
        stock = self.stock_spin.value()

        if not name:
            QMessageBox.warning(self, "Помилка", "Назва є обов'язковою!")
            return

        try:
            if self.service:
                self.cursor.execute("""
                UPDATE Services SET name=?, master_id=?, category_id=?, duration_min=?,
                price_usd=?, stock_quantity=? WHERE id=?
                """, (name, master_id, category_id, duration_min, price, stock, self.service['id']))
            else:
                self.cursor.execute("""
                INSERT INTO Services (name, master_id, category_id, duration_min, price_usd, stock_quantity)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (name, master_id, category_id, duration_min, price, stock))

            self.conn.commit()
            self.accept()
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Помилка", f"Помилка при збереженні: {e}")