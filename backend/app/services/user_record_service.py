from app.repositories.user_record_repository import UserRecordRepository
from app.schemas.user_record import UserRecordCreateRequest, UserRecordResponse, UserRecordUpdateRequest
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.exceptions import BusinessError


class UserRecordService:
    def __init__(self, db: Session, user_id: int) -> None:
        self.repository = UserRecordRepository(db)
        self.user_id = user_id

    def create_record(self, payload: UserRecordCreateRequest) -> UserRecordResponse:
        age = self._calculate_age(payload.birthday)
        zodiac = self._calculate_zodiac(payload.birthday)
        horoscope = self._calculate_horoscope(payload.birthday)
        birth_zodiac_sign = self._calculate_birth_zodiac_sign(payload.birthday)

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

    def update_record(self, payload: UserRecordUpdateRequest) -> UserRecordResponse:
        record = self.repository.get_by_user(self.user_id, payload.id)
        if not record:
            raise BusinessError("档案不存在", status_code=404)

        age = self._calculate_age(payload.birthday)
        zodiac = self._calculate_zodiac(payload.birthday)
        horoscope = self._calculate_horoscope(payload.birthday)
        birth_zodiac_sign = self._calculate_birth_zodiac_sign(payload.birthday)

        updated = self.repository.update(
            record,
            name=payload.name,
            birthday=payload.birthday,
            gender=payload.gender,
            birthplace=payload.birthplace,
            age=age,
            zodiac=zodiac,
            horoscope=horoscope,
            birth_zodiac_sign=birth_zodiac_sign,
        )
        return self._to_response(updated)

    def list_records(self) -> list[UserRecordResponse]:
        records = self.repository.list_by_user(self.user_id)
        return [self._to_response(record) for record in records]

    def delete_record(self, record_id: int) -> None:
        deleted = self.repository.delete(self.user_id, record_id)
        if not deleted:
            raise BusinessError("档案不存在", status_code=404)

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
        return (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )

    def _calculate_zodiac(self, birthday: datetime) -> str:
        animals = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]
        return animals[birthday.year % 12]

    def _calculate_horoscope(self, birthday: datetime) -> str:
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

    def _calculate_birth_zodiac_sign(self, birthday: datetime) -> str:
        return self._calculate_zodiac(birthday)
