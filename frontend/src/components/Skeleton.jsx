/**
 * Skeleton Components
 * Reusable skeleton loaders with glassmorphism styling
 */

// Base skeleton element with shimmer animation
export function Skeleton({ className = '', width, height, borderRadius }) {
  const style = {
    width: width || '100%',
    height: height || '1rem',
    borderRadius: borderRadius || '8px'
  };

  return (
    <div
      className={`skeleton ${className}`}
      style={style}
      aria-label="Loading..."
      role="status"
    />
  );
}

// Text skeleton - for single line text
export function SkeletonText({ width = '100%', height = '1rem', className = '' }) {
  return (
    <Skeleton
      className={`skeleton-text ${className}`}
      width={width}
      height={height}
      borderRadius="4px"
    />
  );
}

// Image skeleton - for images/covers
export function SkeletonImage({ width = '100%', height = '200px', className = '' }) {
  return (
    <Skeleton
      className={`skeleton-image ${className}`}
      width={width}
      height={height}
      borderRadius="12px"
    />
  );
}

// Button skeleton
export function SkeletonButton({ width = '120px', height = '40px', className = '' }) {
  return (
    <Skeleton
      className={`skeleton-button ${className}`}
      width={width}
      height={height}
      borderRadius="8px"
    />
  );
}

// Badge skeleton - for genre tags, etc.
export function SkeletonBadge({ width = '60px', className = '' }) {
  return (
    <Skeleton
      className={`skeleton-badge ${className}`}
      width={width}
      height="24px"
      borderRadius="9999px"
    />
  );
}

// Game Card Skeleton - matches glass-game-card structure
export function SkeletonGameCard() {
  return (
    <div className="skeleton-game-card">
      {/* Image */}
      <SkeletonImage height="180px" className="skeleton-game-image" />

      {/* Content */}
      <div className="skeleton-game-content">
        {/* Title */}
        <SkeletonText width="85%" height="1.25rem" />

        {/* Developer */}
        <SkeletonText width="60%" height="0.875rem" className="mt-2" />

        {/* Genre tags */}
        <div className="skeleton-genres">
          <SkeletonBadge width="50px" />
          <SkeletonBadge width="65px" />
        </div>

        {/* Price */}
        <div className="skeleton-price">
          <SkeletonText width="70px" height="1.5rem" />
        </div>
      </div>
    </div>
  );
}

// Game Cards Grid Skeleton - multiple cards
export function SkeletonGameGrid({ count = 8 }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonGameCard key={index} />
      ))}
    </div>
  );
}

// Game Detail Page Skeleton
export function SkeletonGameDetail() {
  return (
    <div className="glass-container">
      {/* Back button skeleton */}
      <SkeletonButton width="140px" height="36px" className="mb-6" />

      <div className="glass-card glass-card-lg">
        {/* Hero Image */}
        <div className="relative -mx-8 -mt-8 mb-8 rounded-t-lg overflow-hidden">
          <SkeletonImage height="24rem" borderRadius="0" />

          {/* Title overlay area */}
          <div className="absolute bottom-0 left-0 right-0 p-6 md:p-8">
            <SkeletonText width="60%" height="2.5rem" className="mb-2" />
            <SkeletonText width="30%" height="1rem" />
          </div>
        </div>

        {/* Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Content */}
          <div className="flex-1">
            {/* Genres */}
            <div className="flex flex-wrap gap-2 mb-6">
              <SkeletonBadge width="70px" />
              <SkeletonBadge width="85px" />
              <SkeletonBadge width="60px" />
            </div>

            {/* Short Description */}
            <SkeletonText width="100%" height="1.25rem" className="mb-2" />
            <SkeletonText width="90%" height="1.25rem" className="mb-6" />

            {/* About section */}
            <SkeletonText width="180px" height="1.5rem" className="mb-4" />
            <div className="space-y-2 mb-8">
              <SkeletonText width="100%" height="1rem" />
              <SkeletonText width="100%" height="1rem" />
              <SkeletonText width="95%" height="1rem" />
              <SkeletonText width="80%" height="1rem" />
              <SkeletonText width="100%" height="1rem" />
              <SkeletonText width="70%" height="1rem" />
            </div>

            {/* Reviews section */}
            <div className="pt-8 border-t border-white/10">
              <SkeletonText width="120px" height="1.5rem" className="mb-6" />

              {/* Review cards */}
              <div className="space-y-4">
                <SkeletonReviewCard />
                <SkeletonReviewCard />
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:w-80">
            <div className="glass-card">
              {/* Price */}
              <SkeletonText width="120px" height="2rem" className="mb-6" />

              {/* Buttons */}
              <SkeletonButton width="100%" height="48px" className="mb-3" />
              <SkeletonButton width="100%" height="48px" />

              {/* Stats */}
              <div className="mt-6 pt-6 border-t border-white/10 space-y-3">
                <div className="flex justify-between">
                  <SkeletonText width="80px" height="0.875rem" />
                  <SkeletonText width="100px" height="0.875rem" />
                </div>
                <div className="flex justify-between">
                  <SkeletonText width="70px" height="0.875rem" />
                  <SkeletonText width="120px" height="0.875rem" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Review Card Skeleton
export function SkeletonReviewCard() {
  return (
    <div className="glass-card glass-card-sm">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <Skeleton width="40px" height="40px" borderRadius="50%" />
          <SkeletonText width="100px" height="1rem" />
        </div>
        <SkeletonText width="80px" height="1rem" />
      </div>
      <SkeletonText width="100%" height="0.875rem" className="mb-1" />
      <SkeletonText width="85%" height="0.875rem" />
      <SkeletonText width="80px" height="0.75rem" className="mt-3" />
    </div>
  );
}

// Cart Item Skeleton
export function SkeletonCartItem() {
  return (
    <div className="glass-card glass-card-hover">
      <div className="flex gap-4">
        <SkeletonImage width="128px" height="128px" />
        <div className="flex-1 flex flex-col justify-between">
          <div>
            <SkeletonText width="70%" height="1.25rem" />
            <SkeletonText width="40%" height="0.875rem" className="mt-2" />
          </div>
          <div className="flex items-center justify-between mt-4">
            <SkeletonText width="80px" height="1.5rem" />
            <SkeletonButton width="80px" height="32px" />
          </div>
        </div>
      </div>
    </div>
  );
}

// Library Game Skeleton
export function SkeletonLibraryGame() {
  return (
    <div className="glass-card glass-card-hover">
      <div className="flex gap-4">
        <SkeletonImage width="120px" height="68px" />
        <div className="flex-1">
          <SkeletonText width="80%" height="1.125rem" />
          <SkeletonText width="50%" height="0.875rem" className="mt-2" />
        </div>
        <SkeletonButton width="80px" height="36px" />
      </div>
    </div>
  );
}

// Admin/Developer Game Card Skeleton
export function SkeletonAdminGameCard() {
  return (
    <div className="glass-card glass-card-hover">
      <SkeletonImage height="160px" className="mb-4" />
      <div className="flex justify-between items-start mb-2">
        <SkeletonText width="70%" height="1.25rem" />
        <SkeletonBadge width="70px" />
      </div>
      <SkeletonText width="50%" height="0.875rem" className="mb-2" />
      <SkeletonText width="100%" height="0.75rem" className="mb-1" />
      <SkeletonText width="85%" height="0.75rem" className="mb-4" />
      <div className="flex justify-between items-center mb-4">
        <SkeletonText width="60px" height="1.25rem" />
        <SkeletonText width="100px" height="0.75rem" />
      </div>
      <div className="flex gap-2">
        <SkeletonButton width="70px" height="32px" />
        <SkeletonButton width="70px" height="32px" />
      </div>
    </div>
  );
}

// Home Page Full Skeleton
export function SkeletonHomePage() {
  return (
    <div className="glass-container">
      {/* Hero Section Skeleton */}
      <div className="glass-card glass-card-lg mb-8 text-center relative overflow-hidden">
        <div className="relative z-10 py-4">
          <SkeletonText width="300px" height="3rem" className="mx-auto mb-4" />
          <SkeletonText width="400px" height="1.25rem" className="mx-auto" />
        </div>
      </div>

      {/* Filters Skeleton */}
      <div className="glass-card mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <Skeleton height="44px" />
          </div>
          <Skeleton width="192px" height="44px" />
        </div>
      </div>

      {/* Game Grid Skeleton */}
      <SkeletonGameGrid count={8} />

      {/* Stats Skeleton */}
      <div className="mt-8 text-center">
        <SkeletonText width="120px" height="0.875rem" className="mx-auto" />
      </div>
    </div>
  );
}

export default {
  Skeleton,
  SkeletonText,
  SkeletonImage,
  SkeletonButton,
  SkeletonBadge,
  SkeletonGameCard,
  SkeletonGameGrid,
  SkeletonGameDetail,
  SkeletonReviewCard,
  SkeletonCartItem,
  SkeletonLibraryGame,
  SkeletonAdminGameCard,
  SkeletonHomePage
};
