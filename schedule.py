from datetime import datetime


class Scheduler:
    def __init__(self):
        self.__id = 0
        self.__storage: list[dict] = []

    def schedule(self, user_id: int, message: str, send_at: datetime):
        self.__storage.append(
            {
                "id": self.__id,
                "user_id": user_id,
                "message": message,
                "send_at": send_at,
            }
        )
        self.__id += 1
        now = datetime.now()
        for n in self.__storage:
            if n["send_at"] <= now:
                print(f"{n["user_id"]} {n["message"]}")
                self.__storage.remove(n)
