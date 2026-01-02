import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function Profile() {
  const { user, updateProfile, refreshUser } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');

  // Edit form state
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    display_name: '',
    bio: '',
    avatar_url: ''
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // Password change state
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [passwordLoading, setPasswordLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        display_name: user.display_name || '',
        bio: user.bio || '',
        avatar_url: user.avatar_url || ''
      });
      fetchStats();
    }
  }, [user]);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/me/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    const result = await updateProfile(formData);

    if (result.success) {
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
      setEditMode(false);
    } else {
      setMessage({ type: 'error', text: result.error });
    }
    setSaving(false);
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (passwordData.new_password !== passwordData.confirm_password) {
      setMessage({ type: 'error', text: 'New passwords do not match' });
      return;
    }

    if (passwordData.new_password.length < 6) {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
      return;
    }

    setPasswordLoading(true);

    try {
      await axios.put(`${API_URL}/me/password`, {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      });
      setMessage({ type: 'success', text: 'Password changed successfully!' });
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
    } catch (error) {
      const msg = error.response?.data?.detail || 'Failed to change password';
      setMessage({ type: 'error', text: msg });
    } finally {
      setPasswordLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getRoleBadgeClass = (role) => {
    switch (role) {
      case 'admin': return 'glass-badge-admin';
      case 'developer': return 'glass-badge-developer';
      default: return 'glass-badge-user';
    }
  };

  if (!user) {
    return (
      <div className="glass-container">
        <div className="glass-card text-center py-12">
          <p className="text-white/70">Please log in to view your profile</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="glass-container flex justify-center items-center min-h-[60vh]">
        <div className="glass-spinner"></div>
      </div>
    );
  }

  return (
    <div className="glass-container">
      {/* Profile Header */}
      <div className="glass-card glass-card-hover mb-6">
        <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
          {/* Avatar */}
          <div className="relative">
            {user.avatar_url ? (
              <img
                src={user.avatar_url}
                alt={user.username}
                className="w-32 h-32 rounded-full object-cover glass-avatar"
              />
            ) : (
              <div className="w-32 h-32 rounded-full glass-avatar-placeholder flex items-center justify-center">
                <span className="text-5xl">{user.username.charAt(0).toUpperCase()}</span>
              </div>
            )}
            <span className={`absolute bottom-2 right-2 px-2 py-1 rounded-full text-xs font-medium ${getRoleBadgeClass(user.role)}`}>
              {user.role.toUpperCase()}
            </span>
          </div>

          {/* User Info */}
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-3xl font-bold text-white mb-1">
              {user.display_name || user.username}
            </h1>
            <p className="text-white/60 mb-2">@{user.username}</p>

            {/* Public ID */}
            <div className="glass-id-badge inline-block mb-3">
              <span className="text-xs text-white/50">ID:</span>
              <span className="ml-1 font-mono text-cyan-400">{user.public_id}</span>
            </div>

            {user.bio && (
              <p className="text-white/80 mb-4 max-w-lg">{user.bio}</p>
            )}

            <div className="flex flex-wrap gap-4 justify-center md:justify-start text-sm text-white/60">
              <span>📅 Member since {formatDate(user.registration_date)}</span>
              {user.developer_name && (
                <span className="text-purple-400">🎮 {user.developer_name}</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="glass-stat-card">
            <div className="glass-stat-icon">🎮</div>
            <div className="glass-stat-value">{stats.total_games_owned}</div>
            <div className="glass-stat-label">Games Owned</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">💰</div>
            <div className="glass-stat-value">${stats.total_spent.toFixed(2)}</div>
            <div className="glass-stat-label">Total Spent</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">⭐</div>
            <div className="glass-stat-value">{stats.total_reviews}</div>
            <div className="glass-stat-label">Reviews</div>
          </div>
          <div className="glass-stat-card">
            <div className="glass-stat-icon">📆</div>
            <div className="glass-stat-value">{Math.floor((new Date() - new Date(stats.member_since)) / (1000 * 60 * 60 * 24))}</div>
            <div className="glass-stat-label">Days Active</div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="glass-tabs mb-6">
        <button
          onClick={() => setActiveTab('profile')}
          className={`glass-tab ${activeTab === 'profile' ? 'glass-tab-active' : ''}`}
        >
          Edit Profile
        </button>
        <button
          onClick={() => setActiveTab('security')}
          className={`glass-tab ${activeTab === 'security' ? 'glass-tab-active' : ''}`}
        >
          Security
        </button>
      </div>

      {/* Message */}
      {message.text && (
        <div className={`glass-alert ${message.type === 'success' ? 'glass-alert-success' : 'glass-alert-error'} mb-6`}>
          {message.text}
        </div>
      )}

      {/* Tab Content */}
      {activeTab === 'profile' && (
        <div className="glass-card">
          <h2 className="text-xl font-semibold text-white mb-6">Edit Profile</h2>
          <form onSubmit={handleSaveProfile} className="space-y-6">
            <div className="glass-form-group">
              <label className="glass-label">Display Name</label>
              <input
                type="text"
                value={formData.display_name}
                onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                placeholder="Your display name"
                className="glass-input"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Avatar URL</label>
              <input
                type="url"
                value={formData.avatar_url}
                onChange={(e) => setFormData({ ...formData, avatar_url: e.target.value })}
                placeholder="https://example.com/avatar.jpg"
                className="glass-input"
              />
              {formData.avatar_url && (
                <div className="mt-2">
                  <img
                    src={formData.avatar_url}
                    alt="Avatar preview"
                    className="w-20 h-20 rounded-full object-cover glass-avatar"
                    onError={(e) => e.target.style.display = 'none'}
                  />
                </div>
              )}
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Bio</label>
              <textarea
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                placeholder="Tell us about yourself..."
                rows={4}
                className="glass-input glass-textarea"
              />
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={saving}
                className="glass-btn glass-btn-primary"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      )}

      {activeTab === 'security' && (
        <div className="glass-card">
          <h2 className="text-xl font-semibold text-white mb-6">Change Password</h2>
          <form onSubmit={handlePasswordChange} className="space-y-6 max-w-md">
            <div className="glass-form-group">
              <label className="glass-label">Current Password</label>
              <input
                type="password"
                value={passwordData.current_password}
                onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                required
                className="glass-input"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">New Password</label>
              <input
                type="password"
                value={passwordData.new_password}
                onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                required
                minLength={6}
                className="glass-input"
              />
            </div>

            <div className="glass-form-group">
              <label className="glass-label">Confirm New Password</label>
              <input
                type="password"
                value={passwordData.confirm_password}
                onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                required
                className="glass-input"
              />
            </div>

            <button
              type="submit"
              disabled={passwordLoading}
              className="glass-btn glass-btn-primary"
            >
              {passwordLoading ? 'Changing...' : 'Change Password'}
            </button>
          </form>

          {/* Account Info */}
          <div className="mt-8 pt-6 border-t border-white/10">
            <h3 className="text-lg font-medium text-white mb-4">Account Information</h3>
            <div className="space-y-3 text-white/70">
              <p><span className="text-white/50">Email:</span> {user.email}</p>
              <p><span className="text-white/50">Username:</span> {user.username}</p>
              <p><span className="text-white/50">Account ID:</span> <span className="font-mono text-cyan-400">{user.public_id}</span></p>
              <p><span className="text-white/50">Role:</span> <span className="capitalize">{user.role}</span></p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
