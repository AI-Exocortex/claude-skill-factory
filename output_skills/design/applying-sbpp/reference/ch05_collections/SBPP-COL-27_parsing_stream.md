## SBPP-COL-27 - Parsing Stream

> **Type:** Architectural (A)
> **Status:** Adopt/Adapt
> **Normativity:** Normative

### SBPP-COL-27:1 - Problem frame

Simple line-based or token-based parsing is common in configuration loading, CSV
processing, and protocol handling. Beck's pattern uses a `ReadStream` to sequentially
consume tokens. In Java/Kotlin, `Scanner`, `BufferedReader.lines()`, and custom parsers
serve this role.

### SBPP-COL-27:2 - Problem

How do you write a simple parser that reads tokens or lines sequentially, choosing
different processing based on what it reads?

### SBPP-COL-27:3 - Forces

| Force | Tension |
|-------|---------|
| **Simplicity** | Simple sequential parsing ↔ complex grammars need parser generators |
| **Streaming** | Process without loading all input at once ↔ some operations require lookahead |
| **Separation** | Parsing separated from processing ↔ tight integration is simpler for small parsers |

### SBPP-COL-27:4 - Solution — Use `BufferedReader`/`Scanner` for simple parsing; structured parser for complex grammars

**Java — line-based parsing with Stream:**

```java
public List<PolicyRecord> parseFile(Path file) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(file)) {
        return reader.lines()
            .skip(1)                            // skip header
            .filter(line -> !line.isBlank())
            .map(this::parseLine)
            .collect(toList());
    }
}

private PolicyRecord parseLine(String line) {
    String[] parts = line.split(",", -1);
    return new PolicyRecord(
        PolicyId.of(parts[0].trim()),
        PolicyStatus.valueOf(parts[1].trim()),
        Money.of(Long.parseLong(parts[2].trim()), Currency.USD)
    );
}
```

**Java — token-based parsing with Scanner:**

```java
public Config parseConfig(String content) {
    Scanner scanner = new Scanner(content);
    Map<String, String> entries = new LinkedHashMap<>();
    while (scanner.hasNextLine()) {
        String line = scanner.nextLine().trim();
        if (line.isEmpty() || line.startsWith("#")) continue;
        String[] parts = line.split("=", 2);
        if (parts.length == 2) entries.put(parts[0].trim(), parts[1].trim());
    }
    return Config.from(entries);
}
```

**Kotlin:**

```kotlin
fun parseFile(file: Path): List<PolicyRecord> =
    file.readLines()
        .drop(1)          // skip header
        .filter { it.isNotBlank() }
        .map { parseLine(it) }

private fun parseLine(line: String): PolicyRecord {
    val (id, status, premium) = line.split(",", limit = 3)
    return PolicyRecord(PolicyId(id.trim()), PolicyStatus.valueOf(status.trim()), Money(premium.trim().toLong(), Currency.USD))
}
```

**When to use which approach:**
- Simple CSV/TSV: `String.split()` + stream/map
- Multi-format config: `Scanner` with `hasNextLine()`
- Complex grammar: ANTLR, JavaCC, or a parser combinator library

### SBPP-COL-27:5 - Archetypal Grounding

**U.System:** `reader.lines().skip(1).filter(...).map(parseLine)` — a stream-based parser that processes line-by-line without loading the whole file.
**U.Episteme:** The parsing logic is separated from the reading logic — `parseLine()` is independently testable.

### SBPP-COL-27:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Hand-rolled parsers are fragile — complex grammars need parser generators | Use ANTLR/library for non-trivial grammars |
| **Arch** | `Scanner` is not thread-safe; `BufferedReader.lines()` is lazy | Use try-with-resources; don't share `Scanner` across threads |
| **Onto/Epist** | Error reporting in hand-rolled parsers is poor | Include line number in error messages |
| **Prag** | Kotlin `readLines()`, `readText()`, `forEachLine {}` are very clean | Prefer Kotlin file-reading idioms |
| **Did** | Start with the simplest approach (`split`); graduate to parser libraries only when needed | |

### SBPP-COL-27:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-COL27-1** | File parsing SHALL use `BufferedReader.lines()` (Java) or `Path.readLines()` (Kotlin) for line-based input. | Lazy, memory-efficient |
| **CC-COL27-2** | The parsing function (`parseLine`) SHALL be separated from the reading infrastructure. | Testability |
| **CC-COL27-3** | Complex grammars (nested, recursive) SHALL use parser generator libraries (ANTLR, etc.). | Correctness |

### SBPP-COL-27:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1:** Loading entire file into memory for line parsing. Fix: `BufferedReader.lines()` / `readLines()`.
**Anti-pattern 2:** Mixing parsing and processing in one method. Fix: separate `parseLine()` from the iteration driver.

### SBPP-COL-27:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Memory-efficient line-by-line parsing | Error handling requires explicit line tracking |
| Parsing function is independently testable | — |

### SBPP-COL-27:10 - Rationale

Beck's Parsing Stream maps to Java's `BufferedReader.lines()` and Kotlin's `readLines()` /
`forEachLine {}`. Modern Java/Kotlin makes line-based parsing a clean stream operation.

### SBPP-COL-27:11 - SoTA-Echoing

**Adoption verdict: ADOPT/ADAPT**

**Apache Commons CSV / OpenCSV (post-2015):** Production CSV parsing with proper quoting and escaping. *Adapt: use library for real CSV.*

**Kotlin I/O extensions (post-2016):** `Path.readLines()`, `forEachLine {}`. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Kotlin I/O extensions (post-2016) | Clean file reading | **Adopt** |
| OpenCSV / Apache Commons CSV (post-2015) | Production CSV parsing | **Adopt** for CSV |

### SBPP-COL-27:12 - Relations

* **Pairs with:** SBPP-COL-28 (Concatenating Stream — for output)
* **Used when:** Simple line/token parsing is sufficient

### SBPP-COL-27:End
