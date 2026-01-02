import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { SkeletonCartItem, SkeletonText, Skeleton } from '../components/Skeleton';

export default function Cart() {
  const { cart, loading, removeFromCart, clearCart, checkout } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [error, setError] = useState('');
  const [showConfirm, setShowConfirm] = useState(false);

  if (!user) {
    return (
      <div className="glass-container">
        <div className="glass-card text-center py-12">
          <div className="text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold text-white mb-4">Your Cart</h2>
          <p className="text-white/50 mb-6">Please log in to view your cart</p>
          <Link to="/login" className="glass-btn glass-btn-primary">
            Log In
          </Link>
        </div>
      </div>
    );
  }

  const handleRemove = async (gameId) => {
    const result = await removeFromCart(gameId);
    if (!result.success) {
      setError(result.error);
    }
  };

  const handleClearCart = async () => {
    await clearCart();
  };

  const handleCheckout = async () => {
    setCheckoutLoading(true);
    setError('');

    const result = await checkout();

    if (result.success) {
      setShowConfirm(false);
      navigate('/orders', { state: { orderSuccess: true } });
    } else {
      setError(result.error);
    }

    setCheckoutLoading(false);
  };

  const calculateFinalPrice = (price, discount) => {
    return price * (1 - discount / 100);
  };

  if (loading && cart.items.length === 0) {
    return (
      <div className="glass-container">
        {/* Header Skeleton */}
        <div className="glass-card mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <SkeletonText width="200px" height="2rem" className="mb-2" />
              <SkeletonText width="120px" height="1rem" />
            </div>
          </div>
        </div>

        {/* Cart Items Skeleton */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <SkeletonCartItem />
            <SkeletonCartItem />
            <SkeletonCartItem />
          </div>

          {/* Order Summary Skeleton */}
          <div className="lg:col-span-1">
            <div className="glass-card">
              <SkeletonText width="150px" height="1.5rem" className="mb-6" />
              <div className="space-y-4 mb-6">
                <div className="flex justify-between">
                  <SkeletonText width="100px" height="1rem" />
                  <SkeletonText width="60px" height="1rem" />
                </div>
                <div className="border-t border-white/10 pt-4">
                  <div className="flex justify-between">
                    <SkeletonText width="60px" height="1.5rem" />
                    <SkeletonText width="80px" height="1.5rem" />
                  </div>
                </div>
              </div>
              <Skeleton height="48px" />
            </div>
          </div>
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
            <h1 className="text-3xl font-bold text-white mb-1">🛒 Shopping Cart</h1>
            <p className="text-white/50">
              {cart.total_items} {cart.total_items === 1 ? 'item' : 'items'} in your cart
            </p>
          </div>
          {cart.items.length > 0 && (
            <button
              onClick={handleClearCart}
              className="glass-btn glass-btn-sm"
            >
              Clear Cart
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="glass-alert glass-alert-error mb-6">
          <span>⚠️</span> {error}
        </div>
      )}

      {cart.items.length === 0 ? (
        <div className="glass-card text-center py-12">
          <div className="text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold text-white mb-2">Your cart is empty</h2>
          <p className="text-white/50 mb-6">Browse our games and add some to your cart!</p>
          <Link to="/" className="glass-btn glass-btn-primary">
            Browse Games
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cart.items.map(item => (
              <div key={item.id} className="glass-card glass-card-hover">
                <div className="flex gap-4">
                  {/* Game Image */}
                  <Link to={`/game/${item.game_id}`}>
                    {item.game_cover_image_url ? (
                      <img
                        src={item.game_cover_image_url}
                        alt={item.game_title}
                        className="w-24 h-24 md:w-32 md:h-32 rounded-lg object-cover"
                      />
                    ) : (
                      <div className="w-24 h-24 md:w-32 md:h-32 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-600 flex items-center justify-center">
                        <span className="text-4xl">🎮</span>
                      </div>
                    )}
                  </Link>

                  {/* Game Info */}
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <Link
                        to={`/game/${item.game_id}`}
                        className="font-semibold text-lg text-white hover:text-purple-400 transition-colors"
                      >
                        {item.game_title}
                      </Link>
                      <p className="text-white/40 text-sm mt-1">
                        Added {new Date(item.added_at).toLocaleDateString()}
                      </p>
                    </div>

                    <div className="flex items-center justify-between mt-4">
                      <div className="flex items-center gap-2">
                        {item.game_discount_percent > 0 && (
                          <>
                            <span className="glass-badge glass-badge-success">
                              -{item.game_discount_percent}%
                            </span>
                            <span className="text-white/40 line-through text-sm">
                              ${item.game_price.toFixed(2)}
                            </span>
                          </>
                        )}
                        <span className="text-green-400 font-bold text-lg">
                          ${calculateFinalPrice(item.game_price, item.game_discount_percent).toFixed(2)}
                        </span>
                      </div>

                      <button
                        onClick={() => handleRemove(item.game_id)}
                        className="glass-btn glass-btn-sm glass-btn-danger"
                        disabled={loading}
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="glass-card sticky top-24">
              <h2 className="text-xl font-bold text-white mb-6">Order Summary</h2>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-white/60">
                  <span>Subtotal ({cart.total_items} items)</span>
                  <span>${cart.subtotal.toFixed(2)}</span>
                </div>

                {cart.total_discount > 0 && (
                  <div className="flex justify-between text-green-400">
                    <span>Discount</span>
                    <span>-${cart.total_discount.toFixed(2)}</span>
                  </div>
                )}

                <div className="border-t border-white/10 pt-4">
                  <div className="flex justify-between text-white text-xl font-bold">
                    <span>Total</span>
                    <span className="text-green-400">${cart.total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setShowConfirm(true)}
                className="glass-btn glass-btn-primary w-full py-3 text-lg"
                disabled={loading || cart.items.length === 0}
              >
                Proceed to Checkout
              </button>

              <p className="text-white/40 text-xs text-center mt-4">
                By purchasing, you agree to our Terms of Service
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Checkout Confirmation Modal */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="glass-modal max-w-md w-full">
            <h3 className="text-2xl font-bold text-white mb-4">Confirm Purchase</h3>

            <div className="mb-6">
              <p className="text-white/60 mb-4">
                You are about to purchase {cart.total_items} game{cart.total_items > 1 ? 's' : ''}:
              </p>
              <ul className="space-y-2 mb-4">
                {cart.items.map(item => (
                  <li key={item.id} className="flex justify-between text-white">
                    <span>{item.game_title}</span>
                    <span className="text-green-400">
                      ${calculateFinalPrice(item.game_price, item.game_discount_percent).toFixed(2)}
                    </span>
                  </li>
                ))}
              </ul>
              <div className="border-t border-white/10 pt-4 flex justify-between text-xl font-bold">
                <span className="text-white">Total</span>
                <span className="text-green-400">${cart.total.toFixed(2)}</span>
              </div>
            </div>

            {error && (
              <div className="glass-alert glass-alert-error mb-4">
                <span>⚠️</span> {error}
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={handleCheckout}
                disabled={checkoutLoading}
                className="glass-btn glass-btn-success flex-1"
              >
                {checkoutLoading ? 'Processing...' : 'Confirm Purchase'}
              </button>
              <button
                onClick={() => setShowConfirm(false)}
                className="glass-btn flex-1"
                disabled={checkoutLoading}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
