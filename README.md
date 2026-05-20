# Digital Game Marketplace

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=flat&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

A full-stack digital game storefront inspired by Steam and Epic Games. Users can browse and purchase games, developers can publish and manage their titles, and admins oversee the entire platform — all backed by a role-based REST API.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Demo Credentials](#demo-credentials)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [User Roles](#user-roles)
- [License](#license)

---

## Features

**Store & Users**
- Browse, search, and filter games by genre, name, and price range
- Shopping cart with multi-game checkout
- Personal game library and order history
- Game reviews and ratings (must own the game)
- User profiles with avatar, bio, and display name

**Developer Portal**
- Apply to become a developer from any user account
- Publish games with cover image, trailer, description, and genres
- Edit games and adjust pricing / discounts at any time
- Sales dashboard with revenue and unit statistics

**Admin Panel**
- Approve, reject, or suspend games
- Ban and unban users, reassign roles
- Platform-wide statistics
- Genre / category management

**Technical**
- JWT authentication with role-based access control (`USER`, `DEVELOPER`, `ADMIN`)
- Pydantic v2 request/response validation
- SQLAlchemy ORM with SQLite (easy swap to PostgreSQL)
- 100+ pytest test cases across unit and integration layers
- Responsive UI with loading skeletons and live cart badge

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI |
| Database | SQLite via SQLAlchemy ORM |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic v2 |
| Frontend framework | React 19 + Vite 7 |
| Routing | React Router DOM v7 |
| HTTP client | Axios |
| Styling | Tailwind CSS v4 |
| Testing | Pytest, pytest-cov, pytest-mock |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### 1. Clone

```bash
git clone https://github.com/dogukannparlak/Digital_Game_Marketplace.git
cd Digital_Game_Marketplace
```

### 2. Backend

```bash
# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Copy the example env file and set your own secret key:

```bash
cp .env.example .env
```

### 3. Frontend

```bash
cd frontend
cp .env.example .env   # API URL defaults to http://localhost:8000
npm install
```

### 4. Seed the database

```bash
# Run from the project root
python -m backend.seed_data
```

### 5. Run

**Windows (one command):**

```bash
start_project.bat
# or
.\start_project.ps1
```

**Manual:**

```bash
# Terminal 1 — backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## Demo Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Player | `player` | `player123` |
| Developer | `rockstar_games` | `dev123` |

---

## API Reference

Full reference: [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)

### Authentication

```
POST  /token                     Login — returns JWT
POST  /users/                    Register new account
GET   /me                        Current user profile
PUT   /me                        Update profile
PUT   /me/password               Change password
POST  /become-developer          Upgrade account to developer
```

### Games

```
GET    /games                    List approved games (search, filter, paginate)
GET    /games/{id}               Game detail
GET    /games/{id}/reviews       Reviews for a game
POST   /games/{id}/review        Post a review (must own game)
POST   /games                    Publish a game              [DEVELOPER]
PUT    /games/{id}               Update game / price         [DEVELOPER]
DELETE /games/{id}               Delete game                 [DEVELOPER]
GET    /games/developer/my-games My published games          [DEVELOPER]
GET    /games/developer/stats    Sales statistics            [DEVELOPER]
```

### Cart & Orders

```
GET    /cart                     View cart
POST   /cart/add/{game_id}       Add to cart
DELETE /cart/remove/{game_id}    Remove from cart
DELETE /cart/clear               Clear cart
POST   /cart/checkout            Checkout and create order
GET    /orders                   Order history
GET    /orders/{id}              Order detail
GET    /orders/library           Owned game IDs
```

### Admin

```
GET    /admin/stats                       Platform statistics   [ADMIN]
GET    /admin/users                       All users             [ADMIN]
PUT    /admin/users/{id}/ban              Ban user              [ADMIN]
PUT    /admin/users/{id}/role             Change user role      [ADMIN]
GET    /admin/games/pending               Pending approvals     [ADMIN]
PUT    /admin/games/{id}/approve          Approve game          [ADMIN]
PUT    /admin/games/{id}/reject           Reject game           [ADMIN]
PUT    /admin/games/{id}/suspend          Suspend game          [ADMIN]
```

---

## Project Structure

```
Digital_Game_Marketplace/
├── backend/
│   ├── main.py              # App factory, CORS, router registration
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Engine and session factory
│   ├── auth_utils.py        # JWT decode, role guard dependencies
│   ├── seed_data.py         # Demo data loader
│   └── routers/
│       ├── auth.py          # /token, /me, /become-developer
│       ├── users.py         # /users
│       ├── games.py         # /games
│       ├── genres.py        # /genres
│       ├── cart.py          # /cart
│       ├── orders.py        # /orders
│       └── admin.py         # /admin
│
├── frontend/
│   └── src/
│       ├── config.js        # Central API_URL (reads VITE_API_URL)
│       ├── App.jsx          # Routes + context providers
│       ├── context/
│       │   ├── AuthContext.jsx
│       │   └── CartContext.jsx
│       ├── components/
│       │   ├── Navbar.jsx
│       │   └── Skeleton.jsx
│       └── pages/
│           ├── Home.jsx
│           ├── GameDetail.jsx
│           ├── Cart.jsx
│           ├── Library.jsx
│           ├── OrderHistory.jsx
│           ├── Profile.jsx
│           ├── DeveloperDashboard.jsx
│           ├── EditGame.jsx
│           └── admin/
│               ├── AdminDashboard.jsx
│               ├── UserManagement.jsx
│               ├── GameManagement.jsx
│               └── AdminPublishGame.jsx
│
├── tests/
│   ├── conftest.py
│   ├── test_admin.py
│   ├── test_cart.py
│   ├── test_orders.py
│   ├── test_games_search_filter.py
│   ├── test_purchase_service.py
│   ├── test_update_game_price.py
│   └── test_view_developer_games.py
│
├── docs/                    # Extended documentation + PlantUML diagrams
├── .env.example             # Backend environment template
├── requirements.txt
├── pytest.ini
├── start_project.bat
└── start_project.ps1
```

---

## Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=backend --cov-report=html
# Open htmlcov/index.html in your browser

# Run a specific file
pytest tests/test_cart.py -v
pytest tests/test_admin.py -v

# Run by marker
pytest -m unit
pytest -m integration
```

**Coverage target:** `backend/` package · **Test count:** 100+

---

## User Roles

| Role | Capabilities |
|---|---|
| `USER` | Browse store, buy games, manage cart, write reviews, edit profile |
| `DEVELOPER` | Everything a USER can do + publish/manage own games, view sales stats |
| `ADMIN` | Everything a DEVELOPER can do + approve/suspend games, ban users, manage platform |

Any `USER` can upgrade to `DEVELOPER` via `POST /become-developer`.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Built by [Doğukan Parlak](https://github.com/dogukannparlak)*
