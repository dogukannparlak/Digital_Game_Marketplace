# Architecture Overview

This document describes the architecture, design patterns, and key decisions of the Digital Game Marketplace.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              React + Vite + TailwindCSS                  │   │
│  │    ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │   │
│  │    │  Pages   │  │Components│  │     Context      │    │   │
│  │    └──────────┘  └──────────┘  │  (Auth, Cart)    │    │   │
│  │                                 └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP/REST (Axios)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          API LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Application                   │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐   │   │
│  │  │  Auth   │  │  Games  │  │  Cart   │  │  Admin   │   │   │
│  │  │ Router  │  │ Router  │  │ Router  │  │  Router  │   │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └──────────┘   │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │            Authentication Middleware                │ │   │
│  │  │              (JWT + Role-Based Access)              │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │ SQLAlchemy ORM
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  SQLite Database                         │   │
│  │     (Easily replaceable with PostgreSQL)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | High-performance async API framework |
| ORM | SQLAlchemy | Database abstraction and migrations |
| Database | SQLite | Development database (PostgreSQL for production) |
| Validation | Pydantic | Request/response data validation |
| Authentication | python-jose (JWT) | Token-based authentication |
| Password Hashing | bcrypt | Secure password storage |

### Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Library | React 19 | Component-based UI |
| Build Tool | Vite 7 | Fast development server and bundler |
| Styling | TailwindCSS 4 | Utility-first CSS framework |
| Routing | React Router 7 | Client-side navigation |
| HTTP Client | Axios | API requests |
| State Management | React Context | Global state (Auth, Cart) |

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      User       │     │      Game       │     │      Genre      │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │     │ id (PK)         │
│ public_id       │     │ title           │     │ name            │
│ username        │     │ description     │     │ slug            │
│ email           │     │ price           │     │ description     │
│ hashed_password │     │ discount_percent│     └────────┬────────┘
│ role            │     │ status          │              │
│ developer_name  │     │ developer_id(FK)│◄─────────────┤
│ is_banned       │     │ approved_by(FK) │     ┌────────┴────────┐
└────────┬────────┘     └────────┬────────┘     │   game_genres   │
         │                       │              │ (Junction Table)│
         │                       │              └─────────────────┘
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│     Order       │     │     Review      │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ user_id (FK)    │     │ user_id (FK)    │
│ order_date      │     │ game_id (FK)    │
│ total_amount    │     │ rating          │
│ payment_status  │     │ content         │
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   OrderItem     │     │    CartItem     │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ order_id (FK)   │     │ user_id (FK)    │
│ game_id (FK)    │     │ game_id (FK)    │
│ purchase_price  │     │ added_at        │
│ discount_applied│     └─────────────────┘
└─────────────────┘
```

### Models

#### User

```python
class User(Base):
    id: int                    # Primary key
    public_id: str             # Public identifier (USR-XXXXXXXX)
    username: str              # Unique username
    email: str                 # Unique email
    hashed_password: str       # bcrypt hashed password
    role: UserRole             # USER, DEVELOPER, ADMIN
    developer_name: str        # Studio name (if developer)
    developer_verified: bool   # Verified developer status
    is_active: bool            # Account active status
    is_banned: bool            # Ban status
    banned_reason: str         # Reason for ban
```

#### Game

```python
class Game(Base):
    id: int                    # Primary key
    title: str                 # Game title
    description: str           # Full description
    short_description: str     # Brief summary
    price: float               # Base price
    discount_percent: int      # Current discount (0-100)
    release_date: datetime     # Publication date
    developer_id: int          # FK to User (developer)
    status: GameStatus         # PENDING, APPROVED, REJECTED, SUSPENDED
    rejection_reason: str      # Reason if rejected
    approved_by: int           # FK to User (admin who approved)
    cover_image_url: str       # Game cover art URL
    trailer_url: str           # Video trailer URL
    total_sales: int           # Number of copies sold
    total_revenue: float       # Total earnings
```

---

## Role-Based Access Control (RBAC)

### User Roles

| Role | Code | Permissions |
|------|------|-------------|
| **User** | `user` | Browse games, purchase, review, manage profile |
| **Developer** | `developer` | All user permissions + publish games, view sales |
| **Admin** | `admin` | All permissions + approve games, manage users |

### Permission Matrix

| Action | User | Developer | Admin |
|--------|:----:|:---------:|:-----:|
| Browse games | ✅ | ✅ | ✅ |
| Purchase games | ✅ | ✅ | ✅ |
| Write reviews | ✅ | ✅ | ✅ |
| Publish games | ❌ | ✅ | ✅ |
| View sales stats | ❌ | ✅ | ✅ |
| Approve games | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |
| Ban users | ❌ | ❌ | ✅ |

### Implementation

```python
# auth_utils.py
async def require_admin(current_user: User = Depends(get_current_active_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_developer(current_user: User = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.DEVELOPER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Developer access required")
    return current_user
```

---

## Game Approval Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PENDING    │────▶│   APPROVED   │────▶│  SUSPENDED   │
│              │     │              │     │              │
│  (Created)   │     │ (In Store)   │     │  (Removed)   │
└──────────────┘     └──────────────┘     └──────────────┘
       │                                          │
       │                                          │
       ▼                                          │
┌──────────────┐                                  │
│   REJECTED   │◀─────────────────────────────────┘
│              │
│ (Not Shown)  │
└──────────────┘
```

### Status Definitions

| Status | Description | Visible in Store |
|--------|-------------|:----------------:|
| **PENDING** | Awaiting admin review | ❌ |
| **APPROVED** | Available for purchase | ✅ |
| **REJECTED** | Declined by admin (with reason) | ❌ |
| **SUSPENDED** | Temporarily removed from store | ❌ |

---

## Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │     │   API    │     │   Auth   │     │ Database │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │  POST /token   │                │                │
     │───────────────▶│                │                │
     │                │  Verify User   │                │
     │                │───────────────▶│                │
     │                │                │  Query User    │
     │                │                │───────────────▶│
     │                │                │◀───────────────│
     │                │                │                │
     │                │  Check Password│                │
     │                │◀───────────────│                │
     │                │                │                │
     │                │  Generate JWT  │                │
     │                │───────────────▶│                │
     │                │◀───────────────│                │
     │                │                │                │
     │  Access Token  │                │                │
     │◀───────────────│                │                │
     │                │                │                │
     │  GET /me       │                │                │
     │  + Bearer Token│                │                │
     │───────────────▶│                │                │
     │                │  Decode JWT    │                │
     │                │───────────────▶│                │
     │                │◀───────────────│                │
     │                │                │                │
     │  User Data     │                │                │
     │◀───────────────│                │                │
```

### JWT Token Structure

```json
{
  "sub": "username",
  "id": 1,
  "role": "user",
  "exp": 1703980800
}
```

---

## Frontend Architecture

### Component Structure

```
src/
├── main.jsx              # App entry point
├── App.jsx               # Router configuration
├── components/           # Reusable components
│   ├── Navbar.jsx        # Navigation bar
│   └── Skeleton.jsx      # Loading skeletons
├── context/              # Global state
│   ├── AuthContext.jsx   # Authentication state
│   └── CartContext.jsx   # Shopping cart state
└── pages/                # Page components
    ├── Home.jsx          # Store homepage
    ├── GameDetail.jsx    # Game details page
    ├── Cart.jsx          # Shopping cart
    ├── Library.jsx       # Owned games
    ├── Login.jsx         # Login form
    ├── Register.jsx      # Registration form
    ├── Profile.jsx       # User profile
    ├── OrderHistory.jsx  # Purchase history
    ├── DeveloperDashboard.jsx  # Developer panel
    └── admin/            # Admin pages
        ├── AdminDashboard.jsx
        ├── UserManagement.jsx
        └── GameManagement.jsx
```

### State Management

**AuthContext:**
- Stores current user data
- Handles login/logout
- Persists token to localStorage

**CartContext:**
- Manages shopping cart items
- Calculates totals
- Syncs with backend

---

## API Design Patterns

### RESTful Endpoints

```
GET    /games/              # List games (collection)
POST   /games/              # Create game
GET    /games/{id}          # Get single game
PUT    /games/{id}          # Update game
DELETE /games/{id}          # Delete game
```

### Nested Resources

```
GET    /games/{id}/reviews      # Game's reviews
GET    /admin/users/{id}/orders # User's orders (admin)
```

### Actions

```
POST   /cart/add/{game_id}      # Add to cart
POST   /cart/checkout           # Checkout cart
POST   /admin/games/{id}/approve   # Approve game
POST   /admin/users/{id}/ban       # Ban user
```

---

## Security Considerations

### Password Storage
- bcrypt hashing with automatic salt
- Minimum 6 character requirement

### JWT Security
- Short expiration (24 hours)
- Secret key should be environment variable in production
- Token includes user ID and role

### Input Validation
- Pydantic validators on all inputs
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention (React escapes by default)

### CORS Configuration
- Development: Allow all origins
- Production: Restrict to frontend domain

---

## Diagrams

The project includes PlantUML diagrams in `/diagrams`:

| Diagram | Description |
|---------|-------------|
| US-16 | Game Approval Workflow |
| US-17 - US-39 | Various user story diagrams |

These diagrams document:
- Domain models
- User workflows
- System interactions
- State transitions

