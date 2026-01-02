import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { SkeletonText, Skeleton, SkeletonAdminGameCard } from '../../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [pendingGames, setPendingGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAdmin } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAdmin()) {
      navigate('/');
      return;
    }
    fetchData();
  }, [isAdmin, navigate]);

  const fetchData = async () => {
    try {
      const [statsRes, pendingRes] = await Promise.all([
        axios.get(`${API_URL}/admin/stats`),
        axios.get(`${API_URL}/admin/games/pending`)
      ]);
      setStats(statsRes.data);
      setPendingGames(pendingRes.data);
    } catch (err) {
      setError('Failed to load admin data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (gameId) => {
    try {
      await axios.put(`${API_URL}/admin/games/${gameId}/approve`);
      setPendingGames(pendingGames.filter(g => g.id !== gameId));
      setStats({ ...stats, pending_games: stats.pending_games - 1, approved_games: stats.approved_games + 1 });
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
      setPendingGames(pendingGames.filter(g => g.id !== gameId));
      setStats({ ...stats, pending_games: stats.pending_games - 1 });
    } catch (err) {
      alert('Failed to reject game');
    }
  };

  if (loading) {
    return (
      <div className="glass-container">
        {/* Header Skeleton */}
        <div className="glass-card mb-6">
          <SkeletonText width="220px" height="2rem" className="mb-2" />
          <SkeletonText width="180px" height="1rem" />
        </div>

        {/* Stats Skeleton */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="glass-stat-card">
              <SkeletonText width="100px" height="0.875rem" className="mb-2" />
              <SkeletonText width="60px" height="2rem" />
            </div>
          ))}
        </div>

        {/* Quick Links Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Skeleton height="80px" />
          <Skeleton height="80px" />
        </div>

        {/* Pending Games Skeleton */}
        <div className="glass-card">
          <SkeletonText width="180px" height="1.5rem" className="mb-4" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <SkeletonAdminGameCard />
            <SkeletonAdminGameCard />
          </div>
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
            <h1 className="text-3xl font-bold text-white mb-1">Admin Dashboard</h1>
            <p className="text-white/50">System overview and management</p>
          </div>
          <div className="flex gap-3 flex-wrap">
            <Link to="/admin/users" className="glass-btn glass-btn-primary">
              Manage Users
            </Link>
            <Link to="/admin/games" className="glass-btn glass-btn-success">
              All Games
            </Link>
          </div>
        </div>
      </div>

      {error && (
        <div className="glass-alert glass-alert-error mb-6">
          <span>⚠️</span> {error}
        </div>
      )}

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="glass-stat-card">
            <div className="glass-stat-icon">👥</div>
            <div className="glass-stat-value text-cyan-400">{stats.total_users}</div>
            <div className="glass-stat-label">Total Users</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">🔧</div>
            <div className="glass-stat-value text-purple-400">{stats.total_developers}</div>
            <div className="glass-stat-label">Developers</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">🎮</div>
            <div className="glass-stat-value text-green-400">{stats.total_games}</div>
            <div className="glass-stat-label">Total Games</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">⏳</div>
            <div className="glass-stat-value text-yellow-400">{stats.pending_games}</div>
            <div className="glass-stat-label">Pending</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">✅</div>
            <div className="glass-stat-value text-green-400">{stats.approved_games}</div>
            <div className="glass-stat-label">Approved</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">🛒</div>
            <div className="glass-stat-value text-cyan-400">{stats.total_orders}</div>
            <div className="glass-stat-label">Total Orders</div>
          </div>
          <div className="glass-stat-card col-span-2">
            <div className="glass-stat-icon">💰</div>
            <div className="glass-stat-value text-green-400">${stats.total_revenue.toFixed(2)}</div>
            <div className="glass-stat-label">Total Revenue</div>
          </div>
        </div>
      )}

      {/* Pending Games */}
      <div className="glass-card">
        <h2 className="text-xl font-bold text-white mb-6">
          Games Pending Approval <span className="text-white/40">({pendingGames.length})</span>
        </h2>

        {pendingGames.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-5xl mb-4">✅</div>
            <p className="text-white/50">No games pending approval</p>
          </div>
        ) : (
          <div className="space-y-4">
            {pendingGames.map(game => (
              <div key={game.id} className="glass-card glass-card-sm glass-card-hover">
                <div className="flex flex-col md:flex-row justify-between items-start gap-4">
                  <div className="flex gap-4 flex-1">
                    {game.cover_image_url ? (
                      <img
                        src={game.cover_image_url}
                        alt={game.title}
                        className="w-20 h-20 rounded-lg object-cover"
                      />
                    ) : (
                      <div className="w-20 h-20 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-600 flex items-center justify-center">
                        <span className="text-2xl">🎮</span>
                      </div>
                    )}
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg text-white">{game.title}</h3>
                      <p className="text-white/50 text-sm mb-1">
                        by {game.developer?.developer_name || game.developer?.username}
                      </p>
                      <p className="text-white/40 text-sm line-clamp-2">{game.description}</p>
                      <p className="text-green-400 font-bold mt-2">${game.price.toFixed(2)}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
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
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
