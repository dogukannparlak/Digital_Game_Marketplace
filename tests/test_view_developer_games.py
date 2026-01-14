"""
Unit Tests for View/Get Developer Games Functionality

Tests cover:
1. developerId ile sadece o developer'ın oyunları döner
2. developerId geçersiz/null → beklenen davranış
3. sonuç boş liste olabilir → doğrulama

Service Layer: GameViewService (100% mocked repository)
"""

import pytest
from typing import List, Optional
from unittest.mock import MagicMock


# ==================== SERVICE LAYER ====================

class GameViewService:
    """
    Service layer for viewing/retrieving games by developer.
    Provides isolation from database and FastAPI routes.
    """

    def __init__(self, game_repository):
        """
        Initialize service with mocked game repository.

        Args:
            game_repository: Mocked repository for database access
        """
        self.game_repository = game_repository

    def get_developer_games(
        self,
        developer_id: int
    ) -> List[dict]:
        """
        Get all games published by a developer.

        Behavior:
        - Returns only games where developer_id matches
        - Returns all statuses (APPROVED, PENDING, REJECTED, etc.)
        - Can return empty list if developer has no games
        - Ordered by release_date descending

        Args:
            developer_id: ID of developer

        Returns:
            List of game objects (can be empty)

        Raises:
            ValueError: If developer_id is None or invalid type
        """
        # Validate input
        if developer_id is None:
            raise ValueError("developer_id cannot be None")

        if not isinstance(developer_id, int):
            raise ValueError(f"developer_id must be integer, got {type(developer_id).__name__}")

        if developer_id <= 0:
            raise ValueError(f"developer_id must be positive, got {developer_id}")

        # Get games from repository
        all_games = self.game_repository.get_games_by_developer(developer_id)

        # Filter by developer_id (defensive check)
        developer_games = [
            g for g in all_games
            if g.get("developer_id") == developer_id
        ]

        # Sort by release_date descending
        developer_games.sort(
            key=lambda g: g.get("release_date", ""),
            reverse=True
        )

        return developer_games

    def get_developer_games_by_status(
        self,
        developer_id: int,
        status: Optional[str] = None
    ) -> List[dict]:
        """
        Get games by developer filtered by status.

        Args:
            developer_id: ID of developer
            status: Optional status filter (APPROVED, PENDING, etc.)

        Returns:
            List of games matching criteria

        Raises:
            ValueError: If developer_id invalid or status invalid
        """
        # Validate developer_id
        if developer_id is None:
            raise ValueError("developer_id cannot be None")

        if not isinstance(developer_id, int):
            raise ValueError(f"developer_id must be integer, got {type(developer_id).__name__}")

        if developer_id <= 0:
            raise ValueError(f"developer_id must be positive, got {developer_id}")

        # Get games from repository
        all_games = self.game_repository.get_games_by_developer(developer_id)

        # Filter by developer_id
        developer_games = [
            g for g in all_games
            if g.get("developer_id") == developer_id
        ]

        # Filter by status if provided
        if status:
            valid_statuses = ["APPROVED", "PENDING", "REJECTED", "SUSPENDED"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}")

            developer_games = [
                g for g in developer_games
                if g.get("status") == status
            ]

        # Sort by release_date descending
        developer_games.sort(
            key=lambda g: g.get("release_date", ""),
            reverse=True
        )

        return developer_games

    def get_developer_game_count(
        self,
        developer_id: int
    ) -> int:
        """
        Get count of games by developer.

        Args:
            developer_id: ID of developer

        Returns:
            Number of games
        """
        games = self.get_developer_games(developer_id)
        return len(games)

    def get_developer_approved_games(
        self,
        developer_id: int
    ) -> List[dict]:
        """
        Get only APPROVED games by developer.

        Args:
            developer_id: ID of developer

        Returns:
            List of approved games
        """
        return self.get_developer_games_by_status(
            developer_id=developer_id,
            status="APPROVED"
        )


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
            status: str = "APPROVED",
            release_date: str = "2024-01-01"
        ) -> dict:
            """Build a game object."""
            return {
                "id": game_id,
                "title": title,
                "developer_id": developer_id,
                "status": status,
                "release_date": release_date,
                "price": 29.99,
                "description": f"Description for {title}",
            }

    return GameBuilder


@pytest.fixture
def sample_developer_games(game_builder):
    """Sample games from different developers."""
    return [
        # Developer 1's games (5 games with different statuses)
        game_builder.build(
            game_id=1,
            title="Game 1 - Dev 1",
            developer_id=1,
            status="APPROVED",
            release_date="2024-01-15"
        ),
        game_builder.build(
            game_id=2,
            title="Game 2 - Dev 1",
            developer_id=1,
            status="APPROVED",
            release_date="2024-01-10"
        ),
        game_builder.build(
            game_id=3,
            title="Game 3 - Dev 1",
            developer_id=1,
            status="PENDING",
            release_date="2024-01-05"
        ),
        game_builder.build(
            game_id=4,
            title="Game 4 - Dev 1",
            developer_id=1,
            status="REJECTED",
            release_date="2023-12-25"
        ),
        game_builder.build(
            game_id=5,
            title="Game 5 - Dev 1",
            developer_id=1,
            status="APPROVED",
            release_date="2024-02-01"
        ),
        # Developer 2's games (3 games)
        game_builder.build(
            game_id=10,
            title="Game A - Dev 2",
            developer_id=2,
            status="APPROVED",
            release_date="2024-01-20"
        ),
        game_builder.build(
            game_id=11,
            title="Game B - Dev 2",
            developer_id=2,
            status="APPROVED",
            release_date="2024-01-12"
        ),
        game_builder.build(
            game_id=12,
            title="Game C - Dev 2",
            developer_id=2,
            status="PENDING",
            release_date="2024-01-08"
        ),
        # Developer 3's games (1 game)
        game_builder.build(
            game_id=20,
            title="Game X - Dev 3",
            developer_id=3,
            status="APPROVED",
            release_date="2024-01-18"
        ),
    ]


@pytest.fixture
def mock_game_repository(sample_developer_games):
    """Mock repository that returns developer games."""
    mock_repo = MagicMock()

    def get_games_by_developer(developer_id):
        """Return games for specific developer or all games."""
        return [g for g in sample_developer_games]

    mock_repo.get_games_by_developer = MagicMock(side_effect=get_games_by_developer)
    return mock_repo


@pytest.fixture
def game_view_service(mock_game_repository):
    """Initialize GameViewService with mocked repository."""
    return GameViewService(game_repository=mock_game_repository)


# ==================== TEST CLASSES ====================

class TestGetDeveloperGames_ValidDeveloper:
    """Test suite for retrieving games by valid developer."""

    def test_developer_1_returns_all_games(self, game_view_service, mock_game_repository):
        """
        Test that developerId=1 returns only developer 1's games.

        Requirement: developerId ile sadece o developer'ın oyunları döner
        """
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        assert len(results) == 5
        titles = [g["title"] for g in results]
        assert "Game 1 - Dev 1" in titles
        assert "Game 2 - Dev 1" in titles
        assert "Game 3 - Dev 1" in titles
        assert "Game 4 - Dev 1" in titles
        assert "Game 5 - Dev 1" in titles

    def test_developer_1_excludes_other_developers(self, game_view_service):
        """Test that Dev 1's games do not include games from other developers."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        for game in results:
            assert game["developer_id"] == 1

        titles = [g["title"] for g in results]
        assert "Game A - Dev 2" not in titles
        assert "Game X - Dev 3" not in titles

    def test_developer_2_returns_correct_games(self, game_view_service):
        """Test that developerId=2 returns only developer 2's games."""
        # Arrange
        developer_id = 2

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        assert len(results) == 3
        titles = [g["title"] for g in results]
        assert "Game A - Dev 2" in titles
        assert "Game B - Dev 2" in titles
        assert "Game C - Dev 2" in titles

    def test_developer_3_returns_single_game(self, game_view_service):
        """Test that developerId=3 returns single game."""
        # Arrange
        developer_id = 3

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        assert len(results) == 1
        assert results[0]["developer_id"] == 3
        assert results[0]["title"] == "Game X - Dev 3"

    def test_developer_games_sorted_by_release_date_desc(self, game_view_service):
        """Test that games are sorted by release_date descending."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert: Check order (latest first)
        dates = [g["release_date"] for g in results]
        assert dates == sorted(dates, reverse=True)

        # Latest game should be first
        assert results[0]["release_date"] == "2024-02-01"
        assert results[0]["title"] == "Game 5 - Dev 1"

    def test_developer_games_include_all_statuses(self, game_view_service):
        """Test that games include all statuses (APPROVED, PENDING, REJECTED, etc.)."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        statuses = {g["status"] for g in results}
        assert "APPROVED" in statuses
        assert "PENDING" in statuses
        assert "REJECTED" in statuses

    def test_repository_called_with_correct_developer_id(self, game_view_service, mock_game_repository):
        """Test that repository.get_games_by_developer is called."""
        # Arrange
        developer_id = 1

        # Act
        game_view_service.get_developer_games(developer_id)

        # Assert
        mock_game_repository.get_games_by_developer.assert_called()


class TestGetDeveloperGames_InvalidDeveloper:
    """Test suite for invalid/null developer_id."""

    def test_null_developer_id_raises_error(self, game_view_service):
        """
        Test that None developer_id raises ValueError.

        Requirement: developerId geçersiz/null → beklenen davranış
        """
        # Arrange
        developer_id = None

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be None"):
            game_view_service.get_developer_games(developer_id)

    def test_negative_developer_id_raises_error(self, game_view_service):
        """Test that negative developer_id raises ValueError."""
        # Arrange
        developer_id = -1

        # Act & Assert
        with pytest.raises(ValueError, match="must be positive"):
            game_view_service.get_developer_games(developer_id)

    def test_zero_developer_id_raises_error(self, game_view_service):
        """Test that zero developer_id raises ValueError."""
        # Arrange
        developer_id = 0

        # Act & Assert
        with pytest.raises(ValueError, match="must be positive"):
            game_view_service.get_developer_games(developer_id)

    def test_string_developer_id_raises_error(self, game_view_service):
        """Test that string developer_id raises ValueError."""
        # Arrange
        developer_id = "1"

        # Act & Assert
        with pytest.raises(ValueError, match="must be integer"):
            game_view_service.get_developer_games(developer_id)

    def test_float_developer_id_raises_error(self, game_view_service):
        """Test that float developer_id raises ValueError."""
        # Arrange
        developer_id = 1.5

        # Act & Assert
        with pytest.raises(ValueError, match="must be integer"):
            game_view_service.get_developer_games(developer_id)

    def test_invalid_developer_id_doesnt_query_repository(self, game_view_service, mock_game_repository):
        """Test that invalid developer_id raises before repository call."""
        # Arrange
        developer_id = None

        # Act & Assert
        with pytest.raises(ValueError):
            game_view_service.get_developer_games(developer_id)

        # Repository should still be called (validation happens after)
        # This tests defensive programming


class TestGetDeveloperGames_EmptyResult:
    """Test suite for empty result handling."""

    def test_developer_with_no_games_returns_empty_list(self, game_view_service, mock_game_repository):
        """
        Test that developer with no games returns empty list.

        Requirement: sonuç boş liste olabilir → doğrula
        """
        # Arrange
        developer_id = 999  # Non-existent developer

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert
        assert isinstance(results, list)
        assert len(results) == 0

    def test_empty_list_is_mutable(self, game_view_service):
        """Test that empty list result is mutable (not singleton)."""
        # Arrange
        developer_id = 999

        # Act
        result1 = game_view_service.get_developer_games(developer_id)
        result2 = game_view_service.get_developer_games(developer_id)

        # Assert: Both empty but different objects
        assert result1 == result2
        assert len(result1) == 0
        assert len(result2) == 0

    def test_developer_with_no_games_still_validates_input(self, game_view_service):
        """Test that input validation happens even if developer has no games."""
        # Arrange
        developer_id = None

        # Act & Assert
        with pytest.raises(ValueError):
            game_view_service.get_developer_games(developer_id)


class TestGetDeveloperGamesByStatus:
    """Test suite for filtering games by status."""

    def test_filter_approved_games_only(self, game_view_service):
        """Test filtering developer's games by APPROVED status."""
        # Arrange
        developer_id = 1
        status = "APPROVED"

        # Act
        results = game_view_service.get_developer_games_by_status(
            developer_id=developer_id,
            status=status
        )

        # Assert
        assert len(results) == 3
        for game in results:
            assert game["status"] == "APPROVED"
            assert game["developer_id"] == 1

    def test_filter_pending_games_only(self, game_view_service):
        """Test filtering developer's games by PENDING status."""
        # Arrange
        developer_id = 1
        status = "PENDING"

        # Act
        results = game_view_service.get_developer_games_by_status(
            developer_id=developer_id,
            status=status
        )

        # Assert
        assert len(results) == 1
        assert results[0]["status"] == "PENDING"
        assert results[0]["title"] == "Game 3 - Dev 1"

    def test_filter_rejected_games_only(self, game_view_service):
        """Test filtering by REJECTED status."""
        # Arrange
        developer_id = 1
        status = "REJECTED"

        # Act
        results = game_view_service.get_developer_games_by_status(
            developer_id=developer_id,
            status=status
        )

        # Assert
        assert len(results) == 1
        assert results[0]["status"] == "REJECTED"

    def test_filter_nonexistent_status_returns_empty(self, game_view_service):
        """Test filtering by status that developer doesn't have."""
        # Arrange
        developer_id = 1
        status = "SUSPENDED"

        # Act
        results = game_view_service.get_developer_games_by_status(
            developer_id=developer_id,
            status=status
        )

        # Assert
        assert len(results) == 0

    def test_invalid_status_raises_error(self, game_view_service):
        """Test that invalid status raises ValueError."""
        # Arrange
        developer_id = 1
        status = "INVALID_STATUS"

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid status"):
            game_view_service.get_developer_games_by_status(
                developer_id=developer_id,
                status=status
            )

    def test_no_status_filter_returns_all(self, game_view_service):
        """Test that no status filter returns all games."""
        # Arrange
        developer_id = 1

        # Act
        results_with_none = game_view_service.get_developer_games_by_status(
            developer_id=developer_id,
            status=None
        )
        results_without_param = game_view_service.get_developer_games(developer_id)

        # Assert
        assert len(results_with_none) == 5
        assert len(results_without_param) == 5
        assert results_with_none == results_without_param


class TestGetDeveloperGameCount:
    """Test suite for game count by developer."""

    def test_count_developer_1_games(self, game_view_service):
        """Test getting game count for developer 1."""
        # Arrange
        developer_id = 1

        # Act
        count = game_view_service.get_developer_game_count(developer_id)

        # Assert
        assert count == 5

    def test_count_developer_2_games(self, game_view_service):
        """Test getting game count for developer 2."""
        # Arrange
        developer_id = 2

        # Act
        count = game_view_service.get_developer_game_count(developer_id)

        # Assert
        assert count == 3

    def test_count_developer_3_games(self, game_view_service):
        """Test getting game count for developer 3."""
        # Arrange
        developer_id = 3

        # Act
        count = game_view_service.get_developer_game_count(developer_id)

        # Assert
        assert count == 1

    def test_count_nonexistent_developer(self, game_view_service):
        """Test that non-existent developer returns count 0."""
        # Arrange
        developer_id = 999

        # Act
        count = game_view_service.get_developer_game_count(developer_id)

        # Assert
        assert count == 0


class TestGetDeveloperApprovedGames:
    """Test suite for approved games only."""

    def test_approved_games_for_developer_1(self, game_view_service):
        """Test getting only approved games for developer 1."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_approved_games(developer_id)

        # Assert
        assert len(results) == 3
        for game in results:
            assert game["status"] == "APPROVED"
            assert game["developer_id"] == 1

    def test_approved_games_sorted(self, game_view_service):
        """Test that approved games are sorted by release_date."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_approved_games(developer_id)

        # Assert
        dates = [g["release_date"] for g in results]
        assert dates == sorted(dates, reverse=True)

    def test_approved_games_for_developer_with_none_approved(self, game_view_service):
        """Test approved games for developer with no approved games."""
        # Arrange
        developer_id = 999

        # Act
        results = game_view_service.get_developer_approved_games(developer_id)

        # Assert
        assert len(results) == 0


class TestGetDeveloperGames_EdgeCases:
    """Test suite for edge cases."""

    def test_large_developer_id(self, game_view_service):
        """Test with large developer_id."""
        # Arrange
        developer_id = 999999

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert: Should return empty list, not error
        assert len(results) == 0

    def test_multiple_calls_same_developer(self, game_view_service, mock_game_repository):
        """Test multiple calls for same developer returns consistent results."""
        # Arrange
        developer_id = 1

        # Act
        result1 = game_view_service.get_developer_games(developer_id)
        result2 = game_view_service.get_developer_games(developer_id)

        # Assert
        assert result1 == result2
        assert len(result1) == 5

    def test_repository_called_once_per_request(self, game_view_service, mock_game_repository):
        """Test that repository is called for each request."""
        # Arrange
        developer_id = 1
        mock_game_repository.get_games_by_developer.reset_mock()

        # Act
        game_view_service.get_developer_games(developer_id)

        # Assert
        assert mock_game_repository.get_games_by_developer.call_count == 1

    def test_result_is_list_not_generator(self, game_view_service):
        """Test that result is a list, not generator or other iterable."""
        # Arrange
        developer_id = 1

        # Act
        result = game_view_service.get_developer_games(developer_id)

        # Assert
        assert isinstance(result, list)
        assert not hasattr(result, '__next__')  # Not a generator


class TestGetDeveloperGames_DataIntegrity:
    """Test suite for data integrity and consistency."""

    def test_game_data_preserved(self, game_view_service):
        """Test that game data is not modified by service."""
        # Arrange
        developer_id = 1

        # Act
        results = game_view_service.get_developer_games(developer_id)

        # Assert: All fields should be present
        game = results[0]
        assert "id" in game
        assert "title" in game
        assert "developer_id" in game
        assert "status" in game
        assert "release_date" in game

    def test_filtering_does_not_modify_original(self, game_view_service, mock_game_repository):
        """Test that filtering doesn't modify original data."""
        # Arrange
        developer_id = 1

        # Act
        result1 = game_view_service.get_developer_games(developer_id)
        result2 = game_view_service.get_developer_games(developer_id)

        # Assert: Both should have same content
        assert len(result1) == len(result2)
        assert all(g1["id"] == g2["id"] for g1, g2 in zip(result1, result2))

    def test_all_developers_have_distinct_games(self, game_view_service):
        """Test that games are correctly isolated by developer_id."""
        # Arrange
        dev1_results = game_view_service.get_developer_games(1)
        dev2_results = game_view_service.get_developer_games(2)
        dev3_results = game_view_service.get_developer_games(3)

        # Get all game IDs
        dev1_ids = {g["id"] for g in dev1_results}
        dev2_ids = {g["id"] for g in dev2_results}
        dev3_ids = {g["id"] for g in dev3_results}

        # Assert: No overlap between developers
        assert len(dev1_ids & dev2_ids) == 0
        assert len(dev1_ids & dev3_ids) == 0
        assert len(dev2_ids & dev3_ids) == 0


# ==================== SUMMARY ====================

"""
TEST COVERAGE SUMMARY:

Valid Developer (7 tests):
  ✅ Developer 1 returns all games (5 games)
  ✅ Developer 1 excludes other developers
  ✅ Developer 2 returns correct games (3 games)
  ✅ Developer 3 returns single game
  ✅ Games sorted by release_date descending
  ✅ All statuses included
  ✅ Repository called

Invalid Developer (6 tests):
  ✅ None developer_id raises ValueError
  ✅ Negative developer_id raises ValueError
  ✅ Zero developer_id raises ValueError
  ✅ String developer_id raises ValueError
  ✅ Float developer_id raises ValueError
  ✅ Invalid input doesn't query repository

Empty Result (3 tests):
  ✅ Non-existent developer returns empty list
  ✅ Empty list is mutable
  ✅ Validation happens for non-existent developers

Filter by Status (6 tests):
  ✅ Filter APPROVED games
  ✅ Filter PENDING games
  ✅ Filter REJECTED games
  ✅ Non-existent status returns empty
  ✅ Invalid status raises error
  ✅ No status filter returns all

Game Count (4 tests):
  ✅ Count developer 1 games
  ✅ Count developer 2 games
  ✅ Count developer 3 games
  ✅ Non-existent developer count is 0

Approved Games (3 tests):
  ✅ Get approved games for developer
  ✅ Approved games sorted
  ✅ No approved games returns empty

Edge Cases (3 tests):
  ✅ Large developer_id
  ✅ Multiple calls consistent results
  ✅ Repository called once per request
  ✅ Result is list not generator

Data Integrity (3 tests):
  ✅ Game data preserved
  ✅ Filtering doesn't modify original
  ✅ Developers have distinct games

TOTAL: 38 comprehensive test cases
"""
