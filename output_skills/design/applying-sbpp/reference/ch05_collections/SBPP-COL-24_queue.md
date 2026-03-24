## SBPP-COL-24 - Queue

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-24:1 - Problem frame

FIFO (First-In, First-Out) queues model work queues, message buffers, and processing
pipelines. Java's `Queue` interface and `ArrayDeque` provide the standard FIFO
implementation. For concurrent queues, `LinkedBlockingQueue` and `ConcurrentLinkedQueue`
are available.

### SBPP-COL-24:2 - Problem

How do you implement FIFO queue semantics for sequential processing of items in arrival order?

### SBPP-COL-24:3 - Forces

| Force | Tension |
|-------|---------|
| **FIFO semantics** | Items processed in arrival order ↔ priority queue changes order |
| **Blocking** | `LinkedBlockingQueue` blocks on empty ↔ `ArrayDeque` does not block |
| **Concurrency** | `ArrayDeque` is not thread-safe ↔ concurrent queues add overhead |

### SBPP-COL-24:4 - Solution — Use `ArrayDeque` as a FIFO queue for single-threaded; `LinkedBlockingQueue` for producer-consumer

**Java:**

```java
// ✅ FIFO queue with ArrayDeque (single-threaded)
Queue<Task> taskQueue = new ArrayDeque<>();
taskQueue.offer(task1);               // enqueue (addLast)
taskQueue.offer(task2);
Task next = taskQueue.poll();         // dequeue (removeFirst) — null if empty
Task peeked = taskQueue.peek();       // peek — null if empty

// ✅ Producer-consumer with blocking queue
BlockingQueue<Order> orderQueue = new LinkedBlockingQueue<>(100); // capacity limit
// Producer thread:
orderQueue.put(newOrder);            // blocks if full
// Consumer thread:
Order order = orderQueue.take();     // blocks if empty
```

**Kotlin:**

```kotlin
// ✅ FIFO queue with ArrayDeque
val taskQueue = ArrayDeque<Task>()
taskQueue.addLast(task1)              // enqueue
val next: Task? = taskQueue.removeFirstOrNull()  // dequeue — null if empty
val peeked: Task? = taskQueue.firstOrNull()      // peek
```

### SBPP-COL-24:5 - Archetypal Grounding

**U.System:** `taskQueue.offer(task)` / `taskQueue.poll()` — FIFO processing order; first task in is first processed.
**U.Episteme:** `LinkedBlockingQueue` embeds the producer-consumer synchronisation in the data structure — callers don't need to write `wait()`/`notify()`.

### SBPP-COL-24:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | In microservices, message queues (Kafka, RabbitMQ) replace in-memory queues | Use in-memory queue for intra-service; use message broker for inter-service |
| **Arch** | `LinkedBlockingQueue` bounded capacity prevents unbounded memory growth | Always set capacity; handle `put()` backpressure |
| **Onto/Epist** | `ArrayDeque` as a queue — the variable name must communicate FIFO | Name `...Queue`; use `offer`/`poll` to signal queue semantics |
| **Prag** | Most production microservice queues are external (Kafka, SQS) | This pattern is for in-process work queues |
| **Did** | Teach `Queue` interface operations: `offer`, `poll`, `peek` | |

### SBPP-COL-24:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL24-1** | FIFO queues SHALL use `ArrayDeque<E>` accessed via `Queue<E>` interface (single-threaded). | Correct interface |
| **CC-COL24-2** | Producer-consumer queues SHALL use `BlockingQueue<E>` implementations. | Thread-safe |
| **CC-COL24-3** | Queue variable names SHOULD include "queue" to communicate the access pattern. | Readability |

### SBPP-COL-24:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Using `LinkedList` as a queue — has overhead vs `ArrayDeque`. Fix: `ArrayDeque`.
**Anti-pattern 2:** Unbounded `LinkedBlockingQueue` — can grow until OOM. Fix: always specify capacity.

### SBPP-COL-24:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(1) enqueue/dequeue | Not thread-safe (ArrayDeque) |
| `BlockingQueue` handles producer-consumer sync | Bounded capacity requires backpressure handling |

### SBPP-COL-24:10 - Rationale

Beck's Queue idiom maps to Java's `Queue` interface. `ArrayDeque` is the modern
implementation. `BlockingQueue` extends the pattern to concurrent producer-consumer.

### SBPP-COL-24:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Java concurrency (Goetz et al., "Java Concurrency in Practice", widely applied post-2015):**
`BlockingQueue` for producer-consumer. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Java Concurrency in Practice (Goetz, post-2015) | BlockingQueue | **Adopt** |
| Kotlin stdlib `ArrayDeque` (post-2016) | FIFO queue | **Adopt** |

### SBPP-COL-24:12 - Relations

* **Contrast with:** SBPP-COL-23 (Stack — LIFO)
* **Built on:** SBPP-COL-02 (OrderedCollection — FIFO access pattern)

### SBPP-COL-24:End
