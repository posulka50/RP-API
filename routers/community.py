from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import community
from models.community import Community
from models.community_profile import CommunityProfile, CommunityRole
from schemas.community import CommunityCreate, CommunityResponse, CommunityProfileCreate, CommunityProfileResponse
from services.dependencies import get_db
from services.auth import get_current_user

router = APIRouter(prefix='/community', tags=['Community'])


@router.post('/', response_model=CommunityResponse, status_code=status.HTTP_201_CREATED)
def create_community(
        community_schema: CommunityCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)):
    existing = db.query(Community).filter_by(name=community_schema.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Community name already exists")

    new_community = Community(
        name=community_schema.name,
        description=community_schema.description,
        owner_id=current_user.id,
        is_public=community_schema.is_public
    )
    db.add(new_community)
    db.commit()
    db.refresh(new_community)

    owner_profile = CommunityProfile(
        user_id=current_user.id,
        community_id=new_community.id,
        profile_name=current_user.email.split('@')[0],
        role=CommunityRole.OWNER
    )
    db.add(owner_profile)
    db.commit()

    return new_community

@router.delete('/{community_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_community(
        community_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)):
    community_to_delete = db.query(Community).filter_by(id=community_id).first()

    if not community_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")

    if community_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this community")

    db.delete(community_to_delete)
    db.commit()
    return


@router.post('/{community_id}/join', response_model=CommunityProfileResponse, status_code=status.HTTP_201_CREATED)
def join_community(
        community_id: int,
        profile_data: CommunityProfileCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    searched_community = db.query(Community).filter_by(id=community_id).first()
    if not searched_community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")

    if not searched_community.is_public:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Community is private")

    existing_profile = db.query(CommunityProfile).filter_by(
        user_id=current_user.id,
        community_id=community_id
    ).first()
    if existing_profile:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already a member")

    name_taken = db.query(CommunityProfile).filter_by(
        community_id=community_id,
        profile_name=profile_data.profile_name
    ).first()
    if name_taken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile name already taken")

    new_profile = CommunityProfile(
        user_id=current_user.id,
        community_id=community_id,
        profile_name=profile_data.profile_name,
        bio=profile_data.bio,
        role=CommunityRole.MEMBER
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.delete('/{community_id}/leave', status_code=status.HTTP_204_NO_CONTENT)
def leave_community(
        community_id: int, db:
        Session = Depends(get_db),
        current_user=Depends(get_current_user)):

    profile_to_delete = db.query(CommunityProfile).filter_by(
        user_id=current_user.id,
        community_id=community_id
    ).first()

    if not profile_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community profile not found")

    if profile_to_delete.role == CommunityRole.OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Owner cannot leave community")

    db.delete(profile_to_delete)
    db.commit()
    return





