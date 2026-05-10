from fastapi import APIRouter, Depends
from app.api.dependencies import get_user_record_service
from app.core.response import ok
from app.schemas.user_record import UserRecordCreateRequest
from app.services.user_record_service import UserRecordService

router = APIRouter(prefix="/records", tags=["user-records"])


@router.post("/create")
def create_record(
    payload: UserRecordCreateRequest,
    service: UserRecordService = Depends(get_user_record_service),
):
    return ok(service.create_record(payload).model_dump())


@router.get("/list")
def list_records(
    service: UserRecordService = Depends(get_user_record_service),
):
    return ok([item.model_dump() for item in service.list_records()])
