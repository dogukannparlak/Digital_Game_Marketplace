from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from .. import models, schemas
from ..database import SessionLocal
from ..auth_utils import get_current_active_user, get_db
import bcrypt

router = APIRouter(
    tags=["authentication"]
)

# Configuration
SECRET_KEY = "your-secret-key-keep-it-secret-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is banned
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is banned: {user.banned_reason or 'No reason provided'}"
        )

    # Verify password
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token with role info
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )

    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        role=user.role.value,
        developer_name=user.developer_name
    )

@router.get("/me", response_model=schemas.User)
def get_current_user_info(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=schemas.User)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if user_update.display_name is not None:
        current_user.display_name = user_update.display_name
    if user_update.bio is not None:
        current_user.bio = user_update.bio
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url

    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/password")
def change_password(
    password_data: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change current user's password"""
    # Verify current password
    if not bcrypt.checkpw(
        password_data.current_password.encode('utf-8'),
        current_user.hashed_password.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Hash new password
    new_hashed = bcrypt.hashpw(
        password_data.new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    current_user.hashed_password = new_hashed
    db.commit()

    return {"message": "Password changed successfully"}

@router.get("/me/stats", response_model=schemas.UserStats)
def get_user_stats(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's statistics"""
    # Count owned games
    total_games = db.query(func.count(models.OrderItem.id))\
        .join(models.Order)\
        .filter(models.Order.user_id == current_user.id)\
        .scalar() or 0

    # Total spent
    total_spent = db.query(func.sum(models.Order.total_amount))\
        .filter(models.Order.user_id == current_user.id)\
        .scalar() or 0.0

    # Total reviews
    total_reviews = db.query(func.count(models.Review.id))\
        .filter(models.Review.user_id == current_user.id)\
        .scalar() or 0

    return schemas.UserStats(
        total_games_owned=total_games,
        total_spent=float(total_spent),
        total_reviews=total_reviews,
        member_since=current_user.registration_date
    )

@router.post("/become-developer", response_model=schemas.User)
def apply_to_become_developer(
    application: schemas.DeveloperApplication,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply to become a developer"""
    # Check if already a developer
    if current_user.role == models.UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a developer"
        )

    # Check if developer name is taken
    existing = db.query(models.User).filter(
        models.User.developer_name == application.developer_name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Developer name is already taken"
        )

    # Update user to developer
    current_user.role = models.UserRole.DEVELOPER
    current_user.developer_name = application.developer_name
    current_user.developer_verified = False  # Admin can verify later

    db.commit()
    db.refresh(current_user)
    return current_user
