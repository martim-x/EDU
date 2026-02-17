from datetime import datetime

from .schedule import Scheduler

scheduler = Scheduler()

scheduler.schedule("a1b2-c3d4", "Hello!", datetime.now())

scheduler.schedule("x9y8-z7w6", "Future message", datetime(2026, 3, 1, 12, 0))
