from typing import List
from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func
from datetime import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine

from functools import lru_cache
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

@lru_cache()
def get_settings():
    return settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ログインエンドポイント
@app.head('/login')
@app.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == request.id, models.User.password == request.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid ID or password")
    return {"role": user.role}

# READ
@app.get("/users/", response_model=List[schemas.User])
def read_user(db: Session = Depends(get_db)):
    db_user = crud.all_user(db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud  .get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/questions/", response_model=List[schemas.Question])
def read_question(db: Session = Depends(get_db)):
    db_question = crud.all_question(db)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/questions_active/", response_model=List[schemas.Question])
def read_question(db: Session = Depends(get_db)):
    db_question = crud.active_question(db)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/participants/", response_model=List[schemas.Participant])
def read_participant(db: Session = Depends(get_db)):
    db_participant = crud.all_participant(db)
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.get("/participants/{participant_id}", response_model=schemas.Participant)
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = crud  .get_participant(db, participant_id=participant_id)
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant


@app.get("/events/", response_model=List[schemas.Event])
def read_event(db: Session = Depends(get_db)):
    db_event = crud.active_event(db)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_event

# CREATE
@app.post("/users/create")
async def create_user(name: str = Body(), role: int = Body(), login_id:str=Body(), password: str = Body(), is_active: bool = Body(), db: Session = Depends(get_db)):
    user_add = models.User(name=name, role=role, login_id=login_id, password=password, is_active=is_active)
    db.add(user_add)
    db.flush()
    db.commit()
    return "Insert completed !!"

@app.post("/questions/create")
async def create_question(event_id: int = Body(), title: str = Body(), condition: str=Body(), level: int = Body(), limit_memory: int = Body(), limit_millisec: int = Body(), problem: str = Body(), in_format: str = Body(), out_format: str = Body(), in_sample_1:str=Body(), out_sample_1:str=Body(), in_sample_2:str=Body(), out_sample_2:str=Body(), in_test_1: str = Body(), out_test_1: str = Body(), in_test_2: str = Body(), out_test_2: str = Body(), in_test_3: str = Body(), out_test_3: str = Body(), in_test_4: str = Body(), out_test_4: str = Body(), in_test_5: str = Body(), out_test_5: str = Body(), is_active: bool = Body(), db: Session = Depends(get_db)):
    question_add = models.Question(event_id=event_id, title=title, level=level, condition=condition, limit_memory=limit_memory, limit_millisec=limit_millisec,problem=problem,in_format=in_format,out_format=out_format,in_sample_1=in_sample_1,out_sample_1=out_sample_1,in_sample_2=in_sample_2,out_sample_2=out_sample_2,in_test_1=in_test_1, out_test_1=out_test_1, in_test_2=in_test_2,out_test_2=out_test_2,in_test_3=in_test_3,out_test_3=out_test_3,in_test_4=in_test_4,out_test_4=out_test_4,in_test_5=in_test_5,out_test_5=out_test_5 ,is_active=is_active)
    db.add(question_add)
    db.flush()
    db.commit()
    return "Insert completed !!"

@app.post("/events/create")
async def create_event(title: str = Body(), opened_at: str = Body(), end_at: str=Body(), is_active: bool=Body(), db: Session = Depends(get_db)):
    event_add = models.Event(title=title, opened_at=opened_at, end_at=end_at, is_active=is_active)
    db.add(event_add)
    db.flush()
    db.commit()
    return "Insert completed !!"

# UPDATE
@app.put("/users/update/{user_id}")
async def update_user(user_id: int, name: str = Body(), role: int = Body(), login_id:str=Body(), password: str = Body(), is_active: bool=Body(), db: Session = Depends(get_db)):
    user_update = db.query(models.User).filter(models.User.id == user_id).update({
        models.User.name: name,
        models.User.role: role,
        models.User.login_id: login_id,
        models.User.password: password,
        models.User.is_active: is_active
        })
    db.flush()
    db.commit()
    return "Update completed !!"

@app.put("/users/update2/{user_id}")
async def update_user(user_id: int, name: str = Body(), role: int = Body(), login_id:str=Body(), is_active: bool=Body(), db: Session = Depends(get_db)):
    user_update = db.query(models.User).filter(models.User.id == user_id).update({
        models.User.name: name,
        models.User.role: role,
        models.User.login_id: login_id,
        models.User.is_active: is_active
        })
    db.flush()
    db.commit()
    return "Update completed !!"

@app.put("/questions/update/{question_id}")
async def update_question(question_id: int, event_id: int = Body(), title: str = Body(), condition: str=Body(), level: int = Body(), limit_memory: int = Body(), limit_millisec: int = Body(), problem: str = Body(), in_format: str = Body(), out_format: str = Body(), in_sample_1:str=Body(), out_sample_1:str=Body(), in_sample_2:str=Body(), out_sample_2:str=Body(), in_test_1: str = Body(), out_test_1: str = Body(), in_test_2: str = Body(), out_test_2: str = Body(), in_test_3: str = Body(), out_test_3: str = Body(), in_test_4: str = Body(), out_test_4: str = Body(), in_test_5: str = Body(), out_test_5: str = Body(), is_active: bool = Body(), db: Session = Depends(get_db)):
    values_to_update = {
        models.Question.event_id: event_id,
        models.Question.title: title,
        models.Question.level: level,
        models.Question.condition: condition,
        models.Question.limit_memory: limit_memory,
        models.Question.limit_millisec: limit_millisec,
        models.Question.problem: problem,
        models.Question.in_format: in_format,
        models.Question.out_format: out_format,
        models.Question.in_sample_1: in_sample_1,
        models.Question.out_sample_1: out_sample_1,
        models.Question.in_sample_2: in_sample_2,
        models.Question.out_sample_2: out_sample_2,
        models.Question.in_test_1: in_test_1,
        models.Question.out_test_1: out_test_1,
        models.Question.in_test_2: in_test_2,
        models.Question.out_test_2: out_test_2,
        models.Question.in_test_3: in_test_3,
        models.Question.out_test_3: out_test_3,
        models.Question.in_test_4: in_test_4,
        models.Question.out_test_4: out_test_4,
        models.Question.in_test_5: in_test_5,
        models.Question.out_test_5: out_test_5,
        models.Question.is_active: is_active
    }
    db.query(models.Question).filter(models.Question.id == question_id).update(values_to_update)
    db.commit()
    return "Update completed !!"

@app.put("/events/update/{event_id}")
async def update_event(event_id: int, title: str = Body(), opened_at: str = Body(), end_at:str=Body(), is_active: bool=Body(), db: Session = Depends(get_db)):
    user_event = db.query(models.Event).filter(models.Event.id == event_id).update({
        models.Event.title: title,
        models.Event.opened_at: opened_at,
        models.Event.end_at: end_at,
        models.Event.is_active: is_active
        })
    db.flush()
    db.commit()
    return "Update completed !!"

# deactivate
@app.put("/users/{user_id}")
async def deactivateUser(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.is_active = False
        db.flush()
        db.commit()
        return {"message": "User deactivated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/questions/{question_id}")
async def deactivateQuestion(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question:
        question.is_active = False
        db.flush()
        db.commit()
        return {"message": "User deactivated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/events/{event_id}")
async def deactivateEvent(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        event.is_active = False
        db.flush()
        db.commit()
        return {"message": "User deactivated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_delete = db.query(models.User).filter(models.User.id == user_id).delete()
    db.flush()
    db.commit()
    return "Delete completed !!"

# JOIN
@app.get("/users/wp/{user_id}", response_model=schemas.UserWithParticipants)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/wq/{user_id}", response_model=schemas.UserWithQuestions)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/questions/we/", response_model=List[schemas.QuestionWithEvents])
def read_question(db: Session = Depends(get_db)):
    db_question = crud.all_question(db)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/questions/we/{question_id}", response_model=schemas.QuestionWithEvents)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/questions/wa/{question_id}", response_model=schemas.QuestionWithAuthor)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud  .get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/participants/wu/{participant_id}", response_model=schemas.ParticipantWithUser)
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = crud  .get_participant(db, participant_id=participant_id)
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.get("/participants/we/{participant_id}", response_model=schemas.ParticipantWithEvent)
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = crud  .get_participant(db, participant_id=participant_id)
    if db_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.get("/events/wq/{event_id}", response_model=schemas.EventWithQuestion)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud  .get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_event

@app.get("/events/wp/{event_id}", response_model=schemas.EventWithPariticipant)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_event