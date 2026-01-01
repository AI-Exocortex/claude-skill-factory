---
name: nullables
description: Writes tests without mocks using James Shore's Nullables pattern. Use when writing tests and designing code for testability.
---

# Nullables: Testing Without Mocks

Nullables are production code with an "off" switch for external communication. This enables **sociable tests**: tests that exercise real code paths, with only infrastructure I/O neutralized. No mock libraries needed. It also enables really fast and robust tests, which are extremely valuable feedback loops.

## When to Use Nullables

Use Nullables when:
- Testing code that talks to external systems (HTTP, files, databases, clocks)
- You want tests that validate behavior, not implementation details
- Mock setup is becoming complex or brittle
- You need tests that run fast without real I/O

Do NOT use when:
- Testing pure logic (no infrastructure) - just test directly
- You need to verify exact interaction sequences - use mocks
- The external system is simple enough to use directly in tests

## Core Pattern: Two Factory Methods

Every infrastructure wrapper has two creation paths:

```javascript
class Clock {
  static create() {
    return new Clock(Date);  // Real system clock
  }

  static createNull(now = "2020-01-01T00:00:00Z") {
    return new Clock(new StubbedDate(now));  // Controlled clock
  }

  constructor(dateClass) {
    this._dateClass = dateClass;
  }

  now() {
    return new this._dateClass().toISOString();
  }
}

class StubbedDate {
  constructor(isoString) {
    this._time = new Date(isoString).getTime();
  }
  toISOString() {
    return new Date(this._time).toISOString();
  }
}
```

**Key principle**: `createNull()` takes parameters at the caller's abstraction level. Clock accepts ISO strings, not milliseconds.

## Complete Example: Command Line Wrapper

```javascript
import { OutputListener } from "./output_listener.js";

export class CommandLine {
  static create() {
    return new CommandLine(process);
  }

  static createNull({ args = [] } = {}) {
    return new CommandLine(new StubbedProcess(args));
  }

  constructor(proc) {
    this._process = proc;
    this._listener = new OutputListener();
  }

  args() {
    return this._process.argv.slice(2);
  }

  writeOutput(text) {
    this._process.stdout.write(text);
    this._listener.emit(text);
  }

  trackOutput() {
    return this._listener.trackOutput();
  }
}

class StubbedProcess {
  constructor(args) {
    this._args = args;
  }
  get argv() {
    return ["node", "script.js", ...this._args];
  }
  get stdout() {
    return { write() {} };
  }
}
```

## Testing with Nullables

```javascript
describe("App", () => {
  it("transforms input and writes result", () => {
    const { output } = run({ args: ["hello"] });
    assert.deepEqual(output.data, ["uryyb\n"]);  // ROT-13 of "hello"
  });

  it("shows usage when no args", () => {
    const { output } = run({ args: [] });
    assert.deepEqual(output.data, ["Usage: run <text>\n"]);
  });

  function run({ args = [] } = {}) {
    const commandLine = CommandLine.createNull({ args });
    const output = commandLine.trackOutput();

    const app = new App(commandLine);
    app.run();

    return { output };
  }
});
```

**Notice**: Tests exercise real `App` code. Only infrastructure I/O is neutralized.

## Three Supporting Patterns

### 1. Output Tracking

Observe what your code does without real I/O:

```javascript
const log = Log.createNull();
const output = log.trackOutput();

myService.doWork(log);

assert.deepEqual(output.data, [
  { level: "info", message: "Starting work" },
  { level: "info", message: "Work complete" }
]);
```

See [references/output-tracking.md](references/output-tracking.md) for implementation details.

### 2. Configurable Responses

Control what your code receives from external systems:

```javascript
// Single response (repeats forever)
const client = HttpClient.createNull({ status: 200, body: "OK" });

// Multiple responses (sequence)
const client = HttpClient.createNull([
  { status: 200, body: "first" },
  { status: 500, body: "error" },
]);
```

See [references/configurable-responses.md](references/configurable-responses.md) for patterns.

### 3. Embedded Stubs

Minimal fakes for third-party code, living inside your wrapper:

```javascript
class HttpClient {
  static createNull(responses) {
    return new HttpClient(new StubbedHttp(responses));
  }
  // ...
}

class StubbedHttp {  // Implements only what HttpClient actually uses
  request(options) {
    return new StubbedRequest(this._nextResponse());
  }
}
```

See [references/embedded-stubs.md](references/embedded-stubs.md) for async patterns.

## Anti-Patterns

**Using mock libraries** - Don't import sinon, jest.mock, etc. Nullables replace them entirely.

**Writing broad integration tests** - Sociable unit tests with Nullables provide coverage without slow, flaky end-to-end tests.

**Testing interactions instead of outcomes**
```javascript
// BAD: Verifying method calls (mock-style thinking)
verify(logger).info("message");

// GOOD: Verifying what was produced
assert.deepEqual(logOutput.data, [{ level: "info", message: "message" }]);
```

**Constructor does work**
```javascript
// BAD: Constructor connects to database
constructor(connectionString) {
  this._db = new Database(connectionString);  // Immediate connection
}

// GOOD: Deferred connection
constructor(db) {
  this._db = db;
}
async connect() {
  await this._db.connect();
}
```

**Parameters at wrong abstraction level**
```javascript
// BAD: Leaking implementation details
LoginClient.createNull({ httpResponse: { status: 200, body: '{"email":"x"}' } });

// GOOD: Caller's abstraction level
LoginClient.createNull({ email: "user@example.com", verified: true });
```

## Reference Files

**Building Nullables:**
- [references/infrastructure-wrappers.md](references/infrastructure-wrappers.md) - Building complete wrappers
- [references/output-tracking.md](references/output-tracking.md) - Tracking writes and side effects
- [references/configurable-responses.md](references/configurable-responses.md) - Controlling external inputs
- [references/embedded-stubs.md](references/embedded-stubs.md) - Stubbing third-party code

**Testing and Architecture:**
- [references/test-patterns.md](references/test-patterns.md) - Structuring tests, Signature Shielding
- [references/architecture.md](references/architecture.md) - A-Frame, Logic Sandwich, Traffic Cop patterns

**Migrating Existing Code:**
- [references/migration.md](references/migration.md) - Converting from mocks to Nullables
