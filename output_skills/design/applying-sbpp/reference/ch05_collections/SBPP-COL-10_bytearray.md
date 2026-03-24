## SBPP-COL-10 - ByteArray

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-COL-10:1 - Problem frame

Binary data — cryptographic hashes, serialised payloads, image bytes, network packets —
is a common concern in Java/Kotlin microservices. Using generic `List<Byte>` or `List<Integer>`
wastes memory due to boxing. The primitive `byte[]` array is the correct representation,
but its handling requires care regarding immutability and defensive copying.

### SBPP-COL-10:2 - Problem

How do you represent and work with binary data (byte sequences) efficiently and safely?

### SBPP-COL-10:3 - Forces

| Force | Tension |
|-------|---------|
| **Performance** | Primitive `byte[]` avoids boxing overhead ↔ it is mutable and must be defensively copied |
| **Safety** | Defensive copy prevents mutation ↔ copy adds allocation |
| **Abstraction** | `ByteBuffer`, `InputStream`, `byte[]` serve different access patterns | |

### SBPP-COL-10:4 - Solution — Use `byte[]` for binary data; defensively copy at boundaries; consider `ByteBuffer` for structured binary

```java
// ✅ Immutable binary value object — defensive copy in constructor and accessor
public final class HashValue {
    private final byte[] bytes;

    public HashValue(byte[] bytes) {
        this.bytes = Arrays.copyOf(bytes, bytes.length);  // defensive copy
    }

    public byte[] toBytes() {
        return Arrays.copyOf(bytes, bytes.length);        // defensive copy on return
    }

    public int length() { return bytes.length; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof HashValue other)) return false;
        return Arrays.equals(bytes, other.bytes);
    }

    @Override
    public int hashCode() { return Arrays.hashCode(bytes); }
}
```

**Kotlin:**

```kotlin
@JvmInline value class HashValue(private val bytes: ByteArray) {
    fun toBytes(): ByteArray = bytes.copyOf()
    val length: Int get() = bytes.size
    override fun equals(other: Any?): Boolean =
        other is HashValue && bytes.contentEquals(other.bytes)
    override fun hashCode(): Int = bytes.contentHashCode()
}
```

**Using `ByteBuffer` for structured binary:**

```java
// Structured binary parsing
ByteBuffer buf = ByteBuffer.wrap(rawBytes).order(ByteOrder.BIG_ENDIAN);
int version   = buf.getInt();
long timestamp = buf.getLong();
short flags   = buf.getShort();
```

### SBPP-COL-10:5 - Archetypal Grounding

**U.System:** `HashValue` wraps a `byte[]` with defensive copy — callers cannot mutate the internal hash.
**U.Episteme:** `Arrays.equals()` must be used for byte array equality; `==` and `.equals()` on arrays test identity, not content.

### SBPP-COL-10:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Binary data handling in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Raw `byte[]` fields can be mutated by callers | Always defensively copy in constructors and accessors |
| **Arch** | `byte[]` equality with `==` is identity; use `Arrays.equals()` | Wrap in a value class with correct `equals`/`hashCode` |
| **Onto/Epist** | `ByteArray` in Kotlin is a primitive array — correct choice for binary data | Use `ByteArray`, not `Array<Byte>` (which boxes) |
| **Prag** | For large binary blobs, streaming (`InputStream`) is more appropriate than loading into `byte[]` | Use `byte[]` only for small, bounded binary data |
| **Did** | `byte[]` equality trap (`arr1 == arr2` tests reference) is a common Java bug | Always use `Arrays.equals()`; wrap in a value class |

### SBPP-COL-10:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL10-1** | `byte[]` fields SHALL be defensively copied in constructors and accessors. | Immutability safety |
| **CC-COL10-2** | `byte[]` equality MUST use `Arrays.equals()`, not `==` or `.equals()`. | Correct content comparison |
| **CC-COL10-3** | `byte[]` `hashCode` MUST use `Arrays.hashCode()`. | Correct hash semantics |
| **CC-COL10-4** | Kotlin `ByteArray` SHOULD be used instead of `Array<Byte>` for binary data. | Avoids boxing |

### SBPP-COL-10:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Array equality with `.equals()`**
`hash1.bytes.equals(hash2.bytes)` — compares references. Fix: `Arrays.equals(hash1.bytes, hash2.bytes)`.

**Anti-pattern 2: Exposed mutable array field**
`public byte[] getBytes() { return bytes; }` — caller can mutate. Fix: return a copy.

### SBPP-COL-10:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Zero boxing overhead for binary data | Must defensively copy at boundaries |
| `ByteBuffer` provides structured parsing | Requires careful equality/hashCode implementation |

### SBPP-COL-10:10 - Rationale

ByteArray in Java/Kotlin is the canonical binary data container. The critical adaptations
over Smalltalk's `ByteArray` are: (1) defensive copying for immutability, (2) correct
`Arrays.equals()` usage, and (3) Kotlin value class wrapping to provide type safety.

### SBPP-COL-10:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Effective Java 3rd ed. (Bloch, 2018):** Item 50 ("Make defensive copies when needed") — applies
directly to `byte[]` fields. *Adopt.*

**Kotlin value classes (JEP 169 analog, post-2021 stable):** `@JvmInline value class` wraps
`ByteArray` with zero overhead and correct semantics. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Effective Java 3rd ed. Item 50 (Bloch, 2018) | Defensive copies | **Adopt** |
| Kotlin value classes (post-2021 stable) | Zero-overhead wrapping | **Adopt** |

### SBPP-COL-10:12 - Relations

* **Specialises:** SBPP-COL-09 (Array — byte-typed variant)
* **Requires:** Correct `Arrays.equals()` / `Arrays.hashCode()` usage
* **Related to:** SBPP-COL-05 (Equality Method — special case for byte arrays)

### SBPP-COL-10:End
