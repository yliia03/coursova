from .product import Product

class Service(Product):
    def __init__(self, name, master, category, duration_min, price, stock_quantity):
        super().__init__(name, price, stock_quantity)
        self.master = master
        self.category = category
        self.duration_min = duration_min

    def __str__(self):
        return f"{self.name} (Майстер: {self.master}, {self.duration_min} хв)"