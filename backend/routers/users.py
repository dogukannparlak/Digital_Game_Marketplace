"""
Users Router - User registration and public profiles
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..auth_utils import get_db
import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check email
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check username
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash password
    password = user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    # Create user with default USER role
    db_user = models.User(
        email=user.email.lower().strip(),
        username=user.username.strip(),
        hashed_password=hashed_password,
        role=models.UserRole.USER
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/by-public-id/{public_id}", response_model=schemas.UserPublic)
def get_user_by_public_id(public_id: str, db: Session = Depends(get_db)):
    """Get public user profile by public ID"""
    user = db.query(models.User).filter(models.User.public_id == public_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=schemas.UserPublic)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get public user profile"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/developer/{developer_name}", response_model=schemas.UserPublic)
def get_developer_profile(developer_name: str, db: Session = Depends(get_db)):
    """Get developer profile by developer name"""
    user = db.query(models.User).filter(
        models.User.developer_name == developer_name,
        models.User.role == models.UserRole.DEVELOPER
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Developer not found")
    return user
