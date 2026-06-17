# Entity Identification Algorithm

## Context and Problem Statement

SchemaCrawler's ER model builder needs to classify each table as a specific entity type — strong entity, weak entity, subtype, or non-entity — based solely on the table's primary key and foreign key structure. The classification must be deterministic and work without any additional metadata beyond what JDBC provides.


## Considered Options

The algorithm checks each table against a sequence of structural patterns, in order of specificity, stopping at the first match.

### Step 1: Check for non-entity pattern

Tables without a primary key are not considered entities.

If table T has no primary key, classify T as **NON_ENTITY**.

### Step 2: Check for subtype pattern

Subtype tables inherit their entire primary key from a single supertype table, where PK(T) = FK(T→P).

Else if PK(T) exactly matches the child columns of a FK to the parent table P primary key PK(P), classify T as **SUBTYPE** of P.

### Step 3: Check for weak entity pattern

Weak entities combine a parent's full primary key (via identifying FK) with their own discriminator column(s) in PK(T).

Else if PK(T) contains (as a proper subset) the child columns of some FK to parent P primary key PK(P), classify T as **WEAK_ENTITY** owned by P.

### Step 4: Check for strong entity pattern

Strong entities have self-sufficient primary keys (no FK columns in PK) and low referential connectivity to other tables.

Else if no FK columns participate in PK(T) **AND** T has foreign keys to fewer than 2 other tables (excluding self-references), classify T as **STRONG_ENTITY**.

### Step 5: Default classification

Tables with ambiguous patterns (high connectivity, composite FK-based PKs, etc.) cannot be confidently classified.

Otherwise, classify T as **UNKNOWN**.


## Decision Outcome

The sequential pattern-matching algorithm above is used. Each table is evaluated against Steps 1–5 in order, and the first matching rule determines the classification. This approach is deterministic, requires no additional metadata beyond JDBC-provided primary key and foreign key information, and degrades gracefully by assigning **UNKNOWN** to ambiguous cases rather than forcing a potentially incorrect classification.
