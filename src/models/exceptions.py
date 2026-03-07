class SFMShopException(Exception):
    """Базовое исключение для проекта SFMShop"""


class ValidationError(SFMShopException):
    """Ошибка валидации данных"""


class BusinessLogicError(SFMShopException):
    """Ошибка бизнес-логики"""


class DatabaseError(SFMShopException):
    """Ошибка базы данных"""


class NegativePriceError(ValidationError):
    """Отрицательная цена"""


class InsufficientStockError(BusinessLogicError):
    """Товара недостаточно на складе"""


class InvalidOrderError(BusinessLogicError):
    """Заказ невалиден"""


class InvalidUser(DatabaseError):
    """Пользователь не передан или неверного типа"""


class InvalidProducts(DatabaseError):
    """Товары не переданы или неверного типа"""


class InvalidProductName(ValidationError):
    """Невалидное имя товара"""


class InvalidProductPrice(ValidationError):
    """Невалидная цена товара"""
