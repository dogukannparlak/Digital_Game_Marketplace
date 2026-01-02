# User Guide

A comprehensive guide for using the Digital Game Marketplace application.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Test Accounts](#test-accounts)
3. [User Features](#user-features)
4. [Developer Features](#developer-features)
5. [Admin Features](#admin-features)

---

## Getting Started

### Accessing the Application

After starting the servers, access the application at:

| Service | URL |
|---------|-----|
| **Main Application** | http://localhost:5173 |
| **API Documentation** | http://localhost:8000/docs |

### Creating an Account

1. Click **"Register"** in the navigation bar
2. Fill in the registration form:
   - Username (unique)
   - Email address
   - Password (minimum 6 characters)
3. Click **"Register"** to create your account
4. You'll be redirected to the login page

### Logging In

1. Click **"Login"** in the navigation bar
2. Enter your username and password
3. Click **"Sign In"**
4. You'll be redirected to the home page

---

## Test Accounts

The seeded database includes these test accounts:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| **Admin** | `admin` | `admin123` | Full system access |
| **Player** | `player` | `player123` | Regular user account |
| **Developer** | `rockstar_games` | `dev123` | Game developer account |

Additional developer accounts with games:
- `cd_projekt` / `dev123` (CD Projekt Red)
- `bethesda` / `dev123` (Bethesda Game Studios)
- `fromsoftware` / `dev123` (FromSoftware)
- `valve` / `dev123` (Valve Corporation)
- And many more...

---

## User Features

### Browsing Games

**Home Page:**
- View all approved games in the store
- Games display with cover image, title, price, and discount

**Filtering Options:**
- **Search:** Type in the search bar to find games by title
- **Genre:** Filter by game genre (Action, RPG, etc.)
- **Price Range:** Set minimum and maximum price

### Viewing Game Details

1. Click on any game card to view details
2. Game detail page shows:
   - Full description
   - Price and discounts
   - Developer information
   - Genres/tags
   - User reviews

### Adding to Cart

1. On a game detail page, click **"Add to Cart"**
2. If you already own the game, you'll see a message
3. Cart icon in navbar shows item count

### Managing Cart

1. Click the cart icon in the navigation bar
2. View all items in your cart with prices
3. See subtotal, discounts, and total
4. Remove individual items with the ✕ button
5. Clear entire cart with **"Clear Cart"**

### Checkout

1. In the cart page, click **"Checkout"**
2. Order is processed immediately
3. Games are added to your library
4. Redirected to order confirmation

### Viewing Library

1. Click **"Library"** in the navigation
2. See all games you own
3. View purchase date and price paid

### Order History

1. Click **"Orders"** or access from profile
2. View all past orders
3. See order date, total, and items purchased

### Managing Profile

1. Click your username or **"Profile"** in navigation
2. View and edit:
   - Display name
   - Bio
   - Avatar URL
3. View account statistics:
   - Games owned
   - Total spent
   - Reviews written

### Writing Reviews

1. Go to a game you own
2. Scroll to the reviews section
3. Rate the game (1-5 stars)
4. Write your review content
5. Submit the review

---

## Developer Features

### Becoming a Developer

1. Log in with a regular user account
2. Click **"Become Developer"** in navigation
3. Enter your studio/developer name
4. Submit the application
5. Your account is upgraded to developer role

### Developer Dashboard

Access via **"Developer Dashboard"** in navigation.

**Dashboard Shows:**
- Total games published
- Approved games count
- Pending approval count
- Total sales
- Total revenue

### Publishing a Game

1. From Developer Dashboard, click **"Publish New Game"**
2. Fill in game details:
   - **Title** (required)
   - **Description** (required)
   - **Short Description** (optional)
   - **Price** (required, 0 for free games)
   - **Cover Image URL** (optional)
   - **Trailer URL** (optional)
   - **Genres** (select multiple)
3. Click **"Submit for Review"**
4. Game status is set to **"Pending"**
5. Wait for admin approval

### Managing Your Games

**View All Your Games:**
- Developer Dashboard shows all your games
- Filter by status (All, Pending, Approved, Rejected)

**Game Status Indicators:**
- 🟡 **Pending** - Awaiting review
- 🟢 **Approved** - Live in store
- 🔴 **Rejected** - Declined (see reason)
- ⚫ **Suspended** - Removed from store

**Edit a Game:**
1. Click **"Edit"** on any game card
2. Modify game details
3. Save changes

**Delete a Game:**
- Only pending/rejected games can be deleted
- Click **"Delete"** and confirm

### Viewing Sales

Each approved game shows:
- Total copies sold
- Total revenue earned
- Current discount percentage

### Setting Discounts

1. Edit your game
2. Set **Discount Percent** (0-100)
3. Save changes
4. Discount applies immediately in store

---

## Admin Features

### Admin Dashboard

Access via **"Admin"** in navigation (admin only).

**Dashboard Statistics:**
- Total users
- Total developers
- Total games
- Pending approvals
- Approved games
- Total orders
- Total platform revenue

### User Management

Access via **"Manage Users"** in Admin Dashboard.

**List Users:**
- View all registered users
- Filter by role (User, Developer, Admin)
- Search by username or email

**User Actions:**
- View user details
- Change user role
- Ban/unban users

**Banning a User:**
1. Find the user in the list
2. Click **"Ban"**
3. Enter a reason for the ban
4. Confirm

**Unbanning:**
1. Find the banned user
2. Click **"Unban"**
3. User can log in again

### Game Management

Access via **"Manage Games"** in Admin Dashboard.

**Pending Games:**
- Shows all games awaiting approval
- Review game details before deciding

**Approving a Game:**
1. Review game title, description, price
2. Click **"Approve"**
3. Game appears in store immediately

**Rejecting a Game:**
1. Click **"Reject"**
2. Enter a reason for rejection
3. Developer sees the reason in their dashboard

**Suspending a Game:**
- Remove an approved game from store
1. Find the game
2. Click **"Suspend"**
3. Enter suspension reason
4. Game is hidden from store

**All Games View:**
- Filter by status
- Filter by developer
- Search by title

### Publishing Games (Admin)

Admins can publish games on behalf of developers:
1. Go to **"Publish Game"** in admin panel
2. Select a developer from dropdown
3. Fill in game details
4. Game is auto-approved

---

## Common Workflows

### Complete Purchase Flow

```
1. Browse Games → 2. View Details → 3. Add to Cart → 
4. Review Cart → 5. Checkout → 6. View in Library
```

### Developer Publishing Flow

```
1. Become Developer → 2. Create Game → 3. Submit for Review →
4. Wait for Approval → 5. Game Live → 6. Track Sales
```

### Admin Approval Flow

```
1. Check Pending Games → 2. Review Details → 
3. Approve/Reject → 4. Notify Developer (via status)
```

---

## Tips & Best Practices

### For Users
- Add games to cart during sales for discounts
- Check the store regularly for new releases
- Write reviews to help other players

### For Developers
- Write detailed, accurate descriptions
- Use high-quality cover images
- Set competitive prices
- Respond to rejection feedback

### For Admins
- Review pending games promptly
- Provide clear rejection reasons
- Monitor user reports
- Check platform statistics regularly

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Focus search bar (on Home page) |
| `Esc` | Close modals |

---

## Troubleshooting

### "Already Own This Game"
- You cannot purchase a game you already own
- Check your Library to confirm ownership

### "Game Not Found"
- Game may be pending approval
- Game may have been suspended
- Check the URL is correct

### "Cart Checkout Failed"
- Ensure all games in cart are still available
- Remove unavailable games and retry

### "Cannot Delete Game"
- Only pending/rejected games can be deleted
- Approved games must be suspended by admin first

### Login Issues
- Verify username and password
- Check if account is banned
- Clear browser cache/cookies

