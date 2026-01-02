# Digital Game Marketplace

A Steam/Epic/GOG-like digital game marketplace with role-based access control. Built with FastAPI (Python) backend and React (Vite + TailwindCSS) frontend.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg) ![Python](https://img.shields.io/badge/python-3.8+-green.svg) ![Node](https://img.shields.io/badge/node-18+-green.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)
## 🎮 Features
### User Roles
- **User (Player)** - Browse games, add to cart, purchase, write reviews, manage library
- **Developer** - Publish games, track sales & revenue, manage game listings
- **Admin** - Approve/reject games, manage users, view platform statistics
### Core Functionality
- 🛒 Shopping cart with discount support
- 🎯 Game filtering by genre, price, and search
- ⭐ Review and rating system
- 📊 Developer sales dashboard
- 🛡️ Admin moderation panel
- 🔐 JWT-based authentication
## 🚀 Quick Start
### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn
### One-Command Start (Windows PowerShell)
```powershell
# First time setup with sample data
.\start_project.ps1 -Seed
# Normal startup (without reseeding)
.\start_project.ps1
```
### Manual Setup
```bash
# Backend
pip install -r requirements.txt
python -m backend.seed_data  # Seed database
uvicorn backend.main:app --reload --port 8000
# Frontend (in separate terminal)
cd frontend
npm install
npm run dev
```
## 🔗 URLs
| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation (Swagger) | http://localhost:8000/docs |
| API Documentation (ReDoc) | http://localhost:8000/redoc |
## 👤 Test Accounts
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Player | `player` | `player123` |
| Developer | `rockstar_games` | `dev123` |
## 📁 Project Structure
```
Digital Game Marketplace/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   ├── auth_utils.py       # Authentication utilities
│   ├── seed_data.py        # Database seeder
│   └── routers/            # API route handlers
│       ├── auth.py         # Authentication endpoints
│       ├── users.py        # User management
│       ├── games.py        # Game CRUD & store
│       ├── genres.py       # Genre management
│       ├── cart.py         # Shopping cart
│       ├── orders.py       # Order processing
│       └── admin.py        # Admin operations
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── context/        # React contexts
│   │   └── pages/          # Page components
│   └── package.json
├── diagrams/               # PlantUML diagrams (US-16 to US-39)
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── start_project.ps1       # Startup script
```
## 📚 Documentation
Detailed documentation is available in the [docs/](./docs/) folder:
- [Installation Guide](./docs/INSTALLATION.md)
- [API Reference](./docs/API_REFERENCE.md)
- [Architecture Overview](./docs/ARCHITECTURE.md)
- [User Guide](./docs/USER_GUIDE.md)
- [Testing Guide](./docs/TESTING.md)
- [Contribution Guidelines](./docs/CONTRIBUTING.md)
- [Changelog](./docs/CHANGELOG.md)
## 🛠️ Tech Stack
### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Pydantic** - Data validation
- **JWT** - Token-based authentication
- **bcrypt** - Password hashing
### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **TailwindCSS 4** - Utility-first CSS
- **React Router 7** - Client-side routing
- **Axios** - HTTP client
## 📝 License
This project is developed for CSE305 - Software Engineering course.
---
**Developed with ❤️ for Digital Game Marketplace**
