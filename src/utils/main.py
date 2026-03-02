# Создать систему хранения данных о пользователях и товарах, реализовать операции добавления, поиска и проверки уникальности.

# Небольшое пояснение:

# Нужно создать:

# Словарь пользователей, где ключ - ID пользователя (число), значение - словарь с данными (name, email)
# Словарь товаров, где ключ - название товара (строка), значение - словарь с ценой и категорией
# Множество уникальных посетителей
# Реализовать операции:

# Добавление пользователя (ID 1: name "Иван", email "ivan@test.com")
# Поиск товара "Ноутбук" и вывод его цены
# Проверка, был ли посетитель "user_123" на сайте (добавить его в множество, затем проверить)
# Начни с этого:

from dataclasses import dataclass

# storage
user_storage = {}
product_storage = {}
visitors_storage = set()


# types
@dataclass(frozen=True)
class User:
    id: int  # key
    name: str
    email: str


@dataclass(frozen=True)
class Visitor:
    name: str


# @dataclass(frozen=True)
# class Product:
#     name: str  # key
#     price: int
#     category: str


# user
def add_user(user: User) -> None:
    user_storage[user.id] = {"name": user.name, "email": user.email}
    print(f"Пользователь добавлен: {'name': '{user.name}', 'email': '{user.email}'}")


def has_user(user_id: int) -> User | None:
    user: User | None = user_storage.get(user_id)
    (
        print(
            f"Пользователь существует {'name': '{user.name}', 'email': '{user.email}'}"
        )
        if user
        else print(f"Пользователся с id {user_id}не существует")
    )
    return user_storage.get(user_id)


# visitor
def add_visitor(visitor: Visitor) -> None:
    visitors_storage.add(visitor)
    print(f"Посетитель добавлен: {'name': '{visitor.name}'}")


def has_visitor(visitor_name: str) -> bool:
    (
        print(f"Посетитель существует {'name': '{visitor_name}'}")
        if visitor_name in visitors_storage
        else print(f"Посетиеля с name {visitor_name}не существует")
    )
    return visitor_name in visitors_storage


# product
def add_product(product: Product) -> None:
    product_storage[product.name] = {
        "price": product.price,
        "category": product.category,
    }
    print(
        f"Товар добавлен: {'price': '{product.price}', 'category': '{product.category}'}"
    )


def has_product(product_name: str) -> Product | None:
    product: Product | None = product_storage.get(product_name)

    (
        print(
            f"Товар существует {'price': '{product.price}', 'email': '{product.category}'}"
        )
        if product
        else print(f"Товара с product_name {product_name}не существует")
    )

    return product_storage.get(product_name)


# Добавление пользователя (ID 1: name "Иван", email "ivan@test.com")
# Поиск товара "Ноутбук" и вывод его цены
# Проверка, был ли посетитель "user_123" на сайте (добавить его в множество, затем проверить)


add_user(User(id=1, name="Иван", email="ivan@test.com"))
has_user(1)
has_user(2)

add_product(Product(name="Ноутбук", price=999, category="electronic"))
has_product("Ноутбук")
has_product("Компьютер")

add_visitor(Visitor(name="Иван"))
has_visitor("Иван")
has_visitor("Не Иван")
