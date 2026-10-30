# Named Object Index Reference

## Purpose

This document explains the indexes in `schemacrawler.namedobject`, the distinction between structured keys and displayed names, and the lookup behavior exposed by catalogs. Two important cases are schemas with blank or duplicated displayed names, and overloaded routines with the same ordinary name.

These are in-memory metadata indexes, not database indexes or SQL identifier resolvers. Matching uses exact names and structured keys, not regular expressions or database-specific case folding. See [Database Object Case Handling Reference](REF001-database-object-case-handling.md) for identifier case behavior.

## Index Interfaces And Implementations

`NamedObject` and `NamedObjectKey` remain in `schemacrawler.schema`. Their indexing support lives in `schemacrawler.namedobject`. The index interfaces and abstract classes are sealed using Java 17; concrete implementations are final. The hierarchy does not allow external implementations or subclasses.

| Type | Responsibility |
|---|---|
| `NamedObjectIndex<N>` | Read-only complete-key and full-name lookup, sorted enumeration, and unsorted snapshots of named objects. |
| `DatabaseObjectIndex<D>` | Adds schema-scoped enumeration and schema/ordinary-name lookup. |
| `DependantObjectIndex<DO, D>` | Adds exact parent-key/child-name lookup for dependent objects. |
| `BuildableIndex<N>` | Adds keyed `add` and `remove` operations; immutable membership can reject these operations. |
| `BuildableDatabaseObjectIndex<D>` | Combines database-object reads with keyed mutation. |
| `BuildableDependantObjectIndex<DO, D>` | Combines dependent-object reads with keyed mutation. |
| `AbstractDatabaseObjectIndex<D>` | Shares map-backed reads and schema filtering; package-private. |
| `AbstractConcurrentIndex<D>` | Shares concurrent mutable storage and mutation. |
| `MapBackedNamedObjectIndex<N>` | General named-object index, including schemas; concurrent mutable or immutable membership depending on the constructor. |
| `ConcurrentDatabaseObjectIndex<D>` | Concurrent mutable database-object index. |
| `ConcurrentDependantObjectIndex<DO, D>` | Concurrent mutable dependent-object index with parent/name lookup. |
| `ImmutableDatabaseObjectIndex<D>` | Detached, immutable database-object membership. |

The read-only interfaces describe available operations, not deep immutability. Indexed objects remain shared references.

## Structured Keys Are Not Displayed Names

`NamedObjectKey` holds an ordered sequence of name parts. Equality preserves part boundaries and distinguishes `null`, an empty string, and a non-empty string. A dot within a part remains part of that identifier; it is not a separator to split later.

`key.startsWith(prefix)` compares whole components, case-sensitively and with null-safe equality, without constructing arrays or strings. An empty prefix matches every key; a null prefix or a prefix longer than the key does not match. Thus `["CAT", "APP", "a.b", "specific"]` starts with `["CAT", "APP"]` and `["CAT", "APP", "a.b"]`, but not `["CAT", "APP", "a"]`. Null and empty components remain distinct. This is not a prefix comparison of joined strings.

Hierarchical keys begin with their schema's `[catalog, schema]` components. Ordinary database objects append their name, routines append their ordinary name and specific name, and dependent objects append their child name to their parent's complete key. A schema prefix therefore selects all its indexed objects without invoking their schema accessors.

An object's `getFullName()` is its displayed qualified name. Display formatting can omit absent or empty qualifiers and apply quoting, so the displayed string is not a lossless encoding of its key. Different keys can have the same full name.

Indexes store one object per complete key, not one per full name. `lookup(key)` and `containsKey(key)` use key equality. `lookup(fullName)` scans values for exact displayed-name matches and selects their natural minimum, preserving natural-order first-match behavior without sorting the entire index. The plain named-object index copies an unsorted snapshot first; database-object indexes traverse live values without that copy. A name lookup therefore does not prove that the match is unique. When natural comparison ties, selection between tied matches is unspecified.

For n indexed objects and m matching candidates, full-name lookup performs O(n) name checks and O(m) natural comparisons. Unrelated objects are never naturally compared, and zero or one match requires no natural comparisons. Failures comparing actual matching candidates propagate to the caller; comparison metadata must still be ready and stable for those candidates. Matching remains case-sensitive and literal, including dots and quotes; lookup does not parse, normalize, or resolve identifiers.

## Schema Lookup: Blank Names And Duplicate Full Names

Schemas use `MapBackedNamedObjectIndex<Schema>`, rather than a database-object index. A schema's structured key consists of its catalog name and schema name. Either component can be absent or empty, depending on the JDBC metadata and database.

For example, these keys remain distinct even when their displayed full names coincide:

| Catalog component | Schema component | Complete key | Displayed full name |
|---|---|---|---|
| `null` | `"APP"` | `[null, "APP"]` | `APP` |
| `""` | `"APP"` | `["", "APP"]` | `APP` |
| `"APP"` | `null` | `["APP", null]` | `APP` |
| `null` | `null` | `[null, null]` | Empty string |
| `""` | `""` | `["", ""]` | Empty string |

The index retains all of these objects because their keys differ. Do not collapse schema membership into a map keyed only by `getFullName()`, or normalize null components to empty strings.

`MapBackedNamedObjectIndex.lookup(String)` accepts blank full names, including `""`; only a null argument is immediately rejected. It compares the supplied string exactly with `getFullName()`. Consequently, `Catalog.lookupSchema("")` can return an unnamed schema. The argument to `Catalog.lookupSchema(String)` is the complete displayed schema name, not necessarily the unqualified schema component.

When several schemas share that displayed name, lookup selects the natural-order first schema. `SchemaReference` compares catalog components first and schema components second, with nulls before non-null strings. This selection is not insertion-order selection, and the other matching schemas remain indexed.

```java
final Schema first = new SchemaReference(null, "APP");
final Schema second = new SchemaReference("", "APP");
final MapBackedNamedObjectIndex<Schema> schemas =
    new MapBackedNamedObjectIndex<>(List.of(second, first));

final Optional<Schema> byDisplayName = schemas.lookup("APP");
final Optional<Schema> byCompleteKey = schemas.lookup(second.key());
```

Here `byDisplayName` selects `first`, while `byCompleteKey` selects `second`. Both schemas remain members. When exact identity matters, retain the `Schema` or use its complete key on the index. Through the public catalog API, inspect `getSchemas()` and the schema components to disambiguate instead of assuming that a full-name lookup is unique.

## Database-Object Lookup And Overloaded Routines

`DatabaseObjectIndex` separates complete-key identity from schema/ordinary-name matching:

| Operation | Result |
|---|---|
| `lookup(key)` | The object stored under that exact complete key, if present. |
| `lookup(fullName)` | The natural-order first exact full-name match; rejects null or blank full names. |
| `hasObjects(schema)` | Whether any stored key starts with the schema key; short-circuits without fetching objects. |
| `getObjects(schema)` | All objects whose stored keys start with the schema key, sorted naturally. |
| `getObjects(schema, name)` | Ordinary mode: at most one complete-key match. Overload-aware mode: all matching schema/name key prefixes, sorted naturally. |
| `lookup(schema, name)` | Ordinary mode: the complete-key match. Overload-aware mode: the natural minimum among matching schema/name key prefixes. |

Schema matching uses the schema's structured key as a prefix, not displayed-name equality, reference identity, or object schema-accessor calls. All schema-scoped operations return empty results (or false for existence) for a null schema. Schema/name operations also reject a null or blank ordinary name. Filtered collection reads traverse stored keys, retrieve only matching values, and sort only those objects; they do not copy an entire membership snapshot or compare unrelated objects.

`ConcurrentDatabaseObjectIndex<D>()` and `ImmutableDatabaseObjectIndex<D>(values)` default to ordinary exact-key mode. Use `new ConcurrentDatabaseObjectIndex<Routine>(true)` or `new ImmutableDatabaseObjectIndex<Routine>(routines, true)` for overload-aware schema/name reads. The mode is fixed at construction, even for empty indexes; it is not inferred from their contents. Both modes preserve complete-key lookup. Mutable catalogs and immutable catalog projections use overload-aware mode for routines.

Routines show why the collection-returning operation is necessary. Overloaded functions or procedures can have the same schema and `getName()` but distinct complete keys. `MutableRoutine` extends its ordinary database-object key with the specific-name component used to distinguish overloads. Distinct keys allow all such routines to coexist without replacing one another.

Use the collection-returning catalog operation when looking for routines by ordinary name:

```java
final Collection<Routine> overloads = catalog.getRoutines(schema, "CALCULATE");
final Optional<Routine> firstMatch = catalog.lookupRoutine(schema, "CALCULATE");
```

`getRoutines(schema, "CALCULATE")` returns every indexed match, including multiple overloads. `lookupRoutine(schema, "CALCULATE")` returns only the natural-order first match. It does not perform SQL overload resolution, choose a signature based on argument types, or report ambiguity. Comparison ties have unspecified selection.

To select a particular overload, inspect the returned routines' specific names and parameter metadata, or use the routine's complete key when working directly with the index. Prefer an existing object's `key()` rather than reconstructing a key from its displayed full name. Preservation of overloads depends on the metadata supplying distinct complete keys; identical keys cannot coexist in the same index.

## Dependent-Object Lookup

`DependantObjectIndex.lookup(parent, childName)` appends the exact child name as one part of the parent's complete key, then performs a keyed lookup. It does not scan, sort, or search for a parent by displayed name. This supports objects such as table columns and routine parameters, whose identity includes their parent.

This overload rejects a null parent and a null or blank child name with an empty `Optional`. The inherited `lookup(schema, name)` operation is separate: ordinary mode uses the complete key formed from the schema key and supplied name, not a prefix scan. It cannot mistake a parent-name component for a child's name. Use parent/name lookup or a complete key to identify dependent objects.

Blank textual full-name and schema/name queries are rejected by database-object and dependent-object indexes, while plain named-object full-name lookup continues to allow blank names. This validates queries, not stored objects: complete-key lookup can still retrieve an indexed object with a null or blank name component. Nonblank names are matched literally without trimming whitespace.

## Membership, Enumeration, And Concurrency

Mutable indexes replace the previous object when `add(object)` uses an existing complete key. Successful non-null additions return `true`, including replacements. `remove(object)` removes the stored value under the supplied object's key and returns that stored value; it need not be the same instance as the argument. Null mutation arguments are no-ops.

`MapBackedNamedObjectIndex()` creates concurrent mutable membership. Its collection constructor copies immutable membership, retaining the last encountered object for duplicate keys; a null collection creates an empty immutable index. `ImmutableDatabaseObjectIndex` retains the first encountered object for each key and rejects a null collection. Immutable membership does not prevent changes to the referenced objects.

`getObjects()` and iteration create detached, unmodifiable lists sorted afresh, generally requiring O(n log n) comparisons. `snapshot()` creates a detached, unmodifiable collection in O(n) time without comparing elements; its iteration order is unspecified. Keep both operations: callers needing unordered whole-index access can avoid sorting and exclude objects whose comparison metadata is not yet ready.

For n indexed objects and m matching objects, the following bounds assume bounded key lengths and constant-time object accessors and comparisons. These are algorithmic bounds, not measured speedups.

| Operation | Time | Membership traversal |
|---|---|---|
| Complete-key lookup or membership check | Expected O(1) | Direct map read. |
| Ordinary schema/name lookup or collection | Expected O(1) | Direct map read; no scan or sort. |
| Dependent parent/name lookup | Expected O(1) | Direct map read. |
| Schema existence | O(n) worst case | Key-only traversal; stops at the first match. |
| Schema enumeration | O(n + m log m) | Key-prefix filter, matching-value retrieval, then sorting. |
| Overload-aware singular schema/name lookup | O(n) | Key-prefix filter and natural minimum over matches. |
| Overload-aware schema/name collection | O(n + m log m) | Key-prefix filter, matching-value retrieval, then sorting. |
| Displayed full-name lookup | O(n) | Value filter and natural minimum over matches. |

Prefix filtering does not make hash-map scans sublinear or introduce a separately maintained schema index. Schema and overload prefix reads avoid whole-index snapshot copies, but still allocate query keys, stream machinery, or result lists as applicable. Full-name lookup deliberately retains displayed-name access rather than joining keys.

Internal retrieval, task submission, constraint matching, graph construction, set construction, and working-copy creation use snapshots when input order is irrelevant. Their traversal and query-submission order is unspecified. Public catalog and model getters, positional columns and parameters, result-column first-match lookup, index iteration and string output retain their ordered behavior. Related-table lists remain alphabetical, foreign-key lists retain imported/exported grouping and natural ordering, and graph sort indexes retain topological level ordering with views after tables.

Concurrent indexes protect individual map operations. Enumeration, prefix scans, and snapshot copying are weakly consistent during concurrent membership changes, not atomic point-in-time views. A value removed between key traversal and map retrieval is omitted; concurrent additions and replacements may or may not be observed. Key-only existence is an observation during traversal, not a guarantee of subsequent membership. Returned collections remain detached and unmodifiable. Compound operations, changes across indexes, and object metadata are not synchronized. Keys must remain stable while objects are indexed, and comparison state must remain stable during sorting or minimum selection.

## Migration From Specialized Routine Indexes

`ConcurrentRoutineIndex` and `ImmutableRoutineIndex` have been removed, along with the internal `FilterForSchema` helper. Replace their constructors with `ConcurrentDatabaseObjectIndex<>(true)` and `ImmutableDatabaseObjectIndex<>(routines, true)` respectively. Do not omit the flag: default ordinary mode cannot select overloads whose keys contain an appended specific name.

Removing the public routine classes is an intentional source and binary compatibility break; no compatibility wrappers are provided. Recompile consumers against the new types. Previously serialized graphs containing either removed class cannot be deserialized using this version; regenerate those catalogs from their metadata source. New general indexes serialize their construction mode when their indexed objects are serializable.

## SchemaCrawler Code Reference

All paths below are relative to `SchemaCrawler-Core`.

| Source | Relevant behavior |
|---|---|
| `schemacrawler-api\src\main\java\schemacrawler\namedobject\` | Sealed index interfaces, abstract bases, and concrete implementations. |
| `schemacrawler-api\src\main\java\schemacrawler\schema\NamedObjectKey.java` | Structured key equality, component prefixes, and appending child-name parts. |
| `schemacrawler-api\src\main\java\schemacrawler\schemacrawler\SchemaReference.java` | Schema key construction, displayed names, and natural ordering. |
| `schemacrawler-api\src\main\java\schemacrawler\crawl\MutableRoutine.java` | Specific-name key component and routine natural ordering. |
| `schemacrawler-api\src\main\java\schemacrawler\namedobject\AbstractCatalog.java` | Delegation of schema lookup, routine enumeration, and single-routine lookup to indexes. |
| `schemacrawler-api\src\main\java\schemacrawler\schema\Catalog.java` | Public catalog lookup and enumeration API. |
