# 🚀 Installation Guide

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

**Software**:
- Python 3.10 or higher
- Node.js 18.0 or higher
- npm 9.0 or higher
- Git 2.30 or higher

**Hardware**:
- 2 GB RAM (minimum)
- 500 MB disk space
- Internet connection (for dependency downloads)

### Recommended Requirements

**Software**:
- Python 3.11+
- Node.js 20.0+
- npm 10.0+
- Git 2.40+
- VS Code (recommended IDE)

**Hardware**:
- 4 GB+ RAM
- 2 GB disk space
- SSD disk

## Quick Installation

### Windows

```bash
# 1. Clone the project
git clone https://github.com/dogukannparlak/Digital_Game_Marketplace.git
cd Digital_Game_Marketplace

# 2. Backend setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
npm install
cd ..

# 4. Database preparation
python -m backend.seed_data

# 5. Start the project
start_project.bat
```

### Linux / macOS

```bash
# 1. Clone the project
git clone https://github.com/dogukannparlak/Digital_Game_Marketplace.git
cd Digital_Game_Marketplace

# 2. Backend setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Frontend setup
cd frontend
npm install
cd ..

# 4. Database preparation
python -m backend.seed_data

# 5. Start backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# 6. Start frontend (Terminal 2)
cd frontend
npm run dev
```

## Detailed Installation

### 1. Python Installation

#### Windows

1. Download Python 3.10+ from [Python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ Check the "Add Python to PATH" option
4. Click "Install Now"

Verify installation:
```bash
python --version
# Output: Python 3.11.x
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### macOS

```bash
# With Homebrew
brew install python@3.11
```

### 2. Node.js Installation

#### Windows / macOS

1. Download the LTS version from [Node.js](https://nodejs.org/)
2. Run the installer
3. Click "Next" for all steps

Verify installation:
```bash
node --version
# Output: v20.x.x

npm --version
# Output: 10.x.x
```

#### Linux (Ubuntu/Debian)

```bash
# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js
sudo apt-get install -y nodejs
```

### 3. Git Installation

#### Windows

1. Download [Git for Windows](https://git-scm.com/download/win)
2. Run the installer
3. Use default settings

#### Linux

```bash
sudo apt install git
```

#### macOS

```bash
brew install git
```

### 4. Clone the Project

```bash
# Via HTTPS
git clone https://github.com/dogukannparlak/Digital_Game_Marketplace.git

# Via SSH (recommended)
git clone git@github.com:dogukannparlak/Digital_Game_Marketplace.git

# Go to project directory
cd Digital_Game_Marketplace
```

### 5. Backend Setup

#### Create Virtual Environment

**Windows**:
```bash
python -m venv .venv
```

**Linux/macOS**:
```bash
python3 -m venv .venv
```

#### Activate Virtual Environment

**Windows (CMD)**:
```bash
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**:
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS**:
```bash
source .venv/bin/activate
```

Verify it's active - you should see `(.venv)` in the prompt:
```bash
(.venv) C:\...\digital-game-marketplace>
```

#### Install Dependencies

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

**Main packages installed**:
- fastapi - Web framework
- uvicorn - ASGI server
- sqlalchemy - ORM
- pydantic - Validation
- python-jose - JWT
- passlib - Password hashing
- pytest - Testing

### 6. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

**Main packages installed**:
- react - UI library
- react-dom - React DOM rendering
- react-router-dom - Routing
- axios - HTTP client
- vite - Build tool
- tailwindcss - CSS framework

```bash
# Return to main directory
cd ..
```

## Database Setup

### SQLite (Development)

The project uses SQLite by default, no separate installation needed.

#### Create Database

```bash
# In the backend directory
python -m backend.seed_data
```

This command:
1. Creates database tables
2. Adds sample users:
   - Admin: `admin@marketplace.com` / `admin123`
   - Developer: `dev@marketplace.com` / `dev123`
   - User: `user@marketplace.com` / `user123`
3. Adds sample games
4. Adds sample categories

#### Reset Database

```bash
# Delete the database file
rm sql_app.db  # Linux/macOS
del sql_app.db  # Windows

# Recreate it
python -m backend.seed_data
```

### PostgreSQL (Production)

#### PostgreSQL Installation

**Windows**:
1. Download from [PostgreSQL](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Port: 5432 (default)
4. Set a password

**Linux**:
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS**:
```bash
brew install postgresql
brew services start postgresql
```

#### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE game_marketplace;

# Create user
CREATE USER marketplace_user WITH PASSWORD 'secure_password';

# Grant permissions
GRANT ALL PRIVILEGES ON DATABASE game_marketplace TO marketplace_user;

# Exit
\q
```

#### Configuration

Edit the `backend/database.py` file:

```python
# SQLite (development)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# PostgreSQL (production)
SQLALCHEMY_DATABASE_URL = "postgresql://marketplace_user:secure_password@localhost/game_marketplace"
```

## Configuration

### Environment Variables

Create a `.env` file for production:

```bash
# .env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://user:pass@localhost/db_name
ALLOWED_ORIGINS=https://yourdomain.com
DEBUG=False
```

### CORS Settings

In the `backend/main.py` file:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "https://yourdomain.com"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend API URL

Create `frontend/src/config.js`:

```javascript
export const API_BASE_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://api.yourdomain.com'
    : 'http://localhost:8000';
```

## Running the Project

### Development Mode

#### Automatic Start (Windows)

```bash
# Batch script
start_project.bat

# PowerShell script
.\start_project.ps1
```

#### Manual Start

**Terminal 1 - Backend**:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Start server
uvicorn backend.main:app --reload --port 8000
```

Backend running at: http://localhost:8000

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

Frontend running at: http://localhost:5173

### Production Mode

#### Backend

```bash
# With Gunicorn (Linux/macOS)
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker

# With Uvicorn (Windows)
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Create build
npm run build

# Serve build
npm run preview
```

## Production Deployment

### Heroku

#### Backend Deployment

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Database migrate
heroku run python -m backend.seed_data
```

#### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

### Docker

`Dockerfile` (Backend):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/marketplace
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: marketplace
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Çalıştırma:
```bash
docker-compose up -d
```

## Troubleshooting

### Python Hataları

**Problem**: `python: command not found`

**Çözüm**:
```bash
# Python3 kullan (Linux/macOS)
python3 --version
python3 -m venv .venv
```

**Problem**: `pip: command not found`

**Çözüm**:
```bash
# pip'i python module olarak çalıştır
python -m pip install -r requirements.txt
```

### Node.js Hataları

**Problem**: `npm: command not found`

**Çözüm**: Node.js'i yeniden kurun ve PATH'e eklendiğinden emin olun

**Problem**: `EACCES: permission denied`

**Çözüm**:
```bash
# npm cache temizle
npm cache clean --force

# Veya sudo kullan (Linux/macOS)
sudo npm install
```

### Virtual Environment Hataları

**Problem**: PowerShell'de script çalıştırma hatası

**Çözüm**:
```powershell
# Execution policy değiştir (Admin PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database Hataları

**Problem**: `no such table` hatası

**Çözüm**:
```bash
# Veritabanını yeniden oluştur
python -m backend.seed_data
```

**Problem**: PostgreSQL connection error

**Çözüm**:
```bash
# PostgreSQL servisini kontrol et
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Başlat
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

### Port Hataları

**Problem**: `Address already in use`

**Çözüm**:

**Windows**:
```bash
# Port 8000'i kullanan process'i bul
netstat -ano | findstr :8000

# Process'i kapat (PID'yi yukarıdan al)
taskkill /PID <PID> /F
```

**Linux/macOS**:
```bash
# Port 8000'i kullanan process'i bul ve kapat
lsof -ti:8000 | xargs kill -9
```

### CORS Hataları

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Çözüm**: `backend/main.py`'de frontend URL'ini ekleyin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Import Hataları

**Problem**: `ModuleNotFoundError: No module named 'backend'`

**Çözüm**:
```bash
# Ana dizinden çalıştırın (backend klasörünün parent'ı)
cd digital-game-marketplace

# Python path'i kontrol edin
python -c "import sys; print(sys.path)"
```

## Yardım ve Destek

### Dokümantasyon

- [API Reference](API_REFERENCE.md)
- [Architecture](ARCHITECTURE.md)
- [Testing](TESTING.md)
- [User Guide](USER_GUIDE.md)

### Community

- **GitHub Issues**: [Sorun bildirin](https://github.com/dogukannparlak/Digital_Game_Marketplace/issues)
- **Email**: support@marketplace.com
- **Documentation**: http://localhost:8000/docs

### Faydalı Komutlar

```bash
# Python versiyonu
python --version

# pip versiyonu
pip --version

# Node versiyonu
node --version

# npm versiyonu
npm --version

# Virtual environment aktif mi?
where python  # Windows
which python  # Linux/macOS

# Yüklü paketler
pip list
npm list --depth=0

# Port kontrolü
netstat -an | findstr :8000  # Windows
lsof -i :8000  # Linux/macOS
```

---

✅ **Kurulum tamamlandı!** Artık projeyi kullanmaya başlayabilirsiniz.

📖 Sonraki adım: [Kullanıcı Kılavuzu](USER_GUIDE.md)
