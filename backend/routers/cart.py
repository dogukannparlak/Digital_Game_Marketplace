"""
Cart Router - Shopping cart management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..auth_utils import get_db, get_current_active_user

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

def calculate_cart_totals(cart_items):
    """Calculate cart totals"""
    items = []
    subtotal = 0.0
    total_discount = 0.0

    for item in cart_items:
        game = item.game
        original_price = game.price
        discount_amount = original_price * (game.discount_percent / 100)
        final_price = original_price - discount_amount

        items.append(schemas.CartItem(
            id=item.id,
            game_id=game.id,
            game_title=game.title,
            game_price=game.price,
            game_discount_percent=game.discount_percent,
            game_cover_image_url=game.cover_image_url,
            added_at=item.added_at
        ))

        subtotal += original_price
        total_discount += discount_amount

    return schemas.Cart(
        items=items,
        total_items=len(items),
        subtotal=round(subtotal, 2),
        total_discount=round(total_discount, 2),
        total=round(subtotal - total_discount, 2)
    )

@router.get("/", response_model=schemas.Cart)
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user's cart"""
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    return calculate_cart_totals(cart_items)

@router.post("/add/{game_id}", response_model=schemas.Cart)
def add_to_cart(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add a game to cart"""
    # Check if game exists and is approved
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.status == models.GameStatus.APPROVED
    ).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if user already owns the game
    owned = db.query(models.OrderItem).join(models.Order).filter(
        models.Order.user_id == current_user.id,
        models.OrderItem.game_id == game_id
    ).first()

    if owned:
        raise HTTPException(status_code=400, detail="You already own this game")

    # Check if game is already in cart
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.game_id == game_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Game is already in your cart")

    # Add to cart
    cart_item = models.CartItem(
        user_id=current_user.id,
        game_id=game_id
    )
    db.add(cart_item)
    db.commit()

    # Return updated cart
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    return calculate_cart_totals(cart_items)

@router.delete("/remove/{game_id}", response_model=schemas.Cart)
def remove_from_cart(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Remove a game from cart"""
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.game_id == game_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Game not in cart")

    db.delete(cart_item)
    db.commit()

    # Return updated cart
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    return calculate_cart_totals(cart_items)

@router.delete("/clear", response_model=schemas.Cart)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Clear all items from cart"""
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()
    db.commit()

    return schemas.Cart(items=[], total_items=0, subtotal=0.0, total_discount=0.0, total=0.0)

@router.post("/checkout", response_model=schemas.Order)
def checkout_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Checkout all items in cart and create an order"""
    # Get cart items
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total and create order
    total_amount = 0.0
    order_items = []

    for cart_item in cart_items:
        game = cart_item.game

        # Check if still approved
        if game.status != models.GameStatus.APPROVED:
            raise HTTPException(
                status_code=400,
                detail=f"Game '{game.title}' is no longer available"
            )

        # Check if already owned (double check)
        owned = db.query(models.OrderItem).join(models.Order).filter(
            models.Order.user_id == current_user.id,
            models.OrderItem.game_id == game.id
        ).first()

        if owned:
            raise HTTPException(
                status_code=400,
                detail=f"You already own '{game.title}'"
            )

        # Calculate price
        final_price = game.price * (1 - game.discount_percent / 100)
        total_amount += final_price

        order_items.append({
            "game": game,
            "price": final_price,
            "discount": game.discount_percent
        })

    # Create order
    order = models.Order(
        user_id=current_user.id,
        total_amount=round(total_amount, 2)
    )
    db.add(order)
    db.flush()

    # Create order items and update game stats
    for item_data in order_items:
        order_item = models.OrderItem(
            order_id=order.id,
            game_id=item_data["game"].id,
            purchase_price=round(item_data["price"], 2),
            discount_applied=item_data["discount"]
        )
        db.add(order_item)

        # Update game stats
        item_data["game"].total_sales += 1
        item_data["game"].total_revenue += item_data["price"]

    # Clear cart
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()

    db.commit()
    db.refresh(order)

    return order

@router.get("/count")
def get_cart_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get number of items in cart"""
    count = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).count()

    return {"count": count}
