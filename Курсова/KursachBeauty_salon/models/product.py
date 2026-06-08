class Product:
    tax_rate = 0.2

    def __init__(self, name, price, stock_quantity):
        self.name = name
        self._price = price
        self.__stock_quantity = stock_quantity

    def get_price(self):
        return round(self._price * (1 + Product.tax_rate), 2)

    def reduce_stock(self, quantity):
        if quantity <= self.__stock_quantity:
            self.__stock_quantity -= quantity
            return True
        return False

    def get_stock(self):
        return self.__stock_quantity