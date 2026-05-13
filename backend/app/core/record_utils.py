from __future__ import annotations

from datetime import datetime


def calculate_age(birthday: datetime, *, now: datetime | None = None) -> int:
    today = now or datetime.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def calculate_zodiac(birthday: datetime) -> str:
    animals = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]
    return animals[birthday.year % 12]


def calculate_horoscope(birthday: datetime) -> str:
    month = birthday.month
    day = birthday.day
    signs = [
        ("水瓶座", (1, 20)),
        ("双鱼座", (2, 19)),
        ("白羊座", (3, 21)),
        ("金牛座", (4, 20)),
        ("双子座", (5, 21)),
        ("巨蟹座", (6, 22)),
        ("狮子座", (7, 23)),
        ("处女座", (8, 23)),
        ("天秤座", (9, 23)),
        ("天蝎座", (10, 24)),
        ("射手座", (11, 23)),
        ("摩羯座", (12, 22)),
    ]
    for index, (sign, (sign_month, start_day)) in enumerate(signs):
        if month == sign_month:
            if day >= start_day:
                return sign
            return signs[index - 1][0] if index > 0 else "摩羯座"
    return "摩羯座"
