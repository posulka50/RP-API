from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import foreign

from database import Base

class Community(Base):
    __tablename__ = 'community'

    id = Column(Integer,
                primary_key=True,
                index=True)

    name = Column(String,
                  unique=True,
                  index=True,
                  nullable=False)

    description = Column(String,
                         nullable=True)

    owner_id = Column(Integer,
                      nullable=False,
                      foreign_key='user.id')

    is_public = Column(Boolean,
                         default=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())