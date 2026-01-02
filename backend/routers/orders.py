"""
Orders Router - Purchase games and view order history
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..auth_utils import get_db, get_current_active_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post("/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Purchase games"""
    if not order.game_ids:
        raise HTTPException(status_code=400, detail="No games selected")

    # Check for duplicates in order
    if len(order.game_ids) != len(set(order.game_ids)):
        raise HTTPException(status_code=400, detail="Duplicate games in order")

    total_amount = 0
    db_items = []

    for game_id in order.game_ids:
        # Get game (must be approved)
        game = db.query(models.Game).filter(
            models.Game.id == game_id,
            models.Game.status == models.GameStatus.APPROVED
        ).first()

        if not game:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found or not available")

        # Check if user already owns this game
        existing = db.query(models.OrderItem).join(models.Order).filter(
            models.Order.user_id == current_user.id,
            models.OrderItem.game_id == game_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"You already own '{game.title}'"
            )

        # Calculate price with discount
        discount = game.discount_percent or 0
        price = game.price * (1 - discount / 100)
        total_amount += price

        db_items.append(models.OrderItem(
            game_id=game_id,
            purchase_price=price,
            discount_applied=discount
        ))

    # Create order
    db_order = models.Order(
        user_id=current_user.id,
        total_amount=round(total_amount, 2)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add items and update game stats
    for item in db_items:
        item.order_id = db_order.id
        db.add(item)

        # Update game sales stats
        game = db.query(models.Game).filter(models.Game.id == item.game_id).first()
        if game:
            game.total_sales += 1
            game.total_revenue += item.purchase_price

    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.Order])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user's orders"""
    orders = db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.game)
    ).filter(
        models.Order.user_id == current_user.id
    ).order_by(models.Order.order_date.desc()).all()

    return orders

@router.get("/owned-games", response_model=List[int])
def get_owned_game_ids(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get list of game IDs the user owns"""
    owned = db.query(models.OrderItem.game_id).join(models.Order).filter(
        models.Order.user_id == current_user.id
    ).all()

    return [game_id for (game_id,) in owned]

@router.get("/library", response_model=List[schemas.GameSimple])
def get_my_library(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all games the user owns"""
    game_ids = db.query(models.OrderItem.game_id).join(models.Order).filter(
        models.Order.user_id == current_user.id
    ).distinct().all()

    game_ids = [gid for (gid,) in game_ids]

    games = db.query(models.Game).filter(models.Game.id.in_(game_ids)).all()
    return games
