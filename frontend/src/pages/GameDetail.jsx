import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { SkeletonGameDetail } from '../components/Skeleton';

const API_URL = 'http://localhost:8000';

export default function GameDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { addToCart, isInCart } = useCart();

  const [game, setGame] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [owned, setOwned] = useState(false);
  const [purchasing, setPurchasing] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPurchaseModal, setShowPurchaseModal] = useState(false);

  useEffect(() => {
    fetchGame();
    if (user) {
      checkOwnership();
    }
  }, [id, user]);

  const fetchGame = async () => {
    try {
      const [gameRes, reviewsRes] = await Promise.all([
        axios.get(`${API_URL}/games/${id}`),
        axios.get(`${API_URL}/games/${id}/reviews`)
      ]);
      setGame(gameRes.data);
      setReviews(reviewsRes.data);
    } catch (err) {
      console.error('Failed to fetch game:', err);
      setError('Game not found');
    } finally {
      setLoading(false);
    }
  };

  const checkOwnership = async () => {
    try {
      const response = await axios.get(`${API_URL}/orders/owned-games`);
      setOwned(response.data.includes(parseInt(id)));
    } catch (err) {
      console.error('Failed to check ownership:', err);
    }
  };

  const handlePurchase = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (owned) return;

    setPurchasing(true);
    try {
      await axios.post(`${API_URL}/orders/`, { game_ids: [parseInt(id)] });
      setOwned(true);
      setShowPurchaseModal(false);
    } catch (err) {
      alert(err.response?.data?.detail || 'Purchase failed');
    } finally {
      setPurchasing(false);
    }
  };

  const getDiscountedPrice = () => {
    if (game.discount_percent > 0) {
      return game.price * (1 - game.discount_percent / 100);
    }
    return game.price;
  };

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    setAddingToCart(true);
    setError('');
    setSuccess('');

    const result = await addToCart(parseInt(id));

    if (result.success) {
      setSuccess('Added to cart!');
      setTimeout(() => setSuccess(''), 3000);
    } else {
      setError(result.error);
      setTimeout(() => setError(''), 3000);
    }

    setAddingToCart(false);
  };

  const inCart = isInCart(parseInt(id));

  if (loading) {
    return <SkeletonGameDetail />;
  }

  if (error) {
    return (
      <div className="glass-container text-center py-12">
        <div className="glass-card inline-block">
          <div className="text-5xl mb-4">😢</div>
          <p className="text-red-400 text-xl mb-4">{error}</p>
          <Link to="/" className="glass-btn glass-btn-primary">
            Back to Store
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-container">
      {/* Back Button */}
      <Link to="/" className="glass-btn glass-btn-sm mb-6 inline-flex items-center gap-2">
        <span>←</span> Back to Store
      </Link>

      <div className="glass-card glass-card-lg">
        {/* Hero Section */}
        <div className="relative -mx-8 -mt-8 mb-8 rounded-t-lg overflow-hidden">
          {game.cover_image_url ? (
            <img
              src={game.cover_image_url}
              alt={game.title}
              className="w-full h-64 md:h-96 object-cover"
            />
          ) : (
            <div className="w-full h-64 md:h-96 bg-gradient-to-br from-purple-600 via-indigo-600 to-cyan-600 flex items-center justify-center">
              <span className="text-white text-8xl">🎮</span>
            </div>
          )}

          {/* Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />

          {/* Discount Badge */}
          {game.discount_percent > 0 && (
            <div className="absolute top-4 right-4 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-lg text-xl font-bold shadow-lg">
              -{game.discount_percent}%
            </div>
          )}

          {/* Title Overlay */}
          <div className="absolute bottom-0 left-0 right-0 p-6 md:p-8">
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">{game.title}</h1>
            <p className="text-white/70">
              by <span className="text-cyan-400">{game.developer?.developer_name || game.developer?.username}</span>
              {game.developer?.developer_verified && (
                <span className="ml-2 text-cyan-400">✓ Verified</span>
              )}
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Content */}
          <div className="flex-1">
            {/* Genres */}
            {game.genres?.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {game.genres.map(genre => (
                  <span key={genre.id} className="glass-badge glass-badge-user">
                    {genre.name}
                  </span>
                ))}
              </div>
            )}

            {/* Short Description */}
            {game.short_description && (
              <p className="text-white/80 text-lg mb-6 leading-relaxed">{game.short_description}</p>
            )}

            {/* Full Description */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-white mb-4">About This Game</h2>
              <div className="text-white/60 whitespace-pre-line leading-relaxed">
                {game.description}
              </div>
            </div>

            {/* Reviews Section */}
            <div className="pt-8 border-t border-white/10">
              <h2 className="text-xl font-semibold text-white mb-6">
                Reviews <span className="text-white/40">({reviews.length})</span>
              </h2>

              {reviews.length === 0 ? (
                <div className="glass-card glass-card-sm text-center py-8">
                  <p className="text-white/40">No reviews yet. Be the first to review!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {reviews.map(review => (
                    <div key={review.id} className="glass-card glass-card-sm">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full glass-avatar-placeholder flex items-center justify-center text-sm">
                            {review.user?.username?.charAt(0).toUpperCase()}
                          </div>
                          <span className="font-medium text-white">{review.user?.username}</span>
                        </div>
                        <div className="text-yellow-400">
                          {'★'.repeat(review.rating)}
                          <span className="text-white/20">{'★'.repeat(5 - review.rating)}</span>
                        </div>
                      </div>
                      <p className="text-white/70">{review.content}</p>
                      <p className="text-white/30 text-sm mt-3">
                        {new Date(review.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Purchase Sidebar */}
          <div className="lg:w-80">
            <div className="glass-card sticky top-24">
              {/* Price */}
              <div className="mb-6">
                {game.price === 0 ? (
                  <p className="text-3xl font-bold text-green-400">Free to Play</p>
                ) : (
                  <div className="flex items-center gap-3 flex-wrap">
                    {game.discount_percent > 0 && (
                      <span className="text-xl text-white/40 line-through">
                        ${game.price.toFixed(2)}
                      </span>
                    )}
                    <span className="text-3xl font-bold text-white">
                      ${getDiscountedPrice().toFixed(2)}
                    </span>
                    {game.discount_percent > 0 && (
                      <span className="glass-badge glass-badge-success">
                        Save ${(game.price - getDiscountedPrice()).toFixed(2)}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Success/Error Messages */}
              {success && (
                <div className="glass-alert glass-alert-success mb-4">
                  <span>✓</span> {success}
                </div>
              )}
              {error && (
                <div className="glass-alert glass-alert-error mb-4">
                  <span>⚠️</span> {error}
                </div>
              )}

              {/* Buy Button */}
              {owned ? (
                <>
                  <div className="glass-alert glass-alert-success mb-4">
                    <span>✓</span> In Your Library
                  </div>
                  <Link to="/library" className="glass-btn w-full text-center">
                    Go to Library
                  </Link>
                </>
              ) : inCart ? (
                <>
                  <div className="glass-alert glass-alert-info mb-4">
                    <span>🛒</span> In Your Cart
                  </div>
                  <Link to="/cart" className="glass-btn glass-btn-primary w-full text-center">
                    View Cart
                  </Link>
                </>
              ) : (
                <div className="space-y-3">
                  <button
                    onClick={handleAddToCart}
                    disabled={addingToCart}
                    className="glass-btn glass-btn-primary w-full"
                  >
                    {addingToCart ? 'Adding...' : '🛒 Add to Cart'}
                  </button>
                  <button
                    onClick={() => user ? setShowPurchaseModal(true) : navigate('/login')}
                    className="glass-btn glass-btn-success w-full glass-btn-lg"
                  >
                    {game.price === 0 ? 'Get Now' : 'Buy Now'}
                  </button>
                </div>
              )}

              {!user && !owned && !inCart && (
                <p className="text-white/40 text-sm text-center mt-4">
                  <Link to="/login" className="text-cyan-400 hover:text-cyan-300">Sign in</Link> to purchase
                </p>
              )}

              {/* Game Stats */}
              <div className="mt-6 pt-6 border-t border-white/10 space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-white/50">Release Date</span>
                  <span className="text-white/80">
                    {new Date(game.release_date).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/50">Developer</span>
                  <span className="text-white/80">
                    {game.developer?.developer_name || game.developer?.username}
                  </span>
                </div>
                {game.total_sales > 0 && (
                  <div className="flex justify-between">
                    <span className="text-white/50">Sales</span>
                    <span className="text-white/80">{game.total_sales.toLocaleString()}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Purchase Modal */}
      {showPurchaseModal && (
        <div className="glass-modal-overlay" onClick={() => setShowPurchaseModal(false)}>
          <div className="glass-modal" onClick={e => e.stopPropagation()}>
            <div className="glass-modal-header">
              <h3 className="glass-modal-title">Confirm Purchase</h3>
              <button onClick={() => setShowPurchaseModal(false)} className="glass-modal-close">
                ✕
              </button>
            </div>
            <div className="glass-modal-body">
              <div className="flex items-center gap-4 mb-6">
                {game.cover_image_url ? (
                  <img src={game.cover_image_url} alt={game.title} className="w-20 h-20 rounded-lg object-cover" />
                ) : (
                  <div className="w-20 h-20 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-600 flex items-center justify-center">
                    <span className="text-3xl">🎮</span>
                  </div>
                )}
                <div>
                  <h4 className="text-white font-semibold">{game.title}</h4>
                  <p className="text-white/50 text-sm">{game.developer?.developer_name || game.developer?.username}</p>
                </div>
              </div>
              <div className="flex justify-between items-center py-4 border-t border-b border-white/10">
                <span className="text-white/70">Total</span>
                <span className="text-2xl font-bold text-white">${getDiscountedPrice().toFixed(2)}</span>
              </div>
            </div>
            <div className="glass-modal-footer">
              <button onClick={() => setShowPurchaseModal(false)} className="glass-btn">
                Cancel
              </button>
              <button
                onClick={handlePurchase}
                disabled={purchasing}
                className="glass-btn glass-btn-success"
              >
                {purchasing ? 'Processing...' : 'Confirm Purchase'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
