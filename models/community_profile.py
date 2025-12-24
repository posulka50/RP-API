from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import foreign

from database import Base

class CommunityProfile(Base):
    __tablename__ = 'community_profile'

    id = Column(Integer,
                primary_key=True,
                index=True)

    user_id = Column(Integer,
                     nullable=False,
                     foreign_key='user.id')

    community_id = Column(Integer,
                          nullable=False,
                          foreign_key='community.id')

    profile_name = Column(String,
                          unique=True,
                          index=True,
                          nullable=False)

    bio = Column(String,
                 nullable=True)

    is_active = Column(Boolean,
                       default=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())