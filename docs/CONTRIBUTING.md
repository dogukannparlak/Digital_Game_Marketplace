# Contributing to Digital Game Marketplace

Thank you for your interest in contributing to the Digital Game Marketplace project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others. We want to create a welcoming environment for everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/digital-game-marketplace.git
    ```
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/my-new-feature
    ```

## Development Workflow

### Backend

1.  Navigate to the root directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn backend.main:app --reload
    ```

### Frontend

1.  Navigate to the `frontend` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## Coding Standards

### Python (Backend)

-   Follow **PEP 8** style guidelines.
-   Use **type hints** for function arguments and return values.
-   Keep functions small and focused.
-   Document complex logic with comments.

### JavaScript/React (Frontend)

-   Use **functional components** and **hooks**.
-   Follow **ESLint** rules configured in the project.
-   Use meaningful variable and component names.
-   Keep components modular and reusable.

## Commit Messages

-   Use clear and descriptive commit messages.
-   Start with a verb in the present tense (e.g., "Add feature", "Fix bug", "Update docs").
-   Reference issue numbers if applicable.

## Pull Requests

1.  Push your branch to your fork:
    ```bash
    git push origin feature/my-new-feature
    ```
2.  Open a **Pull Request** on the main repository.
3.  Provide a clear description of your changes.
4.  Wait for code review and address any feedback.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible, including steps to reproduce the bug.

Thank you for contributing!

