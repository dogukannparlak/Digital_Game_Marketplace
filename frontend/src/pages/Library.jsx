import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { SkeletonLibraryGame, SkeletonText } from '../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function Library() {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchLibrary();
  }, [user, navigate]);

  const fetchLibrary = async () => {
    try {
      const response = await axios.get(`${API_URL}/orders/library`);
      setGames(response.data);
    } catch (err) {
      console.error('Failed to fetch library:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return null;
  }

  if (loading) {
    return (
      <div className="glass-container">
        {/* Header Skeleton */}
        <div className="glass-card mb-6">
          <SkeletonText width="180px" height="2rem" className="mb-2" />
          <SkeletonText width="100px" height="1rem" />
        </div>

        {/* Library Games Skeleton */}
        <div className="space-y-4">
          <SkeletonLibraryGame />
          <SkeletonLibraryGame />
          <SkeletonLibraryGame />
          <SkeletonLibraryGame />
          <SkeletonLibraryGame />
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
            <h1 className="text-3xl font-bold text-white mb-1">My Library</h1>
            <p className="text-white/50">{games.length} games in your collection</p>
          </div>
          <Link to="/orders" className="glass-btn">
            View Purchase History
          </Link>
        </div>
      </div>

      {games.length === 0 ? (
        <div className="glass-card text-center py-12">
          <div className="text-6xl mb-4">📚</div>
          <p className="text-white/50 text-lg mb-6">Your library is empty</p>
          <Link to="/" className="glass-btn glass-btn-primary">
            Browse Games
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {games.map(game => (
            <Link
              key={game.id}
              to={`/game/${game.id}`}
              className="glass-game-card"
            >
              {game.cover_image_url ? (
                <img
                  src={game.cover_image_url}
                  alt={game.title}
                  className="glass-game-image"
                  loading="lazy"
                />
              ) : (
                <div className="glass-game-placeholder">
                  <span className="text-white text-4xl">🎮</span>
                </div>
              )}
              <div className="glass-game-content">
                <h3 className="glass-game-title">{game.title}</h3>
                <div className="flex items-center gap-2 mt-2">
                  <span className="glass-badge glass-badge-success">Owned</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
