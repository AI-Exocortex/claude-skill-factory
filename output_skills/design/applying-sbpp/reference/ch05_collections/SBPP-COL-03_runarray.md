## SBPP-COL-03 - RunArray

> **Type:** Architectural (A)
> **Status:** Adapt
> **Normativity:** Normative

### SBPP-COL-03:1 - Problem frame

When a collection contains long runs of the same value — rich text attributes, time-series
data with repeated values, sparse sensor readings — storing every element individually
wastes memory. Run-length encoding compresses consecutive equal elements into (value, count) pairs.

### SBPP-COL-03:2 - Problem

How do you compactly represent a collection where the same element repeats many times in a row?

### SBPP-COL-03:3 - Forces

| Force | Tension |
|-------|---------|
| **Memory** | Run-length encoding dramatically reduces memory for repetitive data ↔ random access is O(n) in run count |
| **Simplicity** | Plain list is simple ↔ RLE adds complexity |
| **Correctness** | Must preserve semantics of the original collection ↔ implementation detail must be hidden |

### SBPP-COL-03:4 - Solution — Use run-length encoding for repetitive sequential data; expose as a standard List

No JDK class directly corresponds to Smalltalk's `RunArray`. In Java/Kotlin, implement
run-length encoding as a custom class that implements `List<E>` or use an
`AbstractList<E>` wrapper that exposes RLE-compressed data transparently.

**Java example — transparent RLE wrapper:**

```java
// Stores (value, count) pairs; exposes as List<E>
public final class RunLengthList<E> extends AbstractList<E> {
    private record Run<E>(E value, int count) {}
    private final List<Run<E>> runs;
    private final int totalSize;

    private RunLengthList(List<Run<E>> runs) {
        this.runs = List.copyOf(runs);
        this.totalSize = runs.stream().mapToInt(Run::count).sum();
    }

    public static <E> RunLengthList<E> encode(List<E> source) {
        List<Run<E>> runs = new ArrayList<>();
        for (int i = 0; i < source.size(); ) {
            E val = source.get(i); int count = 0;
            while (i < source.size() && Objects.equals(source.get(i), val)) { i++; count++; }
            runs.add(new Run<>(val, count));
        }
        return new RunLengthList<>(runs);
    }

    @Override public E get(int index) { /* walk runs */ ... }
    @Override public int size() { return totalSize; }
}
```

**Kotlin example:**

```kotlin
data class Run<E>(val value: E, val count: Int)

fun <E> List<E>.runLengthEncode(): List<Run<E>> =
    fold(mutableListOf()) { acc, e ->
        if (acc.isNotEmpty() && acc.last().value == e)
            acc.apply { set(lastIndex, last().copy(count = last().count + 1)) }
        else acc.apply { add(Run(e, 1)) }
    }

// For text decoration runs
data class TextDecoration(val bold: Boolean, val italic: Boolean, val color: String)
val decorations: List<Run<TextDecoration>> = rawDecorations.runLengthEncode()
```

**When to apply:**
Apply only when profiling confirms the optimization is needed. Start with a plain `List`
and switch to RLE if memory profiling reveals the repetition problem.

### SBPP-COL-03:5 - Archetypal Grounding

**U.System:** A rich-text engine stores character styling as `List<Run<Style>>` instead of
`List<Style>` — reducing 10,000 "all-bold" entries to one `Run(bold=true, count=10000)`.

**U.Episteme:** RunArray is a compression pattern: it trades sequential access simplicity
for memory efficiency on repetitive data. Apply only when the trade-off is measured, not assumed.

### SBPP-COL-03:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Memory-optimised sequential collections in Java/Kotlin**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Premature optimization anti-pattern — do not use without profiling | Profile first; document the measured savings |
| **Arch** | Random access into a RunArray is O(number of runs), not O(1) | Only use when sequential access dominates; document access pattern |
| **Onto/Epist** | The "run" abstraction may not match the domain model | Name after the domain concept: `StyleRun`, `PriceRun`, not "run array" |
| **Prag** | Java has no built-in RunArray; must implement custom or use library | Consider Apache Commons `RangeMap` or Guava `RangeSet` for similar use cases |
| **Did** | Exotic pattern — most developers will not encounter it | Introduce in context of performance optimization, not as general collection pattern |

### SBPP-COL-03:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL03-1** | RunArray / RLE SHOULD only be applied after profiling shows memory pressure from repetitive data. | Avoids premature optimization |
| **CC-COL03-2** | RLE collections SHOULD implement the standard `List<E>` interface for transparent use by callers. | Preserves API compatibility |
| **CC-COL03-3** | Access complexity of the RLE structure MUST be documented (O(n_runs) for random access). | Sets correct caller expectations |

### SBPP-COL-03:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Premature RLE**
Using RLE without profiling first. Fix: start with `List`; switch to RLE only when profiling proves the benefit.

**Anti-pattern 2: Exposing the Run structure**
`List<Pair<E, Integer>>` as the API instead of a proper `List<E>` view. Fix: implement `AbstractList<E>`.

### SBPP-COL-03:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Dramatic memory savings for repetitive data | Random access O(n_runs) — only use when sequential access dominates |
| Transparent to callers when wrapped as `List<E>` | Implementation complexity |

### SBPP-COL-03:10 - Rationale

RunArray is a performance optimization pattern, not a general-purpose collection. In modern
JVM environments with abundant memory, its application is narrow. When applicable
(rich text, time-series, sparse signals), it is highly effective.

### SBPP-COL-03:11 - SoTA-Echoing

**Adoption verdict: ADAPT**

**No direct JDK equivalent (Java/Kotlin stdlib).** Guava's `RangeMap` and `ImmutableRangeMap`
serve similar purposes for range-keyed data. Apache Commons Collections has related structures.

**Java 16+ records (JEP 395):** `record Run<E>(E value, int count) {}` makes the run
representation concise. *Adopt for the run record; adapt the wrapping strategy.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Guava `RangeMap` (2015+) | Range-based compact encoding | **Adapt** |
| Java 16+ records | Concise run representation | **Adopt** |
| Kotlin extension functions | Ergonomic RLE encoding | **Adopt** |

### SBPP-COL-03:12 - Relations

* **Specialises:** SBPP-COL-02 (OrderedCollection — compressed variant)
* **Applied when:** profiling shows memory pressure from repetitive sequential data
* **Relates to:** SBPP-COL-26 (Lookup Cache — another performance optimization pattern)

### SBPP-COL-03:End
