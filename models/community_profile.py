from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum

from database import Base

class CommunityRole(str, PyEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"

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

    role = Column(Enum(CommunityRole),
                  default=CommunityRole.MEMBER,
                  nullable=False)

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

    __table_args__ = (
        UniqueConstraint('user_id', 'community_id', name='uq_user_community'),
        UniqueConstraint('community_id', 'profile_name', name='uq_community_profile_name'),
        Index('ix_community_profile_community_id', 'community_id'),
    )