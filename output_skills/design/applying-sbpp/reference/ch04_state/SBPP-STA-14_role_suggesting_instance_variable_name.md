## SBPP-STA-14 - Role Suggesting Instance Variable Name

> **Type:** Architectural (A)
> **Status:** Adopted
> **Normativity:** Normative

### SBPP-STA-14:1 - Problem frame

Field names are the most persistent vocabulary in a codebase — they appear in every
method that accesses them, in error messages, in serialization output, and in team
discussions. A poorly named field forces every reader to stop and decode its meaning.
A well-named field communicates its role instantly.

### SBPP-STA-14:2 - Problem

What do you name an instance variable so that its purpose (role in the domain) and
usage (how it is accessed) are immediately clear?

### SBPP-STA-14:3 - Forces

| Force | Tension |
|-------|---------|
| **Role Communication** | Name communicates purpose ↔ concise names hide the role |
| **Type Redundancy** | Type is already declared ↔ including type info in the name is redundant |
| **Scope** | Field name scoped to class ↔ local variables need more context |

### SBPP-STA-14:4 - Solution — Name fields after their domain role; never include type information

**Java/Kotlin naming guidelines:**

```java
// ❌ Type in name (Hungarian notation) — redundant, couples name to implementation
private List<Claim>  claimList;
private String       statusString;
private boolean      isActiveBoolean;
private LocalDate    expiryDateLocalDate;

// ✅ Role-based names — communicate purpose
private List<Claim>  claims;           // role: the claims on this policy
private PolicyStatus status;           // role: current lifecycle status
private boolean      active;           // role: whether the policy is in force
private LocalDate    expiryDate;       // role: when coverage ends

// ✅ Domain-rich names for multiple fields of same type
private Money        basePremium;      // role: pre-adjustment premium
private Money        netPremium;       // role: post-adjustment premium
private Money        totalClaims;      // role: sum of all approved claims

private CustomerId   holderId;         // role: who holds this policy
private CustomerId   payerId;          // role: who pays the premium (may differ)
```

**Kotlin:**

```kotlin
data class InsurancePolicy(
    val id: PolicyId,
    val holderId: CustomerId,     // role: policy holder
    val payerId: CustomerId,      // role: payer (may differ from holder)
    val basePremium: Money,       // role: pre-adjustment amount
    val netPremium: Money,        // role: after adjustments
    val expiryDate: LocalDate,    // role: coverage end date
    val status: PolicyStatus      // role: lifecycle state
)
```

**Naming vocabulary by role:**

| Role | Preferred name pattern |
|------|------------------------|
| Collection of domain items | plural noun: `claims`, `items`, `adjustments` |
| Identity reference | `[domain]Id`: `holderId`, `claimId` |
| Amount/money | role-specific: `basePremium`, `netPremium`, `discount` |
| Date/time | role + `Date`/`At`: `expiryDate`, `createdAt`, `cancelledAt` |
| Status | role + `Status`: `policyStatus`, or just `status` when unambiguous |
| Boolean flag | role: `active`, `expired`, `underReview` (no `is` prefix on field) |

### SBPP-STA-14:5 - Archetypal Grounding

**U.System:** `holderId` vs `payerId` — two `CustomerId` fields with distinct roles, unambiguous from names alone.
**U.Episteme:** A field named `claims` communicates it is a collection of domain claims; `claimList` says it's a list (type detail) of unspecified claims.

### SBPP-STA-14:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Field naming in Java/Kotlin domain objects**.

| Lens | Bias / Limitation | Mitigation |
|------|-------------------|------------|
| **Gov** | Field renaming is a refactoring that touches many files | IDE rename-refactoring is safe; invest in good names upfront |
| **Arch** | Serialization frameworks use field names; rename breaks JSON/DB compatibility | Map field names to JSON/DB names explicitly at the boundary; keep domain names clean |
| **Onto/Epist** | "Role" requires understanding the domain | Derive names from domain model; use Ubiquitous Language |
| **Prag** | Kotlin data class parameter names become JSON keys by default | Use `@JsonProperty` to separate domain name from wire format |
| **Did** | Teach by example: show what `x`, `tmp`, `data` cost in readability | Code review: reject any field named `data`, `value`, `info`, `temp` |

### SBPP-STA-14:7 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-STA14-1** | Field names SHALL communicate role in the domain, not implementation type. | Readability |
| **CC-STA14-2** | Field names MUST NOT use Hungarian notation or type suffixes. | Modern Java/Kotlin convention |
| **CC-STA14-3** | Multiple fields of the same type SHALL have distinct role-revealing names. | Disambiguation |
| **CC-STA14-4** | Boolean fields SHOULD be named as adjectives (`active`, `expired`) without `is` prefix. | Property getter adds `is`; field does not need it |

### SBPP-STA-14:8 - Common Anti-Patterns and How to Avoid Them

**Anti-pattern 1: Type suffix**
`claimList`, `statusString`, `premiumBigDecimal` — Fix: `claims`, `status`, `premium`.

**Anti-pattern 2: Single-letter field**
`p` for premium, `c` for customer — Fix: full role-based name always.

**Anti-pattern 3: Generic name**
`data`, `value`, `info`, `temp` as field names — Fix: what IS this data? Name after the role.

### SBPP-STA-14:9 - Consequences

| Benefits | Trade-offs / Mitigations |
|----------|--------------------------|
| Field names read as domain vocabulary | Longer names — justified by clarity |
| Multiple same-type fields are unambiguous | Renaming touches many files — use IDE refactoring |
| Ubiquitous Language encoded in the field | — |

### SBPP-STA-14:10 - Rationale

Field naming is the first line of domain communication in code. Beck's "role-suggesting"
principle is identical to Clean Code's "use intention-revealing names" applied to fields.
The anti-Hungarian-notation rule is universally adopted in Java/Kotlin.

### SBPP-STA-14:11 - SoTA-Echoing

**Adoption verdict: ADOPT**

**Clean Code (Martin, 2008/ongoing):** "Use intention-revealing names." Field names must reveal role. *Adopt.*

**Google Java Style Guide (Google, post-2015):** No Hungarian notation; role-based names. *Adopt.*

**DDD Ubiquitous Language (Vernon, 2016):** Domain vocabulary in field names. *Adopt.*

| Tradition / Source | Alignment | Adoption |
|-------------------|-----------|---------|
| Clean Code (Martin, ongoing) | Intention-revealing names | **Adopt** |
| Google Java Style (post-2015) | No Hungarian notation | **Adopt** |
| DDD Ubiquitous Language (Vernon, 2016) | Domain vocab | **Adopt** |

### SBPP-STA-14:12 - Relations

* **Applies to:** SBPP-STA-01 (Common State fields)
* **Implements:** SBPP-BEH-18 (Intention Revealing Selector — for field names)
* **Parallel:** SBPP-STA-20 (Role Suggesting Temporary Variable Name)

### SBPP-STA-14:End
