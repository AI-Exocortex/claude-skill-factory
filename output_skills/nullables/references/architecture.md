# Application Architecture for Nullables

Nullables work best when your application follows specific architectural patterns. These patterns separate logic from infrastructure, making code naturally testable.

## Contents

- [A-Frame Architecture](#a-frame-architecture)
- [Logic Sandwich](#logic-sandwich)
- [Traffic Cop](#traffic-cop)
- [When to Use Each Pattern](#when-to-use-each-pattern)

## A-Frame Architecture

Structure applications with Logic and Infrastructure as peers under the Application layer:

```
            ┌─────────────────┐
            │   Application   │
            │  (coordinates)  │
            └────────┬────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│      Logic      │     │ Infrastructure  │
│  (pure, tested) │     │   (Nullables)   │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Value Objects  │
            │ (shared types)  │
            └─────────────────┘
```

**Key rules:**
- Logic never imports Infrastructure directly
- Application coordinates between Logic and Infrastructure
- Communication happens through Value Objects
- Infrastructure wrappers are Nullables

**Why this matters:** Logic stays pure and easily testable. Infrastructure is isolated behind Nullables. The Application layer is thin, just coordination.

## Logic Sandwich

The Application layer follows a consistent pattern:

```
1. READ    → Get data from Infrastructure (via Nullables)
2. PROCESS → Pass to Logic (pure functions)
3. WRITE   → Send results to Infrastructure (via Nullables)
```

Example:

```javascript
class OrderProcessor {
  constructor(database, emailer, logger) {
    this._db = database;
    this._emailer = emailer;
    this._logger = logger;
  }

  async processOrder(orderId) {
    // 1. READ
    const order = await this._db.getOrder(orderId);
    const inventory = await this._db.getInventory(order.items);

    // 2. PROCESS (pure logic)
    const result = OrderLogic.validate(order, inventory);
    const confirmation = OrderLogic.createConfirmation(result);

    // 3. WRITE
    await this._db.updateOrder(orderId, result.status);
    await this._emailer.send(confirmation);
    this._logger.info("Order processed", { orderId, status: result.status });
  }
}
```

**Testing:** Null the infrastructure, verify the writes:

```javascript
it("sends confirmation email for valid order", async () => {
  const db = Database.createNull({
    order: { id: "123", items: ["widget"] },
    inventory: { widget: 10 }
  });
  const emailer = Emailer.createNull();
  const emails = emailer.trackOutput();
  const logger = Logger.createNull();

  const processor = new OrderProcessor(db, emailer, logger);
  await processor.processOrder("123");

  assert.equal(emails.data.length, 1);
  assert.equal(emails.data[0].subject, "Order Confirmed");
});
```

## Traffic Cop

For event-driven applications, use the Observer pattern with Logic Sandwiches:

```javascript
class ChatServer {
  constructor(network, database, logger) {
    this._network = network;
    this._db = database;
    this._logger = logger;
  }

  start() {
    this._network.on("connection", (client) => this._handleConnection(client));
    this._network.on("message", (client, msg) => this._handleMessage(client, msg));
    this._network.on("disconnect", (client) => this._handleDisconnect(client));
  }

  // Each handler is a Logic Sandwich
  async _handleMessage(client, rawMessage) {
    // READ
    const user = await this._db.getUser(client.userId);

    // PROCESS
    const message = ChatLogic.formatMessage(user, rawMessage);
    const recipients = ChatLogic.findRecipients(message, this._clients);

    // WRITE
    for (const recipient of recipients) {
      this._network.send(recipient, message);
    }
    this._logger.info("Message sent", { from: user.name, to: recipients.length });
  }
}
```

**Testing with Behavior Simulation:**

```javascript
it("broadcasts messages to other clients", async () => {
  const network = Network.createNull();
  const sent = network.trackOutput();
  const db = Database.createNull({ user: { name: "Alice" } });
  const logger = Logger.createNull();

  const server = new ChatServer(network, db, logger);
  server.start();

  // Simulate events
  network.simulateConnection("client-1", { userId: "alice" });
  network.simulateConnection("client-2", { userId: "bob" });
  network.simulateMessage("client-1", "Hello!");

  assert.deepEqual(sent.data, [
    { to: "client-2", message: { from: "Alice", text: "Hello!" } }
  ]);
});
```

**Behavior Simulation pattern:** Add `simulateX()` methods to Nullables that inject events. These share implementation with real event handlers:

```javascript
class Network {
  static createNull() {
    return new Network(new StubbedSocket());
  }

  // Real event handling
  on(event, handler) {
    this._handlers[event] = handler;
  }

  // Behavior simulation - uses same handlers
  simulateConnection(clientId, data) {
    this._handlers["connection"]?.({ id: clientId, ...data });
  }

  simulateMessage(clientId, message) {
    this._handlers["message"]?.(clientId, message);
  }
}
```

## When to Use Each Pattern

| Pattern | Use When |
|---------|----------|
| **A-Frame** | Always. This is the foundational structure. |
| **Logic Sandwich** | Request/response flows, batch processing, CRUD operations |
| **Traffic Cop** | WebSockets, message queues, event-driven systems, real-time apps |

**Avoid:**
- God Classes in Traffic Cop - keep each handler focused
- Logic calling Infrastructure directly - route through Application
- Infrastructure-to-Infrastructure calls - coordinate in Application layer
