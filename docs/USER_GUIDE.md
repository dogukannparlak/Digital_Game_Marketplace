# User Guide

Quick overview of Digital Game Marketplace for players, developers, and admins.

## Players

1. **Register** or sign in from the login page
2. **Browse** the store — search by title, filter by genre or price
3. **Add to cart** and checkout, or buy a single game directly
4. **Library** — owned games appear under your account library
5. **Reviews** — rate and review games you own

## Developers

1. Register, then request or use a **developer** account (seed: `rockstar_games` / `dev123`)
2. **Publish** games from the developer dashboard (status starts as `PENDING`)
3. Wait for **admin approval** before the game appears in the public store
4. Update pricing and view sales stats from developer tools

## Admins

1. Sign in as admin (seed: `admin` / `admin123`)
2. **Approve or reject** pending games
3. **Ban/unban** users and manage roles
4. View platform statistics on the admin dashboard

## Demo accounts (after seed)

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Player | `player` | `player123` |
| Developer | `rockstar_games` | `dev123` |

Run seed data: `python -m backend.seed_data`

## API docs

When the backend is running, open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive OpenAPI documentation.
