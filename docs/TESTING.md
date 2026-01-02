# Testing Guide

This document outlines the testing strategy and instructions for the Digital Game Marketplace.

## Overview

The project currently relies on manual testing and linting. Future updates will include automated unit and integration tests.

## Backend Testing

### Manual API Testing

You can test the API endpoints using the interactive Swagger UI:

1.  Start the backend server:
    ```bash
    uvicorn backend.main:app --reload
    ```
2.  Open your browser and navigate to: `http://localhost:8000/docs`
3.  Use the "Try it out" button on endpoints to send requests.
4.  **Authentication:**
    -   Use the `/token` endpoint to get an access token.
    -   Click the "Authorize" button at the top right and paste the token.

### Automated Testing (Planned)

We plan to use `pytest` for backend testing.

**Setup:**
1.  Uncomment `pytest` and `httpx` in `requirements.txt`.
2.  Install dependencies: `pip install -r requirements.txt`

**Running Tests (Future):**
```bash
pytest
```

## Frontend Testing

### Linting

We use ESLint to ensure code quality and catch potential errors.

**Run Linter:**
```bash
cd frontend
npm run lint
```

### Manual UI Testing

1.  Start the frontend server:
    ```bash
    cd frontend
    npm run dev
    ```
2.  Open `http://localhost:5173`.
3.  **Test Scenarios:**
    -   **User Flow:** Register -> Login -> Browse -> Add to Cart -> Checkout -> Verify Library.
    -   **Developer Flow:** Register/Upgrade -> Dashboard -> Publish Game -> Edit Game.
    -   **Admin Flow:** Login (admin) -> Dashboard -> Approve Game -> Ban User.

## Continuous Integration (CI)

Currently, there is no CI pipeline configured. We recommend setting up GitHub Actions to run linting and tests on every push.

