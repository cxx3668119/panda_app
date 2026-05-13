from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.app_user import AppUser
from app.repositories.account_repository import AccountRepository
from app.repositories.auth_repository import AuthRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.daily_fortune_repository import DailyFortuneRepository
from app.repositories.growth_repository import GrowthRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.reminder_repository import ReminderRepository
from app.services.account_service import AccountService
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.daily_fortune_service import DailyFortuneService
from app.services.growth_archive_service import GrowthArchiveService
from app.services.profile_service import ProfileService
from app.services.reminder_service import ReminderService
from app.services.user_record_service import UserRecordService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db))


def get_account_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> AccountService:
    return AccountService(AccountRepository(db, user))


def get_profile_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> ProfileService:
    return ProfileService(ProfileRepository(db, user))


def get_daily_fortune_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> DailyFortuneService:
    return DailyFortuneService(DailyFortuneRepository(db, user))


def get_chat_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> ChatService:
    profile_repository = ProfileRepository(db, user)
    return ChatService(ChatRepository(db, user, profile_repository), profile_repository)


def get_growth_archive_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> GrowthArchiveService:
    return GrowthArchiveService(GrowthRepository(db, user))


def get_reminder_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> ReminderService:
    return ReminderService(ReminderRepository(db, user))


def get_user_record_service(
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
) -> UserRecordService:
    return UserRecordService(db, user.id)
