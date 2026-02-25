# Cursor Tracking Implementation

This reference provides implementation patterns for cursor tracking. Adapt these principles to your framework and requirements.

## Cursor Position Capture

**Throttling approach**:
```javascript
// Throttle to 50ms intervals
let lastSent = 0;
const THROTTLE_MS = 50;

function handleMouseMove(event) {
  const now = Date.now();
  if (now - lastSent < THROTTLE_MS) return;

  lastSent = now;
  const position = {
    x: event.clientX / window.innerWidth,  // Percentage
    y: event.clientY / window.innerHeight
  };

  sendCursorUpdate(position);
}
```

Using percentages makes positions work across different screen sizes. Absolute coordinates work if all users share the same canvas/viewport dimensions.

**Event binding**:
```javascript
useEffect(() => {
  const handleMove = throttle(handleMouseMove, 50);
  window.addEventListener('mousemove', handleMove);

  return () => window.removeEventListener('mousemove', handleMove);
}, []);
```

Clean up listeners on unmount to prevent memory leaks.

## Cursor Rendering

**Overlay component**:
```jsx
function RemoteCursor({ user, position }) {
  return (
    <div
      style={{
        position: 'absolute',
        left: `${position.x * 100}%`,
        top: `${position.y * 100}%`,
        pointerEvents: 'none',
        transform: 'translate(-50%, -50%)',
        zIndex: 9999,
        transition: 'left 0.1s, top 0.1s' // Smooth movement
      }}
    >
      <div style={{
        width: 12,
        height: 12,
        borderRadius: '50%',
        backgroundColor: user.color,
        border: '2px solid white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
      }} />
      <div style={{
        marginTop: 4,
        padding: '2px 6px',
        backgroundColor: user.color,
        color: 'white',
        fontSize: 11,
        borderRadius: 4,
        whiteSpace: 'nowrap'
      }}>
        {user.name}
      </div>
    </div>
  );
}
```

Use GPU-accelerated CSS transforms for smooth 60fps rendering. The `pointerEvents: 'none'` prevents cursors from blocking interactions.

**Rendering all cursors**:
```jsx
function CursorOverlay({ users }) {
  return (
    <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none' }}>
      {Object.entries(users).map(([userId, user]) =>
        user.cursor.visible && (
          <RemoteCursor key={userId} user={user} position={user.cursor} />
        )
      )}
    </div>
  );
}
```

## Hiding Cursors

Hide cursor when user leaves the viewport context:

```javascript
useEffect(() => {
  const handleMouseLeave = () => {
    sendCursorHide();
  };

  document.addEventListener('mouseleave', handleMouseLeave);
  return () => document.removeEventListener('mouseleave', handleMouseLeave);
}, []);
```

Also hide when switching tabs or views:

```javascript
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      sendCursorHide();
    }
  };

  document.addEventListener('visibilitychange', handleVisibilityChange);
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
}, []);
```

## Color Assignment

Generate consistent colors from user IDs:

```javascript
function getUserColor(userId) {
  // Hash userId to number
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = userId.charCodeAt(i) + ((hash << 5) - hash);
  }

  // Convert to HSL for better color distribution
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 70%, 50%)`;
}
```

Or use a predefined palette:

```javascript
const COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
  '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
];

function getUserColor(userId, users) {
  const existingColors = Object.values(users).map(u => u.color);
  const available = COLORS.filter(c => !existingColors.includes(c));
  return available[0] || COLORS[Math.floor(Math.random() * COLORS.length)];
}
```

These illustrate the principle. Consider what fits your context.
