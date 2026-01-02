import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { SkeletonText, Skeleton, SkeletonAdminGameCard, SkeletonButton } from '../../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function GameManagement() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const { isAdmin } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAdmin()) {
      navigate('/');
      return;
    }
    fetchGames();
  }, [isAdmin, navigate, filter]);

  const fetchGames = async () => {
    try {
      let url = `${API_URL}/admin/games?limit=100`;
      if (filter) url += `&status=${filter}`;

      const response = await axios.get(url);
      setGames(response.data);
    } catch (err) {
      console.error('Failed to fetch games:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (gameId) => {
    try {
      await axios.put(`${API_URL}/admin/games/${gameId}/approve`);
      setGames(games.map(g => g.id === gameId ? { ...g, status: 'approved' } : g));
    } catch (err) {
      alert('Failed to approve game');
    }
  };

  const handleReject = async (gameId) => {
    const reason = prompt('Enter rejection reason (min 10 chars):');
    if (!reason || reason.length < 10) {
      alert('Rejection reason must be at least 10 characters');
      return;
    }
    try {
      await axios.put(`${API_URL}/admin/games/${gameId}/reject?reason=${encodeURIComponent(reason)}`);
      setGames(games.map(g => g.id === gameId ? { ...g, status: 'rejected', rejection_reason: reason } : g));
    } catch (err) {
      alert('Failed to reject game');
    }
  };

  const handleSuspend = async (gameId) => {
    const reason = prompt('Enter suspension reason (min 10 chars):');
    if (!reason || reason.length < 10) {
      alert('Suspension reason must be at least 10 characters');
      return;
    }
    try {
      await axios.put(`${API_URL}/admin/games/${gameId}/suspend?reason=${encodeURIComponent(reason)}`);
      setGames(games.map(g => g.id === gameId ? { ...g, status: 'suspended', rejection_reason: reason } : g));
    } catch (err) {
      alert('Failed to suspend game');
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'approved': return 'glass-badge-success';
      case 'pending': return 'glass-badge-warning';
      case 'rejected': return 'glass-badge-error';
      case 'suspended': return 'glass-badge-user';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className="glass-container">
        {/* Header Skeleton */}
        <div className="glass-card mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <SkeletonText width="200px" height="2rem" className="mb-2" />
              <SkeletonText width="100px" height="1rem" />
            </div>
            <div className="flex gap-2">
              <SkeletonButton width="160px" height="40px" />
              <SkeletonButton width="150px" height="40px" />
            </div>
          </div>
        </div>

        {/* Filters Skeleton */}
        <div className="glass-card mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
            <Skeleton width="192px" height="44px" />
            <SkeletonText width="120px" height="1rem" />
          </div>
        </div>

        {/* Games Grid Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <SkeletonAdminGameCard />
          <SkeletonAdminGameCard />
          <SkeletonAdminGameCard />
          <SkeletonAdminGameCard />
          <SkeletonAdminGameCard />
          <SkeletonAdminGameCard />
        </div>
      </div>
    );
  }

  return (
    <div className="glass-container">
      {/* Header */}
      <div className="glass-card mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">Game Management</h1>
            <p className="text-white/50">{games.length} games</p>
          </div>
          <div className="flex gap-2">
            <Link to="/admin/publish-game" className="glass-btn glass-btn-primary">
              + Publish New Game
            </Link>
            <Link to="/admin" className="glass-btn">
              ← Back to Dashboard
            </Link>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card mb-6">
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="glass-input glass-select md:w-48"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="suspended">Suspended</option>
          </select>
          <span className="text-white/40">
            Showing {games.length} games
          </span>
        </div>
      </div>

      {/* Games Grid */}
      {games.length === 0 ? (
        <div className="glass-card text-center py-12">
          <div className="text-5xl mb-4">🎮</div>
          <p className="text-white/50">No games found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {games.map(game => (
            <div key={game.id} className="glass-card glass-card-hover">
              {game.cover_image_url ? (
                <img
                  src={game.cover_image_url}
                  alt={game.title}
                  className="w-full h-40 object-cover rounded-lg mb-4"
                />
              ) : (
                <div className="w-full h-40 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-600 flex items-center justify-center mb-4">
                  <span className="text-5xl">🎮</span>
                </div>
              )}

              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-lg text-white">{game.title}</h3>
                <span className={`glass-badge ${getStatusBadge(game.status)}`}>
                  {game.status}
                </span>
              </div>

              <p className="text-white/50 text-sm mb-2">
                by {game.developer?.developer_name || game.developer?.username}
              </p>

              <p className="text-white/40 text-sm line-clamp-2 mb-3">{game.description}</p>

              <div className="flex justify-between items-center mb-4">
                <span className="text-green-400 font-bold">${game.price.toFixed(2)}</span>
                <span className="text-white/40 text-sm">
                  {game.total_sales || 0} sales • ${(game.total_revenue || 0).toFixed(2)}
                </span>
              </div>

              {game.rejection_reason && (
                <div className="glass-alert glass-alert-error mb-4 text-sm">
                  <span>⚠️</span> {game.rejection_reason}
                </div>
              )}

              <div className="flex gap-2 flex-wrap">
                {game.status === 'pending' && (
                  <>
                    <button
                      onClick={() => handleApprove(game.id)}
                      className="glass-btn glass-btn-sm glass-btn-success"
                    >
                      Approve
                    </button>
                    <button
                      onClick={() => handleReject(game.id)}
                      className="glass-btn glass-btn-sm glass-btn-danger"
                    >
                      Reject
                    </button>
                  </>
                )}

                {game.status === 'approved' && (
                  <button
                    onClick={() => handleSuspend(game.id)}
                    className="glass-btn glass-btn-sm"
                  >
                    Suspend
                  </button>
                )}

                {(game.status === 'rejected' || game.status === 'suspended') && (
                  <button
                    onClick={() => handleApprove(game.id)}
                    className="glass-btn glass-btn-sm glass-btn-success"
                  >
                    Approve
                  </button>
                )}

                <Link
                  to={`/game/${game.id}`}
                  className="glass-btn glass-btn-sm"
                >
                  View
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
