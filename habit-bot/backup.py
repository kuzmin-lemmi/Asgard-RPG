"""Резервная копия базы. Можно запускать, не останавливая бота."""
import sqlite3

import clock

name = f"backup-{clock.today().isoformat()}.db"

source = sqlite3.connect("habits.db")
target = sqlite3.connect(name)
with target:
    source.backup(target)
source.close()
target.close()

print("Копия готова:", name)
