from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_account_service
from app.core.response import ok
from app.core.security import get_current_user
from app.schemas.account import (
    AccountUpdateRequest,
    ChangePasswordRequest,
    SetCurrentRecordRequest,
)
from app.services.account_service import AccountService

router = APIRouter(prefix="/account", tags=["account"])


@router.get("/me")
def get_me(
    _: object = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    return ok(service.get_me().model_dump())


@router.patch("/me")
def update_me(
    payload: AccountUpdateRequest,
    _: object = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    return ok(service.update_me(payload).model_dump())


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    _: object = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    service.change_password(payload)
    return ok({"success": True})


@router.post("/set-current-record")
def set_bound_record(
    payload: SetCurrentRecordRequest,
    _: object = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    service.set_bound_record(payload)
    return ok({"success": True})
