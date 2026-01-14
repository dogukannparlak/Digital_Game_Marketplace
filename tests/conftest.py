"""
Shared test fixtures and configuration
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch
from sqlalchemy.orm import Session
from backend import models, schemas


# ==================== DATABASE & USER FIXTURES ====================

@pytest.fixture
def mock_db():
    """Mock SQLAlchemy Session"""
    return MagicMock(spec=Session)


@pytest.fixture
def sample_user():
    """Sample authenticated user"""
    user = models.User(
        id=1,
        public_id="USR-TEST1234",
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role=models.UserRole.USER,
        display_name="Test User",
        is_active=True,
        is_banned=False,
        registration_date=datetime.utcnow()
    )
    return user


@pytest.fixture
def admin_user():
    """Admin user fixture"""
    user = models.User(
        id=2,
        public_id="USR-ADMIN123",
        username="adminuser",
        email="admin@example.com",
        hashed_password="hashed_password",
        role=models.UserRole.ADMIN,
        display_name="Admin User",
        is_active=True,
        is_banned=False,
        registration_date=datetime.utcnow()
    )
    return user


@pytest.fixture
def banned_user():
    """Banned user fixture"""
    user = models.User(
        id=3,
        public_id="USR-BANNED",
        username="banneduser",
        email="banned@example.com",
        hashed_password="hashed_password",
        role=models.UserRole.USER,
        is_active=True,
        is_banned=True,
        banned_reason="Violation of terms",
        registration_date=datetime.utcnow()
    )
    return user


@pytest.fixture
def developer_user():
    """Developer user fixture"""
    user = models.User(
        id=4,
        public_id="USR-DEV1234",
        username="devuser",
        email="dev@example.com",
        hashed_password="hashed_password",
        role=models.UserRole.DEVELOPER,
        display_name="Developer User",
        developer_name="DevStudio",
        developer_verified=True,
        is_active=True,
        is_banned=False,
        registration_date=datetime.utcnow()
    )
    return user


# ==================== GAME FIXTURES ====================

@pytest.fixture
def sample_approved_game():
    """Sample approved game for sale"""
    game = models.Game(
        id=1,
        title="Test Game",
        description="A test game description",
        short_description="Test game",
        price=29.99,
        discount_percent=10,
        release_date=datetime.utcnow(),
        developer_id=4,
        status=models.GameStatus.APPROVED,
        approved_by=2,
        approved_at=datetime.utcnow(),
        cover_image_url="https://example.com/cover.jpg",
        total_sales=0,
        total_revenue=0.0
    )
    return game


@pytest.fixture
def sample_pending_game():
    """Sample pending game (not approved)"""
    game = models.Game(
        id=2,
        title="Pending Game",
        description="A pending game",
        price=19.99,
        discount_percent=0,
        release_date=datetime.utcnow(),
        developer_id=4,
        status=models.GameStatus.PENDING,
        cover_image_url="https://example.com/cover2.jpg",
        total_sales=0,
        total_revenue=0.0
    )
    return game


@pytest.fixture
def sample_discounted_game():
    """Sample game with high discount"""
    game = models.Game(
        id=3,
        title="Discounted Game",
        description="A game on sale",
        price=49.99,
        discount_percent=50,
        release_date=datetime.utcnow(),
        developer_id=4,
        status=models.GameStatus.APPROVED,
        approved_by=2,
        approved_at=datetime.utcnow(),
        total_sales=100,
        total_revenue=2499.50
    )
    return game


@pytest.fixture
def multiple_approved_games():
    """Multiple approved games"""
    games = [
        models.Game(
            id=10 + i,
            title=f"Game {i}",
            description=f"Game {i} description",
            price=10.00 + i * 5,
            discount_percent=i * 5,
            release_date=datetime.utcnow(),
            developer_id=4,
            status=models.GameStatus.APPROVED,
            approved_by=2,
            approved_at=datetime.utcnow(),
            total_sales=0,
            total_revenue=0.0
        )
        for i in range(1, 4)
    ]
    return games


# ==================== CART FIXTURES ====================

@pytest.fixture
def sample_cart_item(sample_user, sample_approved_game):
    """Sample cart item"""
    item = models.CartItem(
        id=1,
        user_id=sample_user.id,
        game_id=sample_approved_game.id,
        added_at=datetime.utcnow()
    )
    # Set relationship
    item.user = sample_user
    item.game = sample_approved_game
    return item


@pytest.fixture
def multiple_cart_items(sample_user, multiple_approved_games):
    """Multiple cart items"""
    items = []
    for i, game in enumerate(multiple_approved_games, start=1):
        item = models.CartItem(
            id=i,
            user_id=sample_user.id,
            game_id=game.id,
            added_at=datetime.utcnow()
        )
        item.user = sample_user
        item.game = game
        items.append(item)
    return items


# ==================== ORDER FIXTURES ====================

@pytest.fixture
def sample_order(sample_user):
    """Sample order"""
    order = models.Order(
        id=1,
        user_id=sample_user.id,
        order_date=datetime.utcnow(),
        total_amount=26.99,  # 29.99 with 10% discount
        payment_status="completed"
    )
    order.user = sample_user
    order.items = []
    return order


@pytest.fixture
def sample_order_item(sample_approved_game):
    """Sample order item"""
    item = models.OrderItem(
        id=1,
        order_id=1,
        game_id=sample_approved_game.id,
        purchase_price=26.99,
        discount_applied=10
    )
    item.game = sample_approved_game
    return item


@pytest.fixture
def order_with_items(sample_user, multiple_approved_games):
    """Order with multiple items"""
    order = models.Order(
        id=2,
        user_id=sample_user.id,
        order_date=datetime.utcnow(),
        total_amount=0.0,
        payment_status="completed"
    )
    order.user = sample_user
    items = []
    total = 0.0

    for i, game in enumerate(multiple_approved_games, start=1):
        price = game.price * (1 - game.discount_percent / 100)
        total += price
        item = models.OrderItem(
            id=i,
            order_id=order.id,
            game_id=game.id,
            purchase_price=round(price, 2),
            discount_applied=game.discount_percent
        )
        item.game = game
        items.append(item)

    order.items = items
    order.total_amount = round(total, 2)
    return order


# ==================== MOCK HELPERS ====================

@pytest.fixture
def mock_db_with_game(mock_db, sample_approved_game):
    """Mock DB that returns a game on query"""
    mock_query = MagicMock()
    mock_filter = MagicMock()

    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = sample_approved_game

    return mock_db


@pytest.fixture
def mock_db_empty_results(mock_db):
    """Mock DB that returns empty results"""
    mock_query = MagicMock()
    mock_filter = MagicMock()

    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_query.all.return_value = []
    mock_filter.first.return_value = None

    return mock_db


# ==================== SCHEMA FIXTURES ====================

@pytest.fixture
def order_create_schema():
    """OrderCreate schema with game IDs"""
    return schemas.OrderCreate(game_ids=[1, 3])


@pytest.fixture
def cart_schema():
    """Empty cart schema"""
    return schemas.Cart(
        items=[],
        total_items=0,
        subtotal=0.0,
        total_discount=0.0,
        total=0.0
    )


# ==================== PYTEST CONFIGURATION ====================

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks before each test"""
    yield


def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "unit: Mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: Mark test as an integration test"
    )
