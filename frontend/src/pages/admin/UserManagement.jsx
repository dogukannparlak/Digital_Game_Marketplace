import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { SkeletonText, Skeleton, SkeletonBadge, SkeletonButton } from '../../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [search, setSearch] = useState('');
  const { isAdmin } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAdmin()) {
      navigate('/');
      return;
    }
    fetchUsers();
  }, [isAdmin, navigate, filter]);

  const fetchUsers = async () => {
    try {
      let url = `${API_URL}/admin/users?limit=100`;
      if (filter) url += `&role=${filter}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;

      const response = await axios.get(url);
      setUsers(response.data);
    } catch (err) {
      console.error('Failed to fetch users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchUsers();
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await axios.put(`${API_URL}/admin/users/${userId}/role`, { role: newRole });
      setUsers(users.map(u => u.id === userId ? { ...u, role: newRole } : u));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to change role');
    }
  };

  const handleBan = async (userId) => {
    const reason = prompt('Enter ban reason:');
    if (!reason) return;

    try {
      await axios.put(`${API_URL}/admin/users/${userId}/ban`, { reason });
      setUsers(users.map(u => u.id === userId ? { ...u, is_banned: true, banned_reason: reason } : u));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to ban user');
    }
  };

  const handleUnban = async (userId) => {
    try {
      await axios.put(`${API_URL}/admin/users/${userId}/unban`);
      setUsers(users.map(u => u.id === userId ? { ...u, is_banned: false, banned_reason: null } : u));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to unban user');
    }
  };

  const handleVerifyDeveloper = async (userId) => {
    try {
      await axios.put(`${API_URL}/admin/users/${userId}/verify-developer`);
      setUsers(users.map(u => u.id === userId ? { ...u, developer_verified: true } : u));
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to verify developer');
    }
  };

  const getRoleBadgeClass = (role) => {
    switch (role) {
      case 'admin': return 'glass-badge-admin';
      case 'developer': return 'glass-badge-developer';
      default: return 'glass-badge-user';
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
            <SkeletonButton width="150px" height="40px" />
          </div>
        </div>

        {/* Filters Skeleton */}
        <div className="glass-card mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <Skeleton height="44px" className="flex-1" />
            <Skeleton width="150px" height="44px" />
          </div>
        </div>

        {/* Users Table Skeleton */}
        <div className="glass-card overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-4 px-4"><SkeletonText width="60px" height="1rem" /></th>
                <th className="text-left py-4 px-4"><SkeletonText width="80px" height="1rem" /></th>
                <th className="text-left py-4 px-4"><SkeletonText width="100px" height="1rem" /></th>
                <th className="text-left py-4 px-4"><SkeletonText width="50px" height="1rem" /></th>
                <th className="text-left py-4 px-4"><SkeletonText width="60px" height="1rem" /></th>
                <th className="text-left py-4 px-4"><SkeletonText width="80px" height="1rem" /></th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3, 4, 5].map(i => (
                <tr key={i} className="border-b border-white/5">
                  <td className="py-4 px-4"><SkeletonText width="30px" height="1rem" /></td>
                  <td className="py-4 px-4"><SkeletonText width="100px" height="1rem" /></td>
                  <td className="py-4 px-4"><SkeletonText width="150px" height="1rem" /></td>
                  <td className="py-4 px-4"><SkeletonBadge width="60px" /></td>
                  <td className="py-4 px-4"><SkeletonBadge width="50px" /></td>
                  <td className="py-4 px-4">
                    <div className="flex gap-2">
                      <SkeletonButton width="60px" height="28px" />
                      <SkeletonButton width="50px" height="28px" />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
            <h1 className="text-3xl font-bold text-white mb-1">User Management</h1>
            <p className="text-white/50">{users.length} users</p>
          </div>
          <Link to="/admin" className="glass-btn">
            ← Back to Dashboard
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card mb-6">
        <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="glass-input glass-select md:w-48"
          >
            <option value="">All Roles</option>
            <option value="user">Users</option>
            <option value="developer">Developers</option>
            <option value="admin">Admins</option>
          </select>
          <input
            type="text"
            placeholder="Search by username or email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="glass-input flex-1"
          />
          <button type="submit" className="glass-btn glass-btn-primary">
            Search
          </button>
        </form>
      </div>

      {/* Users List */}
      <div className="glass-card">
        {/* Desktop Table */}
        <div className="hidden lg:block glass-table-container">
          <table className="glass-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id} style={user.is_banned ? { background: 'rgba(239, 68, 68, 0.1)' } : {}}>
                  <td>
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full glass-avatar-placeholder flex items-center justify-center text-sm">
                        {user.username.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <div className="font-medium text-white">{user.username}</div>
                        {user.developer_name && (
                          <div className="text-sm text-white/50">
                            {user.developer_name}
                            {user.developer_verified && <span className="text-cyan-400 ml-1">✓</span>}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="text-white/70">{user.email}</td>
                  <td>
                    <span className={`glass-badge ${getRoleBadgeClass(user.role)}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>
                    {user.is_banned ? (
                      <span className="glass-badge glass-badge-error">Banned</span>
                    ) : (
                      <span className="glass-badge glass-badge-success">Active</span>
                    )}
                  </td>
                  <td>
                    <div className="flex gap-2 flex-wrap">
                      <select
                        value={user.role}
                        onChange={(e) => handleRoleChange(user.id, e.target.value)}
                        className="glass-input glass-select text-sm py-1 px-2"
                        style={{ width: 'auto' }}
                      >
                        <option value="user">User</option>
                        <option value="developer">Developer</option>
                        <option value="admin">Admin</option>
                      </select>

                      {user.is_banned ? (
                        <button
                          onClick={() => handleUnban(user.id)}
                          className="glass-btn glass-btn-sm glass-btn-success"
                        >
                          Unban
                        </button>
                      ) : (
                        <button
                          onClick={() => handleBan(user.id)}
                          className="glass-btn glass-btn-sm glass-btn-danger"
                        >
                          Ban
                        </button>
                      )}

                      {user.role === 'developer' && !user.developer_verified && (
                        <button
                          onClick={() => handleVerifyDeveloper(user.id)}
                          className="glass-btn glass-btn-sm glass-btn-accent"
                        >
                          Verify
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Cards */}
        <div className="lg:hidden space-y-4">
          {users.map(user => (
            <div
              key={user.id}
              className="glass-card glass-card-sm"
              style={user.is_banned ? { background: 'rgba(239, 68, 68, 0.1)' } : {}}
            >
              <div className="flex items-start gap-3 mb-4">
                <div className="w-12 h-12 rounded-full glass-avatar-placeholder flex items-center justify-center">
                  {user.username.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-white">{user.username}</div>
                  <div className="text-sm text-white/50">{user.email}</div>
                  {user.developer_name && (
                    <div className="text-sm text-purple-400">
                      {user.developer_name}
                      {user.developer_verified && <span className="text-cyan-400 ml-1">✓</span>}
                    </div>
                  )}
                </div>
                <div className="flex flex-col gap-1">
                  <span className={`glass-badge ${getRoleBadgeClass(user.role)}`}>
                    {user.role}
                  </span>
                  {user.is_banned ? (
                    <span className="glass-badge glass-badge-error">Banned</span>
                  ) : (
                    <span className="glass-badge glass-badge-success">Active</span>
                  )}
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                <select
                  value={user.role}
                  onChange={(e) => handleRoleChange(user.id, e.target.value)}
                  className="glass-input glass-select text-sm py-1 px-2"
                  style={{ width: 'auto' }}
                >
                  <option value="user">User</option>
                  <option value="developer">Developer</option>
                  <option value="admin">Admin</option>
                </select>

                {user.is_banned ? (
                  <button onClick={() => handleUnban(user.id)} className="glass-btn glass-btn-sm glass-btn-success">
                    Unban
                  </button>
                ) : (
                  <button onClick={() => handleBan(user.id)} className="glass-btn glass-btn-sm glass-btn-danger">
                    Ban
                  </button>
                )}

                {user.role === 'developer' && !user.developer_verified && (
                  <button onClick={() => handleVerifyDeveloper(user.id)} className="glass-btn glass-btn-sm glass-btn-accent">
                    Verify
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        {users.length === 0 && (
          <div className="text-center py-12">
            <div className="text-5xl mb-4">👥</div>
            <p className="text-white/50">No users found</p>
          </div>
        )}
      </div>
    </div>
  );
}
