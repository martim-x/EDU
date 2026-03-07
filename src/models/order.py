from models.exceptions import InvalidUser, InvalidProducts, BusinessLogicError
from models.product import Product
from models.user import User


class Order:
    def __init__(self, user: User, products: list[Product]) -> None:
        if not isinstance(user, User):
            raise InvalidUser(f"Ожидается User, получен {type(user).__name__}")
        if not isinstance(products, list) or not all(
            isinstance(p, Product) for p in products
        ):
            raise InvalidProducts("Все элементы списка должны быть объектами Product")
        if not products:
            raise BusinessLogicError("Список товаров не может быть пустым")

        self.user = user
        self.products: list[Product] = products

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise InvalidProducts(
                f"Ожидается Product, получен {type(product).__name__}"
            )
        self.products.append(product)

    def calculate_total(self) -> float:
        return round(sum(self.products), 2)

    def __str__(self) -> str:
        return f"Заказ пользователя {self.user.name} на сумму {self.calculate_total()} руб."

    def __repr__(self) -> str:
        return f"Order({self.user!r}, {self.products!r})"
