import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const API_URL = 'http://localhost:8000';

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState({
    items: [],
    total_items: 0,
    subtotal: 0,
    total_discount: 0,
    total: 0
  });
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  // Fetch cart when user logs in
  const fetchCart = useCallback(async () => {
    if (!user) {
      setCart({ items: [], total_items: 0, subtotal: 0, total_discount: 0, total: 0 });
      return;
    }

    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/cart/`);
      setCart(response.data);
    } catch (err) {
      console.error('Failed to fetch cart:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const addToCart = async (gameId) => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/cart/add/${gameId}`);
      setCart(response.data);
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.detail || 'Failed to add to cart'
      };
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (gameId) => {
    try {
      setLoading(true);
      const response = await axios.delete(`${API_URL}/cart/remove/${gameId}`);
      setCart(response.data);
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.detail || 'Failed to remove from cart'
      };
    } finally {
      setLoading(false);
    }
  };

  const clearCart = async () => {
    try {
      setLoading(true);
      const response = await axios.delete(`${API_URL}/cart/clear`);
      setCart(response.data);
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.detail || 'Failed to clear cart'
      };
    } finally {
      setLoading(false);
    }
  };

  const checkout = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_URL}/cart/checkout`);
      setCart({ items: [], total_items: 0, subtotal: 0, total_discount: 0, total: 0 });
      return { success: true, order: response.data };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.detail || 'Checkout failed'
      };
    } finally {
      setLoading(false);
    }
  };

  const isInCart = (gameId) => {
    return cart.items.some(item => item.game_id === gameId);
  };

  const value = {
    cart,
    loading,
    addToCart,
    removeFromCart,
    clearCart,
    checkout,
    isInCart,
    fetchCart,
    cartCount: cart.total_items
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}
