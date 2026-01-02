"""
Admin Router - User management, game approval, statistics
Only accessible by users with ADMIN role
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from .. import models, schemas
from ..auth_utils import get_db, require_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# ==================== DASHBOARD ====================

@router.get("/stats", response_model=schemas.AdminStats)
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Get admin dashboard statistics"""
    total_users = db.query(models.User).count()
    total_developers = db.query(models.User).filter(
        models.User.role == models.UserRole.DEVELOPER
    ).count()
    total_games = db.query(models.Game).count()
    pending_games = db.query(models.Game).filter(
        models.Game.status == models.GameStatus.PENDING
    ).count()
    approved_games = db.query(models.Game).filter(
        models.Game.status == models.GameStatus.APPROVED
    ).count()
    total_orders = db.query(models.Order).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).scalar() or 0.0

    return schemas.AdminStats(
        total_users=total_users,
        total_developers=total_developers,
        total_games=total_games,
        pending_games=pending_games,
        approved_games=approved_games,
        total_orders=total_orders,
        total_revenue=total_revenue
    )

# ==================== USER MANAGEMENT ====================

@router.get("/users", response_model=List[schemas.UserAdmin])
def list_all_users(
    skip: int = 0,
    limit: int = 50,
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """List all users with optional filtering"""
    query = db.query(models.User)

    if role:
        try:
            role_enum = models.UserRole(role)
            query = query.filter(models.User.role == role_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid role")

    if search:
        query = query.filter(
            (models.User.username.ilike(f"%{search}%")) |
            (models.User.email.ilike(f"%{search}%")) |
            (models.User.developer_name.ilike(f"%{search}%"))
        )

    return query.offset(skip).limit(limit).all()

@router.get("/users/{user_id}", response_model=schemas.UserAdmin)
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Get detailed user info"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role_update: schemas.UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Change a user's role"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from changing their own role
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")

    try:
        user.role = models.UserRole(role_update.role.value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")

    db.commit()
    return {"message": f"User role changed to {role_update.role.value}"}

@router.put("/users/{user_id}/ban")
def ban_user(
    user_id: int,
    ban_request: schemas.UserBanRequest,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Ban a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from banning themselves
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot ban yourself")

    # Prevent banning other admins
    if user.role == models.UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot ban another admin")

    user.is_banned = True
    user.banned_reason = ban_request.reason
    db.commit()

    return {"message": "User banned successfully"}

@router.put("/users/{user_id}/unban")
def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Unban a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_banned = False
    user.banned_reason = None
    db.commit()

    return {"message": "User unbanned successfully"}

@router.put("/users/{user_id}/verify-developer")
def verify_developer(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Verify a developer (add verified badge)"""
    user = db.query(models.User).filter(
        models.User.id == user_id,
        models.User.role == models.UserRole.DEVELOPER
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Developer not found")

    user.developer_verified = True
    db.commit()

    return {"message": "Developer verified successfully"}

# ==================== GAME MANAGEMENT ====================

@router.get("/developers", response_model=List[schemas.UserPublic])
def list_developers(
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """List all developers for game assignment"""
    developers = db.query(models.User).filter(
        models.User.role.in_([models.UserRole.DEVELOPER, models.UserRole.ADMIN])
    ).all()
    return developers

@router.post("/games", response_model=schemas.GameAdmin)
def admin_create_game(
    game: schemas.AdminGameCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """
    Admin creates a game and assigns it to a developer.
    Can auto-approve the game.
    """
    # Check developer exists
    developer = db.query(models.User).filter(
        models.User.id == game.developer_id,
        models.User.role.in_([models.UserRole.DEVELOPER, models.UserRole.ADMIN])
    ).first()

    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")

    # Create game
    db_game = models.Game(
        title=game.title,
        description=game.description,
        short_description=game.short_description,
        price=game.price,
        developer_id=game.developer_id,
        status=models.GameStatus.APPROVED if game.auto_approve else models.GameStatus.PENDING,
        cover_image_url=game.cover_image_url,
        trailer_url=game.trailer_url
    )

    if game.auto_approve:
        db_game.approved_by = admin.id
        db_game.approved_at = datetime.utcnow()

    # Add genres
    if game.genre_ids:
        genres = db.query(models.Genre).filter(
            models.Genre.id.in_(game.genre_ids)
        ).all()
        db_game.genres = genres

    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/games", response_model=List[schemas.GameAdmin])
def list_all_games(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """List all games with optional status filter"""
    query = db.query(models.Game)

    if status:
        try:
            status_enum = models.GameStatus(status)
            query = query.filter(models.Game.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")

    return query.order_by(models.Game.release_date.desc()).offset(skip).limit(limit).all()

@router.get("/games/pending", response_model=List[schemas.GameAdmin])
def list_pending_games(
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """List all games pending approval"""
    return db.query(models.Game).filter(
        models.Game.status == models.GameStatus.PENDING
    ).order_by(models.Game.release_date.asc()).all()

@router.get("/games/{game_id}", response_model=schemas.GameAdmin)
def get_game_detail(
    game_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Get detailed game info for admin"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.put("/games/{game_id}/approve")
def approve_game(
    game_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Approve a game for the store"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.status == models.GameStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Game is already approved")

    game.status = models.GameStatus.APPROVED
    game.approved_by = admin.id
    game.approved_at = datetime.utcnow()
    game.rejection_reason = None

    db.commit()
    return {"message": "Game approved successfully"}

@router.put("/games/{game_id}/reject")
def reject_game(
    game_id: int,
    reason: str = Query(..., min_length=10, description="Rejection reason"),
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Reject a game"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game.status = models.GameStatus.REJECTED
    game.rejection_reason = reason

    db.commit()
    return {"message": "Game rejected"}

@router.put("/games/{game_id}/suspend")
def suspend_game(
    game_id: int,
    reason: str = Query(..., min_length=10, description="Suspension reason"),
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Suspend a game from the store"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    game.status = models.GameStatus.SUSPENDED
    game.rejection_reason = reason

    db.commit()
    return {"message": "Game suspended"}

# ==================== GENRE MANAGEMENT ====================

@router.post("/genres", response_model=schemas.Genre)
def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Create a new genre (admin only)"""
    existing = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Genre already exists")

    slug = genre.slug or genre.name.lower().replace(" ", "-")
    db_genre = models.Genre(
        name=genre.name,
        slug=slug,
        description=genre.description
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@router.delete("/genres/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(require_admin)
):
    """Delete a genre (admin only)"""
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    db.delete(genre)
    db.commit()
    return {"message": "Genre deleted"}
