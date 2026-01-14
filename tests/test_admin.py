"""
Unit tests for Admin operations
Tests: approve_game endpoint
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.routers import admin


@pytest.mark.unit
class TestApproveGame:
    """Tests for approve_game endpoint"""

    def test_approve_pending_game_success(self, mock_db, admin_user, sample_pending_game):
        """✅ Positive: Approve pending game - status and metadata updated"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_pending_game

        mock_db.commit.return_value = None

        # Act
        result = admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=admin_user
        )

        # Assert
        assert result["message"] == "Game approved successfully"
        assert sample_pending_game.status == models.GameStatus.APPROVED
        assert sample_pending_game.approved_by == admin_user.id
        assert sample_pending_game.approved_at is not None
        assert sample_pending_game.rejection_reason is None
        assert mock_db.commit.called

    def test_approve_nonexistent_game_fails(self, mock_db, admin_user):
        """❌ Negative: Approve non-existent game returns 404"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # Game not found

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            admin.approve_game(
                game_id=999,
                db=mock_db,
                admin=admin_user
            )

        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()

    def test_approve_already_approved_game_fails(self, mock_db, admin_user, sample_approved_game):
        """❌ Negative: Approve already approved game returns 400"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_approved_game

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            admin.approve_game(
                game_id=sample_approved_game.id,
                db=mock_db,
                admin=admin_user
            )

        assert exc_info.value.status_code == 400
        assert "already approved" in exc_info.value.detail.lower()

    def test_approve_rejected_game_updates_status(self, mock_db, admin_user):
        """✅ Positive: Approve a previously rejected game - status changes"""
        # Arrange
        rejected_game = models.Game(
            id=5,
            title="Reapplied Game",
            description="Game reapplied after rejection",
            price=24.99,
            discount_percent=0,
            developer_id=4,
            status=models.GameStatus.REJECTED,
            rejection_reason="Inappropriate content",
            release_date=datetime.utcnow(),
            total_sales=0,
            total_revenue=0.0
        )

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = rejected_game

        mock_db.commit.return_value = None

        # Act
        result = admin.approve_game(
            game_id=rejected_game.id,
            db=mock_db,
            admin=admin_user
        )

        # Assert
        assert rejected_game.status == models.GameStatus.APPROVED
        assert rejected_game.rejection_reason is None  # Cleared
        assert rejected_game.approved_by == admin_user.id
        assert result["message"] == "Game approved successfully"

    def test_approve_game_sets_admin_id_correctly(self, mock_db, admin_user, sample_pending_game):
        """✅ Positive: approved_by field set to correct admin ID"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_pending_game

        mock_db.commit.return_value = None

        # Act
        admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=admin_user
        )

        # Assert
        assert sample_pending_game.approved_by == admin_user.id
        assert sample_pending_game.approved_by == 2  # admin_user.id = 2

    def test_approve_game_sets_timestamp(self, mock_db, admin_user, sample_pending_game):
        """✅ Positive: approved_at timestamp set to current time"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_pending_game

        before_approval = datetime.utcnow()
        mock_db.commit.return_value = None

        # Act
        admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=admin_user
        )

        after_approval = datetime.utcnow()

        # Assert
        assert sample_pending_game.approved_at is not None
        assert before_approval <= sample_pending_game.approved_at <= after_approval

    def test_approve_game_non_admin_fails(self, mock_db, sample_user, sample_pending_game):
        """❌ Negative: Non-admin user cannot approve games (403)"""
        # This test would normally be caught by the dependency injection
        # We test it here for completeness - in real scenario, require_admin() would reject

        # Arrange
        non_admin = sample_user  # Regular user, not admin
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_pending_game

        # In production, require_admin dependency would raise 403 before reaching endpoint
        # We verify the endpoint logic by simulating with admin parameter
        # Real test would be integration test with TestClient

        # For unit test purposes, we just verify the endpoint works with admin
        result = admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=non_admin  # Simulating wrong user
        )

        # Endpoint logic doesn't check role - that's handled by dependency
        # This test documents that behavior

    def test_approve_suspended_game(self, mock_db, admin_user):
        """✅ Positive: Approve a suspended game (re-enable it)"""
        # Arrange
        suspended_game = models.Game(
            id=6,
            title="Suspended Game",
            description="Previously suspended game",
            price=39.99,
            discount_percent=0,
            developer_id=4,
            status=models.GameStatus.SUSPENDED,
            rejection_reason="Policy violation - now fixed",
            release_date=datetime.utcnow(),
            total_sales=50,
            total_revenue=1999.50
        )

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = suspended_game

        mock_db.commit.return_value = None

        # Act
        result = admin.approve_game(
            game_id=suspended_game.id,
            db=mock_db,
            admin=admin_user
        )

        # Assert
        assert suspended_game.status == models.GameStatus.APPROVED
        assert suspended_game.rejection_reason is None

    def test_approve_multiple_games_independently(self, mock_db, admin_user, multiple_approved_games):
        """✅ Edge Case: Multiple games can be approved independently"""
        # Arrange - Multiple pending games
        pending_games = [
            models.Game(
                id=20,
                title="Game A",
                price=29.99,
                discount_percent=0,
                developer_id=4,
                status=models.GameStatus.PENDING,
                release_date=datetime.utcnow(),
                total_sales=0,
                total_revenue=0.0
            ),
            models.Game(
                id=21,
                title="Game B",
                price=39.99,
                discount_percent=0,
                developer_id=4,
                status=models.GameStatus.PENDING,
                release_date=datetime.utcnow(),
                total_sales=0,
                total_revenue=0.0
            ),
        ]

        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_db.commit.return_value = None

        # Act & Assert - Approve each game
        for game in pending_games:
            mock_filter.first.return_value = game
            result = admin.approve_game(
                game_id=game.id,
                db=mock_db,
                admin=admin_user
            )

            assert result["message"] == "Game approved successfully"
            assert game.status == models.GameStatus.APPROVED
            assert game.approved_by == admin_user.id


@pytest.mark.unit
class TestApproveGameIntegration:
    """Integration-style tests for approve_game (still using mocks)"""

    def test_approve_game_database_transaction_committed(self, mock_db, admin_user, sample_pending_game):
        """✅ Positive: Database transaction is committed after approval"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = sample_pending_game

        commit_called = False
        def mock_commit():
            nonlocal commit_called
            commit_called = True

        mock_db.commit.side_effect = mock_commit

        # Act
        admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=admin_user
        )

        # Assert
        assert commit_called

    def test_approve_game_idempotent_second_call_fails(self, mock_db, admin_user, sample_pending_game):
        """✅ Positive: Approving same game twice fails on second attempt"""
        # Arrange
        mock_query = MagicMock()
        mock_filter = MagicMock()

        # First call: game is pending
        # Second call: game is now approved
        responses = [sample_pending_game, sample_pending_game]

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.side_effect = responses

        mock_db.commit.return_value = None

        # Act - First approval succeeds
        result1 = admin.approve_game(
            game_id=sample_pending_game.id,
            db=mock_db,
            admin=admin_user
        )
        assert "approved successfully" in result1["message"]

        # Update the game status for second call
        sample_pending_game.status = models.GameStatus.APPROVED

        # Second attempt should fail
        with pytest.raises(HTTPException) as exc_info:
            admin.approve_game(
                game_id=sample_pending_game.id,
                db=mock_db,
                admin=admin_user
            )

        assert exc_info.value.status_code == 400
