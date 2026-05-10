from app.repositories.user_record_repository import UserRecordRepository
from app.schemas.user_record import UserRecordCreateRequest, UserRecordResponse
from sqlalchemy.orm import Session
from datetime import datetime


class UserRecordService:
    def __init__(self, db: Session, user_id: int) -> None:
        self.repository = UserRecordRepository(db)
        self.user_id = user_id

    def create_record(self, payload: UserRecordCreateRequest) -> UserRecordResponse:
        age = self._calculate_age(payload.birthday)  # 年龄
        zodiac = self._calculate_zodiac(payload.birthday)  # 生肖
        horoscope = self._calculate_horoscope(payload.birthday)  # 星座
        birth_zodiac_sign = self._calculate_birth_zodiac_sign(
            payload.birthday
        )  # 生辰八字

        record = self.repository.create(
            user_id=self.user_id,
            name=payload.name,
            birthday=payload.birthday,
            gender=payload.gender,
            birthplace=payload.birthplace,
            age=age,
            zodiac=zodiac,
            horoscope=horoscope,
            birth_zodiac_sign=birth_zodiac_sign,
        )
        return self._to_response(record)

    def _to_response(self, record) -> UserRecordResponse:
        return UserRecordResponse(
            id=record.id,
            name=record.name,
            birthday=record.birthday,
            gender=record.gender,
            birthZodiacSign=record.birth_zodiac_sign,
            birthplace=record.birthplace,
            age=record.age,
            zodiac=record.zodiac,
            horoscope=record.horoscope,
        )

    def _calculate_age(self, birthday: datetime) -> int:
        today = datetime.today()
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        return age

    def _calculate_zodiac(self, birthday: datetime) -> str:
        animals = [
            "猴",
            "鸡",
            "狗",
            "猪",
            "鼠",
            "牛",
            "虎",
            "兔",
            "龙",
            "蛇",
            "马",
            "羊",
        ]
        return animals[birthday.year % 12]

    def _calculate_horoscope(self, birthday: datetime) -> str:
        month = birthday.month
        day = birthday.day
        signs = [
            ("摩羯座", (1, 20)),
            ("水瓶座", (2, 19)),
            ("双鱼座", (3, 21)),
            ("白羊座", (4, 20)),
            ("金牛座", (5, 21)),
            ("双子座", (6, 22)),
            ("巨蟹座", (7, 23)),
            ("狮子座", (8, 23)),
            ("处女座", (9, 23)),
            ("天秤座", (10, 24)),
            ("天蝎座", (11, 23)),
            ("射手座", (12, 22)),
            ("摩羯座", (12, 32)),
        ]
        for sign, (sign_month, start_day) in signs:
            if month == sign_month and day < start_day:
                return sign
        return "摩羯座"

    def _calculate_birth_zodiac_sign(self, birthday: datetime) -> str:
        return self._calculate_zodiac(birthday)

    def list_records(self) -> list[UserRecordResponse]:
        records = self.repository.list_by_user(self.user_id)
        return [self._to_response(record) for record in records]
