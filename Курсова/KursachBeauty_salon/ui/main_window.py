from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from .customers_ui import CustomersWindow
from .orders_ui import OrdersWindow
from .services_ui import ServicesWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управління | Yuliia Beauty Salon")

        self.customer_win = None
        self.order_win = None
        self.service_win = None

        self.resize(600, 450)
        self.setMinimumSize(550, 420)

        container = QWidget()
        self.layout = QVBoxLayout()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.layout.addStretch(1)

        self.label_welcome = QLabel("Вітаємо в 'Yuliia Beauty Salon'!")
        font_welcome = QFont("Arial", 26, QFont.Bold)
        self.label_welcome.setFont(font_welcome)
        self.label_welcome.setAlignment(Qt.AlignCenter)
        self.label_welcome.setStyleSheet("color: #5d3f94; margin-bottom: 10px;")
        self.layout.addWidget(self.label_welcome)

        self.label_slogan = QLabel("Місце, де ваша краса розквітає")
        font_slogan = QFont("Arial", 12, QFont.StyleItalic)
        self.label_slogan.setFont(font_slogan)
        self.label_slogan.setAlignment(Qt.AlignCenter)
        self.label_slogan.setStyleSheet("color: #6c757d; margin-bottom: 30px;")
        self.layout.addWidget(self.label_slogan)

        self.btn_customers = QPushButton("👤  Клієнти")
        self.btn_orders = QPushButton("🗓️  Записи та Замовлення")
        self.btn_services = QPushButton("💅  Послуги та Товари")

        for btn in [self.btn_customers, self.btn_orders, self.btn_services]:
            btn.setMinimumHeight(65)
            btn.setStyleSheet("font-size: 16pt;")
            self.layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.layout.addStretch(1)

        self.btn_customers.clicked.connect(self.open_customers)
        self.btn_orders.clicked.connect(self.open_orders)
        self.btn_services.clicked.connect(self.open_services)

    def _open_window(self, window_name):
        win = None
        current_geometry = self.geometry()

        if window_name == "customers":
            if self.customer_win is None:
                self.customer_win = CustomersWindow(self)
            win = self.customer_win
        elif window_name == "orders":
            if self.order_win is None:
                self.order_win = OrdersWindow(self)
            win = self.order_win
        elif window_name == "services":
            if self.service_win is None:
                self.service_win = ServicesWindow(self)
            win = self.service_win

        if win:
            win.setGeometry(current_geometry)
            win.show()
            self.hide()

    def open_customers(self): self._open_window("customers")
    def open_orders(self): self._open_window("orders")
    def open_services(self): self._open_window("services")