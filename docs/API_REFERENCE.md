# API Reference

Complete API documentation for the Digital Game Marketplace backend.

**Base URL:** `http://localhost:8000`

**Authentication:** JWT Bearer Token (obtained via `/token` endpoint)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Games](#games)
4. [Genres](#genres)
5. [Cart](#cart)
6. [Orders](#orders)
7. [Admin](#admin)

---

## Authentication

### Login

Obtain an access token for API authentication.

```http
POST /token
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | User's username |
| password | string | Yes | User's password |

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "player",
  "role": "user",
  "developer_name": null
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - Account is banned

---

### Get Current User

```http
GET /me
Authorization: Bearer {token}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "public_id": "USR-A1B2C3D4",
  "username": "player",
  "email": "player@gamestore.com",
  "registration_date": "2024-01-15T10:30:00",
  "role": "user",
  "display_name": "Game Player",
  "avatar_url": null,
  "bio": null,
  "developer_name": null,
  "developer_verified": false,
  "is_active": true,
  "is_banned": false
}
```

---

### Update Current User

```http
PUT /me
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "display_name": "New Display Name",
  "bio": "I love games!",
  "avatar_url": "https://example.com/avatar.png"
}
```

**Response:** `200 OK` - Updated user object

---

### Register New User

```http
POST /users/
Content-Type: application/json
```

**Request Body:**

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**Response:** `201 Created`

```json
{
  "id": 5,
  "public_id": "USR-X9Y8Z7W6",
  "username": "newuser",
  "email": "newuser@example.com",
  "role": "user"
}
```

**Error Responses:**
- `400 Bad Request` - Username or email already exists
- `422 Unprocessable Entity` - Validation error

---

### Become a Developer

Upgrade a user account to developer role.

```http
POST /become-developer
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "developer_name": "My Game Studio"
}
```

**Response:** `200 OK`

```json
{
  "message": "You are now a developer!",
  "developer_name": "My Game Studio",
  "role": "developer"
}
```

---

## Users

### Get User Statistics

```http
GET /users/me/stats
Authorization: Bearer {token}
```

**Response:** `200 OK`

```json
{
  "total_games_owned": 5,
  "total_spent": 149.95,
  "total_reviews": 3,
  "member_since": "2024-01-15T10:30:00"
}
```

---

### Get User Library

```http
GET /users/me/library
Authorization: Bearer {token}
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Grand Theft Auto V",
    "cover_image_url": "https://...",
    "purchase_date": "2024-02-01T15:00:00",
    "purchase_price": 29.99
  }
]
```

---

### Change Password

```http
PUT /users/me/password
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

**Response:** `200 OK`

```json
{
  "message": "Password changed successfully"
}
```

---

## Games

### List Games (Store)

Get all approved games in the store.

```http
GET /games/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Pagination offset (default: 0) |
| limit | int | Max results (default: 100) |
| genre_id | int | Filter by genre ID |
| search | string | Search in game titles |
| min_price | float | Minimum price filter |
| max_price | float | Maximum price filter |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Grand Theft Auto V",
    "description": "An open world action-adventure game...",
    "short_description": "Open world crime action",
    "price": 29.99,
    "discount_percent": 20,
    "release_date": "2024-01-01T00:00:00",
    "status": "approved",
    "cover_image_url": "https://...",
    "genres": [
      {"id": 1, "name": "Action"},
      {"id": 14, "name": "Open World"}
    ],
    "developer": {
      "id": 3,
      "developer_name": "Rockstar Games"
    }
  }
]
```

---

### Get Single Game

```http
GET /games/{game_id}
```

**Response:** `200 OK` - Game object

**Error:** `404 Not Found` - Game not found or not approved

---

### Get Game Reviews

```http
GET /games/{game_id}/reviews
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Pagination offset |
| limit | int | Max results (default: 50) |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "user_id": 2,
    "game_id": 1,
    "rating": 5,
    "content": "Amazing game!",
    "created_at": "2024-02-15T10:00:00",
    "helpful_count": 10,
    "user": {
      "username": "player",
      "display_name": "Game Player"
    }
  }
]
```

---

### Create Game (Developer)

```http
POST /games/
Authorization: Bearer {developer_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "My New Game",
  "description": "A detailed game description...",
  "short_description": "Brief description",
  "price": 19.99,
  "genre_ids": [1, 3, 10],
  "cover_image_url": "https://...",
  "trailer_url": "https://youtube.com/..."
}
```

**Response:** `201 Created`

> **Note:** Newly created games have `status: "pending"` and require admin approval.

---

### Get My Games (Developer)

```http
GET /games/developer/my-games
Authorization: Bearer {developer_token}
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status: pending, approved, rejected, suspended |

**Response:** `200 OK` - List of developer's games with all statuses

---

### Update Game (Developer)

```http
PUT /games/{game_id}
Authorization: Bearer {developer_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "price": 24.99,
  "discount_percent": 25
}
```

---

### Delete Game (Developer)

```http
DELETE /games/{game_id}
Authorization: Bearer {developer_token}
```

> **Note:** Only pending or rejected games can be deleted.

---

## Genres

### List All Genres

```http
GET /genres/
```

**Response:** `200 OK`

```json
[
  {"id": 1, "name": "Action", "slug": "action", "description": "Fast-paced action games"},
  {"id": 2, "name": "Adventure", "slug": "adventure", "description": "Story-driven exploration"},
  {"id": 3, "name": "RPG", "slug": "rpg", "description": "Role-playing games"}
]
```

---

### Get Genre by ID

```http
GET /genres/{genre_id}
```

---

### Get Games by Genre

```http
GET /genres/{genre_id}/games
```

---

## Cart

### Get Cart

```http
GET /cart/
Authorization: Bearer {token}
```

**Response:** `200 OK`

```json
{
  "items": [
    {
      "id": 1,
      "game_id": 5,
      "game_title": "Cyberpunk 2077",
      "game_price": 59.99,
      "game_discount_percent": 50,
      "game_cover_image_url": "https://...",
      "added_at": "2024-03-01T10:00:00"
    }
  ],
  "total_items": 1,
  "subtotal": 59.99,
  "total_discount": 30.00,
  "total": 29.99
}
```

---

### Add to Cart

```http
POST /cart/add/{game_id}
Authorization: Bearer {token}
```

**Response:** `200 OK` - Updated cart object

**Error Responses:**
- `404 Not Found` - Game not found
- `400 Bad Request` - Already own game or already in cart

---

### Remove from Cart

```http
DELETE /cart/remove/{game_id}
Authorization: Bearer {token}
```

---

### Clear Cart

```http
DELETE /cart/clear
Authorization: Bearer {token}
```

---

### Checkout Cart

```http
POST /cart/checkout
Authorization: Bearer {token}
```

**Response:** `200 OK` - Order object

---

## Orders

### Create Order

```http
POST /orders/
Authorization: Bearer {token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "game_ids": [1, 5, 12]
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "user_id": 2,
  "order_date": "2024-03-01T15:30:00",
  "total_amount": 89.97,
  "payment_status": "completed",
  "items": [
    {
      "game_id": 1,
      "game": {"title": "Grand Theft Auto V"},
      "purchase_price": 23.99,
      "discount_applied": 20
    }
  ]
}
```

---

### Get My Orders

```http
GET /orders/
Authorization: Bearer {token}
```

**Response:** `200 OK` - List of orders with items

---

### Get Order Details

```http
GET /orders/{order_id}
Authorization: Bearer {token}
```

---

## Admin

> **Note:** All admin endpoints require `role: "admin"`.

### Get Dashboard Statistics

```http
GET /admin/stats
Authorization: Bearer {admin_token}
```

**Response:** `200 OK`

```json
{
  "total_users": 150,
  "total_developers": 25,
  "total_games": 100,
  "pending_games": 5,
  "approved_games": 90,
  "total_orders": 500,
  "total_revenue": 15000.00
}
```

---

### List All Users

```http
GET /admin/users
Authorization: Bearer {admin_token}
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Pagination offset |
| limit | int | Max results (default: 50) |
| role | string | Filter by role: user, developer, admin |
| search | string | Search username, email, or developer name |

---

### Get User Details

```http
GET /admin/users/{user_id}
Authorization: Bearer {admin_token}
```

---

### Change User Role

```http
PUT /admin/users/{user_id}/role
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "role": "developer"
}
```

---

### Ban User

```http
POST /admin/users/{user_id}/ban
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "reason": "Violation of terms of service"
}
```

---

### Unban User

```http
POST /admin/users/{user_id}/unban
Authorization: Bearer {admin_token}
```

---

### List All Games (Admin)

```http
GET /admin/games
Authorization: Bearer {admin_token}
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status |
| developer_id | int | Filter by developer |

---

### Approve Game

```http
POST /admin/games/{game_id}/approve
Authorization: Bearer {admin_token}
```

---

### Reject Game

```http
POST /admin/games/{game_id}/reject
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "reason": "Inappropriate content"
}
```

---

### Suspend Game

```http
POST /admin/games/{game_id}/suspend
Authorization: Bearer {admin_token}
Content-Type: application/json
```

**Request Body:**

```json
{
  "reason": "Policy violation"
}
```

---

## Error Responses

All endpoints may return these common error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid data format |
| 500 | Internal Server Error |

**Error Response Format:**

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production, consider adding rate limiting middleware.

---

## Pagination

List endpoints support pagination via `skip` and `limit` parameters:

```http
GET /games/?skip=0&limit=20    # First 20 games
GET /games/?skip=20&limit=20   # Next 20 games
```

