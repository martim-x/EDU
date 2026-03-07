from abc import ABC, abstractmethod

from models.exceptions import ValidationError


class Payment(ABC):
    def __init__(self, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("Сумма платежа должна быть положительной")
        self.amount = amount

    @abstractmethod
    def process_payment(self) -> str: ...


class CardPayment(Payment):
    def __init__(self, amount: float, card_number: str) -> None:
        super().__init__(amount)
        clean = card_number.replace(" ", "")
        if not clean.isdigit() or len(clean) != 16:
            raise ValidationError("Номер карты должен содержать 16 цифр")
        self.__card_number = clean

    def process_payment(self) -> str:
        return f"Оплата картой **** {self.__card_number[-4:]}: {self.amount} руб."


class PayPalPayment(Payment):
    def __init__(self, amount: float, email: str) -> None:
        super().__init__(amount)
        if "@" not in email:
            raise ValidationError("Неверный формат email для PayPal")
        self.email = email

    def process_payment(self) -> str:
        return f"Оплата PayPal ({self.email}): {self.amount} руб."
