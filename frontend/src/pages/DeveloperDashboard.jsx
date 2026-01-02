import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { SkeletonAdminGameCard, SkeletonText, Skeleton, SkeletonButton } from '../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function DeveloperDashboard() {
  const [games, setGames] = useState([]);
  const [genres, setGenres] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    short_description: '',
    price: '',
    genre_ids: [],
    cover_image_url: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { user, isDeveloper } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isDeveloper()) {
      navigate('/become-developer');
      return;
    }
    fetchData();
  }, [isDeveloper, navigate]);

  const fetchData = async () => {
    try {
      const [gamesRes, genresRes, statsRes] = await Promise.all([
        axios.get(`${API_URL}/games/developer/my-games`),
        axios.get(`${API_URL}/genres/`),
        axios.get(`${API_URL}/games/developer/stats`)
      ]);
      setGames(gamesRes.data);
      setGenres(genresRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.title.length < 2) {
      setError('Title must be at least 2 characters');
      return;
    }
    if (formData.description.length < 10) {
      setError('Description must be at least 10 characters');
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/games/`, {
        ...formData,
        price: parseFloat(formData.price) || 0
      });

      setGames([response.data, ...games]);
      setSuccess('Game submitted for approval!');
      setFormData({
        title: '',
        description: '',
        short_description: '',
        price: '',
        genre_ids: [],
        cover_image_url: ''
      });
      setShowForm(false);
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to publish game');
    }
  };

  const handleGenreToggle = (genreId) => {
    setFormData(prev => ({
      ...prev,
      genre_ids: prev.genre_ids.includes(genreId)
        ? prev.genre_ids.filter(id => id !== genreId)
        : [...prev.genre_ids, genreId]
    }));
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
              <SkeletonText width="250px" height="2rem" className="mb-2" />
              <SkeletonText width="150px" height="1rem" />
            </div>
            <SkeletonButton width="150px" height="40px" />
          </div>
        </div>

        {/* Stats Skeleton */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="glass-stat-card">
              <SkeletonText width="80px" height="0.875rem" className="mb-2" />
              <SkeletonText width="60px" height="2rem" />
            </div>
          ))}
        </div>

        {/* Games Grid Skeleton */}
        <div className="glass-card mb-6">
          <SkeletonText width="120px" height="1.5rem" className="mb-4" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
            <h1 className="text-3xl font-bold text-white mb-1">Developer Dashboard</h1>
            <p className="text-white/50">
              Welcome, <span className="text-purple-400">{user?.developer_name || user?.username}</span>
              {user?.developer_verified && <span className="text-cyan-400 ml-2">✓ Verified</span>}
            </p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="glass-btn glass-btn-primary"
          >
            {showForm ? 'Cancel' : '+ Publish New Game'}
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <div className="glass-stat-card">
            <div className="glass-stat-icon">📦</div>
            <div className="glass-stat-value">{stats.total_games}</div>
            <div className="glass-stat-label">Total Games</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">✅</div>
            <div className="glass-stat-value text-green-400">{stats.approved_games}</div>
            <div className="glass-stat-label">Approved</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">⏳</div>
            <div className="glass-stat-value text-yellow-400">{stats.pending_games}</div>
            <div className="glass-stat-label">Pending</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">🛒</div>
            <div className="glass-stat-value text-cyan-400">{stats.total_sales}</div>
            <div className="glass-stat-label">Total Sales</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">💰</div>
            <div className="glass-stat-value text-green-400">${stats.total_revenue.toFixed(2)}</div>
            <div className="glass-stat-label">Revenue</div>
          </div>
        </div>
      )}

      {/* New Game Form */}
      {showForm && (
        <div className="glass-card mb-6">
          <h2 className="text-xl font-bold text-white mb-6">Publish New Game</h2>

          {error && (
            <div className="glass-alert glass-alert-error mb-6">
              <span>⚠️</span> {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="glass-form-group">
              <label className="glass-label">Game Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="glass-input"
                required
                placeholder="Enter game title"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Short Description</label>
              <input
                type="text"
                value={formData.short_description}
                onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
                className="glass-input"
                maxLength={500}
                placeholder="Brief description for store listing"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Full Description *</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="glass-input glass-textarea"
                required
                placeholder="Detailed game description"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-form-group">
                <label className="glass-label">Price ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  className="glass-input"
                  placeholder="0.00 for free"
                />
              </div>

              <div className="glass-form-group">
                <label className="glass-label">Cover Image URL</label>
                <input
                  type="url"
                  value={formData.cover_image_url}
                  onChange={(e) => setFormData({ ...formData, cover_image_url: e.target.value })}
                  className="glass-input"
                  placeholder="https://..."
                />
              </div>
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Genres</label>
              <div className="flex flex-wrap gap-2">
                {genres.map(genre => (
                  <button
                    key={genre.id}
                    type="button"
                    onClick={() => handleGenreToggle(genre.id)}
                    className={`glass-btn glass-btn-sm ${
                      formData.genre_ids.includes(genre.id)
                        ? 'glass-btn-primary'
                        : ''
                    }`}
                  >
                    {genre.name}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex gap-4">
              <button type="submit" className="glass-btn glass-btn-success">
                Submit for Approval
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="glass-btn"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {success && (
        <div className="glass-alert glass-alert-success mb-6">
          <span>✓</span> {success}
        </div>
      )}

      {/* Games List */}
      <div className="glass-card">
        <h2 className="text-xl font-bold text-white mb-6">My Games ({games.length})</h2>

        {games.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-5xl mb-4">🎮</div>
            <p className="text-white/50">You haven&apos;t published any games yet.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {games.map(game => (
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
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <h3 className="font-semibold text-lg text-white">{game.title}</h3>
                        <span className={`glass-badge ${getStatusBadge(game.status)}`}>
                          {game.status}
                        </span>
                      </div>
                      <p className="text-white/50 text-sm line-clamp-2 mb-2">{game.description}</p>

                      {game.rejection_reason && (
                        <p className="text-red-400 text-sm">
                          ⚠️ Rejection reason: {game.rejection_reason}
                        </p>
                      )}

                      <div className="flex flex-wrap gap-4 text-sm text-white/40">
                        <span>💰 ${game.price.toFixed(2)}</span>
                        <span>🛒 {game.total_sales || 0} sales</span>
                        <span>💵 ${(game.total_revenue || 0).toFixed(2)} revenue</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    {game.status === 'approved' && (
                      <Link to={`/game/${game.id}`} className="glass-btn glass-btn-sm">
                        View
                      </Link>
                    )}
                    <Link to={`/developer/edit-game/${game.id}`} className="glass-btn glass-btn-sm">
                      Edit
                    </Link>
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
