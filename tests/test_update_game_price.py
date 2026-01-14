"""
Unit Tests for Game Price Update Functionality

Tests cover:
1. Game not found → HTTPException 404
2. Unauthorized developer (another dev's game) → HTTPException 403
3. Invalid price (negative/zero) → ValueError
4. Successful update → price updated, repository saved
5. Audit/logging side-effects → mocked and verified

Service Layer: GamePriceUpdateService (100% mocked repository)
"""

import pytest
from typing import Optional
from unittest.mock import MagicMock, call
from datetime import datetime


# ==================== SERVICE LAYER ====================

class GamePriceUpdateService:
    """
    Service layer for game price update operations.
    Handles authorization, validation, and persistence.
    """

    def __init__(self, game_repository, audit_service=None):
        """
        Initialize service with mocked repositories.

        Args:
            game_repository: Mocked repository for database access
            audit_service: Optional audit/logging service
        """
        self.game_repository = game_repository
        self.audit_service = audit_service

    def update_game_price(
        self,
        game_id: int,
        new_price: float,
        developer_id: int
    ) -> dict:
        """
        Update game price with authorization and validation.

        Behavior:
        1. Fetch game from repository
        2. Verify developer owns the game (authorization)
        3. Validate new price (must be > 0)
        4. Update game price
        5. Save changes to repository
        6. Audit log the change

        Args:
            game_id: ID of game to update
            new_price: New price (must be > 0)
            developer_id: Current developer's ID

        Returns:
            Updated game object (dict)

        Raises:
            HTTPException(404): Game not found
            HTTPException(403): Developer unauthorized
            ValueError: Invalid price
        """
        # 1. Fetch game from repository
        game = self.game_repository.get_game(game_id)

        if game is None:
            # 404: Game not found
            from fastapi import HTTPException
            raise HTTPException(
                status_code=404,
                detail=f"Game {game_id} not found"
            )

        # 2. Authorization: verify developer owns game
        if game.get("developer_id") != developer_id:
            # 403: Unauthorized
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update this game"
            )

        # 3. Validation: price must be > 0
        if new_price <= 0:
            raise ValueError(f"Price must be greater than 0, got {new_price}")

        # 4. Update game price
        old_price = game.get("price")
        game["price"] = new_price

        # 5. Save to repository
        self.game_repository.save_game(game)

        # 6. Audit log (if audit service available)
        if self.audit_service:
            self.audit_service.log_price_change(
                game_id=game_id,
                developer_id=developer_id,
                old_price=old_price,
                new_price=new_price
            )

        return game

    def bulk_update_game_prices(
        self,
        updates: list,  # [{"game_id": 1, "new_price": 29.99}, ...]
        developer_id: int
    ) -> list:
        """
        Update multiple game prices in one operation.

        Args:
            updates: List of price update dictionaries
            developer_id: Current developer's ID

        Returns:
            List of updated games

        Raises:
            ValueError: If any update is invalid
        """
        updated_games = []

        for update in updates:
            game_id = update.get("game_id")
            new_price = update.get("new_price")

            # Use single update method for consistency
            updated_game = self.update_game_price(
                game_id=game_id,
                new_price=new_price,
                developer_id=developer_id
            )
            updated_games.append(updated_game)

        return updated_games


# ==================== TEST FIXTURES ====================

@pytest.fixture
def game_builder():
    """Builder for creating test game objects."""
    class GameBuilder:
        @staticmethod
        def build(
            game_id: int = 1,
            title: str = "Test Game",
            developer_id: int = 1,
            price: float = 29.99,
            status: str = "APPROVED"
        ) -> dict:
            """Build a game object."""
            return {
                "id": game_id,
                "title": title,
                "developer_id": developer_id,
                "price": price,
                "status": status,
                "discount_percent": 0,
                "genres": ["Action"],
            }

    return GameBuilder


@pytest.fixture
def mock_game_repository():
    """Mock game repository."""
    mock_repo = MagicMock()
    mock_repo.get_game = MagicMock()
    mock_repo.save_game = MagicMock()
    return mock_repo


@pytest.fixture
def mock_audit_service():
    """Mock audit/logging service."""
    mock_audit = MagicMock()
    mock_audit.log_price_change = MagicMock()
    return mock_audit


@pytest.fixture
def game_price_update_service(mock_game_repository, mock_audit_service):
    """Initialize service with mocked dependencies."""
    return GamePriceUpdateService(
        game_repository=mock_game_repository,
        audit_service=mock_audit_service
    )


@pytest.fixture
def game_price_update_service_no_audit(mock_game_repository):
    """Service without audit logging."""
    return GamePriceUpdateService(
        game_repository=mock_game_repository,
        audit_service=None
    )


# ==================== TEST CLASSES ====================

class TestUpdateGamePrice_GameNotFound:
    """Test suite for game not found scenario."""

    def test_game_not_found_returns_404(self, game_price_update_service, mock_game_repository):
        """
        Test that updating non-existent game raises HTTPException 404.

        Requirement 1: Game yok → hata
        """
        # Arrange
        mock_game_repository.get_game.return_value = None
        game_id = 999
        new_price = 39.99
        developer_id = 1

        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            game_price_update_service.update_game_price(
                game_id=game_id,
                new_price=new_price,
                developer_id=developer_id
            )

        # Assert exception details
        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()

    def test_game_not_found_does_not_save(self, game_price_update_service, mock_game_repository):
        """Test that repository.save is not called for non-existent game."""
        # Arrange
        mock_game_repository.get_game.return_value = None

        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            game_price_update_service.update_game_price(
                game_id=999,
                new_price=39.99,
                developer_id=1
            )

        # Assert save not called
        mock_game_repository.save_game.assert_not_called()

    def test_repository_called_with_correct_game_id(self, game_price_update_service, mock_game_repository):
        """Test that repository.get_game is called with correct game_id."""
        # Arrange
        mock_game_repository.get_game.return_value = None
        game_id = 42

        # Act
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            game_price_update_service.update_game_price(
                game_id=game_id,
                new_price=39.99,
                developer_id=1
            )

        # Assert
        mock_game_repository.get_game.assert_called_once_with(game_id)


class TestUpdateGamePrice_UnauthorizedDeveloper:
    """Test suite for authorization checks."""

    def test_unauthorized_developer_returns_403(self, game_price_update_service, game_builder, mock_game_repository):
        """
        Test that developer cannot update another dev's game.

        Requirement 2: Developer yetkisiz → 403/exception
        """
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game
        current_developer_id = 2  # Different developer

        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=39.99,
                developer_id=current_developer_id
            )

        # Assert exception details
        assert exc_info.value.status_code == 403
        assert "permission" in exc_info.value.detail.lower()

    def test_unauthorized_developer_does_not_save(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that save is not called when authorization fails."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=39.99,
                developer_id=2  # Unauthorized
            )

        # Assert
        mock_game_repository.save_game.assert_not_called()

    def test_unauthorized_developer_no_audit_log(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """Test that audit log is not created when authorization fails."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=39.99,
                developer_id=2
            )

        # Assert
        mock_audit_service.log_price_change.assert_not_called()

    def test_authorized_developer_succeeds(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that same developer can update game."""
        # Arrange
        developer_id = 1
        game = game_builder.build(game_id=1, developer_id=developer_id, price=29.99)
        mock_game_repository.get_game.return_value = game
        new_price = 39.99

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=new_price,
            developer_id=developer_id
        )

        # Assert: No exception, save called
        mock_game_repository.save_game.assert_called_once()


class TestUpdateGamePrice_PriceValidation:
    """Test suite for price validation."""

    def test_negative_price_raises_error(self, game_price_update_service, game_builder, mock_game_repository):
        """
        Test that negative price raises ValueError.

        Requirement 3: newPrice <= 0 → validation hatası
        """
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game
        negative_price = -10.0

        # Act & Assert
        with pytest.raises(ValueError, match="greater than 0"):
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=negative_price,
                developer_id=1
            )

    def test_zero_price_raises_error(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that zero price raises ValueError."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        # Act & Assert
        with pytest.raises(ValueError, match="greater than 0"):
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=0.0,
                developer_id=1
            )

    def test_invalid_price_does_not_save(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that save is not called for invalid price."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        # Act & Assert
        with pytest.raises(ValueError):
            game_price_update_service.update_game_price(
                game_id=1,
                new_price=-5.0,
                developer_id=1
            )

        # Assert
        mock_game_repository.save_game.assert_not_called()

    def test_very_small_positive_price_succeeds(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that very small positive price is accepted."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game
        tiny_price = 0.01

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=tiny_price,
            developer_id=1
        )

        # Assert
        assert result["price"] == tiny_price
        mock_game_repository.save_game.assert_called_once()

    def test_large_price_succeeds(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that large price is accepted."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game
        large_price = 999.99

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=large_price,
            developer_id=1
        )

        # Assert
        assert result["price"] == large_price


class TestUpdateGamePrice_SuccessfulUpdate:
    """Test suite for successful price updates."""

    def test_successful_update_returns_updated_game(self, game_price_update_service, game_builder, mock_game_repository):
        """
        Test that successful update returns updated game object.

        Requirement 4: Başarı → price güncellenir
        """
        # Arrange
        original_game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = original_game
        new_price = 39.99

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=new_price,
            developer_id=1
        )

        # Assert
        assert result["price"] == new_price
        assert result["id"] == 1
        assert result["title"] == "Test Game"

    def test_successful_update_calls_save(self, game_price_update_service, game_builder, mock_game_repository):
        """
        Test that successful update calls repository.save_game.

        Requirement 4: repository save çağrılır
        """
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Assert
        mock_game_repository.save_game.assert_called_once()

    def test_successful_update_saves_correct_price(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that save is called with correct price."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game
        new_price = 49.99

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=new_price,
            developer_id=1
        )

        # Assert: save_game called with updated game
        save_call = mock_game_repository.save_game.call_args[0][0]
        assert save_call["price"] == new_price

    def test_successful_update_preserves_other_fields(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that update only changes price, not other fields."""
        # Arrange
        original_game = game_builder.build(
            game_id=1,
            developer_id=1,
            title="Original Title",
            price=29.99
        )
        mock_game_repository.get_game.return_value = original_game

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Assert
        assert result["title"] == "Original Title"
        assert result["id"] == 1
        assert result["price"] == 39.99


class TestUpdateGamePrice_AuditLogging:
    """Test suite for audit/logging side-effects."""

    def test_audit_log_called_on_success(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """
        Test that audit service is called on successful update.

        Requirement 5: audit/log side-effects'leri mockla ve doğrula
        """
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game
        new_price = 39.99

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=new_price,
            developer_id=1
        )

        # Assert
        mock_audit_service.log_price_change.assert_called_once()

    def test_audit_log_called_with_correct_parameters(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """Test that audit log receives correct parameters."""
        # Arrange
        old_price = 29.99
        new_price = 39.99
        game_id = 1
        developer_id = 1

        game = game_builder.build(game_id=game_id, developer_id=developer_id, price=old_price)
        mock_game_repository.get_game.return_value = game

        # Act
        game_price_update_service.update_game_price(
            game_id=game_id,
            new_price=new_price,
            developer_id=developer_id
        )

        # Assert
        mock_audit_service.log_price_change.assert_called_once_with(
            game_id=game_id,
            developer_id=developer_id,
            old_price=old_price,
            new_price=new_price
        )

    def test_audit_log_not_called_without_audit_service(self, game_price_update_service_no_audit, game_builder, mock_game_repository):
        """Test that no audit errors occur when audit service is None."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game

        # Act (should not raise)
        result = game_price_update_service_no_audit.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Assert
        assert result["price"] == 39.99
        mock_game_repository.save_game.assert_called_once()

    def test_audit_log_records_price_decrease(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """Test that audit log is called for price decrease."""
        # Arrange
        old_price = 49.99
        new_price = 29.99  # Decrease

        game = game_builder.build(game_id=1, developer_id=1, price=old_price)
        mock_game_repository.get_game.return_value = game

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=new_price,
            developer_id=1
        )

        # Assert
        call_args = mock_audit_service.log_price_change.call_args[1]
        assert call_args["old_price"] == old_price
        assert call_args["new_price"] == new_price

    def test_audit_log_called_after_save(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """Test that audit is called after save (order check)."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game

        call_order = []

        def save_side_effect(g):
            call_order.append("save")

        def audit_side_effect(*args, **kwargs):
            call_order.append("audit")

        mock_game_repository.save_game.side_effect = save_side_effect
        mock_audit_service.log_price_change.side_effect = audit_side_effect

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Assert: save called before audit
        assert call_order == ["save", "audit"]


class TestUpdateGamePrice_EdgeCases:
    """Test suite for edge cases."""

    def test_fractional_price_accepted(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that fractional prices (e.g., $9.99) are accepted."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=9.99,
            developer_id=1
        )

        # Assert
        assert result["price"] == 9.99

    def test_same_price_update_succeeds(self, game_price_update_service, game_builder, mock_game_repository, mock_audit_service):
        """Test that updating to same price succeeds."""
        # Arrange
        same_price = 29.99
        game = game_builder.build(game_id=1, developer_id=1, price=same_price)
        mock_game_repository.get_game.return_value = game

        # Act
        result = game_price_update_service.update_game_price(
            game_id=1,
            new_price=same_price,
            developer_id=1
        )

        # Assert
        assert result["price"] == same_price
        mock_game_repository.save_game.assert_called_once()
        mock_audit_service.log_price_change.assert_called_once()

    def test_multiple_updates_same_game(self, game_price_update_service, game_builder, mock_game_repository):
        """Test multiple sequential updates to same game."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1, price=29.99)
        mock_game_repository.get_game.return_value = game

        # Act - First update
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Update mock to return updated game
        game["price"] = 39.99
        mock_game_repository.get_game.return_value = game

        # Second update
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=49.99,
            developer_id=1
        )

        # Assert: save called twice
        assert mock_game_repository.save_game.call_count == 2

    def test_repository_get_called_before_save(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that repository.get is called before save."""
        # Arrange
        game = game_builder.build(game_id=1, developer_id=1)
        mock_game_repository.get_game.return_value = game

        call_order = []

        def get_side_effect(game_id):
            call_order.append("get")
            return game

        def save_side_effect(g):
            call_order.append("save")

        mock_game_repository.get_game.side_effect = get_side_effect
        mock_game_repository.save_game.side_effect = save_side_effect

        # Act
        game_price_update_service.update_game_price(
            game_id=1,
            new_price=39.99,
            developer_id=1
        )

        # Assert
        assert call_order == ["get", "save"]


class TestBulkUpdateGamePrices:
    """Test suite for bulk price updates."""

    def test_bulk_update_multiple_games(self, game_price_update_service, game_builder, mock_game_repository):
        """Test updating multiple games at once."""
        # Arrange
        game1 = game_builder.build(game_id=1, developer_id=1, price=29.99)
        game2 = game_builder.build(game_id=2, developer_id=1, price=39.99)

        def get_game(game_id):
            if game_id == 1:
                return game1
            elif game_id == 2:
                return game2
            return None

        mock_game_repository.get_game.side_effect = get_game

        updates = [
            {"game_id": 1, "new_price": 34.99},
            {"game_id": 2, "new_price": 44.99},
        ]

        # Act
        results = game_price_update_service.bulk_update_game_prices(
            updates=updates,
            developer_id=1
        )

        # Assert
        assert len(results) == 2
        assert results[0]["price"] == 34.99
        assert results[1]["price"] == 44.99
        assert mock_game_repository.save_game.call_count == 2

    def test_bulk_update_stops_on_error(self, game_price_update_service, game_builder, mock_game_repository):
        """Test that bulk update stops on first error."""
        # Arrange
        game1 = game_builder.build(game_id=1, developer_id=1)

        mock_game_repository.get_game.return_value = game1

        updates = [
            {"game_id": 1, "new_price": 34.99},
            {"game_id": 2, "new_price": -10.0},  # Invalid price
        ]

        # Act & Assert
        with pytest.raises(ValueError):
            game_price_update_service.bulk_update_game_prices(
                updates=updates,
                developer_id=1
            )


# ==================== SUMMARY ====================

"""
TEST COVERAGE SUMMARY:

Game Not Found (3 tests):
  ✅ Returns HTTPException 404
  ✅ Does not call save
  ✅ Repository called with correct game_id

Authorization (4 tests):
  ✅ Different developer returns 403
  ✅ Unauthorized does not save
  ✅ Unauthorized no audit log
  ✅ Same developer succeeds

Price Validation (5 tests):
  ✅ Negative price raises ValueError
  ✅ Zero price raises ValueError
  ✅ Invalid price does not save
  ✅ Very small positive price succeeds
  ✅ Large price succeeds

Successful Update (4 tests):
  ✅ Returns updated game object
  ✅ Calls repository.save_game
  ✅ Saves correct price
  ✅ Preserves other fields

Audit Logging (5 tests):
  ✅ Audit log called on success
  ✅ Audit log called with correct parameters
  ✅ No audit service → no errors
  ✅ Price decrease recorded
  ✅ Audit called after save

Edge Cases (4 tests):
  ✅ Fractional prices accepted
  ✅ Same price update succeeds
  ✅ Multiple updates to same game
  ✅ Repository order (get before save)

Bulk Updates (2 tests):
  ✅ Bulk update multiple games
  ✅ Bulk update stops on error

TOTAL: 27 comprehensive test cases
"""
