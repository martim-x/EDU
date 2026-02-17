from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class Notification:
    id: int
    user_id: str
    message: str
    send_at: datetime
    priority: Literal["high", "normal"] = "normal"


class Scheduler:
    def __init__(self):
        self.__id: int = 0
        self.__storage: list[Notification] = []

    def schedule(
        self,
        user_id: str,
        message: str,
        send_at: datetime,
        priority: Literal["high", "normal"] = "normal",
    ) -> None:
        notification = Notification(
            id=self.__id,
            user_id=user_id,
            message=message,
            send_at=send_at,
            priority=priority,
        )

        self.__storage.append(notification)
        self.__id += 1

    def run_pending(self):
        self.__storage.sort(key=lambda n: (n.priority != "high"))
        now = datetime.now()

        ready_to_send = [n for n in self.__storage if n.send_at <= now]
        self.__storage = [n for n in self.__storage if n.send_at > now]

        for n in ready_to_send:
            print(f"{n.user_id} {n.message}")
