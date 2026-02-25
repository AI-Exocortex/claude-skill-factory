---
name: realtime-collaboration
description: Guides implementation of collaborative features: cursor tracking, presence indicators, WebSocket synchronization for shared editing and multiplayer interfaces.
---

STARTER_CHARACTER = 👥

# Real-Time Collaboration Implementation

Build collaborative features where multiple users interact in the same space simultaneously.

## Core Components

**Presence System**
- Track who's connected (user ID, name, color, last activity timestamp)
- Broadcast join/leave events
- Handle timeouts for disconnected users
- Store active users in shared state

**Cursor Tracking**
- Capture local cursor/pointer position
- Throttle position updates (aim for 50-100ms intervals)
- Broadcast position with user ID
- Render remote cursors as overlays with user labels
- Remove cursors when users disconnect or navigate away

**WebSocket Protocol**
- Define message types: `presence:join`, `presence:leave`, `cursor:move`, `cursor:hide`
- Include user metadata in join messages
- Use compact payloads (position as `{x, y}` percentages or coordinates)
- Handle reconnection (rejoin with existing session ID)

## Implementation Patterns

**State Management**
Structure presence data by user ID:
```javascript
{
  userId: {
    name: string,
    color: string,
    cursor: { x, y, visible },
    lastSeen: timestamp
  }
}
```

Track cursor positions separately from other presence data to optimize rendering.

**Performance Considerations**
- Throttle cursor updates (don't send every mousemove event)
- Use CSS transforms for cursor rendering (GPU acceleration)
- Debounce presence UI updates
- Clean up stale cursors periodically
- Consider viewport culling for large numbers of users

**Component Architecture**
- Separate cursor rendering from business logic
- Make presence indicators independent from cursor overlays
- Keep WebSocket connection management in a provider/context
- Use absolute positioning for cursor overlays (portal/overlay layer)

## Anti-Patterns

Don't synchronize every UI interaction - focus on high-value collaborative signals.

Don't use polling - WebSockets provide bidirectional real-time communication.

Don't block UI on network updates - apply optimistic updates locally, reconcile asynchronously.

Don't hard-code user colors - generate from user ID or let users choose.

Don't forget to clean up event listeners and timers on unmount.

## Edge Cases

**Rapid navigation**: Hide cursor when user changes view/context

**Connection loss**: Show "reconnecting" state, maintain local session

**User ID conflicts**: Generate unique session IDs server-side

**High latency**: Show cursor position even if slightly delayed, add latency indicators if needed

**Mobile/touch**: Adapt cursor tracking to touch events

## Security Considerations

Validate user identity server-side before broadcasting presence.

Rate-limit cursor updates to prevent spam.

Sanitize user names and metadata before rendering.

Consider privacy settings (allow users to hide cursor/presence).

## References

For detailed implementation patterns:
- [Cursor Implementation](references/cursor-implementation.md) - Throttling, rendering, color assignment
- [Presence System](references/presence-system.md) - Join/leave flows, heartbeats, reconnection
- [WebSocket Protocol](references/websocket-protocol.md) - Message types, broadcasting, rate limiting
- [Performance Optimization](references/performance-optimization.md) - Scaling, memory management, network optimization
