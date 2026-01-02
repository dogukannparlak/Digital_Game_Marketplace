from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Table, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum
import uuid
import secrets
import string

def generate_public_id():
    """Generate a unique public ID like USR-A1B2C3D4"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(chars) for _ in range(8))
    return f"USR-{random_part}"

# ==================== ENUMS ====================

class UserRole(enum.Enum):
    """User role types"""
    USER = "user"           # Normal user - can buy games
    DEVELOPER = "developer" # Developer - can publish games
    ADMIN = "admin"         # Admin - can manage everything

class GameStatus(enum.Enum):
    """Game approval status"""
    PENDING = "pending"     # Waiting for admin approval
    APPROVED = "approved"   # Approved, visible in store
    REJECTED = "rejected"   # Rejected by admin
    SUSPENDED = "suspended" # Suspended from store

# ==================== ASSOCIATION TABLES ====================

# Game-Genre many-to-many
game_genres = Table('game_genres', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

# User wishlist - games user wants to buy
user_wishlist = Table('user_wishlist', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

# ==================== MODELS ====================

class User(Base):
    """User model with role-based access control"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True, default=generate_public_id)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Role system - default is USER
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

    # Profile info
    display_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    # Developer info (only used if role=DEVELOPER)
    developer_name = Column(String, nullable=True, unique=True)
    developer_verified = Column(Boolean, default=False)

    # Account status
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    banned_reason = Column(String, nullable=True)

    # Relationships
    orders = relationship("Order", back_populates="user")
    games = relationship("Game", back_populates="developer", foreign_keys="Game.developer_id")
    reviews = relationship("Review", back_populates="user")
    wishlist = relationship("Game", secondary=user_wishlist, backref="wishlisted_by")

class Game(Base):
    """Game model with approval status"""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    short_description = Column(String(500), nullable=True)
    price = Column(Float)
    discount_percent = Column(Integer, default=0)
    release_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Developer (User with role=DEVELOPER)
    developer_id = Column(Integer, ForeignKey("users.id"))

    # Approval system
    status = Column(SQLEnum(GameStatus), default=GameStatus.PENDING)
    rejection_reason = Column(String, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    # Game details
    cover_image_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)

    # Statistics
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)

    # Relationships
    developer = relationship("User", back_populates="games", foreign_keys=[developer_id])
    approver = relationship("User", foreign_keys=[approved_by])
    genres = relationship("Genre", secondary=game_genres, back_populates="games")
    order_items = relationship("OrderItem", back_populates="game")
    reviews = relationship("Review", back_populates="game")

class Genre(Base):
    """Game genre/category"""
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=True)
    description = Column(String, nullable=True)

    games = relationship("Game", secondary=game_genres, back_populates="genres")

class Review(Base):
    """Game reviews by users"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    rating = Column(Integer)  # 1-5
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    helpful_count = Column(Integer, default=0)

    user = relationship("User", back_populates="reviews")
    game = relationship("Game", back_populates="reviews")

class CartItem(Base):
    """Shopping cart item"""
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", backref="cart_items")
    game = relationship("Game")

class Order(Base):
    """Purchase order"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float)
    payment_status = Column(String, default="completed")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """Individual game in an order"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    purchase_price = Column(Float)
    discount_applied = Column(Integer, default=0)

    order = relationship("Order", back_populates="items")
    game = relationship("Game", back_populates="order_items")
