import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function DeveloperRegister() {
  const [developerName, setDeveloperName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { user, isDeveloper, becomeDeveloper } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
    } else if (isDeveloper()) {
      navigate('/developer');
    }
  }, [user, isDeveloper, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (developerName.trim().length < 2) {
      setError('Developer name must be at least 2 characters');
      return;
    }

    setLoading(true);
    const result = await becomeDeveloper(developerName.trim());
    setLoading(false);

    if (result.success) {
      navigate('/developer');
    } else {
      setError(result.error);
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="glass-container min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="glass-card glass-card-lg">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4">🚀</div>
            <h1 className="text-2xl font-bold text-white mb-2">Become a Developer</h1>
            <p className="text-white/50">Start publishing your games on our platform</p>
          </div>

          {error && (
            <div className="glass-alert glass-alert-error mb-6">
              <span>⚠️</span> {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="glass-form-group">
              <label htmlFor="developerName" className="glass-label">Developer / Studio Name</label>
              <input
                id="developerName"
                type="text"
                value={developerName}
                onChange={(e) => setDeveloperName(e.target.value)}
                className="glass-input"
                placeholder="Enter your developer name"
                required
                disabled={loading}
              />
              <p className="text-white/40 text-sm mt-1">
                This will be displayed on all your published games
              </p>
            </div>

            {/* Benefits */}
            <div className="glass-card glass-card-sm" style={{ background: 'rgba(139, 92, 246, 0.1)', borderColor: 'rgba(139, 92, 246, 0.2)' }}>
              <h3 className="font-semibold text-purple-300 mb-3">As a Developer you can:</h3>
              <ul className="space-y-2 text-sm text-white/70">
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Publish games to the marketplace
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Track your sales and revenue
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Manage your game listings
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-400">✓</span> Respond to user reviews
                </li>
              </ul>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="glass-btn w-full glass-btn-lg"
              style={{ background: 'linear-gradient(135deg, #8b5cf6, #6d28d9)', borderColor: '#8b5cf6' }}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Processing...
                </span>
              ) : (
                'Become a Developer'
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-white/50">
            <Link to="/" className="text-cyan-400 hover:text-cyan-300 transition-colors">
              ← Back to Home
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
