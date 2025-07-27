from datetime import datetime


def new_reminder(datetime_str: str, title: str, description: str = ""):
    datetime_obj = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
    return f"Напоминание {title} установлено в {datetime_obj}"
