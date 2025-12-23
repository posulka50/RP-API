from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,
                primary_key=True,
                index=True)
    email = Column(String,
                   unique=True,
                   index=True)
    hashed_password = Column(String,
                             nullable=False)
    is_active = Column(Boolean,
                       default=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())
