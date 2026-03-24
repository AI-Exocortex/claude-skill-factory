## SBPP-COL-23 - Stack

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-23:1 - Problem frame

Stack (LIFO) semantics are needed when processing nested structures, implementing
undo/redo, managing recursive state, or evaluating expressions. Java has `Deque`
as the recommended stack interface.

### SBPP-COL-23:2 - Problem

How do you implement LIFO (Last-In, First-Out) stack semantics in Java/Kotlin?

### SBPP-COL-23:3 - Forces

| Force | Tension |
|-------|---------|
| **Clarity** | `Deque` methods (`push`/`pop`/`peek`) communicate LIFO ↔ `java.util.Stack` is legacy and synchronized |
| **Thread safety** | `ArrayDeque` is not thread-safe ↔ `ConcurrentLinkedDeque` is thread-safe |
| **Type** | `Deque<E>` vs `Stack<E>` — `Stack` is a legacy class |

### SBPP-COL-23:4 - Solution — Use `ArrayDeque` as a stack via `Deque` interface; never use `java.util.Stack`

**Java:**

```java
// ✅ Stack via Deque (correct modern approach)
Deque<State> undoStack = new ArrayDeque<>();

undoStack.push(currentState);         // push (addFirst)
State previous = undoStack.pop();     // pop (removeFirst) — throws if empty
State peeked   = undoStack.peek();    // peek (peekFirst) — null if empty

// ✅ Non-recursive tree traversal using a stack
Deque<TreeNode> nodeStack = new ArrayDeque<>();
nodeStack.push(root);
while (!nodeStack.isEmpty()) {
    TreeNode node = nodeStack.pop();
    process(node);
    if (node.right != null) nodeStack.push(node.right);
    if (node.left  != null) nodeStack.push(node.left);
}
```

**Kotlin:**

```kotlin
// ✅ ArrayDeque as stack (Kotlin stdlib ArrayDeque)
val undoStack = ArrayDeque<State>()
undoStack.addLast(currentState)      // push
val previous = undoStack.removeLast() // pop — throws if empty
val peeked = undoStack.lastOrNull()   // peek — null if empty

// ✅ Kotlin extension idiom
fun <T> ArrayDeque<T>.push(item: T) = addLast(item)
fun <T> ArrayDeque<T>.pop(): T = removeLast()
fun <T> ArrayDeque<T>.peek(): T? = lastOrNull()
```

### SBPP-COL-23:5 - Archetypal Grounding

**U.System:** `undoStack.push(state)` / `undoStack.pop()` — clear LIFO semantics; the type name `undoStack` communicates the access pattern.
**U.Episteme:** LIFO is a fundamental data structure invariant; expressing it via `Deque.push/pop` documents the invariant in the API calls.

### SBPP-COL-23:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | `java.util.Stack` is synchronized (legacy); `ArrayDeque` is not | Use `ArrayDeque`; synchronize explicitly if needed |
| **Arch** | `Deque.pop()` throws on empty; `peek()` returns null | Prefer `isEmpty()` check before `pop()`; or use `poll()` (returns null on empty) |
| **Onto/Epist** | `ArrayDeque` also serves as a queue — the variable name communicates the usage pattern | Name the variable `...Stack` or `...Queue` to indicate the access pattern |
| **Prag** | Kotlin `ArrayDeque` is the stdlib choice | Use it |
| **Did** | Teach `ArrayDeque` not `Stack` | "Never use `java.util.Stack`" |

### SBPP-COL-23:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL23-1** | LIFO stacks SHALL be implemented with `ArrayDeque<E>` accessed via `Deque<E>` interface. | Modern, unsynchronised, correct |
| **CC-COL23-2** | `java.util.Stack` SHALL NOT be used in new code. | Legacy class avoidance |
| **CC-COL23-3** | Stack variable names SHOULD include "stack" to communicate the access pattern. | Readability |

### SBPP-COL-23:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** `java.util.Stack<T>` — legacy, synchronized. Fix: `ArrayDeque<T>`.
**Anti-pattern 2:** `deque.pop()` without empty check — throws `NoSuchElementException`. Fix: check `isEmpty()` first or use `poll()`.

### SBPP-COL-23:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| O(1) push/pop with `ArrayDeque` | Not thread-safe — synchronize if shared |
| Clear LIFO semantics in variable name + methods | — |

### SBPP-COL-23:10 - Rationale

Beck's Stack idiom maps directly to `ArrayDeque` as a LIFO stack. The key Java adaptation
is avoiding the legacy `java.util.Stack` class.

### SBPP-COL-23:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** `Deque` (specifically `ArrayDeque`) is recommended
over `Stack`. *Adopt.*

**Java API docs (post-2015):** `java.util.Stack` Javadoc recommends using `ArrayDeque` instead. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | Use ArrayDeque | **Adopt** |
| Java API docs | `Stack` is legacy | **Adopt** |

### SBPP-COL-23:12 - Relations

* **Built on:** SBPP-COL-02 (OrderedCollection — LIFO access pattern)
* **Contrast with:** SBPP-COL-24 (Queue — FIFO access pattern)

### SBPP-COL-23:End
