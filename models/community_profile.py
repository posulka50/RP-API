from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import foreign, relationship

from database import Base

class CommunityProfile(Base):
    __tablename__ = 'community_profile'

    id = Column(Integer,
                primary_key=True,
                index=True)

    user_id = Column(Integer,
                     ForeignKey('user.id',
                                 ondelete='CASCADE'),
                     nullable=False)

    community_id = Column(Integer,
                        ForeignKey('community.id',
                                 ondelete='CASCADE'),
                        nullable=False)

    profile_name = Column(String,
                          index=True,
                          nullable=False)

    display_name = Column(String)

    bio = Column(String,
                 nullable=True)

    is_active = Column(Boolean,
                       default=True)

    joined_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())

    user = relationship("User", back_populates="community_profiles")
    community = relationship("Community", back_populates="profiles")