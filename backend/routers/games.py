"""
Games Router - Public store and developer game management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..auth_utils import get_db, require_developer, get_current_active_user

router = APIRouter(
    prefix="/games",
    tags=["games"]
)

# ==================== PUBLIC ENDPOINTS ====================

@router.get("/", response_model=List[schemas.GamePublic])
def read_games(
    skip: int = 0,
    limit: int = 100,
    genre_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    List all APPROVED games in the store.
    Supports filtering by genre, search, and price range.
    """
    query = db.query(models.Game).filter(
        models.Game.status == models.GameStatus.APPROVED
    )

    # Filter by genre
    if genre_id:
        query = query.join(models.Game.genres).filter(models.Genre.id == genre_id)

    # Search by title
    if search:
        query = query.filter(models.Game.title.ilike(f"%{search}%"))

    # Price filters
    if min_price is not None:
        query = query.filter(models.Game.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Game.price <= max_price)

    return query.order_by(models.Game.release_date.desc()).offset(skip).limit(limit).all()

@router.get("/{game_id}", response_model=schemas.GamePublic)
def read_game(game_id: int, db: Session = Depends(get_db)):
    """Get a single game by ID (only if approved)"""
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.status == models.GameStatus.APPROVED
    ).first()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/{game_id}/reviews", response_model=List[schemas.Review])
def get_game_reviews(
    game_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get reviews for a game"""
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    reviews = db.query(models.Review).filter(
        models.Review.game_id == game_id
    ).order_by(models.Review.created_at.desc()).offset(skip).limit(limit).all()

    return reviews

# ==================== DEVELOPER ENDPOINTS ====================

@router.get("/developer/my-games", response_model=List[schemas.Game])
def get_my_games(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_developer)
):
    """
    Get games published by the current developer.
    Shows all statuses (pending, approved, rejected, suspended).
    """
    query = db.query(models.Game).filter(
        models.Game.developer_id == current_user.id
    )

    if status:
        try:
            status_enum = models.GameStatus(status)
            query = query.filter(models.Game.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")

    return query.order_by(models.Game.release_date.desc()).all()

@router.get("/developer/stats")
def get_developer_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_developer)
):
    """Get developer sales statistics"""
    games = db.query(models.Game).filter(
        models.Game.developer_id == current_user.id
    ).all()

    total_games = len(games)
    approved_games = len([g for g in games if g.status == models.GameStatus.APPROVED])
    pending_games = len([g for g in games if g.status == models.GameStatus.PENDING])
    total_sales = sum(g.total_sales for g in games)
    total_revenue = sum(g.total_revenue for g in games)

    return {
        "total_games": total_games,
        "approved_games": approved_games,
        "pending_games": pending_games,
        "total_sales": total_sales,
        "total_revenue": total_revenue
    }

@router.post("/", response_model=schemas.Game)
def create_game(
    game: schemas.GameCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_developer)
):
    """
    Publish a new game (Developer only).
    Game will have PENDING status until approved by admin.
    """
    # Create game with PENDING status
    db_game = models.Game(
        title=game.title,
        description=game.description,
        short_description=game.short_description,
        price=game.price,
        developer_id=current_user.id,
        status=models.GameStatus.PENDING,
        cover_image_url=game.cover_image_url,
        trailer_url=game.trailer_url
    )

    # Add genres
    if game.genre_ids:
        genres = db.query(models.Genre).filter(
            models.Genre.id.in_(game.genre_ids)
        ).all()
        if len(genres) != len(game.genre_ids):
            raise HTTPException(status_code=400, detail="One or more genres not found")
        db_game.genres = genres

    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.put("/{game_id}", response_model=schemas.Game)
def update_game(
    game_id: int,
    game_update: schemas.GameUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_developer)
):
    """Update a game (Developer only, own games)"""
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.developer_id == current_user.id
    ).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found or not owned by you")

    # Update fields
    if game_update.title is not None:
        game.title = game_update.title
    if game_update.description is not None:
        game.description = game_update.description
    if game_update.short_description is not None:
        game.short_description = game_update.short_description
    if game_update.price is not None:
        game.price = game_update.price
    if game_update.discount_percent is not None:
        game.discount_percent = game_update.discount_percent
    if game_update.cover_image_url is not None:
        game.cover_image_url = game_update.cover_image_url
    if game_update.trailer_url is not None:
        game.trailer_url = game_update.trailer_url

    # Update genres
    if game_update.genre_ids is not None:
        genres = db.query(models.Genre).filter(
            models.Genre.id.in_(game_update.genre_ids)
        ).all()
        game.genres = genres

    db.commit()
    db.refresh(game)
    return game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_developer)
):
    """Delete a game (Developer only, own games, only if not approved)"""
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.developer_id == current_user.id
    ).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found or not owned by you")

    if game.status == models.GameStatus.APPROVED and game.total_sales > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a game that has been sold. Contact support."
        )

    db.delete(game)
    db.commit()
    return {"message": "Game deleted successfully"}

# ==================== USER INTERACTIONS ====================

@router.post("/{game_id}/review", response_model=schemas.Review)
def create_review(
    game_id: int,
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a review for a game (must own the game)"""
    # Check if game exists and is approved
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.status == models.GameStatus.APPROVED
    ).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if user owns the game
    owned = db.query(models.OrderItem).join(models.Order).filter(
        models.Order.user_id == current_user.id,
        models.OrderItem.game_id == game_id
    ).first()
    if not owned:
        raise HTTPException(status_code=400, detail="You must own the game to review it")

    # Check if user already reviewed
    existing = db.query(models.Review).filter(
        models.Review.user_id == current_user.id,
        models.Review.game_id == game_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already reviewed this game")

    db_review = models.Review(
        user_id=current_user.id,
        game_id=game_id,
        rating=review.rating,
        content=review.content
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
