from repository.user_repository import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from utils.helper_functions import hash_password
from sqlalchemy.orm import Session
from serializers.user_serializer import UserCreate, UserUpdate


def add_user_service(db: Session, user_data: UserCreate):
    user_data.password = hash_password(user_data.password)
    return create_user(db, user_data.dict())


def list_users_service(db: Session):
    return get_all_users(db)


def get_user_service(db: Session, user_id: int):
    return get_user_by_id(db, user_id)


def update_user_service(db: Session, user_id: int, updates: UserUpdate):
    if updates.password:
        updates.password = hash_password(updates.password)
    return update_user(db, user_id, updates.dict(exclude_unset=True))


def delete_user_service(db: Session, user_id: int):
    return delete_user(db, user_id)
