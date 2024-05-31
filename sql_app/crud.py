from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.sql import func
from . import models, schemas
# JWT
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

def authenticate_user(db: Session, login_id: str, password: str):
    user = get_user_login(db, login_id)
    if not user:
        print("ユーザー無し")
        return False
    else:
        print("ユーザーいる！")
        # Password hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # OAuth2 settings
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

        if not pwd_context.verify(password, user.password):  # 第一引数が生パスワード、第二引数が暗号化パスワード
            # pwd_context.verify(plain_password, hashed_password)
            # print("パスワード一致！", plain_password, hashed_password)
            print("パスワード一致しません！", password, user.password)
            return False
        print("パスワード一致！", password, user.password)
        return user

def create_user(db: Session, user: schemas.User):
    db_user = models.User(id=user.id, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_login(db: Session, login_id: str):
    return db.query(models.User).filter(models.User.login_id == login_id).first()

def all_user(db: Session):
    db_user = db.query(models.User).filter(models.User.is_active == True).order_by(models.User.id).all()
    for user in db_user:
        user.created_at_str = user.created_at.strftime("%Y/%m/%d")
        # user.logined_at_str = user.logined_at.strftime("%Y/%m/%d")
    return db_user

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id, models.Question.is_active == True).first()

# def all_question(db: Session):
#     return db.query(models.Question).order_by(models.Question.id)
def all_question(db: Session):
    return db.query(models.Question).filter(models.Question.is_active == True).order_by(models.Question.id)

def get_participant(db: Session, participant_id: int):
    return db.query(models.Participant).filter(models.Participant.id == participant_id).first()

def all_participant(db: Session):
    return db.query(models.Participant).order_by(models.Participant.id)

# def all_event(db: Session):
#     return db.query(models.Event).order_by(models.Event.id)
def all_event(db: Session):
    db_event = db.query(models.Event).filter(models.Event.is_active == True).order_by(models.Event.id)
    for event in db_event:
        event.created_at_str = event.opened_at.strftime("%Y/%m/%d %H:%M")
        event.logined_at_str = event.end_at.strftime("%Y/%m/%d %H:%M")
    return db_event

def active_event(db: Session):
    db_event = db.query(models.Event).order_by(models.Event.id)
    for event in db_event:
        event.opened_at_str = event.opened_at.strftime("%Y/%m/%d %H:%M")
        event.end_at_str = event.end_at.strftime("%Y/%m/%d %H:%M")
    db_event = db.query(models.Event).filter(
        (models.Event.opened_at <= func.now()) &
        (models.Event.end_at >= func.now()) &
        (models.Event.is_active == True)
        ).order_by(models.Event.created_at)
    return db_event

def active_question(db: Session):
    return db.query(models.Question).filter(models.Question.is_active is True).order_by(models.Event.id)

def get_event(db: Session, event_id: int):
    q = db.query(models.Event).filter(models.Event.id == event_id,models.Event.is_active == True)
    print(q.statement)
    return q.first()