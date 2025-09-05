from sqlalchemy.orm import Session
from models.user_model import User
def create_user(db: Session, user_data: dict):
   user = User(**user_data)
   db.add(user)
   db.commit()
   db.refresh(user)
   return user
def get_all_users(db: Session):
   return db.query(User).all()
def get_user_by_id(db: Session, user_id: int):
   return db.query(User).filter(User.id == user_id).first()
def update_user(db: Session, user_id: int, updates: dict):
   user = db.query(User).filter(User.id == user_id).first()
   if user:
       for key, value in updates.items():
           setattr(user, key, value)
       db.commit()
       db.refresh(user)
   return user
def delete_user(db: Session, user_id: int):
   user = db.query(User).filter(User.id == user_id).first()
   if user:
       db.delete(user)
       db.commit()
   return user
