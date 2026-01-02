import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const API_URL = 'http://localhost:8000';

export default function EditGame() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isDeveloper } = useAuth();

  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    short_description: '',
    price: '',
    discount_percent: 0,
    genre_ids: [],
    cover_image_url: '',
    trailer_url: ''
  });

  useEffect(() => {
    if (!isDeveloper()) {
      navigate('/become-developer');
      return;
    }
    fetchData();
  }, [isDeveloper, navigate, id]);

  const fetchData = async () => {
    try {
      const [gameRes, genresRes] = await Promise.all([
        axios.get(`${API_URL}/games/developer/my-games`),
        axios.get(`${API_URL}/genres/`)
      ]);

      // Find the game in developer's games
      const game = gameRes.data.find(g => g.id === parseInt(id));
      if (!game) {
        setError('Game not found or you do not own this game');
        setLoading(false);
        return;
      }

      setFormData({
        title: game.title || '',
        description: game.description || '',
        short_description: game.short_description || '',
        price: game.price?.toString() || '0',
        discount_percent: game.discount_percent || 0,
        genre_ids: game.genres?.map(g => g.id) || [],
        cover_image_url: game.cover_image_url || '',
        trailer_url: game.trailer_url || ''
      });
      setGenres(genresRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      setError('Failed to load game data');
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

    setSaving(true);
    try {
      await axios.put(`${API_URL}/games/${id}`, {
        ...formData,
        price: parseFloat(formData.price) || 0,
        discount_percent: parseInt(formData.discount_percent) || 0
      });
      setSuccess('Game updated successfully!');
      setTimeout(() => navigate('/developer'), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update game');
    } finally {
      setSaving(false);
    }
  };

  const handleGenreToggle = (genreId) => {
    setFormData(prev => ({
      ...prev,
      genre_ids: prev.genre_ids.includes(genreId)
        ? prev.genre_ids.filter(gid => gid !== genreId)
        : [...prev.genre_ids, genreId]
    }));
  };

  if (loading) {
    return (
      <div className="glass-container flex justify-center items-center min-h-[60vh]">
        <div className="glass-spinner" />
      </div>
    );
  }

  if (error && !formData.title) {
    return (
      <div className="glass-container">
        <div className="glass-card text-center py-12">
          <div className="text-5xl mb-4">😢</div>
          <p className="text-red-400 text-xl mb-4">{error}</p>
          <Link to="/developer" className="glass-btn glass-btn-primary">
            Back to Dashboard
          </Link>
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
            <h1 className="text-3xl font-bold text-white mb-1">Edit Game</h1>
            <p className="text-white/50">Update your game information</p>
          </div>
          <Link to="/developer" className="glass-btn">
            ← Back to Dashboard
          </Link>
        </div>
      </div>

      {/* Form */}
      <div className="glass-card">
        {error && (
          <div className="glass-alert glass-alert-error mb-6">
            <span>⚠️</span> {error}
          </div>
        )}

        {success && (
          <div className="glass-alert glass-alert-success mb-6">
            <span>✓</span> {success}
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

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
              <label className="glass-label">Discount (%)</label>
              <input
                type="number"
                min="0"
                max="100"
                value={formData.discount_percent}
                onChange={(e) => setFormData({ ...formData, discount_percent: e.target.value })}
                className="glass-input"
                placeholder="0"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Final Price</label>
              <div className="glass-input bg-transparent flex items-center">
                <span className="text-green-400 font-bold">
                  ${((parseFloat(formData.price) || 0) * (1 - (parseInt(formData.discount_percent) || 0) / 100)).toFixed(2)}
                </span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-form-group">
              <label className="glass-label">Cover Image URL</label>
              <input
                type="url"
                value={formData.cover_image_url}
                onChange={(e) => setFormData({ ...formData, cover_image_url: e.target.value })}
                className="glass-input"
                placeholder="https://..."
              />
              {formData.cover_image_url && (
                <img
                  src={formData.cover_image_url}
                  alt="Cover preview"
                  className="mt-2 w-32 h-20 object-cover rounded-lg"
                  onError={(e) => e.target.style.display = 'none'}
                />
              )}
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Trailer URL</label>
              <input
                type="url"
                value={formData.trailer_url}
                onChange={(e) => setFormData({ ...formData, trailer_url: e.target.value })}
                className="glass-input"
                placeholder="https://youtube.com/..."
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
                    formData.genre_ids.includes(genre.id) ? 'glass-btn-primary' : ''
                  }`}
                >
                  {genre.name}
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-4 pt-4 border-t border-white/10">
            <button
              type="submit"
              disabled={saving}
              className="glass-btn glass-btn-success"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
            <Link to="/developer" className="glass-btn">
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
