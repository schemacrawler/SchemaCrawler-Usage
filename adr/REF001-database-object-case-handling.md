# Database Object Case Handling Reference

## Purpose

This document is a reference on how databases handle database-object identifier case, and how
SchemaCrawler represents, searches, and displays those database object names.

The first part is database research: it describes identifier storage, identifier resolution, JDBC
metadata flags, and vendor-specific configuration without taking a SchemaCrawler position. The
second part states SchemaCrawler's position and points to the relevant code so this can be used as a
future implementation and design reference.

The repeated-test discussion is intentionally excluded.

## Identifier Case Concepts

Before comparing databases, separate the two behaviors that are often compressed into the phrase
"case sensitivity." A database can change how an identifier is stored, and it can independently
decide whether differently cased spellings resolve to the same object.

1. **Storage or normalization** - whether an identifier is folded to uppercase, folded to lowercase,
   or retained in its original spelling.
2. **Resolution** - whether the database resolves different spellings as the same identifier or
   distinguishes them.

Also distinguish:

- Regular or unquoted identifiers, such as `CustomerOrder`.
- Delimited or quoted identifiers, such as `"CustomerOrder"` or MySQL's `` `CustomerOrder` ``.
- Catalog spelling returned by metadata calls.
- Object-specific or instance-specific behavior.

The four practically useful case modes are:

| Mode | Meaning |
|---|---|
| `UPPER / CI` | Unquoted names are normalized or stored uppercase and are case-insensitive when resolved. |
| `lower / CI` | Unquoted names are normalized or stored lowercase and are case-insensitive when resolved. |
| `preserve / CI` | Original spelling is retained, but lookup is case-insensitive. |
| `preserve / CS` | Original spelling is retained and lookup is case-sensitive. |

`CI` means case-insensitive and `CS` means case-sensitive.

### Why `UPPER / CS` Is Usually Not A Useful Mode

If an engine converts every unquoted input to uppercase before lookup, then these references all
become the same identifier:

```sql
SELECT * FROM customer;
SELECT * FROM Customer;
SELECT * FROM CUSTOMER;
```

Consequently, the externally observable behavior is `UPPER / CI`, even if the catalog internally
compares already-uppercase strings using a case-sensitive comparison. The same reasoning applies to
`lower / CS`.

An individual quoted object can be named `"CUSTOMER"` or `"customer"` and still be case-sensitive.
That is normally part of the broader `preserve / CS` quoted-identifier model, not a separate
`UPPER / CS` or `lower / CS` model.

## Database Behavior Matrix

The matrix below summarizes common behavior for schemas, databases, tables, and similar object
names. It is a behavioral model, not a guarantee of what every JDBC driver will report. Columns,
aliases, session settings, compatibility modes, and vendor-specific catalogs can add more rules.

| Database System | Regular Or Unquoted Identifiers | Delimited Or Quoted Identifiers | Configuration And Design Implications |
|---|---|---|---|
| Oracle Database | `UPPER / CI` | `preserve / CS` | Ordinary identifiers are interpreted as uppercase. Quoted identifiers preserve case and must be referenced with the appropriate quoting and spelling. [web:17] |
| PostgreSQL | `lower / CI` | `preserve / CS` | Unquoted identifiers are folded to lowercase. `"foo"` and unquoted `foo` can refer to the same lowercase object, while `"Foo"` is distinct. [web:22] |
| MySQL | Depends on `lower_case_table_names`: `0` is generally `preserve / CS`, `1` is `lower / CI`, and `2` is `preserve / CI` | Quoting does not provide an independent table-name case mode; table and database rules still apply | The setting is important for database and table names, is affected by the filesystem, and is normally fixed when the data directory is initialized. Column names have different rules. [web:58] |
| MariaDB | Similar `lower_case_table_names` modes: `0`, `1`, and `2` | Similar to regular table/database-name behavior | The setting is documented as an initialization-time setting. [web:143] |
| Microsoft SQL Server | Usually `preserve / CI`, or `preserve / CS` under a case-sensitive catalog/database collation | Delimitation does not independently change case sensitivity; the applicable collation still controls resolution | The database or catalog collation is significant for schemas, tables, and columns. `QUOTED_IDENTIFIER` controls parsing of double quotes, not identifier case sensitivity. [web:28] |
| IBM Db2 | `UPPER / CI` | `preserve / CS` | Ordinary identifiers are folded to uppercase. Delimited identifiers preserve lowercase and mixed-case characters. [web:61] |
| Snowflake | `UPPER / CI` | Default `preserve / CS` | `QUOTED_IDENTIFIERS_IGNORE_CASE` can change quoted-identifier behavior for the relevant session and object-creation context. [web:41] |
| SQLite | Generally `preserve / CI` for ordinary ASCII case comparisons | Generally `preserve / CI`; quoting primarily delimits the name | SQLite does not provide the usual Oracle/PostgreSQL model in which double quotes automatically make identifiers case-sensitive. The default case-insensitivity is primarily defined for ASCII characters. [web:73] |
| H2 | Default `UPPER / CI`, because unquoted names are converted to uppercase | Default `preserve / CS` | `DATABASE_TO_UPPER`, `DATABASE_TO_LOWER`, and `CASE_INSENSITIVE_IDENTIFIERS` can change behavior. These are database settings and should be considered when interpreting metadata. [web:75][web:83] |
| HSQLDB / HyperSQL | `UPPER / CI` | `preserve / CS` | Unquoted identifiers are converted to uppercase; quoted identifiers are retained and case-sensitive. [web:82] |

## JDBC Metadata Mapping

JDBC exposes identifier-case behavior through `java.sql.DatabaseMetaData`. The method names are easy
to misread: `storesMixedCaseIdentifiers()` means "preserve mixed case but do not distinguish it,"
while `supportsMixedCaseIdentifiers()` means "preserve and distinguish mixed case."

For regular identifiers:

| Method | Meaning |
|---|---|
| `storesUpperCaseIdentifiers()` | Mixed-case regular identifiers are treated as case-insensitive and stored uppercase. |
| `storesLowerCaseIdentifiers()` | Mixed-case regular identifiers are treated as case-insensitive and stored lowercase. |
| `storesMixedCaseIdentifiers()` | Mixed-case regular identifiers are treated as case-insensitive and stored with mixed case preserved. |
| `supportsMixedCaseIdentifiers()` | Mixed-case regular identifiers are treated as case-sensitive and stored with mixed case preserved. |

For quoted identifiers:

| Method | Meaning |
|---|---|
| `storesUpperCaseQuotedIdentifiers()` | Mixed-case quoted identifiers are treated as case-insensitive and stored uppercase. |
| `storesLowerCaseQuotedIdentifiers()` | Mixed-case quoted identifiers are treated as case-insensitive and stored lowercase. |
| `storesMixedCaseQuotedIdentifiers()` | Mixed-case quoted identifiers are treated as case-insensitive and stored with mixed case preserved. |
| `supportsMixedCaseQuotedIdentifiers()` | Mixed-case quoted identifiers are treated as case-sensitive and stored with mixed case preserved. |

A diagnostic classification can be written as:

```java
static String identifierMode(final DatabaseMetaData metaData, final boolean quoted)
    throws SQLException {
  if (quoted) {
    if (metaData.storesLowerCaseQuotedIdentifiers()) {
      return "lower / case-insensitive";
    }
    if (metaData.storesUpperCaseQuotedIdentifiers()) {
      return "UPPER / case-insensitive";
    }
    if (metaData.storesMixedCaseQuotedIdentifiers()) {
      return "preserve / case-insensitive";
    }
    if (metaData.supportsMixedCaseQuotedIdentifiers()) {
      return "preserve / case-sensitive";
    }
  } else {
    if (metaData.storesLowerCaseIdentifiers()) {
      return "lower / case-insensitive";
    }
    if (metaData.storesUpperCaseIdentifiers()) {
      return "UPPER / case-insensitive";
    }
    if (metaData.storesMixedCaseIdentifiers()) {
      return "preserve / case-insensitive";
    }
    if (metaData.supportsMixedCaseIdentifiers()) {
      return "preserve / case-sensitive";
    }
  }

  return "unknown or non-standard driver behavior";
}
```

Useful connection diagnostics include:

```java
final DatabaseMetaData metaData = connection.getMetaData();

System.out.println(metaData.getDatabaseProductName());
System.out.println(metaData.getDatabaseProductVersion());
System.out.println(metaData.getDriverName());
System.out.println(metaData.getDriverVersion());
System.out.println("Regular: " + identifierMode(metaData, false));
System.out.println("Quoted:  " + identifierMode(metaData, true));
System.out.println("Quote:   " + metaData.getIdentifierQuoteString());
```

`getIdentifierQuoteString()` reports the delimiter used by the driver, or a space when identifier
quoting is unsupported. JDBC-compliant drivers commonly report `"`; MySQL drivers commonly use the
vendor-appropriate delimiter. [web:126]

## Metadata Search Patterns And Catalog Spelling

JDBC metadata methods do not parse SQL. A `getTables()` or `getColumns()` argument is a metadata
search pattern, not an SQL identifier whose case will necessarily be normalized by the database
parser.

For example:

```java
try (ResultSet tables =
    metaData.getTables(catalog, schemaPattern, tableNamePattern, new String[] {"TABLE", "VIEW"})) {

  while (tables.next()) {
    final String returnedCatalog = tables.getString("TABLE_CAT");
    final String returnedSchema = tables.getString("TABLE_SCHEM");
    final String returnedTable = tables.getString("TABLE_NAME");

    // Preserve these values exactly for later metadata calls.
  }
}
```

Portable metadata traversal generally follows these rules:

1. Enumerate schemas and objects using broad or null patterns when the desired case is unknown.
2. Preserve the exact catalog spelling returned in `TABLE_SCHEM`, `TABLE_NAME`, and related columns.
3. Reuse those returned values for subsequent JDBC metadata calls.
4. Do not blindly call `toUpperCase()` or `toLowerCase()` on names returned by metadata.
5. Use identifier mode only when interpreting or generating a new unquoted SQL name.
6. Treat quoted, case-sensitive names as opaque strings that must retain their exact spelling.
7. Escape `%` and `_` when searching for a literal name, using `getSearchStringEscape()`.

## Configuration Not Always Exposed By JDBC

The metadata flags are a portable baseline. Configuration-dependent systems may need vendor-specific
queries or connection settings to understand the effective behavior.

| System | Configuration Check | Why It Matters |
|---|---|---|
| MySQL | `SELECT @@lower_case_table_names` | Determines the handling of database and table names. |
| MariaDB | `SELECT @@lower_case_table_names` | Determines the handling of database and table names. |
| SQL Server | `SELECT DATABASEPROPERTYEX(DB_NAME(), 'Collation')` | The database/catalog collation can distinguish `CI` from `CS`. [web:28] |
| Snowflake | `SHOW PARAMETERS LIKE 'QUOTED_IDENTIFIERS_IGNORE_CASE' IN SESSION` | Quoted identifier resolution can be session-dependent. [web:41] |
| H2 | Inspect URL/settings such as `DATABASE_TO_UPPER`, `DATABASE_TO_LOWER`, and `CASE_INSENSITIVE_IDENTIFIERS` | These settings can alter the normal H2 behavior. [web:75] |

The effective policy can therefore depend on:

- Server or database configuration.
- Session settings.
- Filesystem behavior, particularly for MySQL and MariaDB.
- Database edition or compatibility mode.
- Object category, such as table versus column.
- JDBC driver implementation.

## Database Research Conclusions

The database-side research leads to these general conclusions:

- Do not model identifier behavior as a single case-sensitive or case-insensitive switch.
- Keep regular and quoted identifier behavior separate.
- Keep storage or normalization separate from resolution.
- Treat metadata-returned spelling as authoritative for later metadata traversal.
- Treat JDBC metadata as a capability report, not a complete configuration report.
- Expect an `unknown` or contradictory state from some drivers and configurations.
- Do not confuse identifier case with data comparison collation.

Case sensitivity for object names is separate from case sensitivity in predicates such as:

```sql
WHERE name = 'Alice'
```

SQL Server collations can affect both areas, but identifier behavior and column-data comparison
behavior should be reasoned about separately.

## SchemaCrawler Position

SchemaCrawler's position is intentionally conservative:

1. **Do not rewrite database object names to a preferred case.**
2. **Preserve the names that the database and JDBC metadata return.**
3. **Use exact keys for internal catalog identity and retrieval.**
4. **Provide search and filter APIs that can be case-insensitive when callers ask for that behavior.**
5. **Make full-name regular-expression matching quote-tolerant so displayed quoting does not block
   user intent.**

SchemaCrawler should not infer a global "database case" and apply it to every name. Database object
names are data returned by the database. If a database returns `BOOKS`, `books`, or `"Books.Table"`,
SchemaCrawler keeps that spelling for display, output, filtering, and follow-up metadata traversal.

## SchemaCrawler Code Reference

These are the main code locations for current case and lookup behavior.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schema\IdentifiersBuilder.java`
captures identifier-quoting metadata. `fromConnection(Connection)` reads
`DatabaseMetaData.getIdentifierQuoteString()` and derives `quoteMixedCaseIdentifiers` from
`!metaData.supportsMixedCaseIdentifiers()`.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schemacrawler\SchemaRetrievalOptionsBuilder.java`
handles schema-retrieval quote-string defaulting. `lookupIdentifierQuoteString(DatabaseMetaData)`
defaults to SQL-standard `"`, allows an explicit override, and otherwise asks `DatabaseMetaData`.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schema\NamedObjectKey.java`
is the internal identity key. It stores key parts exactly as supplied, compares with
`Arrays.equals(...)`, and joins non-blank parts with `.` without splitting embedded delimiters.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\crawl\NamedObjectList.java`
is the internal catalog lookup container. It stores objects in a
`ConcurrentHashMap<NamedObjectKey, N>` and looks them up by the exact `NamedObjectKey`.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\CatalogSearcher.java`
is the catalog search wrapper. It provides `findTables`, `findRoutines`, `findColumns`, and other
search methods that apply caller-provided `NamedObjectFilter`s without changing the catalog.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\NamedObjectFilter.java`
defines the filter contract: a typed `Predicate<N extends NamedObject>` for named-object selection.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\NamedObjectFilters.java`
contains the public filter factories. `nameRegex(String)` and `fullNameRegex(String)` compile
patterns with `Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE`. `fullName(InclusionRule)` preserves
the caller's rule and flags, and routes regex rules to the quote-tolerant full-name implementation.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\InclusionRuleFilter.java`
wraps an `InclusionRule` as a `NamedObjectFilter` over displayed full names.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\QuoteTolerantFullNameInclusionRuleFilter.java`
implements quote-tolerant regex full-name matching. It tests regex inclusion and exclusion against
both displayed full name and unquoted joined-key full name.

## Preserve Database-Provided Case

SchemaCrawler should preserve database object names as returned by JDBC metadata and vendor-specific
retrievers. It should not use the JDBC metadata case flags as an instruction to normalize every
returned name.

This is the safest behavior because:

- JDBC search patterns are not SQL identifiers.
- The spelling returned in metadata result sets is the best value to reuse in later metadata calls.
- Databases can have different rules for unquoted identifiers, quoted identifiers, table names,
  column names, aliases, schemas, and catalog names.
- Vendor configuration can change behavior at the database, filesystem, session, or compatibility
  level.

## Use Exact Keys For Internal Identity

SchemaCrawler's internal identity mechanism is exact-key based.

`NamedObjectKey` stores key parts as supplied, compares them with `Arrays.equals(...)`, and hashes
them with `Arrays.hashCode(...)`. It does not case-fold key parts. `NamedObjectList` stores and
retrieves objects by `NamedObjectKey` in maps.

That means internal identity and lookup remain deterministic and do not depend on a guessed database
case policy. If two objects differ only by case and the database reports them as distinct, exact keys
allow SchemaCrawler to represent that distinction.

## Use Identifier Metadata For Quoting, Not Global Renaming

SchemaCrawler reads identifier metadata so it can quote or render identifiers appropriately, not so
it can rewrite catalog object names.

Important code paths:

- `IdentifiersBuilder.fromConnection(Connection)` reads:
  - `DatabaseMetaData.getIdentifierQuoteString()`
  - `DatabaseMetaData.supportsMixedCaseIdentifiers()`
- `SchemaRetrievalOptionsBuilder.lookupIdentifierQuoteString(DatabaseMetaData)` uses:
  - explicit SchemaCrawler options when provided
  - JDBC metadata when available
  - SQL-standard `"` as a default

This keeps the metadata useful for display and SQL generation while preserving the database-provided
catalog spelling.

## Allow Case-Insensitive Searches

SchemaCrawler supports case-insensitive object searches at the filter layer instead of changing the
stored catalog names.

`NamedObjectFilters.nameRegex(String)` and `NamedObjectFilters.fullNameRegex(String)` compile
regular expressions with:

```java
Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE
```

This provides case-insensitive search behavior for callers who want it, while leaving object names
and internal keys unchanged.

`CatalogSearcher` is the search entry point for catalog contents. It wraps a `Catalog` and offers
typed methods such as `findTables(...)`, `findRoutines(...)`, and `findColumns(...)`, each accepting
a `NamedObjectFilter<? super T>`. The searcher filters the current visible catalog; it does not
change the catalog.

## Allow Quote-Tolerant Full-Name Searches

SchemaCrawler also supports quote-tolerant full-name regex matching for callers who are searching by
database object name.

The important distinction is:

- `NamedObject.getFullName()` is the displayed full name. It may include quotes or other display
  formatting when needed.
- `NamedObject.key().join()` is the joined internal key form. It preserves embedded delimiter
  characters within individual key parts and joins the captured parts with `.`.

`QuoteTolerantFullNameInclusionRuleFilter` tests regular-expression inclusion and exclusion against
both forms:

1. the displayed full name, and
2. the unquoted joined-key full name.

This allows a user-supplied unquoted regex to match a displayed full name that is quoted only because
the identifier needs quoting for display. It also prevents exclusion bypasses: exclusions are tested
against both forms before an object is accepted.

`NamedObjectFilters.fullName(InclusionRule)` is the public factory that selects this behavior for
regular-expression inclusion rules. Callers that need to preserve their own `Pattern` flags should
construct a `RegularExpressionInclusionRule` and pass it to `NamedObjectFilters.fullName(...)`
instead of using `fullNameRegex(...)`, which intentionally compiles case-insensitive patterns.

## Preserve Caller Intent In Filter APIs

SchemaCrawler should keep these search modes distinct:

| Caller Need | Preferred API | Case Behavior |
|---|---|---|
| Case-insensitive simple-name regex | `NamedObjectFilters.nameRegex(regex)` | Compiles case-insensitive and Unicode-aware. |
| Case-insensitive full-name regex | `NamedObjectFilters.fullNameRegex(regex)` | Compiles case-insensitive and Unicode-aware; also quote-tolerant. |
| Caller-provided inclusion rule | `NamedObjectFilters.fullName(inclusionRule)` | Preserves the rule's own regex flags; regex rules are quote-tolerant. |
| Catalog-wide typed search | `CatalogSearcher.search(catalog).findTables(filter)` and related methods | Applies the supplied filter without mutating names. |
| Exact internal catalog identity | `NamedObjectKey` and `NamedObjectList` | Exact key comparison; no case folding. |

This keeps the database-facing representation stable while giving callers explicit search behavior.

## Future Reference Checklist

Use this checklist when changing code that deals with database object names:

- Preserve the spelling returned by JDBC metadata or vendor-specific retrievers.
- Do not apply global `toUpperCase()` or `toLowerCase()` transformations to catalog names.
- Use exact `NamedObjectKey` lookup for internal identity.
- Use `CatalogSearcher` and `NamedObjectFilter` for search behavior.
- Use `NamedObjectFilters.nameRegex(...)` for case-insensitive simple-name searches.
- Use `NamedObjectFilters.fullNameRegex(...)` for case-insensitive, quote-tolerant full-name
  searches.
- Use `NamedObjectFilters.fullName(new RegularExpressionInclusionRule(pattern))` when caller-provided
  regex flags must be preserved.
- Keep JDBC metadata flags as diagnostics and quoting guidance, not as a mandate to rewrite catalog
  names.
- Consider vendor configuration separately when diagnosing observed database behavior.
