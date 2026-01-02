# Installation Guide

This guide covers the complete setup process for the Digital Game Marketplace project.

## Prerequisites

Before you begin, ensure you have the following installed:

| Software | Minimum Version | Download |
|----------|-----------------|----------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| npm | 9+ | Included with Node.js |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

## Quick Start (Windows)

The easiest way to start the project on Windows is using the PowerShell script:

```powershell
# Navigate to project directory
cd "C:\path\to\Digital Game Marketplace"

# First time setup with sample data
.\start_project.ps1 -Seed

# Normal startup (without reseeding database)
.\start_project.ps1
```

This script will:
1. Seed the database with sample data (if `-Seed` flag is used)
2. Start the backend server on port 8000
3. Start the frontend development server on port 5173

## Manual Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Digital Game Marketplace"
```

### Step 2: Backend Setup

#### Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Seed the Database

This creates the database schema and populates it with sample data including:
- Admin, player, and developer accounts
- 21 game genres
- Multiple game developers with real-world inspired games

```bash
python -m backend.seed_data
```

#### Start the Backend Server

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Step 3: Frontend Setup

Open a new terminal window/tab:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

## Configuration

### Backend Configuration

Key configuration files:

| File | Purpose |
|------|---------|
| `backend/database.py` | Database connection settings |
| `backend/auth_utils.py` | JWT secret key and algorithm |
| `backend/routers/auth.py` | Token expiration settings |

#### Database Configuration

By default, the project uses SQLite. To switch to PostgreSQL:

```python
# backend/database.py
# Change from:
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# To:
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

#### JWT Configuration

For production, update the secret key in `backend/auth_utils.py`:

```python
SECRET_KEY = "your-production-secret-key-here"
```

### Frontend Configuration

The API base URL is configured in the Axios instances within components. The default is `http://localhost:8000`.

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port 8000 (Windows)
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

#### 2. Module Not Found Errors

Ensure you're running commands from the project root directory:

```bash
# Correct way to run seed script
python -m backend.seed_data

# NOT
python backend/seed_data.py
```

#### 3. CORS Errors

The backend is configured to allow all origins in development. For production, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    # ...
)
```

#### 4. Database Locked (SQLite)

If you see "database is locked" errors, ensure only one instance of the backend is running.

#### 5. npm Install Fails

Clear the npm cache and retry:

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment

### Backend

1. Use Gunicorn with Uvicorn workers:
```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Use a production database (PostgreSQL recommended)
3. Set environment variables for secrets
4. Use HTTPS with a reverse proxy (nginx)

### Frontend

1. Build the production bundle:
```bash
cd frontend
npm run build
```

2. Serve the `dist` folder with a static file server or CDN

## Development Tips

### Hot Reload

Both backend (`--reload` flag) and frontend (`npm run dev`) support hot reload during development.

### API Testing

Use the Swagger UI at http://localhost:8000/docs to test API endpoints interactively.

### Database Reset

To reset the database and reseed:

```bash
# Delete the database file
rm sql_app.db  # or del sql_app.db on Windows

# Reseed
python -m backend.seed_data
```

