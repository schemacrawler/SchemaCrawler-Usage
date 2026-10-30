# Catalog Projection Reference

## Purpose

This document explains how SchemaCrawler creates command-specific catalog projections from loaded metadata, how those projections relate to their source catalogs, and where this behavior is implemented.

## Catalog Projection

`CatalogProjectionBuilder` constructs an ordinary `Catalog` projection from an already loaded catalog. It applies `LimitOptions`, `FilterOptions`, and `GrepOptions` to objects present in the supplied catalog. Projection does not connect to a database, retrieve metadata, or make objects outside the source membership visible. The public `Catalog` contract contains catalog operations, not reduction or undo operations.

```java
final SchemaCrawlerOptions projectionOptions =
    SchemaCrawlerOptionsBuilder.newSchemaCrawlerOptions()
        .withFilterOptions(
            FilterOptionsBuilder.builder().omitEmptyTables(true).toOptions());

final Catalog projection =
    CatalogProjectionBuilder.builder(baseline)
        .withOptions(projectionOptions)
        .build();
```

The builder consumes the options used to construct the projection; `LoadOptions` do not cause retrieval during this operation. `NamedObjectFilters` supplies public predicates for additional name, full-name, and object-type filtering of named-object collections.

## Projected Membership And Lookups

The projection captures its visible membership when `build()` runs. It exposes projected schemas, tables, routines, sequences, synonyms, column data types, and database users through the ordinary `Catalog` interface. Returned collections are immutable, and building another projection does not change an existing projection.

Catalog enumeration and lookup use the same projected membership. A hidden table is absent from table enumeration and lookup, and its columns cannot be found through catalog column lookup. Schema-scoped enumeration is limited to the projected objects. Lookups use the catalog's exact lookup conventions; they do not treat a name as a regular expression.

The projection retains the source's catalog identity, crawl information, database information, and JDBC driver information. It takes a read-only snapshot of catalog attributes and stores catalog remarks separately. Catalog-level attribute and remarks setters on a projection are unsupported.

## Baseline Context And Shared Objects

Projection does not copy the database-object graph. The caller can keep the loaded baseline separately and use it when broader context is needed. A new, independent command projection should use that baseline. A projection built from another projection narrows the incoming visible membership and cannot restore objects hidden by the earlier projection.

Projected database objects are shared with the source. Their existing attribute and remarks setters remain available; changes may be visible through other catalogs that reference the same objects. Such changes do not recompute membership in an existing projection. The projection is therefore not deeply immutable, does not isolate arbitrary metadata writes, and is not an access-control boundary.

Relationships also retain their original object references. A projected table's foreign key can point to a crawled table that is not visible in the projection. The relationship endpoint remains available through that reference, but it does not become part of projected enumeration or lookup. Use the retained baseline to resolve broader catalog context.

## Filter Options And Empty Tables

`FilterOptions` combines parent and child table expansion depths with `omitEmptyTables`. Grep identifies seed tables; parent and child expansions are calculated independently from those seeds and are restricted to objects eligible in the supplied catalog.

When `omitEmptyTables` is enabled, a table is omitted only if its row count is known to be zero. A positive or unknown count remains eligible. The option filters projection membership, not the baseline, and does not load or query row counts.

## Offline Catalogs

The offline loader deserializes the catalog stored in the snapshot before command projection. That catalog retains its serialized active membership. Current projection options can narrow a command's projection but do not rewrite the offline catalog or add metadata that is absent from it. Different commands can therefore create independent projections from the same loaded offline catalog.

In the interactive shell, grep and filter changes apply on the next command execution without another load. Load and limit changes mark the loaded catalog stale and require `load`; for an offline connection, this reads the snapshot again rather than crawling a live database. See the [execution pipeline](../website/schemacrawler-execution-pipeline.md) for the live and offline workflows.

## AI Function Execution

`FunctionCallback` creates a new executor for each call and provides it with the retained baseline. `AbstractFunctionExecutor` lazily builds an invocation-specific catalog projection and, when needed, an ER model from that projection. Command-backed executors run against the projected catalog; their output is materialized for that invocation. Resource reads and database-information queries continue to use the baseline.

This isolates catalog projection and invocation-owned results. It does not change JDBC sources, leases, connection services, or startup and shutdown behavior. It does not guarantee that physical JDBC connections can be shared safely or isolate arbitrary concurrent writes through shared metadata setters.

## SchemaCrawler Code Reference

### SchemaCrawler-Core

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\CatalogProjectionBuilder.java` builds a projected `Catalog`. `withOptions(SchemaCrawlerOptions)` accepts the composed options, and `build()` filters eligible objects from the source.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\CatalogProjection.java` stores the projected membership and implements enumeration, lookup, and projection-owned catalog attributes. It retains references to the projected database objects rather than deep-copying them.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schema\Catalog.java` defines the ordinary catalog enumeration and lookup API. It does not define reduction or undo operations.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schemacrawler\FilterOptions.java` and `SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\schemacrawler\SchemaCrawlerOptions.java` define filter, grep, limit, and load options. `SchemaCrawlerOptions.crawlOptions()` groups the title, load, and limit settings used to determine whether a shell catalog needs reloading.

`SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\RelatedTableFilter.java` expands seed tables in the projection to eligible parents and children. `SchemaCrawler-Core\schemacrawler-api\src\main\java\schemacrawler\filter\OmitEmptyTablesFilter.java` rejects only tables whose known row count is zero.

### SchemaCrawler

`SchemaCrawler-Core\schemacrawler-loader\src\main\java\schemacrawler\loader\catalog\offline\OfflineCatalogLoader.java` loads the serialized catalog through `SerializedCatalogUtility` before later projection. The corresponding regression coverage is in `SchemaCrawler-Core\schemacrawler-loader\src\test\java\schemacrawler\test\OfflineCatalogLoaderTest.java`.

`SchemaCrawler\schemacrawler-commandline\src\main\java\schemacrawler\tools\commandline\state\ShellState.java` retains the loaded catalog and compares its loaded `CrawlOptions` with the current options. Grep and filter changes do not make that crawl state stale; load and limit changes do.

### SchemaCrawler-AI

`SchemaCrawler-AI\schemacrawler-ai-core\src\main\java\schemacrawler\tools\ai\tools\FunctionCallback.java` creates and configures an executor for each function call. `SchemaCrawler-AI\schemacrawler-ai-core\src\main\java\schemacrawler\tools\ai\tools\base\AbstractFunctionExecutor.java` builds the invocation's projected catalog and corresponding ER model. `SchemaCrawler-AI\schemacrawler-ai-core\src\main\java\schemacrawler\tools\ai\tools\base\AbstractExecutableFunctionExecutor.java` executes command-backed functions against that projection and creates invocation-specific output.
