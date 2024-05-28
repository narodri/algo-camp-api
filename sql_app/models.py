from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    logined_at = Column(DateTime(timezone=True), default=func.now())
    created_at_str = Column(String)
    logined_at_str = Column(String)
    login_id = Column(String)
    name = Column(String)
    role = Column(Integer)
    password = Column(String)
    is_active = Column(Boolean)
    access_token = Column(String)
    access_expired = Column(DateTime(timezone=True), default=func.now())
    access_expired = Column(DateTime(timezone=True))
    profile_image_path = Column(String)
    #relationship
    questions = relationship("Question", back_populates="author")
    participants = relationship("Participant", back_populates="user")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    title = Column(String, default="")
    condition = Column(String)
    level = Column(Integer)
    problem = Column(String)
    limit_millisec = Column(Integer, default=2000)
    limit_memory = Column(Integer, default=2000000)
    in_format = Column(String)
    out_format = Column(String)
    in_sample_1 = Column(String)
    out_sample_1 = Column(String)
    in_sample_2 = Column(String)
    out_sample_2 = Column(String)
    in_test_1 = Column(String, default="")
    in_test_2 = Column(String, default="")
    in_test_3 = Column(String, default="")
    in_test_4 = Column(String, default="")
    in_test_5 = Column(String, default="")
    out_test_1 = Column(String, default="")
    out_test_2 = Column(String, default="")
    out_test_3 = Column(String, default="")
    out_test_4 = Column(String, default="")
    out_test_5 = Column(String, default="")
    is_active = Column(Boolean, default=True)
    #外部キー
    author_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    #relationship
    author = relationship("User", back_populates="questions")
    event = relationship("Event", back_populates="question")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    code = Column(String, default="")
    usage_memory = Column(Integer, default=0)
    execution_time = Column(Integer, default=0)
    score = Column(Integer, default=0)
    test_1_pass = Column(Boolean, default=False)
    test_2_pass = Column(Boolean, default=False)
    test_3_pass = Column(Boolean, default=False)
    test_4_pass = Column(Boolean, default=False)
    test_5_pass = Column(Boolean, default=False)
    #外部キー
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    # relationship
    event = relationship("Event", back_populates="participant")
    user = relationship("User", back_populates="participants")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    opened_at = Column(DateTime(timezone=True))
    end_at = Column(DateTime(timezone=True))
    opened_at_str = Column(String)
    end_at_str = Column(String)
    is_active = Column(Boolean)
    #外部キー
    # question_id = Column(Integer, ForeignKey("questions.id"))
    #relationship
    participant = relationship("Participant", back_populates="event")
    question = relationship("Question", back_populates="event")