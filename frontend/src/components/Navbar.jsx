import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function Navbar() {
  const { user, logout, isAdmin, isDeveloper } = useAuth();
  const { cartCount } = useCart();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const getRoleBadgeClass = () => {
    if (!user) return '';
    if (user.role === 'admin') return 'glass-badge-admin';
    if (user.role === 'developer') return 'glass-badge-developer';
    return 'glass-badge-user';
  };

  const closeMobileMenu = () => setMobileMenuOpen(false);

  const NavLinks = ({ mobile = false }) => (
    <>
      <Link
        to="/"
        onClick={closeMobileMenu}
        className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'} ${isActive('/') ? 'glass-nav-link-active' : ''}`}
      >
        Store
      </Link>

      {user && (
        <Link
          to="/cart"
          onClick={closeMobileMenu}
          className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'} ${isActive('/cart') ? 'glass-nav-link-active' : ''} relative`}
        >
          <span className="flex items-center gap-1">
            🛒 Cart
            {cartCount > 0 && (
              <span className="glass-cart-badge">
                {cartCount}
              </span>
            )}
          </span>
        </Link>
      )}

      {user ? (
        <>
          <Link
            to="/library"
            onClick={closeMobileMenu}
            className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'} ${isActive('/library') ? 'glass-nav-link-active' : ''}`}
          >
            Library
          </Link>

          <Link
            to="/orders"
            onClick={closeMobileMenu}
            className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'} ${isActive('/orders') ? 'glass-nav-link-active' : ''}`}
          >
            Orders
          </Link>

          <Link
            to="/profile"
            onClick={closeMobileMenu}
            className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'} ${isActive('/profile') ? 'glass-nav-link-active' : ''}`}
          >
            Profile
          </Link>

          {isDeveloper() && (
            <Link
              to="/developer"
              onClick={closeMobileMenu}
              className={`${mobile ? 'glass-mobile-link' : ''} glass-btn glass-btn-sm`}
              style={{ background: 'linear-gradient(135deg, #8b5cf6, #6d28d9)', borderColor: '#8b5cf6' }}
            >
              Developer
            </Link>
          )}

          {isAdmin() && (
            <Link
              to="/admin"
              onClick={closeMobileMenu}
              className={`${mobile ? 'glass-mobile-link' : ''} glass-btn glass-btn-sm glass-btn-danger`}
            >
              Admin
            </Link>
          )}

          {!isDeveloper() && (
            <Link
              to="/become-developer"
              onClick={closeMobileMenu}
              className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'}`}
              style={{ color: '#c4b5fd', borderColor: 'rgba(139, 92, 246, 0.3)' }}
            >
              Become Developer
            </Link>
          )}

          {mobile && <div className="border-t border-white/10 my-4" />}

          <div className={`flex items-center gap-3 ${mobile ? 'mt-4' : ''}`}>
            {user.avatar_url ? (
              <img
                src={user.avatar_url}
                alt={user.username}
                className="w-8 h-8 rounded-full object-cover glass-avatar"
              />
            ) : (
              <div className="w-8 h-8 rounded-full glass-avatar-placeholder flex items-center justify-center text-sm font-medium">
                {user.username.charAt(0).toUpperCase()}
              </div>
            )}
            <span className="text-white/80 text-sm hidden md:inline">
              {user.display_name || user.username}
            </span>
            <span className={`glass-badge text-xs ${getRoleBadgeClass()}`}>
              {user.role.toUpperCase()}
            </span>
            <button
              onClick={() => { logout(); closeMobileMenu(); }}
              className="glass-btn glass-btn-sm"
            >
              Logout
            </button>
          </div>
        </>
      ) : (
        <>
          <Link
            to="/login"
            onClick={closeMobileMenu}
            className={`${mobile ? 'glass-mobile-link' : 'glass-nav-link'}`}
          >
            Login
          </Link>
          <Link
            to="/register"
            onClick={closeMobileMenu}
            className="glass-btn glass-btn-sm glass-btn-accent"
          >
            Register
          </Link>
        </>
      )}
    </>
  );

  return (
    <>
      <nav className="glass-navbar">
        <div className="glass-navbar-content">
          {/* Logo */}
          <Link to="/" className="glass-navbar-logo">
            <span className="text-2xl">🎮</span>
            <span className="glass-text-gradient font-bold">GameStore</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="glass-navbar-links hidden md:flex">
            <NavLinks />
          </div>

          {/* Mobile Hamburger */}
          <button
            className={`glass-hamburger md:hidden ${mobileMenuOpen ? 'active' : ''}`}
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <span className="glass-hamburger-line" />
            <span className="glass-hamburger-line" />
            <span className="glass-hamburger-line" />
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div className={`glass-mobile-menu ${mobileMenuOpen ? 'open' : ''}`}>
        <NavLinks mobile />
      </div>
    </>
  );
}
