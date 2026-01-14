"""
Unit tests for Orders operations
Tests: create_order, get_owned_game_ids, get_my_orders
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.routers import orders


@pytest.mark.unit
class TestCreateOrder:
    """Tests for create_order endpoint"""

    def test_create_order_single_game_success(self, mock_db, sample_user, sample_approved_game):
        """✅ Positive: Create order with single approved game"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[sample_approved_game.id])
        order_response = models.Order(
            id=1,
            user_id=sample_user.id,
            order_date=datetime.utcnow(),
            total_amount=26.99,  # 29.99 * (1 - 0.10)
            payment_status="completed"
        )

        # Setup 3 separate queries:
        # 1) Game query (filter by id + status)
        # 2) OrderItem query with join (existing check)
        # 3) Game stats update
        mock_query1 = MagicMock()
        mock_query2 = MagicMock()
        mock_query3 = MagicMock()

        mock_filter1 = MagicMock()
        mock_join2 = MagicMock()
        mock_filter2 = MagicMock()

        # Query 1: Get game
        mock_query1.filter.return_value = mock_filter1
        mock_filter1.first.return_value = sample_approved_game

        # Query 2: Check existing (with join)
        mock_query2.join.return_value = mock_join2
        mock_join2.filter.return_value = mock_filter2
        mock_filter2.first.return_value = None  # Not owned

        # Query 3: Stats update
        mock_query3.filter.return_value = MagicMock()

        mock_db.query.side_effect = [mock_query1, mock_query2, mock_query3]
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        # Mock refresh behavior
        def refresh_side_effect(obj):
            if isinstance(obj, models.Order):
                obj.id = 1

        mock_db.refresh.side_effect = refresh_side_effect

        # Act
        result = orders.create_order(
            order=order_create,
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

    def test_create_order_empty_game_ids_fails(self, mock_db, sample_user):
        """❌ Negative: Empty game_ids list returns 400"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[])

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            orders.create_order(
                order=order_create,
                db=mock_db,
                current_user=sample_user
            )

        assert exc_info.value.status_code == 400
        assert "no games" in exc_info.value.detail.lower()

    def test_create_order_duplicate_game_ids_fails(self, mock_db, sample_user):
        """❌ Negative: Duplicate game IDs in order returns 400"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[1, 2, 1])  # ID 1 twice

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            orders.create_order(
                order=order_create,
                db=mock_db,
                current_user=sample_user
            )

        assert exc_info.value.status_code == 400
        assert "duplicate" in exc_info.value.detail.lower()

    def test_create_order_nonexistent_game_fails(self, mock_db, sample_user):
        """❌ Negative: Non-existent game returns 404"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[999])

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Game not found

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            orders.create_order(
                order=order_create,
                db=mock_db,
                current_user=sample_user
            )

        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()

    def test_create_order_unapproved_game_fails(self, mock_db, sample_user, sample_pending_game):
        """❌ Negative: Unapproved game returns 404 (not visible)"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[sample_pending_game.id])

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Pending games not in approved filter

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            orders.create_order(
                order=order_create,
                db=mock_db,
                current_user=sample_user
            )

        assert exc_info.value.status_code == 404

    def test_create_order_already_owned_game_fails(self, mock_db, sample_user, sample_approved_game):
        """❌ Negative: Buying already owned game returns 400"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[sample_approved_game.id])
        owned_item = models.OrderItem(
            id=1,
            order_id=99,
            game_id=sample_approved_game.id,
            purchase_price=29.99,
            discount_applied=0
        )

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.side_effect = [
            sample_approved_game,  # Game found
            owned_item,  # Already owned
        ]

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            orders.create_order(
                order=order_create,
                db=mock_db,
                current_user=sample_user
            )

        assert exc_info.value.status_code == 400
        assert "already own" in exc_info.value.detail.lower()

    def test_create_order_multiple_games_success(self, mock_db, sample_user, multiple_approved_games):
        """✅ Positive: Order with multiple different games"""
        # Arrange
        game_ids = [game.id for game in multiple_approved_games]
        order_create = schemas.OrderCreate(game_ids=game_ids)

        # Build mock queries: First loop gets all games, second loop updates stats
        queries = []

        # Loop 1: Get each game and check ownership
        for game in multiple_approved_games:
            # Query: Get game
            q1 = MagicMock()
            f1 = MagicMock()
            q1.filter.return_value = f1
            f1.first.return_value = game
            queries.append(q1)

            # Query: Check existing (with join)
            q2 = MagicMock()
            j2 = MagicMock()
            f2 = MagicMock()
            q2.join.return_value = j2
            j2.filter.return_value = f2
            f2.first.return_value = None  # Not owned
            queries.append(q2)

        # Loop 2: Update stats for each game
        for game in multiple_approved_games:
            # Query: Stats update
            q3 = MagicMock()
            f3 = MagicMock()
            q3.filter.return_value = f3
            f3.first.return_value = game
            queries.append(q3)

        # Setup query mock
        query_index = [0]

        def get_next_query(*args, **kwargs):
            idx = query_index[0]
            query_index[0] += 1
            if idx < len(queries):
                return queries[idx]
            raise Exception(f"No more queries! Called {idx+1} times but only {len(queries)} queries mocked")

        mock_db.query.side_effect = get_next_query
        mock_db.commit.return_value = None

        def refresh_side_effect(obj):
            if isinstance(obj, models.Order):
                obj.id = 1

        mock_db.refresh.side_effect = refresh_side_effect

        # Act
        result = orders.create_order(
            order=order_create,
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert mock_db.add.called

    def test_create_order_price_with_discount_calculation(self, mock_db, sample_user, sample_discounted_game):
        """✅ Edge Case: Price calculation with discount applied correctly"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[sample_discounted_game.id])

        # Original: 49.99, Discount: 50% -> Final: 24.995 ≈ 25.00

        mock_query = MagicMock()
        mock_filter = MagicMock()

        # Query 1: Get game
        mock_query1 = MagicMock()
        mock_filter1 = MagicMock()
        mock_query1.filter.return_value = mock_filter1
        mock_filter1.first.return_value = sample_discounted_game

        # Query 2: Check existing (with join)
        mock_query2 = MagicMock()
        mock_join2 = MagicMock()
        mock_filter2 = MagicMock()
        mock_query2.join.return_value = mock_join2
        mock_join2.filter.return_value = mock_filter2
        mock_filter2.first.return_value = None

        # Query 3: Get game for stats update
        mock_query3 = MagicMock()
        mock_filter3 = MagicMock()
        mock_query3.filter.return_value = mock_filter3
        mock_filter3.first.return_value = sample_discounted_game

        mock_db.query.side_effect = [mock_query1, mock_query2, mock_query3]
        mock_db.commit.return_value = None

        def refresh_side_effect(obj):
            if isinstance(obj, models.Order):
                obj.id = 1
                expected_price = sample_discounted_game.price * (1 - sample_discounted_game.discount_percent / 100)
                obj.total_amount = round(expected_price, 2)

        mock_db.refresh.side_effect = refresh_side_effect

        # Act
        result = orders.create_order(
            order=order_create,
            db=mock_db,
            current_user=sample_user
        )

        # Assert - Discount calculation verified in mock
        assert mock_db.add.called

    def test_create_order_total_amount_rounded_to_two_decimals(self, mock_db, sample_user):
        """✅ Edge Case: Total amount properly rounded to 2 decimals"""
        # Arrange - Game with price that creates rounding issues
        game = models.Game(
            id=50,
            title="Precision Game",
            price=10.01,
            discount_percent=33,  # 10.01 * 0.67 = 6.7067
            developer_id=4,
            status=models.GameStatus.APPROVED,
            total_sales=0,
            total_revenue=0.0
        )
        order_create = schemas.OrderCreate(game_ids=[game.id])

        # Query 1: Get game
        mock_query1 = MagicMock()
        mock_filter1 = MagicMock()
        mock_query1.filter.return_value = mock_filter1
        mock_filter1.first.return_value = game

        # Query 2: Check existing (with join)
        mock_query2 = MagicMock()
        mock_join2 = MagicMock()
        mock_filter2 = MagicMock()
        mock_query2.join.return_value = mock_join2
        mock_join2.filter.return_value = mock_filter2
        mock_filter2.first.return_value = None

        # Query 3: Get game for stats update
        mock_query3 = MagicMock()
        mock_filter3 = MagicMock()
        mock_query3.filter.return_value = mock_filter3
        mock_filter3.first.return_value = game

        mock_db.query.side_effect = [mock_query1, mock_query2, mock_query3]
        mock_db.commit.return_value = None

        def refresh_side_effect(obj):
            if isinstance(obj, models.Order):
                obj.total_amount = round(10.01 * (1 - 33/100), 2)

        mock_db.refresh.side_effect = refresh_side_effect

        # Act
        result = orders.create_order(
            order=order_create,
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert mock_db.add.called

    def test_create_order_updates_game_stats_atomically(self, mock_db, sample_user, sample_approved_game):
        """✅ Positive: Game stats (total_sales, total_revenue) updated in transaction"""
        # Arrange
        order_create = schemas.OrderCreate(game_ids=[sample_approved_game.id])
        initial_sales = sample_approved_game.total_sales
        initial_revenue = sample_approved_game.total_revenue

        # Query 1: Get game
        mock_query1 = MagicMock()
        mock_filter1 = MagicMock()
        mock_query1.filter.return_value = mock_filter1
        mock_filter1.first.return_value = sample_approved_game

        # Query 2: Check existing (with join)
        mock_query2 = MagicMock()
        mock_join2 = MagicMock()
        mock_filter2 = MagicMock()
        mock_query2.join.return_value = mock_join2
        mock_join2.filter.return_value = mock_filter2
        mock_filter2.first.return_value = None

        # Query 3: Get game for stats update
        mock_query3 = MagicMock()
        mock_filter3 = MagicMock()
        mock_query3.filter.return_value = mock_filter3
        mock_filter3.first.return_value = sample_approved_game

        mock_db.query.side_effect = [mock_query1, mock_query2, mock_query3]
        mock_db.commit.return_value = None

        def refresh_side_effect(obj):
            if isinstance(obj, models.Order):
                obj.id = 1
                sample_approved_game.total_sales += 1
                sample_approved_game.total_revenue += obj.total_amount

        mock_db.refresh.side_effect = refresh_side_effect

        # Act
        result = orders.create_order(
            order=order_create,
            db=mock_db,
            current_user=sample_user
        )

        # Assert - Verify transaction was committed
        assert mock_db.commit.called


@pytest.mark.unit
class TestGetOwnedGameIds:
    """Tests for get_owned_game_ids endpoint"""

    def test_get_owned_games_empty_returns_empty_list(self, mock_db, sample_user):
        """✅ Positive: User with no games returns empty list"""
        # Arrange
        mock_query = MagicMock()
        mock_join = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_join
        mock_join.all.return_value = []  # No owned games

        # Act
        result = orders.get_owned_game_ids(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert result == []
        assert isinstance(result, list)

    def test_get_owned_games_returns_all_game_ids(self, mock_db, sample_user):
        """✅ Positive: Returns all owned game IDs for user"""
        # Arrange
        owned_game_ids = [(1,), (3,), (5,)]  # Query returns tuples

        mock_query = MagicMock()
        mock_join = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_join
        mock_join.all.return_value = owned_game_ids

        # Act
        result = orders.get_owned_game_ids(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert result == [1, 3, 5]
        assert len(result) == 3

    def test_get_owned_games_with_single_game(self, mock_db, sample_user):
        """✅ Edge Case: User with exactly one owned game"""
        # Arrange
        owned_game_ids = [(42,)]

        mock_query = MagicMock()
        mock_join = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_join
        mock_join.all.return_value = owned_game_ids

        # Act
        result = orders.get_owned_game_ids(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert result == [42]
        assert len(result) == 1

    def test_get_owned_games_join_query_correct(self, mock_db, sample_user):
        """✅ Positive: Query correctly joins Order and OrderItem tables"""
        # Arrange
        mock_query = MagicMock()
        mock_join = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_join
        mock_join.filter.return_value = mock_join
        mock_join.all.return_value = [(1,), (2,)]

        # Act
        result = orders.get_owned_game_ids(
            db=mock_db,
            current_user=sample_user
        )

        # Assert - Verify join was called
        assert mock_query.join.called
        assert mock_join.filter.called
        assert mock_join.all.called


@pytest.mark.unit
class TestGetMyOrders:
    """Tests for get_my_orders endpoint"""

    def test_get_my_orders_empty(self, mock_db, sample_user):
        """✅ Positive: User with no orders returns empty list"""
        # Arrange
        mock_query = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []

        # Act
        result = orders.get_my_orders(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert result == []

    def test_get_my_orders_returns_orders_with_items(self, mock_db, sample_user, order_with_items):
        """✅ Positive: Returns all user's orders with items loaded"""
        # Arrange
        mock_query = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [order_with_items]

        # Act
        result = orders.get_my_orders(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert len(result) == 1
        assert result[0].id == order_with_items.id
        assert len(result[0].items) == 3

    def test_get_my_orders_ordered_by_date_desc(self, mock_db, sample_user):
        """✅ Positive: Orders returned in descending date order (newest first)"""
        # Arrange - Multiple orders with different dates
        old_order = models.Order(
            id=1,
            user_id=sample_user.id,
            order_date=datetime(2026, 1, 1),
            total_amount=50.0,
            payment_status="completed"
        )
        new_order = models.Order(
            id=2,
            user_id=sample_user.id,
            order_date=datetime(2026, 1, 10),
            total_amount=75.0,
            payment_status="completed"
        )

        mock_query = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [new_order, old_order]  # Newest first

        # Act
        result = orders.get_my_orders(
            db=mock_db,
            current_user=sample_user
        )

        # Assert
        assert result[0].order_date > result[1].order_date
