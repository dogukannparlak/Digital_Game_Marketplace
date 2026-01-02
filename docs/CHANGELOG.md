# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-03-15

### Added
-   **Role-Based Access Control (RBAC):** Distinct roles for Users, Developers, and Admins.
-   **Developer Dashboard:** Interface for developers to publish and manage games.
-   **Admin Dashboard:** Comprehensive panel for user management, game approval, and statistics.
-   **Game Approval Workflow:** New status system (Pending -> Approved/Rejected/Suspended).
-   **Shopping Cart:** Full cart functionality with discount support.
-   **Order System:** Purchase history and order tracking.
-   **Review System:** Users can rate and review games.
-   **Search & Filtering:** Advanced game search by genre, price, and title.
-   **JWT Authentication:** Secure token-based login system.

### Changed
-   Migrated frontend to **React 19** and **Vite**.
-   Updated UI to use **TailwindCSS 4**.
-   Refactored backend structure into modular routers.
-   Improved database schema with proper relationships.

### Fixed
-   Resolved issues with user session persistence.
-   Fixed calculation errors in cart totals.
-   Addressed security vulnerabilities in API endpoints.

## [1.0.0] - 2023-12-01

### Added
-   Initial release of the Digital Game Marketplace.
-   Basic user registration and login.
-   Simple game listing and details page.
-   Basic "Buy Now" functionality.

