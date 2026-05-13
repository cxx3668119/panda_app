from sqlalchemy.orm import Session

from app.core.exceptions import BusinessError
from app.core.record_utils import calculate_age, calculate_horoscope, calculate_zodiac
from app.repositories.user_record_repository import UserRecordRepository
from app.schemas.user_record import UserRecordCreateRequest, UserRecordResponse, UserRecordUpdateRequest


class UserRecordService:
    def __init__(self, db: Session, user_id: int) -> None:
        self.repository = UserRecordRepository(db)
        self.user_id = user_id

    def create_record(self, payload: UserRecordCreateRequest) -> UserRecordResponse:
        zodiac = calculate_zodiac(payload.birthday)
        record = self.repository.create(
            user_id=self.user_id,
            name=payload.name,
            birthday=payload.birthday,
            gender=payload.gender,
            birthplace=payload.birthplace,
            age=calculate_age(payload.birthday),
            zodiac=zodiac,
            horoscope=calculate_horoscope(payload.birthday),
            birth_zodiac_sign=zodiac,
        )
        return self._to_response(record)

    def update_record(self, payload: UserRecordUpdateRequest) -> UserRecordResponse:
        record = self.repository.get_by_user(self.user_id, payload.id)
        if not record:
            raise BusinessError("档案不存在", status_code=404)

        zodiac = calculate_zodiac(payload.birthday)
        updated = self.repository.update(
            record,
            name=payload.name,
            birthday=payload.birthday,
            gender=payload.gender,
            birthplace=payload.birthplace,
            age=calculate_age(payload.birthday),
            zodiac=zodiac,
            horoscope=calculate_horoscope(payload.birthday),
            birth_zodiac_sign=zodiac,
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
