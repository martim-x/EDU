from models.exceptions import ValidationError


class Product:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        if not name or not isinstance(name, str):
            raise ValidationError("Имя товара не может быть пустым")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        if quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")

        self.name = name
        self.price = price
        self.quantity = quantity

    def set_price(self, price: float) -> None:
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price

    def get_total_price(self) -> float:
        return self.price * self.quantity

    def __str__(self) -> str:
        return (
            f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"
        )

    def __repr__(self) -> str:
        return f"Product('{self.name}', {self.price}, {self.quantity})"

    def __lt__(self, other: "Product") -> bool:
        if not isinstance(other, Product):
            raise TypeError(f"Ожидается Product, получен {type(other).__name__}")
        return self.price < other.price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            raise TypeError(f"Ожидается Product, получен {type(other).__name__}")
        return self.name == other.name and self.price == other.price

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError(f"Ожидается Product, получен {type(other).__name__}")
        return self.get_total_price() + other.get_total_price()

    def __radd__(self, other: int | float) -> float:
        if not isinstance(other, (int, float)):
            raise TypeError(f"Ожидается число, получен {type(other).__name__}")
        return other + self.get_total_price()
