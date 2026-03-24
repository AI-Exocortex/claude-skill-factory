## SBPP-BEH-11 - Execute Around Method

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-BEH-11:1 - Problem frame

In Java/Kotlin microservices, many operations require a setup step and a guaranteed
teardown step — file/connection open/close, transaction begin/commit/rollback, lock
acquire/release, metric timer start/stop. Requiring callers to perform both steps
explicitly leads to resource leaks and error-handling omissions.

### SBPP-BEH-11:2 - Problem

How do you ensure that a pair of operations (setup + teardown) is always executed
together, in the right order, and that the teardown happens even when the code between
them throws an exception?

### SBPP-BEH-11:3 - Forces

| Force | Tension |
|-------|---------|
| **Safety** | Guarantee teardown ↔ callers forget or get it wrong under exceptions |
| **Flexibility** | Code between setup and teardown varies ↔ the frame is always the same |
| **Ergonomics** | Java try-with-resources is verbose ↔ lambdas are concise |

### SBPP-BEH-11:4 - Solution — Accept a lambda/Consumer that executes within the managed pair

Provide a method that takes a `Runnable`, `Consumer<T>`, `Supplier<T>`, or
`ThrowingConsumer<T>` as its argument. The method handles setup, calls the lambda,
and handles teardown in a `finally` block (or via try-with-resources).

**Java example:**

```java
public final class DatabaseTransaction {
    private final DataSource dataSource;

    // Execute Around Method: caller provides work; this class provides the frame
    public <T> T executeInTransaction(ThrowingSupplier<T> work) throws Exception {
        Connection conn = dataSource.getConnection();
        try {
            conn.setAutoCommit(false);
            T result = work.get(conn);
            conn.commit();
            return result;
        } catch (Exception e) {
            conn.rollback();
            throw e;
        } finally {
            conn.close();
        }
    }
}

@FunctionalInterface
interface ThrowingSupplier<T> {
    T get(Connection conn) throws Exception;
}

// Usage: caller provides only the business logic
Order order = txManager.executeInTransaction(conn -> {
    orderRepo.save(conn, order);
    inventoryRepo.deduct(conn, order.items());
    return order;
});
```

**Kotlin idiomatic version:**

```kotlin
class DatabaseTransaction(private val dataSource: DataSource) {

    fun <T> executeInTransaction(work: (Connection) -> T): T {
        val conn = dataSource.connection
        return try {
            conn.autoCommit = false
            val result = work(conn)
            conn.commit()
            result
        } catch (e: Exception) {
            conn.rollback()
            throw e
        } finally {
            conn.close()
        }
    }
}

// Usage — clean lambda syntax
val order = txManager.executeInTransaction { conn ->
    orderRepo.save(conn, newOrder)
    inventoryRepo.deduct(conn, newOrder.items)
    newOrder
}
```

**Note:** For `AutoCloseable` resources, Java's try-with-resources and Kotlin's `use {}` 
extension function are the standard mechanism. Execute Around Method is preferred when
the resource does not implement `AutoCloseable` or when the frame involves
non-trivial exception handling (e.g., rollback vs. commit).

### SBPP-BEH-11:5 - Archetypal Grounding

**U.System (Java/Kotlin microservice):**
*Tell:* Resource lifecycle management is encapsulated in an "execute around" method; callers provide only the work.
*Show:* `txManager.executeInTransaction { conn -> ... }` — the transaction lifecycle is invisible to the caller.

**U.Episteme (design reasoning):**
*Tell:* The Execute Around Method separates the what (caller-defined work) from the how (framework-managed lifecycle).
*Show:* A caller cannot forget to commit or rollback because those operations are not part of the API.

### SBPP-BEH-11:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Resource-lifecycle management in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Lambda-based APIs are harder to trace in stack dumps | Use meaningful lambda variable names; structured logging inside the frame |
| **Arch** | Java checked exceptions inside lambdas require `ThrowingX` functional interfaces | Kotlin handles this naturally; Java requires wrapper interfaces |
| **Onto/Epist** | "Execute around" assumes the frame is fixed; if setup/teardown varies, this pattern doesn't fit | Use Strategy pattern when the frame itself varies |
| **Prag** | Spring's `@Transactional` and `TransactionTemplate` implement this pattern for database transactions | Prefer framework-provided Execute Around when available; implement custom only for novel resource types |
| **Did** | Developers may implement both the frame and its escape hatch (direct API) | Remove the direct API where possible to enforce the frame |

### SBPP-BEH-11:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-BEH11-1** | Execute Around methods SHALL use `finally` or try-with-resources to guarantee teardown even on exception. | Prevents resource leaks |
| **CC-BEH11-2** | The method name SHOULD communicate the frame: `executeInTransaction`, `withLock`, `timed`. | Makes the lifecycle visible at the call site |
| **CC-BEH11-3** | For resources implementing `AutoCloseable`, Kotlin's `use {}` or Java's try-with-resources SHOULD be preferred over hand-written frames. | Leverages language mechanisms |
| **CC-BEH11-4** | Execute Around methods MUST NOT swallow exceptions thrown by the work lambda. | Ensures error propagation |

### SBPP-BEH-11:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Swallowed Exception**
```java
} catch (Exception e) { log.error("...", e); /* exception not re-thrown */ }
```
Fix: Always re-throw (or wrap and re-throw) exceptions from within the frame.

**Anti-pattern 2: Exposing Both Frame and Direct API**
Providing both `executeInTransaction(work)` and `beginTransaction()` / `commitTransaction()`.
Fix: Remove the direct API or mark it `@Deprecated` to force callers into the safe frame.

### SBPP-BEH-11:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Resource leaks are structurally impossible | Lambda / functional interface overhead — negligible on JVM |
| Callers cannot misuse the lifecycle | Requires functional interface design for checked exceptions in Java |
| Frame logic (transaction, locking) is in one place | — |

### SBPP-BEH-11:10 - Rationale

Execute Around Method is one of Beck's most durable patterns. In Java/Kotlin microservices
it appears as Spring's `TransactionTemplate`, JDBC `execute()`, and Kotlin's `use {}`.
The lambda-based API makes the pattern idiomatic in modern Java (8+) and Kotlin.

### SBPP-BEH-11:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 9 (try-with-resources) and Item 8 (avoid
finalizers). Execute Around is the programmatic equivalent when `AutoCloseable` is unavailable. *Adopt.*

**Spring Framework TransactionTemplate (2015+):** The canonical Java Execute Around for
database transactions. All custom resource frames should follow the same shape. *Adopt.*

**Kotlin standard library `use {}` (post-2016):** `AutoCloseable.use { ... }` is the
idiomatic Kotlin Execute Around for resources. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. (Bloch, 2018) | try-with-resources | **Adopt** |
| Spring TransactionTemplate (2015+) | Transaction Execute Around | **Adopt** |
| Kotlin `use {}` (post-2016) | `AutoCloseable` Execute Around | **Adopt** |

### SBPP-BEH-11:12 - Relations

* **Implements:** Loan Pattern / Template Method (for resource lifecycle)
* **Constrains:** Callers cannot access resource lifecycle directly
* **Relates to:** SBPP-BEH-28 (Pluggable Block — the work lambda is a pluggable block)
* **Constrained by:** Exception propagation must not be suppressed

### SBPP-BEH-11:End
