# 📚 API Reference Documentation

## 📋 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Games](#games)
- [Cart](#cart)
- [Orders](#orders)
- [Users](#users)
- [Admin](#admin)
- [Genres](#genres)
- [Error Handling](#error-handling)

## Overview

**Base URL**: `http://localhost:8000`

**API Version**: `v2.0.0`

**Interactive Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication

The API uses JWT (JSON Web Token). Send a POST request to the `/token` endpoint to obtain a token.

**Header Format**:
```http
Authorization: Bearer <your_jwt_token>
```

### Response Format

**Successful Response**:
```json
{
  "id": 1,
  "title": "Game Title",
  "price": 29.99
}
```

**Error Response**:
```json
{
  "detail": "Error message here"
}
```

### Pagination

List endpoints support pagination:
```
GET /games?skip=0&limit=20
```

---

## Authentication

### POST /token
Login and obtain JWT token

**Request Body** (form-data):
```
username: string (required) - email or username
password: string (required)
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- `401 Unauthorized` - Invalid credentials

**Example (curl)**:
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=user123"
```

**Example (Python)**:
```python
import requests

response = requests.post(
    "http://localhost:8000/token",
    data={"username": "user@example.com", "password": "user123"}
)
token = response.json()["access_token"]
```

**Example (JavaScript)**:
```javascript
const response = await fetch('http://localhost:8000/token', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: 'username=user@example.com&password=user123'
});
const {access_token} = await response.json();
```

---

### POST /register
New user registration

**Request Body** (JSON):
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "role": "user",
  "registration_date": "2026-01-14T10:00:00",
  "is_active": true,
  "is_banned": false
}
```

**Errors**:
- `400 Bad Request` - Validation error
- `409 Conflict` - Email or username already in use

**Example**:
```javascript
const response = await fetch('http://localhost:8000/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'newuser',
    email: 'user@example.com',
    password: 'secure_password'
  })
});
```

---

### GET /me
Get current user information

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "public_id": "USR-A1B2C3D4",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "user",
  "display_name": "John Doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Game enthusiast",
  "registration_date": "2026-01-10T10:00:00",
  "is_active": true,
  "is_banned": false,
  "developer_name": null,
  "developer_verified": false
}
```

**Errors**:
- `401 Unauthorized` - Token invalid or missing

---

### POST /become-developer
Upgrade user to developer

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "developer_name": "Awesome Games Studio"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "role": "developer",
  "developer_name": "Awesome Games Studio",
  "developer_verified": false
}
```

**Errors**:
- `400 Bad Request` - Already a developer
- `409 Conflict` - Developer name already in use

---

## Games

### GET /games
List games (with filtering and search)

**Query Parameters**:
- `skip` (int, default=0) - Pagination offset
- `limit` (int, default=20) - Records per page
- `genre` (string, optional) - Genre filter
- `search` (string, optional) - Title search
- `min_price` (float, optional) - Minimum price
- `max_price` (float, optional) - Maximum price
- `status` (string, optional) - Game status (pending/approved/rejected/suspended)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Epic Adventure",
    "short_description": "An amazing RPG game",
    "price": 29.99,
    "discount_percent": 10,
    "final_price": 26.99,
    "cover_image_url": "https://example.com/cover.jpg",
    "status": "approved",
    "release_date": "2026-01-01T00:00:00",
    "developer_name": "Awesome Studio",
    "genres": ["RPG", "Adventure"],
    "average_rating": 4.5,
    "review_count": 120
  }
]
```

**Example**:
```bash
# All games
GET /games

# RPG games
GET /games?genre=RPG

# Price range search
GET /games?min_price=10&max_price=50

# Title search
GET /games?search=adventure
```

---

### GET /games/{game_id}
Get game details

**Path Parameters**:
- `game_id` (int) - Game ID

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Epic Adventure",
  "description": "A long detailed description...",
  "short_description": "An amazing RPG game",
  "price": 29.99,
  "discount_percent": 10,
  "final_price": 26.99,
  "cover_image_url": "https://example.com/cover.jpg",
  "trailer_url": "https://youtube.com/watch?v=...",
  "status": "approved",
  "release_date": "2026-01-01T00:00:00",
  "developer_id": 2,
  "developer_name": "Awesome Studio",
  "developer_verified": true,
  "genres": [
    {"id": 1, "name": "RPG", "slug": "rpg"},
    {"id": 2, "name": "Adventure", "slug": "adventure"}
  ],
  "average_rating": 4.5,
  "review_count": 120,
  "total_sales": 1500,
  "reviews": [
    {
      "id": 1,
      "user_id": 3,
      "username": "gamer123",
      "rating": 5,
      "content": "Amazing game!",
      "created_at": "2026-01-10T15:30:00"
    }
  ]
}
```

**Errors**:
- `404 Not Found` - Game not found

---

### POST /games
Publish new game (DEVELOPER or ADMIN)

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "title": "My New Game",
  "description": "Full game description",
  "short_description": "Brief description",
  "price": 29.99,
  "discount_percent": 0,
  "cover_image_url": "https://example.com/cover.jpg",
  "trailer_url": "https://youtube.com/watch?v=...",
  "genre_ids": [1, 2, 3]
}
```

**Response** (201 Created):
```json
{
  "id": 10,
  "title": "My New Game",
  "status": "pending",
  "developer_id": 2,
  "created_at": "2026-01-14T10:00:00"
}
```

**Errors**:
- `401 Unauthorized` - Token invalid
- `403 Forbidden` - User is not a DEVELOPER
- `400 Bad Request` - Validation error

---

### PUT /games/{game_id}
Update game (Owner or ADMIN)

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `game_id` (int) - Game ID

**Request Body** (JSON):
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "short_description": "Updated brief",
  "cover_image_url": "https://example.com/new-cover.jpg"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "title": "Updated Title",
  "updated_at": "2026-01-14T11:00:00"
}
```

**Errors**:
- `403 Forbidden` - Not the owner of the game
- `404 Not Found` - Game not found

---

### PUT /games/{game_id}/price
Update game price (Owner or ADMIN)

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "price": 39.99,
  "discount_percent": 20
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "price": 39.99,
  "discount_percent": 20,
  "final_price": 31.99
}
```

---

### DELETE /games/{game_id}
Delete game (Owner or ADMIN)

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (204 No Content)

**Errors**:
- `403 Forbidden` - Unauthorized
- `404 Not Found` - Game not found

---

### GET /games/developer/me
My published games (DEVELOPER)

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "My Game 1",
    "status": "approved",
    "total_sales": 100,
    "total_revenue": 2999.00
  },
  {
    "id": 2,
    "title": "My Game 2",
    "status": "pending",
    "total_sales": 0,
    "total_revenue": 0.00
  }
]
```

---

## Cart

### GET /cart
View cart

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "game_id": 5,
      "game_title": "Epic Adventure",
      "price": 29.99,
      "discount_percent": 10,
      "final_price": 26.99,
      "cover_image_url": "https://example.com/cover.jpg",
      "added_at": "2026-01-14T10:00:00"
    }
  ],
  "total": 26.99,
  "item_count": 1
}
```

---

### POST /cart/add/{game_id}
Add game to cart

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `game_id` (int) - Game ID to add

**Response** (200 OK):
```json
{
  "message": "Game added to cart",
  "cart_item_id": 1
}
```

**Errors**:
- `400 Bad Request` - Game already purchased
- `409 Conflict` - Game already in cart
- `404 Not Found` - Game not found

---

### DELETE /cart/remove/{game_id}
Remove game from cart

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `game_id` (int) - Game ID to remove

**Response** (200 OK):
```json
{
  "message": "Game removed from cart"
}
```

---

### POST /cart/checkout
Purchase games in cart

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "message": "Purchase successful",
  "order_id": 15,
  "total_amount": 26.99,
  "games_purchased": 1
}
```

**Errors**:
- `400 Bad Request` - Cart is empty

---

## Orders

### GET /orders
Order history

**Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=20)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "order_date": "2026-01-14T10:00:00",
    "total_amount": 59.98,
    "payment_status": "completed",
    "items": [
      {
        "id": 1,
        "game_id": 5,
        "game_title": "Epic Adventure",
        "purchase_price": 29.99,
        "discount_applied": 10
      },
      {
        "id": 2,
        "game_id": 8,
        "game_title": "Space Shooter",
        "purchase_price": 29.99,
        "discount_applied": 0
      }
    ]
  }
]
```

---

### GET /orders/{order_id}
Order details

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `order_id` (int) - Order ID

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 3,
  "order_date": "2026-01-14T10:00:00",
  "total_amount": 29.99,
  "payment_status": "completed",
  "items": [
    {
      "id": 1,
      "game_id": 5,
      "game_title": "Epic Adventure",
      "purchase_price": 29.99,
      "discount_applied": 10,
      "final_price": 26.99
    }
  ]
}
```

**Errors**:
- `403 Forbidden` - Order belongs to another user
- `404 Not Found` - Order not found

---

### GET /orders/library
User's library (owned games)

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "game_id": 5,
    "title": "Epic Adventure",
    "cover_image_url": "https://example.com/cover.jpg",
    "purchase_date": "2026-01-14T10:00:00",
    "purchase_price": 26.99
  }
]
```

---

## Users

### GET /users/{user_id}
View user profile

**Path Parameters**:
- `user_id` (int) - User ID

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "johndoe",
  "display_name": "John Doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Game enthusiast",
  "role": "user",
  "registration_date": "2026-01-10T10:00:00",
  "developer_name": null,
  "developer_verified": false
}
```

---

### PUT /users/me
Update own profile

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "display_name": "New Display Name",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "bio": "Updated bio text"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "display_name": "New Display Name",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "bio": "Updated bio text"
}
```

---

## Admin

**Note**: All admin endpoints require ADMIN role

### GET /admin/games/pending
Games pending approval

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
[
  {
    "id": 10,
    "title": "New Game",
    "developer_id": 2,
    "developer_name": "Awesome Studio",
    "status": "pending",
    "submitted_at": "2026-01-14T09:00:00"
  }
]
```

---

### PUT /admin/games/{game_id}/approve
Approve game

**Headers**:
```
Authorization: Bearer <token>
```

**Path Parameters**:
- `game_id` (int) - Game ID to approve

**Response** (200 OK):
```json
{
  "id": 10,
  "status": "approved",
  "approved_by": 1,
  "approved_at": "2026-01-14T10:00:00"
}
```

---

### PUT /admin/games/{game_id}/reject
Reject game

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "reason": "Does not meet quality standards"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "status": "rejected",
  "rejection_reason": "Does not meet quality standards"
}
```

---

### PUT /admin/games/{game_id}/suspend
Suspend game

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "reason": "Violates terms of service"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "status": "suspended",
  "suspension_reason": "Violates terms of service"
}
```

---

### PUT /admin/users/{user_id}/ban
Ban user

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "reason": "Spam and abuse"
}
```

**Response** (200 OK):
```json
{
  "id": 5,
  "is_banned": true,
  "banned_reason": "Spam and abuse"
}
```

---

### PUT /admin/users/{user_id}/unban
Unban user

**Headers**:
```
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": 5,
  "is_banned": false,
  "banned_reason": null
}
```

---

### GET /admin/users
List all users

**Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=50)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "role": "user",
    "is_banned": false,
    "registration_date": "2026-01-01T00:00:00"
  }
]
```

---

### GET /admin/games
Tüm oyunları listele (status dahil)

**Headers**:
```
Authorization: Bearer <token>
```

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=50)
- `status` (string, optional) - pending/approved/rejected/suspended

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Game Title",
    "status": "approved",
    "developer_name": "Studio Name",
    "total_sales": 100
  }
]
```

---

## Genres

### GET /genres
Tüm kategorileri listele

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "RPG",
    "slug": "rpg",
    "description": "Role-playing games"
  },
  {
    "id": 2,
    "name": "Action",
    "slug": "action",
    "description": "Action games"
  }
]
```

---

### POST /genres
Yeni kategori oluştur (ADMIN)

**Headers**:
```
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "name": "Simulation",
  "slug": "simulation",
  "description": "Simulation games"
}
```

**Response** (201 Created):
```json
{
  "id": 10,
  "name": "Simulation",
  "slug": "simulation",
  "description": "Simulation games"
}
```

---

## Error Handling

### Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Başarılı GET/PUT isteği |
| 201 | Created | Başarılı POST (kayıt oluşturuldu) |
| 204 | No Content | Başarılı DELETE |
| 400 | Bad Request | Validation hatası, geçersiz input |
| 401 | Unauthorized | Token geçersiz veya eksik |
| 403 | Forbidden | Yetkisiz erişim |
| 404 | Not Found | Kaynak bulunamadı |
| 409 | Conflict | Duplicate kayıt |
| 422 | Unprocessable Entity | Pydantic validation error |
| 500 | Internal Server Error | Sunucu hatası |

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

**Validation Error (422)**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Common Errors

**Authentication Required**:
```json
{
  "detail": "Not authenticated"
}
```

**Insufficient Permissions**:
```json
{
  "detail": "Insufficient permissions"
}
```

**Resource Not Found**:
```json
{
  "detail": "Game not found"
}
```

**Duplicate Resource**:
```json
{
  "detail": "Username already registered"
}
```

---

## Rate Limiting

*Şu anda aktif değil, production için önerilir*

Örnek rate limit yapılandırması:
- Anonymous: 100 req/hour
- Authenticated: 1000 req/hour
- Admin: Unlimited

---

## Versioning

API versiyonlama şu anda kullanılmıyor. Gelecekte `/v1/`, `/v2/` prefix'leri eklenebilir.

---

📖 **Daha fazla bilgi için:**
- [Swagger UI](http://localhost:8000/docs) - İnteraktif API testi
- [Architecture](ARCHITECTURE.md) - Sistem mimarisi
- [Testing](TESTING.md) - Test dokümantasyonu
