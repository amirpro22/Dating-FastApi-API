import datetime
from app.database import Base 
from sqlalchemy import Boolean, Column,VARCHAR,UUID,TEXT, ForeignKey,Integer,TIMESTAMP, UniqueConstraint
import pytz

class Users(Base):
    __tablename__ = "users"

    user_id = Column(UUID,primary_key=True)
    email = Column(VARCHAR(255),nullable=False,unique=True)
    password = Column(TEXT,nullable=False)
    likes = Column(Integer,nullable=False,default=0)
    dislikes = Column(Integer,nullable=False,default=0)
    gender = Column(VARCHAR(255),nullable=False)
    last_seen = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    registered_at = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    


class Photos(Base):
    __tablename__ = "photos"

    photo_id = Column(UUID,primary_key=True)
    owner_id = Column(UUID,ForeignKey("users.user_id"),nullable=False)
    photo_path = Column(TEXT,nullable=False)
    is_main = Column(Boolean,nullable=False)
    is_active = Column(Boolean,nullable=False)
    
    

class History(Base):
    __tablename__ = "history"

    action_id = Column(UUID,primary_key=True)
    action = Column(VARCHAR(255),nullable=False)
    seen = Column(Boolean,nullable=False)
    valuer_id = Column(UUID,ForeignKey("users.user_id"),nullable=False)
    evaluated_user_id = Column(UUID,ForeignKey("users.user_id"),nullable=False)
    action_time = Column(TIMESTAMP(timezone=True),nullable=False,default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint('valuer_id', 'evaluated_user_id', name='_valuer_id_evaluated_user_id_UC'),
                     )
    