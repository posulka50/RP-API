from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from services.dependencies import get_db
from services.auth import verify_password, create_access_token, get_current_user, get_password_hash

router = APIRouter(prefix='/auth', tags=['Authentication'])

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(email=user.email).first()

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    else:
        hashed_password = get_password_hash(user.password)
        new_user = User(
            email=user.email,
            hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(User).filter_by(email=form_data.username).first()  # username = email

    if not user_db or not verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user_db.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user