# Performance Optimization

Strategies for keeping collaborative features smooth at scale.

## Cursor Rendering Optimization

**Use CSS transforms instead of top/left**:
```javascript
// Slower - triggers layout
<div style={{ left: `${x}px`, top: `${y}px` }} />

// Faster - GPU accelerated
<div style={{ transform: `translate(${x}px, ${y}px)` }} />
```

**Memoize cursor components**:
```javascript
const RemoteCursor = React.memo(({ user, position }) => {
  return (
    <div
      style={{
        position: 'absolute',
        transform: `translate(${position.x}px, ${position.y}px)`,
        willChange: 'transform'
      }}
    >
      {/* cursor UI */}
    </div>
  );
}, (prev, next) => {
  // Only re-render if position actually changed
  return prev.position.x === next.position.x &&
         prev.position.y === next.position.y &&
         prev.user.color === next.user.color;
});
```

**Use requestAnimationFrame for smooth updates**:
```javascript
let pendingUpdate = null;

function updateCursor(userId, position) {
  if (pendingUpdate) return;

  pendingUpdate = requestAnimationFrame(() => {
    setCursors(prev => ({
      ...prev,
      [userId]: { ...prev[userId], position }
    }));
    pendingUpdate = null;
  });
}
```

## Throttling and Debouncing

**Throttle cursor movements**:
```javascript
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      func(...args);
    }
  };
}

const sendCursorUpdate = throttle((position) => {
  websocket.send(JSON.stringify({
    type: 'cursor:move',
    position
  }));
}, 50); // Max 20 updates per second
```

**Debounce presence UI updates**:
```javascript
function debounce(func, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

const updatePresenceIndicator = debounce((users) => {
  setActiveCount(Object.keys(users).length);
}, 500);
```

## Viewport Culling

Render only cursors visible in viewport:

```javascript
function CursorOverlay({ users }) {
  const [viewportBounds, setViewportBounds] = useState({
    left: 0, top: 0,
    right: window.innerWidth,
    bottom: window.innerHeight
  });

  const visibleCursors = Object.entries(users).filter(([id, user]) => {
    const x = user.cursor.x * window.innerWidth;
    const y = user.cursor.y * window.innerHeight;

    return x >= viewportBounds.left && x <= viewportBounds.right &&
           y >= viewportBounds.top && y <= viewportBounds.bottom;
  });

  return visibleCursors.map(([id, user]) => (
    <RemoteCursor key={id} user={user} />
  ));
}
```

For canvas-based applications with zoom/pan:
```javascript
function isInViewport(position, viewport) {
  const worldX = position.x * canvasWidth;
  const worldY = position.y * canvasHeight;

  const screenX = (worldX - viewport.x) * viewport.zoom;
  const screenY = (worldY - viewport.y) * viewport.zoom;

  return screenX >= 0 && screenX <= window.innerWidth &&
         screenY >= 0 && screenY <= window.innerHeight;
}
```

## State Update Batching

**Batch multiple cursor updates**:
```javascript
let updateQueue = {};
let batchTimeout = null;

function queueCursorUpdate(userId, position) {
  updateQueue[userId] = position;

  if (!batchTimeout) {
    batchTimeout = setTimeout(() => {
      setCursors(prev => {
        const next = { ...prev };
        Object.entries(updateQueue).forEach(([id, pos]) => {
          if (next[id]) {
            next[id].cursor = pos;
          }
        });
        return next;
      });

      updateQueue = {};
      batchTimeout = null;
    }, 16); // ~60fps
  }
}
```

**Use React transitions for non-critical updates**:
```javascript
import { useTransition } from 'react';

function PresenceList({ users }) {
  const [isPending, startTransition] = useTransition();

  function handleUserJoin(newUser) {
    startTransition(() => {
      setUsers(prev => ({ ...prev, [newUser.id]: newUser }));
    });
  }

  return (
    <div style={{ opacity: isPending ? 0.7 : 1 }}>
      {/* user list */}
    </div>
  );
}
```

## Memory Management

**Clean up stale cursors**:
```javascript
useEffect(() => {
  const cleanupInterval = setInterval(() => {
    const now = Date.now();
    const STALE_THRESHOLD = 30000; // 30 seconds

    setUsers(prev => {
      const active = {};
      Object.entries(prev).forEach(([id, user]) => {
        if (now - user.lastSeen < STALE_THRESHOLD) {
          active[id] = user;
        }
      });
      return active;
    });
  }, 10000); // Check every 10 seconds

  return () => clearInterval(cleanupInterval);
}, []);
```

**Limit message history**:
```javascript
const messageBuffer = useRef([]);
const MAX_BUFFER_SIZE = 1000;

function addMessage(message) {
  messageBuffer.current.push(message);

  if (messageBuffer.current.length > MAX_BUFFER_SIZE) {
    messageBuffer.current = messageBuffer.current.slice(-MAX_BUFFER_SIZE);
  }
}
```

## Network Optimization

**Binary message format** (for high-frequency updates):
```javascript
// Encode cursor position as binary
function encodeCursorUpdate(userId, x, y) {
  const buffer = new ArrayBuffer(20);
  const view = new DataView(buffer);

  // Message type (1 byte)
  view.setUint8(0, 1); // 1 = cursor:move

  // User ID as 32-bit integer (4 bytes)
  view.setUint32(1, parseInt(userId));

  // X and Y as floats (4 bytes each)
  view.setFloat32(5, x);
  view.setFloat32(9, y);

  // Timestamp (8 bytes)
  view.setBigInt64(13, BigInt(Date.now()));

  return buffer;
}

// Send binary data
websocket.send(encodeCursorUpdate(userId, 0.5, 0.7));

// Decode on receive
websocket.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    const view = new DataView(event.data);
    const type = view.getUint8(0);

    if (type === 1) { // cursor:move
      const userId = view.getUint32(1).toString();
      const x = view.getFloat32(5);
      const y = view.getFloat32(9);

      updateCursor(userId, { x, y });
    }
  }
};
```

Binary format reduces message size from ~80 bytes (JSON) to 20 bytes.

**Differential updates** (send only what changed):
```javascript
// Track previous state
const previousPositions = useRef({});

function sendCursorUpdate(userId, position) {
  const prev = previousPositions.current[userId];

  // Only send if position changed significantly (> 1px)
  if (prev && Math.abs(prev.x - position.x) < 0.001 &&
              Math.abs(prev.y - position.y) < 0.001) {
    return;
  }

  previousPositions.current[userId] = position;
  websocket.send(JSON.stringify({
    type: 'cursor:move',
    userId,
    position
  }));
}
```

## Scaling to Many Users

**Spatial partitioning** (for 100+ users):
```javascript
// Divide canvas into grid cells
const GRID_SIZE = 5;

function getGridCell(position) {
  const cellX = Math.floor(position.x * GRID_SIZE);
  const cellY = Math.floor(position.y * GRID_SIZE);
  return `${cellX},${cellY}`;
}

// Only broadcast to users in nearby cells
socket.on('cursor:move', (data) => {
  const cell = getGridCell(data.position);
  const nearbyCells = getNearbyCells(cell);

  nearbyCells.forEach(nearbyCell => {
    io.to(`cell:${nearbyCell}`).emit('cursor:move', data);
  });
});
```

**User limit with priority**:
```javascript
// Show only closest N users
const MAX_CURSORS = 20;

function getClosestUsers(users, myPosition) {
  return Object.entries(users)
    .map(([id, user]) => ({
      id,
      user,
      distance: Math.hypot(
        user.cursor.x - myPosition.x,
        user.cursor.y - myPosition.y
      )
    }))
    .sort((a, b) => a.distance - b.distance)
    .slice(0, MAX_CURSORS);
}
```

These illustrate the principle. Consider what fits your context.
