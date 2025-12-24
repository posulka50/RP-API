from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import foreign, relationship

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
                      ForeignKey('community_profile.id',
                                 ondelete='CASCADE'),
                      nullable=False,)

    is_public = Column(Boolean,
                         default=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())

    owner = relationship("User", back_populates="owned_communities", foreign_keys=[owner_id])
    profiles = relationship("CommunityProfile", back_populates="community")