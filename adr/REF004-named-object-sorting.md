# Named Object Sorting Reference

## Purpose

This reference describes how SchemaCrawler orders catalog objects, database objects, and their dependants. It covers the public alphabetical and natural sort modes, the structural rules shared by model implementations, and database-specific naming observations relevant to sorting.

Sorting is based on the completed model's object roles, metadata fields, displayed names, and structured keys. It does not use a database product name to choose a different comparator.

## Public Sorting Modes

`NamedObjectSort` provides two public modes:

| Mode | Ordering |
|---|---|
| `alphabetical` | Normalized full name, then exact structured key |
| `natural` | The object's `compareTo` implementation and its model-specific ordering stages |

Both public comparators place a null object before a non-null object, and two null objects compare as equal. A direct call on a non-null object's `compareTo(null)` places that object after null. These are separate entry points with the same null-first ordering.

The shared null/identity comparison is an early stage for named-object comparisons. A null operand is resolved before object fields are read, and identical references compare as equal. Otherwise, comparison continues with the remaining stages.

## Why Nulls First

Nulls first has two useful effects:

1. It is a safe first check. Missing operands are ordered before a comparator dereferences either object or reads its fields.
2. It places system-scoped objects before named-schema objects. Schema keys contain catalog and schema components, and null key components sort before non-null components. System schemas represented without a name therefore precede named schemas without a separate system-schema category.

Null and an empty string remain distinct values. For most named objects with populated fields, the null policy does not alter their ordinary ordering.

## Natural Ordering: Shared Structural Stages

`NamedObjectComparators` supplies reusable comparison stages. The broad ordering separates object families before applying fields that only make sense within a compatible family.

### Outer groups

The outer group order is:

1. Catalogs
2. Schemas
3. Database objects, including dependant objects
4. Database users
5. Other named objects, including ER-model wrappers

Within the database-object group, objects are first compared by schema. Category order is applied only when their schemas compare equally. This means schema order takes precedence over category order: an object in an earlier schema sorts before a different category in a later schema.

Within the same schema, category order is:

| Order | Category |
|---:|---|
| 1 | Table |
| 2 | View |
| 3 | Procedure |
| 4 | Function |
| 5 | Dependant database object |
| 6 | Sequence |
| 7 | Synonym |
| 8 | Unknown or other database object |

Table and view classification is based on table type. Procedure and function roles are distinct. The comparator maps the `SimpleDatabaseObjectType` values to explicit category ranks; it does not rely on enum declaration order or implementation class names.

### Dependant objects

When two dependant objects reach the same structural category, their parent objects are compared naturally first. If the parents compare equally, dependant role order is:

1. Key column
2. Ordinary column, routine parameter, or result column
3. Index
4. Table reference, including foreign keys and implicit associations
5. Other table constraint
6. Privilege
7. Trigger
8. Other dependant

Role classification checks specialized interfaces before their broader interfaces. In particular, `KeyColumn` precedes `BaseColumn`, and `TableReference` precedes `TableConstraint`. A foreign key's parent for this ordering is its containing table.

## Object-Specific Natural Ordering

After the shared structural stages, built-in model objects apply their relevant fields:

| Object | Remaining comparison fields, in order |
|---|---|
| Generic database object | Compatible natural type, normalized full name, exact key |
| Table or view | Graph sort index, natural table type, normalized full name, exact key |
| Ordinary column, result column, or routine parameter | Ordinal position, natural column data type, normalized full name, exact key |
| Key column | Key ordinal position, natural column data type, normalized full name, exact key |
| Index | Primary-key-index flag (true first), uniqueness (unique first), natural index type, normalized full name, exact key |
| Table reference | Natural constraint type, normalized full name, exact key |
| Other table constraint | Natural constraint type, normalized full name, exact key |
| Routine | Natural routine type and normalized full name, then specific name and exact key |
| Generic named object or ER-model wrapper | Normalized full name, exact key |

The graph sort index on tables reflects the table dependency ordering prepared by SchemaCrawler. For indexes, comparison uses scalar properties and the index's name and key; it does not compare the list of indexed columns. Table-reference ordering likewise uses its structural role, type, name, and key rather than its column mappings. Mapping comparison remains a separate operation used for mapping-level matching and ordering.

Routine order does not read the parameter list. A routine's specific name is compared after its type and normalized full name, with the exact key as the terminal tie-breaker. Parameter objects are ordered as dependants of their routine, then by their own ordinal position, type, name, and key.

Compatible type objects use their natural ordering. Type comparison is reached only after the structural stages establish a compatible object family. Partial database objects whose type accessor is not available are tolerated by the shared type comparison.

## Names and Structured Keys

Normalized full names are case-insensitive and lossy: sorting retains letters, digits, underscores, and dots, and ignores other punctuation and whitespace. This is not database-specific collation, numeric-aware ordering, Unicode normalization, or full Unicode case folding.

Different displayed names can normalize to the same text. Alphabetical sorting resolves such ties, and natural ordering resolves remaining model-field ties, using the exact `NamedObjectKey`. Keys compare component by component, preserving case, component boundaries, and the distinction between null and empty components. A flattened or joined display string is not a substitute for the structured key.

If both the normalized name and exact key compare equally, the ordering returns zero. There is no instance-identity or identity-hash tie-breaker for named objects. Sorted collections use comparison results to determine membership, so comparison equality—not `equals`—determines whether two values occupy distinct sorted positions.

## Consistency of `equals`, `hashCode` and `compareTo`

Natural ordering is deliberately richer than identity. Several classes therefore have a `compareTo` that is not consistent with `equals`. In every class, `hashCode` is consistent with `equals`, with the exception noted for `ProposedAssociation`. Code must not assume that `compareTo(x) == 0` means `equals(x)`, or the reverse, for the classes listed below. In particular, a `TreeSet` or `TreeMap` uses `compareTo` for membership while a `HashSet` or `HashMap` uses `equals` and `hashCode`; the two can disagree.

### Consistent

For these classes, `equals`, `hashCode`, and `compareTo` agree on which values are the same:

| Class | Basis |
|---|---|
| `NamedObjectKey` | Component-wise key |
| `SchemaReference` | Catalog name and schema name |
| `TableType` | Case-insensitive table type name |
| `PropertyName` | Case-insensitive name; the description is ignored by all three |
| `DatabaseServerType` | Identifier (case-insensitive); the unknown type sorts first but is not equal to any other type |

### Not consistent

| Class | `equals` and `hashCode` use | `compareTo` uses | How they diverge |
|---|---|---|---|
| Database objects: table, view, column, index, sequence and other `AbstractDatabaseObject` types | Name and schema | Structural stages, then fields such as graph sort index, table type, index uniqueness and type, then normalized name and key | Objects that are equal can order differently when these fields differ. Fields are populated during model construction, so ordering may change until the model is built. |
| Dependant objects: columns, key columns, indexes, constraints, foreign keys, implicit associations, triggers, privileges | Name and parent | Parent, dependant role, ordinal or key position, type, name, and key | Equal objects can differ in ordinal position, key position, or type. Foreign keys and implicit associations are ordered by constraint type, name, and key, and never by column mappings. |
| `MutableRoutine` (procedures and functions) | Name and schema | Type and normalized name, then specific name, then key | Overloads with the same name and different specific names are equal but sort differently. |
| `ImmutableColumnReference` | Foreign-key column and primary-key column | Key sequence, then foreign-key and primary-key column names | References to the same column pair with different key sequences are equal but sort differently. |
| `MutablePrivilege.PrivilegeGrant` | Parent, grantor, grantee, and grantable flag; case-sensitive | Grantor and grantee (case-insensitive), then parent key, then grantable flag | Grants whose grantor or grantee differ only by case compare as zero but are not equal. |
| `JavaSqlType` | Vendor type number | Case-insensitive type name | Types with the same name and different vendor type numbers compare as zero but are not equal. Types with the same vendor type number and different names are equal but sort differently. |
| `Property` implementations (`AbstractProperty`, including `ImmutableDatabaseProperty` and `ImmutableServerInfoProperty`) | Property name and value | Name by default; `ImmutableDatabaseProperty` compares the description | Properties that differ only by value compare as zero but are not equal. |
| ER-model wrappers (`AbstractDatabaseObjectBacked`) | Key of the wrapped object; accepts any `NamedObject` with an equal key | Object family, normalized name, then key | Comparison is field-based while equality is key-only. Because `equals` accepts any `NamedObject`, equality with a non-wrapper object is not symmetric. |
| `ObjectAttributes` (YAML attribute DTOs) | Identity (not overridden) | Case-insensitive name | Two instances with the same name compare as zero but are not equal. |
| `ProposedAssociation` | Not supported: `equals` and `hashCode` throw `UnsupportedOperationException` | Not supported for any operand other than itself or null | Intentional guard that prevents instances from being added to hash-based or sorted collections. |

Within the database-object and dependant rows, the exact key is the terminal tie-breaker, so `compareTo` returns zero only when keys are equal. The reverse direction does not hold: equal objects do not always compare as zero. Use the `NamedObjectSort.natural` comparator for ordering and the object's `equals` for identity, and do not use one in place of the other.

The consistency of the classes in both tables, using values that avoid the divergences listed, is asserted by `equalsHashCodeAndCompareToAreConsistent` and `equalsHashCodeAndCompareToAreConsistentForRelatedObjects` in [CompareToTest.java](../../SchemaCrawler-Core/schemacrawler-api/src/test/java/schemacrawler/test/sort/CompareToTest.java). The divergences themselves are not exercised by those tests, apart from the existing sort tests. Existing Javadoc on `AbstractDatabaseObject`, `MutableRoutine`, `ImmutableColumnReference`, and `PrivilegeGrant` also states that `compareTo` is not compatible with `equals`.

## Database-System Naming Observations

Database systems supply object names through metadata, and some names are generated by the database or by SchemaCrawler when metadata does not provide one. Names observed in checked-in connection fixtures include the following:

| Database or captured test path | Primary-key names | Index names | Foreign-key names |
|---|---|---|---|
| SQLite | Missing names confirmed in the main details and edge-case fixtures | Named indexes observed, including `sqlite_autoindex_A_1` | Missing metadata names observed; SchemaCrawler supplies fallback names |
| Cassandra 5.0.4 / Cassandra JDBC Driver 5.0.3 | Missing primary-key name confirmed | Named statistic index observed | Not shown |
| DuckDB v1.5.6 / DuckDBJ 1.0 | Missing names confirmed | Not established by the fixture because index names are hidden | Named foreign-key headings observed |
| H2 | Named in captured output | Hidden explicitly by test options; this does not establish missing metadata names | Named in captured output |
| HSQLDB | Named, including generated names | Named | Named, including generated names |
| DB2, Microsoft Access, Firebird, Informix, MariaDB, MySQL, Oracle, PostgreSQL, SQL Server | Named in captured output | Named in captured output, with SQL Server's index query excluding null names | Named in captured output |
| ClickHouse and Hive | Named primary-key headings observed | Not shown | Not shown |
| Calcite, Snowflake, Teiid, and Trino | Not shown in the inspected outputs | Not shown | Not shown |

These are observations from the inspected test fixtures, not a universal capability matrix for every engine version or JDBC driver. “Not shown” means the fixtures do not establish whether the object or its name is available. A generated identifier is still a name. An output formatter that hides names also does not demonstrate that metadata names are missing.

Representative evidence is available in the checked-in [SQLite details fixture](../../SchemaCrawler/schemacrawler-sqlite/src/test/resources/SQLiteTest.details), [Cassandra connection output](../../SchemaCrawler/schemacrawler-dbconnectors/src/test/resources/testCassandraWithConnection.txt), [DuckDB connection output](../../SchemaCrawler/schemacrawler-dbconnectors/src/test/resources/testDuckDBWithConnection.txt), and [H2 connection output](../../SchemaCrawler/schemacrawler-dbconnectors/src/test/resources/testH2WithConnection.txt). Other captured connection outputs are in the [connector test resources](../../SchemaCrawler/schemacrawler-dbconnectors/src/test/resources/).

SchemaCrawler recognizes common system-generated foreign-key name patterns associated with Firebird, H2, HSQLDB, DB2, MySQL and MariaDB, Oracle, PostgreSQL, and SQL Server. These names are treated as ordinary object names by the sorting algorithm. Missing names may be assigned fallback names during metadata retrieval; where a source name is absent, exact parent and object-key components still supply structured comparison information.

## Implementation Reference

The primary implementation points in SchemaCrawler-Core are:

| Source | Sorting responsibility |
|---|---|
| [NamedObjectSort.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/namedobject/NamedObjectSort.java) | Public alphabetical and natural modes |
| [NamedObjectComparators.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/namedobject/NamedObjectComparators.java) | Shared null/identity, family, schema, dependant, type, normalized-name, and key stages |
| [MetaDataUtility.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/utility/MetaDataUtility.java) | Database-object and dependant-role classification |
| [AbstractDatabaseObject.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/AbstractDatabaseObject.java) | Common natural ordering for database objects |
| [MutableTable.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/MutableTable.java) | Table graph-index ordering |
| [AbstractColumn.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/AbstractColumn.java) and [AbstractKeyColumn.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/AbstractKeyColumn.java) | Column and key-column ordering |
| [MutableIndex.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/MutableIndex.java) | Index scalar-property, type, name, and key ordering |
| [MutableRoutine.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/crawl/MutableRoutine.java) | Routine type/name/specific-name/key ordering |
| [SchemaReference.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/schemacrawler/SchemaReference.java) and [NamedObjectKey.java](../../SchemaCrawler-Core/schemacrawler-api/src/main/java/schemacrawler/schema/NamedObjectKey.java) | Schema-key and component-wise key ordering |
| [AbstractDatabaseObjectBacked.java](../../SchemaCrawler-Core/schemacrawler-ermodel/src/main/java/schemacrawler/ermodel/implementation/AbstractDatabaseObjectBacked.java) | Named-object ordering for database-backed ER-model wrappers |

Comparison fields must remain stable while objects are being sorted. Some natural-order fields, such as graph sort indices and dependant positions, are populated during model construction.
