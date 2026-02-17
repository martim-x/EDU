from datetime import datetime

from schedule import Scheduler

scheduler = Scheduler()
now = datetime.now()

scheduler.schedule("a1b2g-c3d4hf", "Hello!1", now)
scheduler.schedule("a345h-cs3d4h", "Hello!2", now)
scheduler.schedule("a232s-c3scfg", "Hello!3", now, "high")
scheduler.schedule("a1b2h-c3scd4", "Hello!4", now, "high")
scheduler.run_pending()

scheduler.schedule("x56u8-z657w6", "Future message1", datetime(2026, 3, 1, 12, 0))
scheduler.schedule("x9y8j-z7w6yj", "Future message2", datetime(2026, 3, 1, 12, 0))
scheduler.run_pending()
