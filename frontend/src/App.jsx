import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Cart from './pages/Cart';
import DeveloperRegister from './pages/DeveloperRegister';
import DeveloperDashboard from './pages/DeveloperDashboard';
import EditGame from './pages/EditGame';
import GameDetail from './pages/GameDetail';
import OrderHistory from './pages/OrderHistory';
import Library from './pages/Library';
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagement from './pages/admin/UserManagement';
import GameManagement from './pages/admin/GameManagement';
import AdminPublishGame from './pages/admin/AdminPublishGame';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <CartProvider>
          <div className="min-h-screen glass-bg">
          <Navbar />
            <main className="pb-8">
            <Routes>
                {/* Public Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
                <Route path="/game/:id" element={<GameDetail />} />

                {/* User Routes */}
                <Route path="/profile" element={<Profile />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/library" element={<Library />} />
                <Route path="/orders" element={<OrderHistory />} />

                {/* Developer Routes */}
                <Route path="/become-developer" element={<DeveloperRegister />} />
                <Route path="/developer" element={<DeveloperDashboard />} />
                <Route path="/developer/edit-game/:id" element={<EditGame />} />

                {/* Admin Routes */}
                <Route path="/admin" element={<AdminDashboard />} />
                <Route path="/admin/users" element={<UserManagement />} />
                <Route path="/admin/games" element={<GameManagement />} />
                <Route path="/admin/publish-game" element={<AdminPublishGame />} />

                {/* Legacy routes - redirect */}
              <Route path="/developer-register" element={<DeveloperRegister />} />
              <Route path="/developer-dashboard" element={<DeveloperDashboard />} />
              <Route path="/games/:id" element={<GameDetail />} />
            </Routes>
          </main>
        </div>
        </CartProvider>
      </Router>
    </AuthProvider>
  );
}

export default App;
