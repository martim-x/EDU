from models.exceptions import ValidationError


class User:
    def __init__(self, name: str, email: str) -> None:
        if not name or not isinstance(name, str):
            raise ValidationError("Имя пользователя не может быть пустым")
        self.name = name
        self._email: str = ""
        self.set_email(email)

    def set_email(self, email: str) -> None:
        if "@" not in email:
            raise ValidationError("Неверный формат email")
        self._email = email

    def get_email(self) -> str:
        return self._email

    def __str__(self) -> str:
        return f"Пользователь: {self.name}, Email: {self._email}"

    def __repr__(self) -> str:
        return f"User('{self.name}', '{self._email}')"
