import datetime
import uuid
from app.database import Base 
from sqlalchemy import Boolean, Column,VARCHAR,UUID,TEXT, ForeignKey,Integer,TIMESTAMP, UniqueConstraint
import pytz

class Threads(Base):
    __tablename__ = "threads"

    thread_id = Column(UUID,primary_key=True,default=uuid.uuid4)
    subject = Column(VARCHAR(255),nullable=False,default="Dialog")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True,default=None)
    

class Participants(Base):
    __tablename__ = "participants"

    participant_id = Column(UUID,primary_key=True,default=uuid.uuid4)
    thread_id = Column(UUID,ForeignKey("threads.thread_id"),nullable=False)
    user_id = Column(UUID,ForeignKey("users.user_id"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True,default=None)



class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(UUID,primary_key=True,default=uuid.uuid4)
    thread_id = Column(UUID,ForeignKey("threads.thread_id"),nullable=False)
    user_id = Column(UUID,ForeignKey("users.user_id"),nullable=False)
    text = Column(TEXT,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=True),nullable=True,default=None)


    
    
