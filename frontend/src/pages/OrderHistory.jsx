import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const API_URL = 'http://localhost:8000';

export default function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchOrders();
  }, [user, navigate]);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API_URL}/orders/`);
      setOrders(response.data);
    } catch (err) {
      console.error('Failed to fetch orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!user) {
    return null;
  }

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
            <h1 className="text-3xl font-bold text-white mb-1">Purchase History</h1>
            <p className="text-white/50">{orders.length} orders</p>
          </div>
          <Link to="/library" className="glass-btn">
            Go to Library
          </Link>
        </div>
      </div>

      {orders.length === 0 ? (
        <div className="glass-card text-center py-12">
          <div className="text-6xl mb-4">🛒</div>
          <p className="text-white/50 text-lg mb-6">No purchases yet</p>
          <Link to="/" className="glass-btn glass-btn-primary">
            Browse Games
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div key={order.id} className="glass-card">
              {/* Order Header */}
              <div className="flex flex-col sm:flex-row justify-between items-start gap-4 mb-6 pb-4 border-b border-white/10">
                <div>
                  <p className="text-white/50 text-sm">Order #{order.id}</p>
                  <p className="text-white/70 text-sm">{formatDate(order.order_date)}</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-400">
                    ${order.total_amount.toFixed(2)}
                  </p>
                  <span className="glass-badge glass-badge-success">
                    {order.payment_status}
                  </span>
                </div>
              </div>

              {/* Order Items */}
              <div className="space-y-3">
                {order.items.map(item => (
                  <div key={item.id} className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 p-3 rounded-lg bg-white/5">
                    <div className="flex items-center gap-3">
                      {item.game?.cover_image_url ? (
                        <img
                          src={item.game.cover_image_url}
                          alt={item.game?.title}
                          className="w-14 h-14 object-cover rounded-lg"
                        />
                      ) : (
                        <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-600 flex items-center justify-center">
                          <span className="text-2xl">🎮</span>
                        </div>
                      )}
                      <div>
                        {item.game ? (
                          <Link
                            to={`/game/${item.game.id}`}
                            className="font-medium text-cyan-400 hover:text-cyan-300 transition-colors"
                          >
                            {item.game.title}
                          </Link>
                        ) : (
                          <span className="font-medium text-white">Game #{item.game_id}</span>
                        )}
                        {item.discount_applied > 0 && (
                          <p className="text-xs text-green-400">
                            -{item.discount_applied}% discount applied
                          </p>
                        )}
                      </div>
                    </div>
                    <span className="font-semibold text-white">
                      ${item.purchase_price.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
