from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    login_id: str
    name: str
    role: int
    is_active: bool
    password: str
    created_at: datetime
    logined_at: datetime
    created_at_str: str
    logined_at_str: str

    class Config:
        orm_mode = True

class Question(BaseModel):
    id: int
    title: str
    level: int
    problem: str
    event_id: int
    limit_millisec: int
    limit_memory: int
    in_format :str
    out_format :str
    in_sample_1 :str
    out_sample_1 :str
    in_sample_2 :str
    out_sample_2 :str
    condition: str
    created_at: datetime
    is_active:bool

    class Config:
        orm_mode = True

class Event(BaseModel):
    id: int
    title: str
    created_at: datetime
    opened_at: datetime
    is_active: bool
    # question_id: int
    end_at: datetime
    opened_at_str: str
    end_at_str : str

    class Config:
        orm_mode = True

class Participant(BaseModel):
    id: int
    user_id:int
    created_at: datetime
    event_id: int

    class Config:
        orm_mode = True

# Pydanticモデル
class LoginRequest(BaseModel):
    id: int
    password: str

class LoginResponse(BaseModel):
    role: int

#relationship
class EventWithPariticipant(Event):
    participant: List[Participant] = []

class EventWithQuestion(Event):
    # question: Question
    question: List[Question] = []

class ParticipantWithEvent(Participant):
    event: Event

class ParticipantWithUser(Participant):
    user: User

class UserWithQuestions(User):
    questions: List[Question] = []

class UserWithParticipants(User):
    participants: List[Participant] = []

class QuestionWithAuthor(Question):
    author: User

class QuestionWithEvents(Question):
    # event: List[Event] = []
    event: Event



