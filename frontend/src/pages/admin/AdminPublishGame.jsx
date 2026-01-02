import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

const API_URL = 'http://localhost:8000';

export default function AdminPublishGame() {
  const [developers, setDevelopers] = useState([]);
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
    genre_ids: [],
    cover_image_url: '',
    trailer_url: '',
    developer_id: '',
    auto_approve: true
  });

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
      const [developersRes, genresRes] = await Promise.all([
        axios.get(`${API_URL}/admin/developers`),
        axios.get(`${API_URL}/genres/`)
      ]);
      setDevelopers(developersRes.data);
      setGenres(genresRes.data);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.developer_id) {
      setError('Please select a developer');
      return;
    }

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
      await axios.post(`${API_URL}/admin/games`, {
        ...formData,
        price: parseFloat(formData.price) || 0,
        developer_id: parseInt(formData.developer_id)
      });
      setSuccess('Game published successfully!');
      setTimeout(() => navigate('/admin/games'), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to publish game');
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

  return (
    <div className="glass-container">
      {/* Header */}
      <div className="glass-card mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">Publish New Game</h1>
            <p className="text-white/50">Add a game to the store (Admin)</p>
          </div>
          <Link to="/admin/games" className="glass-btn">
            ← Back to Game Management
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
          {/* Developer Selection */}
          <div className="glass-form-group">
            <label className="glass-label">Developer *</label>
            <select
              value={formData.developer_id}
              onChange={(e) => setFormData({ ...formData, developer_id: e.target.value })}
              className="glass-input glass-select"
              required
            >
              <option value="">Select a developer...</option>
              {developers.map(dev => (
                <option key={dev.id} value={dev.id}>
                  {dev.developer_name || dev.username} ({dev.email})
                </option>
              ))}
            </select>
          </div>

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
            <label className="glass-label">Trailer URL</label>
            <input
              type="url"
              value={formData.trailer_url}
              onChange={(e) => setFormData({ ...formData, trailer_url: e.target.value })}
              className="glass-input"
              placeholder="https://youtube.com/..."
            />
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

          {/* Auto-approve toggle */}
          <div className="glass-form-group">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.auto_approve}
                onChange={(e) => setFormData({ ...formData, auto_approve: e.target.checked })}
                className="glass-checkbox"
              />
              <span className="text-white">Auto-approve this game (publish immediately)</span>
            </label>
          </div>

          <div className="flex gap-4 pt-4 border-t border-white/10">
            <button
              type="submit"
              disabled={saving}
              className="glass-btn glass-btn-success"
            >
              {saving ? 'Publishing...' : 'Publish Game'}
            </button>
            <Link to="/admin/games" className="glass-btn">
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
