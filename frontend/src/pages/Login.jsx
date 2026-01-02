import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error || 'Login failed');
    }
    setLoading(false);
  };

  return (
    <div className="glass-container min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="glass-card glass-card-lg">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4">🎮</div>
            <h1 className="text-2xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-white/50">Sign in to your GameStore account</p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="glass-alert glass-alert-error mb-6">
              <span>⚠️</span>
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="glass-form-group">
              <label htmlFor="username" className="glass-label">Username</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
                className="glass-input"
                autoComplete="username"
              />
            </div>

            <div className="glass-form-group">
              <label htmlFor="password" className="glass-label">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                className="glass-input"
                autoComplete="current-password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="glass-btn glass-btn-primary w-full glass-btn-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-white/50">
              Don&apos;t have an account?{' '}
              <Link to="/register" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                Create one
              </Link>
            </p>
          </div>

          {/* Demo Accounts */}
          <div className="mt-6 pt-6 border-t border-white/10">
            <p className="text-white/40 text-sm text-center mb-3">Demo Accounts</p>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <button
                type="button"
                onClick={() => { setUsername('admin'); setPassword('admin123'); }}
                className="glass-btn glass-btn-sm"
              >
                Admin
              </button>
              <button
                type="button"
                onClick={() => { setUsername('developer'); setPassword('dev123'); }}
                className="glass-btn glass-btn-sm"
              >
                Developer
              </button>
              <button
                type="button"
                onClick={() => { setUsername('user'); setPassword('user123'); }}
                className="glass-btn glass-btn-sm"
              >
                User
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
