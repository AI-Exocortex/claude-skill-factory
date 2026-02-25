# WebSocket Protocol Design

Define message types and payloads for real-time collaboration.

## Message Structure

All messages follow this structure:
```javascript
{
  type: string,      // Message type identifier
  timestamp: number, // Client timestamp
  ...payload         // Type-specific data
}
```

## Message Types

### Presence Messages

**presence:join** - User joins session
```javascript
{
  type: 'presence:join',
  timestamp: 1645564800000,
  user: {
    id: 'user-123',
    name: 'Alice',
    sessionId: 'session-abc'
  }
}
```

**presence:leave** - User leaves session
```javascript
{
  type: 'presence:leave',
  timestamp: 1645564900000,
  userId: 'user-123'
}
```

**presence:heartbeat** - Keep-alive ping
```javascript
{
  type: 'presence:heartbeat',
  timestamp: 1645564850000
}
```

**presence:userJoined** - Broadcast when user joins
```javascript
{
  type: 'presence:userJoined',
  timestamp: 1645564800000,
  user: {
    id: 'user-123',
    name: 'Alice',
    color: '#FF6B6B',
    sessionId: 'session-abc'
  }
}
```

**presence:userLeft** - Broadcast when user leaves
```javascript
{
  type: 'presence:userLeft',
  timestamp: 1645564900000,
  userId: 'user-123'
}
```

**presence:currentUsers** - Initial user list on join
```javascript
{
  type: 'presence:currentUsers',
  timestamp: 1645564800000,
  users: [
    { id: 'user-456', name: 'Bob', color: '#4ECDC4' },
    { id: 'user-789', name: 'Carol', color: '#45B7D1' }
  ]
}
```

### Cursor Messages

**cursor:move** - Update cursor position
```javascript
{
  type: 'cursor:move',
  timestamp: 1645564850000,
  userId: 'user-123',
  position: {
    x: 0.45,  // Percentage of viewport width (0-1)
    y: 0.67   // Percentage of viewport height (0-1)
  }
}
```

Use percentages for viewport-relative positioning. Use absolute coordinates if working with fixed canvas dimensions:
```javascript
{
  position: {
    x: 450,  // Pixels from left
    y: 670   // Pixels from top
  }
}
```

**cursor:hide** - Hide cursor (user left viewport)
```javascript
{
  type: 'cursor:hide',
  timestamp: 1645564900000,
  userId: 'user-123'
}
```

## Broadcast Patterns

**Server broadcast strategy**:
```javascript
// Broadcast to all connected clients
io.emit('presence:userJoined', userData);

// Broadcast to all except sender
socket.broadcast.emit('cursor:move', cursorData);

// Send to specific user
io.to(socketId).emit('presence:currentUsers', userList);
```

**Client filtering**:
```javascript
// Client ignores own cursor updates
websocket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);

  if (message.type === 'cursor:move' && message.userId !== currentUserId) {
    updateRemoteCursor(message.userId, message.position);
  }
});
```

## Rate Limiting

**Client-side throttling**:
```javascript
// Throttle cursor updates to 50ms
const throttledSend = throttle((position) => {
  websocket.send(JSON.stringify({
    type: 'cursor:move',
    timestamp: Date.now(),
    userId: currentUserId,
    position
  }));
}, 50);
```

**Server-side rate limiting**:
```javascript
const userRateLimits = new Map();

socket.on('cursor:move', (data) => {
  const userId = data.userId;
  const now = Date.now();
  const lastUpdate = userRateLimits.get(userId) || 0;

  // Enforce minimum 40ms between updates (max 25 updates/sec)
  if (now - lastUpdate < 40) {
    return; // Drop message
  }

  userRateLimits.set(userId, now);
  socket.broadcast.emit('cursor:move', data);
});
```

## Error Handling

**Connection errors**:
```javascript
websocket.onerror = (error) => {
  console.error('WebSocket error:', error);
  setConnectionState('error');
};

websocket.onclose = (event) => {
  if (event.code === 1000) {
    // Normal closure
    setConnectionState('disconnected');
  } else {
    // Abnormal closure - attempt reconnect
    setConnectionState('reconnecting');
    setTimeout(attemptReconnect, 1000);
  }
};
```

**Invalid messages**:
```javascript
websocket.addEventListener('message', (event) => {
  try {
    const message = JSON.parse(event.data);

    // Validate message structure
    if (!message.type || !message.timestamp) {
      console.warn('Invalid message format:', message);
      return;
    }

    // Route to handler
    handleMessage(message);
  } catch (error) {
    console.error('Failed to parse message:', error);
  }
});
```

## Security Considerations

**Server-side validation**:
```javascript
socket.on('cursor:move', (data) => {
  // Verify user owns this socket
  const user = activeUsers.get(socket.id);
  if (!user || user.id !== data.userId) {
    socket.disconnect();
    return;
  }

  // Validate position bounds
  if (data.position.x < 0 || data.position.x > 1 ||
      data.position.y < 0 || data.position.y > 1) {
    return; // Ignore invalid positions
  }

  // Broadcast validated update
  socket.broadcast.emit('cursor:move', {
    type: 'cursor:move',
    timestamp: Date.now(), // Use server time
    userId: user.id,
    position: data.position
  });
});
```

**Input sanitization**:
```javascript
socket.on('presence:join', (data) => {
  // Sanitize user name
  const sanitizedName = sanitizeHtml(data.user.name, {
    allowedTags: [],
    allowedAttributes: {}
  }).substring(0, 50); // Limit length

  const user = {
    id: data.user.id,
    name: sanitizedName,
    sessionId: data.user.sessionId
  };

  handleUserJoin(user);
});
```

## Protocol Versioning

Include version in initial handshake:

```javascript
// Client sends version on connect
websocket.onopen = () => {
  websocket.send(JSON.stringify({
    type: 'protocol:version',
    version: '1.0.0'
  }));
};

// Server validates version
socket.on('protocol:version', (data) => {
  if (!isCompatible(data.version)) {
    socket.emit('protocol:incompatible', {
      serverVersion: CURRENT_VERSION,
      clientVersion: data.version
    });
    socket.disconnect();
  }
});
```

These illustrate the principle. Consider what fits your context.
