# Presence System Implementation

Presence systems track who's active in a collaborative session.

## State Structure

**User presence data**:
```javascript
const presenceState = {
  users: {
    'user-123': {
      id: 'user-123',
      name: 'Alice',
      color: '#FF6B6B',
      joinedAt: 1645564800000,
      lastSeen: 1645564900000,
      cursor: { x: 0.5, y: 0.3, visible: true }
    }
  }
};
```

Separate cursor from other presence data if updating cursor frequently.

## Join Flow

**Client sends join message**:
```javascript
const joinMessage = {
  type: 'presence:join',
  user: {
    id: currentUserId,
    name: currentUserName,
    sessionId: generateSessionId()
  }
};

websocket.send(JSON.stringify(joinMessage));
```

**Server broadcasts to others**:
```javascript
// Server-side
socket.on('presence:join', (data) => {
  // Validate user identity
  const user = authenticateUser(data.user);

  // Assign color
  user.color = assignColor(user.id);

  // Add to active users
  activeUsers.set(socket.id, user);

  // Broadcast to all except sender
  socket.broadcast.emit('presence:userJoined', user);

  // Send current users list to joiner
  socket.emit('presence:currentUsers', Array.from(activeUsers.values()));
});
```

**Client handles join**:
```javascript
websocket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);

  if (message.type === 'presence:userJoined') {
    setUsers(prev => ({
      ...prev,
      [message.user.id]: {
        ...message.user,
        lastSeen: Date.now(),
        cursor: { x: 0, y: 0, visible: false }
      }
    }));
  }

  if (message.type === 'presence:currentUsers') {
    const usersMap = {};
    message.users.forEach(user => {
      usersMap[user.id] = {
        ...user,
        lastSeen: Date.now(),
        cursor: { x: 0, y: 0, visible: false }
      };
    });
    setUsers(usersMap);
  }
});
```

## Leave Flow

**Explicit leave** (user closes tab):
```javascript
useEffect(() => {
  const handleBeforeUnload = () => {
    websocket.send(JSON.stringify({ type: 'presence:leave' }));
  };

  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, []);
```

**Timeout-based leave** (handle crashes/network loss):
```javascript
// Client sends heartbeat
setInterval(() => {
  websocket.send(JSON.stringify({ type: 'presence:heartbeat' }));
}, 30000); // Every 30 seconds

// Server tracks last heartbeat
socket.on('presence:heartbeat', () => {
  activeUsers.get(socket.id).lastSeen = Date.now();
});

// Server checks for stale connections
setInterval(() => {
  const now = Date.now();
  const TIMEOUT = 60000; // 1 minute

  activeUsers.forEach((user, socketId) => {
    if (now - user.lastSeen > TIMEOUT) {
      activeUsers.delete(socketId);
      io.emit('presence:userLeft', { userId: user.id });
    }
  });
}, 10000); // Check every 10 seconds
```

**Client handles leave**:
```javascript
if (message.type === 'presence:userLeft') {
  setUsers(prev => {
    const next = { ...prev };
    delete next[message.userId];
    return next;
  });
}
```

## Presence Indicators UI

**User list component**:
```jsx
function PresenceIndicators({ users }) {
  const activeUsers = Object.values(users).filter(u => u.id !== currentUserId);

  if (activeUsers.length === 0) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 16,
      right: 16,
      display: 'flex',
      gap: 8,
      alignItems: 'center'
    }}>
      {activeUsers.map(user => (
        <div
          key={user.id}
          style={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            backgroundColor: user.color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: 14,
            fontWeight: 'bold',
            cursor: 'pointer',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}
          title={user.name}
        >
          {user.name.charAt(0).toUpperCase()}
        </div>
      ))}
      <span style={{ fontSize: 14, color: '#666' }}>
        {activeUsers.length} online
      </span>
    </div>
  );
}
```

## Reconnection Handling

**Client tracks connection state**:
```javascript
const [connectionState, setConnectionState] = useState('connected');

websocket.onclose = () => {
  setConnectionState('disconnected');
  attemptReconnect();
};

function attemptReconnect() {
  setTimeout(() => {
    setConnectionState('reconnecting');
    websocket = new WebSocket(WS_URL);
    setupWebSocketHandlers();
  }, 1000);
}
```

**Preserve session on reconnect**:
```javascript
// Store sessionId
const sessionId = useRef(generateSessionId());

// On reconnect, rejoin with same sessionId
const joinMessage = {
  type: 'presence:join',
  user: {
    id: currentUserId,
    name: currentUserName,
    sessionId: sessionId.current // Reuse session
  }
};
```

**Server recognizes returning session**:
```javascript
socket.on('presence:join', (data) => {
  const existingSession = findSession(data.user.sessionId);

  if (existingSession) {
    // Restore previous state
    activeUsers.set(socket.id, existingSession);
    socket.emit('presence:restored', existingSession);
  } else {
    // New session
    handleNewJoin(data);
  }
});
```

These illustrate the principle. Consider what fits your context.
