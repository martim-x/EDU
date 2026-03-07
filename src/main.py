import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from models import (
    CardPayment,
    Order,
    PayPalPayment,
    Product,
    SFMShopException,
    User,
    ValidationError,
)

# --- Пользователь ---
print("\n[1] Создание пользователя")
user = User("Иван", "ivan@test.com")
print(user)

# --- Товары ---
print("\n[2] Создание товаров")
product1 = Product("Ноутбук", 50000, 2)
product2 = Product("Мышь", 1500, 3)
print(product1)
print(product2)
print("repr:", repr(product1))

# --- Заказ ---
print("\n[3] Создание заказа")
order = Order(user, [product1, product2])
print(order)
total = order.calculate_total()
print(f"Общая стоимость заказа: {total} руб.")

# --- Добавление товара в заказ ---
print("\n[4] Добавление товара в заказ")
product3 = Product("Клавиатура", 3000, 1)
order.add_product(product3)
print(f"После добавления {product3.name}: {order.calculate_total()} руб.")

# --- Платежи ---
print("\n[5] Обработка платежей")
payments = [
    CardPayment(1000, "1234 5678 9012 3456"),
    PayPalPayment(2000, "test@paypal.com"),
]
for payment in payments:
    print(payment.process_payment())

# --- Сортировка товаров ---
print("\n[6] Сортировка товаров по цене")
sorted_products = sorted([product1, product2, product3])
for p in sorted_products:
    print(p)

# --- Сравнение товаров ---
print("\n[7] Сравнение товаров")
print(f"{product2.name} < {product1.name}: {product2 < product1}")
print(f"{product1.name} == {product1.name}: {product1 == Product('Ноутбук', 50000, 2)}")

# --- Обработка исключений ---
print("\n[8] Демонстрация обработки ошибок")

try:
    product1.set_price(-1000)
except ValidationError as e:
    print(f"  ValidationError (цена): {e}")

try:
    user.set_email("bad-email-format")
except ValidationError as e:
    print(f"  ValidationError (email): {e}")

try:
    order.add_product("не товар")  # type: ignore
except SFMShopException as e:
    print(f"  InvalidProducts {e}")

try:
    CardPayment(500, "1234")
except ValidationError as e:
    print(f"  ValidationError (карта): {e}")

try:
    Order(user, [])
except SFMShopException as e:
    print(f"  BusinessLogicError (пустой заказ): {e}")
