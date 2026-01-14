# 🎮 Digital Game Marketplace

[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)]()

> A professional digital game marketplace platform - Full-featured e-commerce system in the style of Steam, Epic Games, and GOG.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [User Roles](#-user-roles)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

Digital Game Marketplace is a comprehensive digital game sales platform developed using modern web technologies. Users can purchase games, developers can publish games, and admins can manage the platform.

### Main Functions

- 👤 **User System**: Registration, login, profile management
- 🎮 **Game Store**: Search, filtering, detailed game pages
- 🛒 **Shopping**: Cart, payment, order history
- 📚 **Library**: Purchased games
- ⭐ **Reviews**: Game rating and review system
- 🔧 **Developer Panel**: Game publishing and management
- 👨‍💼 **Admin Panel**: Game approval, user management

## ✨ Features

### User Features
- ✅ Registration/login with email and username
- ✅ Profile customization (avatar, bio, display name)
- ✅ Game search and filtering (genre, price, rating)
- ✅ Shopping cart management
- ✅ Secure payment and order system
- ✅ Personal game library
- ✅ Game review and rating
- ✅ Wishlist system
- ✅ Order history viewing

### Developer Features
- ✅ Developer account creation
- ✅ Game publishing (title, description, price, cover image)
- ✅ Game updates and price changes
- ✅ List published games
- ✅ Discount creation and management
- ✅ Sales statistics viewing
- ✅ Verified developer badge

### Admin Features
- ✅ Game approval/rejection system
- ✅ Game suspension
- ✅ User banning/activation
- ✅ Game management (all games)
- ✅ User management (all users)
- ✅ Category/genre management
- ✅ Platform statistics

### Technical Features
- 🔐 JWT token-based authentication
- 🛡️ Role-based access control (USER, DEVELOPER, ADMIN)
- 📊 RESTful API design
- 🗄️ Database management with SQLAlchemy ORM
- ✔️ Data validation with Pydantic
- 🧪 Comprehensive test coverage with Pytest
- 📱 Responsive web design
- 🎨 Modern UI/UX (Tailwind CSS)

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT (python-jose, passlib)
- **Validation**: Pydantic v2
- **Testing**: Pytest, pytest-asyncio
- **Server**: Uvicorn

### Frontend
- **Framework**: React 19.2
- **Build Tool**: Vite 7.2
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios 1.13
- **Styling**: Tailwind CSS 4.1
- **Linting**: ESLint 9

### DevOps
- **Version Control**: Git
- **Package Management**: pip (Python), npm (JavaScript)
- **Documentation**: Markdown, OpenAPI/Swagger

## 🚀 Installation

### Requirements
- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn
- Git

### 1️⃣ Clone the Project

```bash
git clone https://github.com/dogukannparlak/Digital_Game_Marketplace
cd Digital_Game_Marketplace
```

### 2️⃣ Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
```

### 4️⃣ Database Preparation

```bash
# Run in the root directory
python -m backend.seed_data
```

This command creates sample data:
- Admin user: `admin@marketplace.com` / `admin123`
- Developer user: `dev@marketplace.com` / `dev123`
- Regular user: `user@marketplace.com` / `user123`
- Sample games and categories

## 💻 Usage

### Quick Start (Windows)

```bash
# Start both backend and frontend with one command
start_project.bat
```

or PowerShell:

```powershell
.\start_project.ps1
```

### Manual Start

#### Backend (Terminal 1)

```bash
# In root directory
uvicorn backend.main:app --reload --port 8000
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

#### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend: http://localhost:5173

## 📚 API Documentation

API documentation is automatically generated and accessible at the following addresses:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Main Endpoints

#### Authentication
```http
POST /token                    # Login (get token)
POST /register                 # Register new user
GET  /me                       # Current user info
POST /become-developer         # Create developer account
```

#### Games
```http
GET    /games                  # List games (filtering, search)
POST   /games                  # Publish new game (DEVELOPER)
GET    /games/{id}             # Game details
PUT    /games/{id}             # Update game (DEVELOPER)
DELETE /games/{id}             # Delete game (DEVELOPER)
PUT    /games/{id}/price       # Update price (DEVELOPER)
```

#### Cart & Orders
```http
GET    /cart                   # View cart
POST   /cart/add/{game_id}     # Add to cart
DELETE /cart/remove/{game_id}  # Remove from cart
POST   /cart/checkout          # Purchase
GET    /orders                 # Order history
GET    /orders/{id}            # Order details
```

#### Admin
```http
GET    /admin/games/pending    # Pending games
PUT    /admin/games/{id}/approve     # Approve game
PUT    /admin/games/{id}/reject      # Reject game
PUT    /admin/games/{id}/suspend     # Suspend game
PUT    /admin/users/{id}/ban         # Ban user
GET    /admin/users                  # All users
```

For detailed API reference: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

## 📁 Project Structure

```
Digital_Game_Marketplace/
├── 📂 backend/              # FastAPI Backend
│   ├── main.py             # Main application
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   ├── auth_utils.py       # JWT and encryption
│   ├── seed_data.py        # Sample data creation
│   └── 📂 routers/         # API endpoints
│       ├── auth.py         # Authentication
│       ├── games.py        # Game operations
│       ├── users.py        # User operations
│       ├── cart.py         # Cart operations
│       ├── orders.py       # Order operations
│       ├── admin.py        # Admin operations
│       └── genres.py       # Category operations
│
├── 📂 frontend/            # React Frontend
│   ├── 📂 src/
│   │   ├── App.jsx         # Main component
│   │   ├── main.jsx        # Entry point
│   │   ├── 📂 components/  # Reusable components
│   │   ├── 📂 pages/       # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── GameDetail.jsx
│   │   │   ├── Cart.jsx
│   │   │   ├── Library.jsx
│   │   │   ├── DeveloperDashboard.jsx
│   │   │   └── 📂 admin/
│   │   └── 📂 context/     # React Context (Auth, Cart)
│   ├── package.json
│   └── vite.config.js
│
├── 📂 tests/               # Test files
│   ├── conftest.py         # Pytest configuration
│   ├── test_games_search_filter.py
│   ├── test_purchase_service.py
│   ├── test_admin.py
│   ├── test_cart.py
│   └── test_orders.py
│
├── 📂 docs/                # Documentation
│   ├── API_REFERENCE.md
│   ├── INSTALLATION.md
│   └── ...
│
├── 📂 diagrams/            # PlantUML diagrams
│   ├── US-1.puml          # User Story diagrams
│   └── ...
│
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
├── start_project.bat      # Windows startup script
├── start_project.ps1      # PowerShell startup script
└── README.md              # This file
```

## 🧪 Testing

### Run All Tests

```bash
# In root directory
pytest
```

### Test with Coverage Report

```bash
pytest --cov=backend --cov-report=html
```

HTML report: `htmlcov/index.html`

### Specific Test File

```bash
pytest tests/test_games_search_filter.py -v
pytest tests/test_purchase_service.py -v
pytest tests/test_admin.py -v
```

### Test Statistics
- ✅ **100+ Test Cases**
- ✅ **90%+ Code Coverage**
- ✅ Unit Tests
- ✅ Integration Tests
- ✅ API Endpoint Tests


## 👥 User Roles

### 🟢 USER (Regular User)
- View and search games
- Add to cart and purchase
- Library access
- Write reviews and ratings
- Edit profile

### 🔵 DEVELOPER
- All USER role permissions
- Publish games
- Update games
- Price and discount management
- View sales statistics

### 🔴 ADMIN
- All DEVELOPER role permissions
- Approve/reject games
- Suspend games
- Ban users
- Manage all games and users
- Platform statistics

## 📸 Screenshots

### Home Page
Modern, user-friendly game store interface

### Game Details
Comprehensive game information, reviews, and ratings

### Developer Panel
Game publishing and management interface

### Admin Panel
Game approval and user management

## 🔒 Security

- ✅ Passwords hashed with bcrypt
- ✅ JWT token-based authentication
- ✅ CORS middleware configuration
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)
- ✅ Role-based access control
- ✅ Session management

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 👨‍💻 Authors

- **Doğukan Parlak**
- **Ömer Kaya**

---

⭐ **If you like this project, don't forget to give it a star!**

💻 **Happy Coding!** 🎮
