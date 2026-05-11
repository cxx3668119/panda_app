from fastapi import APIRouter, Depends
from app.api.dependencies import get_user_record_service
from app.core.response import ok
from app.schemas.user_record import UserRecordCreateRequest, UserRecordDeleteRequest, UserRecordUpdateRequest
from app.services.user_record_service import UserRecordService

router = APIRouter(prefix="/records", tags=["user-records"])


@router.post("/create")
def create_record(
    payload: UserRecordCreateRequest,
    service: UserRecordService = Depends(get_user_record_service),
):
    return ok(service.create_record(payload).model_dump())

@router.post("/update")
def update_record(
    payload: UserRecordUpdateRequest,
    service: UserRecordService = Depends(get_user_record_service),
):
    return ok(service.update_record(payload).model_dump())

@router.get("/list")
def list_records(
    service: UserRecordService = Depends(get_user_record_service),
):
    return ok([item.model_dump() for item in service.list_records()])


@router.post("/delete")
def delete_record(
    payload: UserRecordDeleteRequest,
    service: UserRecordService = Depends(get_user_record_service),
):
    service.delete_record(payload.id)
    return ok()

