from datetime import date, timedelta

def count_streak(days: list[date], today: date) -> int:
    streak = 0
    expected = today
    for day in days:
        if day != expected:
            break
        streak += 1
        expected -= timedelta(days=1)
    return streak
