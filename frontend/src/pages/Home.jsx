import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { SkeletonHomePage } from '../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function Home() {
  const [games, setGames] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    const debounce = setTimeout(() => {
      fetchGames();
    }, 300);
    return () => clearTimeout(debounce);
  }, [selectedGenre, search]);

  const fetchInitialData = async () => {
    try {
      const [gamesRes, genresRes] = await Promise.all([
        axios.get(`${API_URL}/games/`),
        axios.get(`${API_URL}/genres/`)
      ]);
      setGames(gamesRes.data);
      setGenres(genresRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchGames = async () => {
    try {
      let url = `${API_URL}/games/?limit=100`;
      if (selectedGenre) url += `&genre_id=${selectedGenre}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;

      const response = await axios.get(url);
      setGames(response.data);
    } catch (error) {
      console.error('Error fetching games:', error);
    }
  };

  const getDiscountedPrice = (game) => {
    if (game.discount_percent > 0) {
      return game.price * (1 - game.discount_percent / 100);
    }
    return game.price;
  };

  if (loading) {
    return <SkeletonHomePage />;
  }

  return (
    <div className="glass-container">
      {/* Hero Section */}
      <div className="glass-card glass-card-lg mb-8 text-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 via-transparent to-cyan-600/20" />
        <div className="relative z-10">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="glass-text-gradient">Game Store</span>
          </h1>
          <p className="text-white/60 text-lg max-w-2xl mx-auto">
            Discover and purchase amazing games from indie developers and major studios
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search games..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="glass-input w-full"
            />
          </div>
          <select
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
            className="glass-input glass-select md:w-48"
          >
            <option value="">All Genres</option>
            {genres.map(genre => (
              <option key={genre.id} value={genre.id}>{genre.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Games Grid */}
      {games.length === 0 ? (
        <div className="glass-card text-center py-12">
          <div className="text-5xl mb-4">🎮</div>
          <p className="text-white/50 text-lg mb-4">No games found</p>
          {(search || selectedGenre) && (
            <button
              onClick={() => { setSearch(''); setSelectedGenre(''); }}
              className="glass-btn glass-btn-primary"
            >
              Clear filters
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
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
                  <span className="text-white text-5xl">🎮</span>
                </div>
              )}

              <div className="glass-game-content">
                <h3 className="glass-game-title">{game.title}</h3>
                <p className="glass-game-developer">
                  {game.developer?.developer_name || game.developer?.username}
                </p>

                {/* Genres */}
                {game.genres?.length > 0 && (
                  <div className="glass-game-genres">
                    {game.genres.slice(0, 2).map(genre => (
                      <span key={genre.id} className="glass-genre-tag">
                        {genre.name}
                      </span>
                    ))}
                  </div>
                )}

                {/* Price */}
                <div className="glass-game-price">
                  {game.discount_percent > 0 && (
                    <span className="glass-price-discount">
                      -{game.discount_percent}%
                    </span>
                  )}
                  {game.price === 0 ? (
                    <span className="glass-price-free">Free to Play</span>
                  ) : game.discount_percent > 0 ? (
                    <>
                      <span className="glass-price-original">${game.price.toFixed(2)}</span>
                      <span className="glass-price-current">${getDiscountedPrice(game).toFixed(2)}</span>
                    </>
                  ) : (
                    <span className="glass-price-current" style={{ color: 'var(--text-primary)' }}>
                      ${game.price.toFixed(2)}
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Stats */}
      <div className="mt-8 text-center text-white/40 text-sm">
        Showing {games.length} games
      </div>
    </div>
  );
}
