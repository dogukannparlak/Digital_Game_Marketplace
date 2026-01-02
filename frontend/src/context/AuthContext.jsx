import { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Helper functions
  const isAdmin = () => user?.role === 'admin';
  const isDeveloper = () => user?.role === 'developer' || user?.role === 'admin';
  const isUser = () => !!user;

  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          // Fetch current user info
          const response = await axios.get(`${API_URL}/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Token validation failed:', error);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, [token]);

  const login = async (username, password) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post(`${API_URL}/token`, formData);
      const { access_token, user_id, username: dbUsername, role, developer_name } = response.data;

      setToken(access_token);
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Set user data from token response
      setUser({
        id: user_id,
        username: dbUsername,
        role: role,
        developer_name: developer_name
      });

      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      let message = 'Login failed';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        // Handle validation error arrays from FastAPI
        if (Array.isArray(detail)) {
          message = detail.map(e => e.msg || e.message || String(e)).join(', ');
        } else if (typeof detail === 'object') {
          message = detail.msg || detail.message || JSON.stringify(detail);
        } else {
          message = String(detail);
        }
      }
      return { success: false, error: message };
    }
  };

  const register = async (username, email, password) => {
    try {
      await axios.post(`${API_URL}/users/`, {
        username,
        email,
        password
      });
      return await login(username, password);
    } catch (error) {
      console.error('Registration failed:', error);
      let message = 'Registration failed';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          message = detail.map(e => e.msg || e.message || String(e)).join(', ');
        } else if (typeof detail === 'object') {
          message = detail.msg || detail.message || JSON.stringify(detail);
        } else {
          message = String(detail);
        }
      }
      return { success: false, error: message };
    }
  };

  const becomeDeveloper = async (developerName) => {
    try {
      const response = await axios.post(`${API_URL}/become-developer`, {
        developer_name: developerName
      });

      setUser({
        ...user,
        role: 'developer',
        developer_name: response.data.developer_name
      });

      return { success: true };
    } catch (error) {
      console.error('Developer application failed:', error);
      const message = error.response?.data?.detail || 'Failed to become developer';
      return { success: false, error: message };
    }
  };

  const updateProfile = async (updates) => {
    try {
      const response = await axios.put(`${API_URL}/me`, updates);
      setUser(response.data);
      return { success: true };
    } catch (error) {
      console.error('Profile update failed:', error);
      const message = error.response?.data?.detail || 'Failed to update profile';
      return { success: false, error: message };
    }
  };

  const refreshUser = async () => {
    try {
      const response = await axios.get(`${API_URL}/me`);
      setUser(response.data);
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    becomeDeveloper,
    updateProfile,
    refreshUser,
    isAdmin,
    isDeveloper,
    isUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
