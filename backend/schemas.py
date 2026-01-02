from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from enum import Enum

# ==================== ENUMS ====================

class UserRole(str, Enum):
    USER = "user"
    DEVELOPER = "developer"
    ADMIN = "admin"

class GameStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

# ==================== GENRE SCHEMAS ====================

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    slug: Optional[str] = None
    description: Optional[str] = None

class Genre(GenreBase):
    id: int
    slug: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class UserStats(BaseModel):
    """User statistics"""
    total_games_owned: int
    total_spent: float
    total_reviews: int
    member_since: datetime

class DeveloperApplication(BaseModel):
    """Request to become a developer"""
    developer_name: str

    @field_validator('developer_name')
    @classmethod
    def developer_name_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Developer name must be at least 2 characters')
        if len(v) > 100:
            raise ValueError('Developer name must be at most 100 characters')
        return v

class UserPublic(BaseModel):
    """Public user info (for reviews, etc.)"""
    id: int
    public_id: str
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    public_id: str
    registration_date: datetime
    role: UserRole
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    developer_name: Optional[str] = None
    developer_verified: bool = False
    is_active: bool = True
    is_banned: bool = False

    class Config:
        from_attributes = True

class UserAdmin(User):
    """Extended user info for admin"""
    banned_reason: Optional[str] = None

# ==================== GAME SCHEMAS ====================

class GameBase(BaseModel):
    title: str
    description: str
    price: float

    @field_validator('title')
    @classmethod
    def title_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Title must be at least 2 characters')
        return v

    @field_validator('price')
    @classmethod
    def price_valid(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Price cannot be negative')
        return round(v, 2)

class GameCreate(GameBase):
    short_description: Optional[str] = None
    genre_ids: List[int] = []
    cover_image_url: Optional[str] = None
    trailer_url: Optional[str] = None

class AdminGameCreate(GameBase):
    """Admin can create games and assign to a developer"""
    short_description: Optional[str] = None
    genre_ids: List[int] = []
    cover_image_url: Optional[str] = None
    trailer_url: Optional[str] = None
    developer_id: int
    auto_approve: bool = True

class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = None
    discount_percent: Optional[int] = None
    cover_image_url: Optional[str] = None
    trailer_url: Optional[str] = None
    genre_ids: Optional[List[int]] = None

class DeveloperInfo(BaseModel):
    """Developer info embedded in Game"""
    id: int
    username: str
    developer_name: Optional[str] = None
    developer_verified: bool = False

    class Config:
        from_attributes = True

class Game(GameBase):
    id: int
    short_description: Optional[str] = None
    release_date: datetime
    status: GameStatus
    discount_percent: int = 0
    cover_image_url: Optional[str] = None
    trailer_url: Optional[str] = None
    developer: DeveloperInfo
    genres: List[Genre] = []
    total_sales: int = 0

    class Config:
        from_attributes = True

class GameAdmin(Game):
    """Extended game info for admin"""
    rejection_reason: Optional[str] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    total_revenue: float = 0.0

class GamePublic(GameBase):
    """Public game info (only approved games)"""
    id: int
    short_description: Optional[str] = None
    release_date: datetime
    discount_percent: int = 0
    cover_image_url: Optional[str] = None
    developer: DeveloperInfo
    genres: List[Genre] = []

    class Config:
        from_attributes = True

# ==================== REVIEW SCHEMAS ====================

class ReviewBase(BaseModel):
    rating: int
    content: str

    @field_validator('rating')
    @classmethod
    def rating_valid(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewCreate(ReviewBase):
    game_id: int

class Review(ReviewBase):
    id: int
    user: UserPublic
    game_id: int
    created_at: datetime
    helpful_count: int = 0

    class Config:
        from_attributes = True

# ==================== CART SCHEMAS ====================

class CartItemCreate(BaseModel):
    game_id: int

class CartItem(BaseModel):
    id: int
    game_id: int
    game_title: str
    game_price: float
    game_discount_percent: int = 0
    game_cover_image_url: Optional[str] = None
    added_at: datetime

    class Config:
        from_attributes = True

class Cart(BaseModel):
    items: List["CartItem"] = []
    total_items: int = 0
    subtotal: float = 0.0
    total_discount: float = 0.0
    total: float = 0.0

# ==================== ORDER SCHEMAS ====================

class GameSimple(BaseModel):
    """Simple game info for orders"""
    id: int
    title: str
    price: float
    cover_image_url: Optional[str] = None

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    game_id: int

class OrderItem(OrderItemBase):
    id: int
    purchase_price: float
    discount_applied: int = 0
    game: Optional[GameSimple] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    game_ids: List[int]

class Order(BaseModel):
    id: int
    order_date: datetime
    total_amount: float
    payment_status: str = "completed"
    items: List[OrderItem] = []

    class Config:
        from_attributes = True

# ==================== ADMIN SCHEMAS ====================

class AdminStats(BaseModel):
    """Admin dashboard statistics"""
    total_users: int
    total_developers: int
    total_games: int
    pending_games: int
    approved_games: int
    total_orders: int
    total_revenue: float

class UserRoleUpdate(BaseModel):
    """Change user role"""
    role: UserRole

class UserBanRequest(BaseModel):
    """Ban user request"""
    reason: str

class GameApprovalRequest(BaseModel):
    """Approve/reject game"""
    approved: bool
    reason: Optional[str] = None

# ==================== AUTH SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: UserRole
    developer_name: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None
