# SchemaCrawler Has Three Programmatic Models. Here Is When to Use Each One

Your database already contains one of the most valuable maps of your application: its schema. The problem is that this map is usually trapped behind JDBC metadata calls, vendor-specific system tables, and a sprawling tangle of hundreds of objects.

[SchemaCrawler](https://www.schemacrawler.com/) is an open-source database schema discovery and documentation tool. Connect it to almost any JDBC-accessible database and it turns raw metadata into searchable documentation, database diagrams, lint reports, machine-readable output, and a rich Java API. It is designed for the moments when you inherit an undocumented database, need to understand the blast radius of a change, or want to make schema knowledge available to developers and AI agents without relying on tribal knowledge.

The command line is a fast way to explore and document a schema. The Java API is where SchemaCrawler becomes a building block: you can create a custom report, power an internal developer portal, enforce design rules in CI, or teach an agent how your data fits together.

You connect to a database and call SchemaCrawler. What do you get back?

Not one enormous, do-everything object. SchemaCrawler gives you three increasingly expressive models:

1. `Catalog` for physical database metadata.
2. `ERModel` for inferred entity-relationship meaning.
3. `ImportanceModel` for dependency topology, table importance, and domain clustering.

Think of them as three lenses over the same database. Start with facts. Add data-model semantics when you need them. Reach for graph analysis when you need to understand what is central, connected, or naturally grouped.

## 1. `Catalog`: the facts-on-the-ground model

`Catalog` is SchemaCrawler's foundational model. It is the in-memory result of crawling database metadata through JDBC, and it represents the physical objects your database actually exposes.

It gives you schemas, tables, views, columns, indexes, primary keys, foreign keys, routines, sequences, synonyms, users, data types, and database/driver information. Every other model in this article starts here.

```java
import schemacrawler.schema.Catalog;
import schemacrawler.schemacrawler.SchemaCrawlerOptions;
import schemacrawler.tools.utility.SchemaCrawlerUtility;
import us.fatehi.utility.datasource.DatabaseConnectionSource;

DatabaseConnectionSource connectionSource = /* configure JDBC connection */;
SchemaCrawlerOptions options = SchemaCrawlerOptions.builder().toOptions();

Catalog catalog = SchemaCrawlerUtility.getCatalog(connectionSource, options);

catalog.getTables().forEach(table -> {
  System.out.printf("%s: %d columns%n",
      table.getFullName(),
      table.getColumns().size());
});
```

The API is deliberately direct. Need a table by schema and unqualified name? Use `lookupTable`. Need all tables in a schema? Use `getTables(schema)`. Need routines, sequences, or synonyms? The `Catalog` has those too.

### Use `Catalog` when...

- You are documenting or inspecting the literal database structure.
- You need DDL-oriented facts: columns, nullability, indexes, constraints, triggers, comments, and privileges.
- You are writing a schema linter, migration check, documentation generator, or custom report.
- You want to decide what is present before making a higher-level interpretation.

`Catalog` is the right answer for questions such as:

> Which tables have no primary key?
>
> Which views reference this table?
>
> Does `ORDERS` have an index beginning with `CUSTOMER_ID`?

It is intentionally not an opinionated business model. A table is a table, even if it looks suspiciously like a join table or a subtype. That restraint is a feature: physical metadata remains the trustworthy base layer.

## 2. `ERModel`: turn tables and keys into a data model

Physical metadata tells you that `BOOK_AUTHORS` has two foreign keys. It does not, by itself, tell you that the table is probably expressing a many-to-many relationship between `BOOKS` and `AUTHORS`.

That is the job of `ERModel`.

Build it from the catalog:

```java
import schemacrawler.ermodel.model.ERModel;
import schemacrawler.tools.utility.SchemaCrawlerUtility;

ERModel erModel = SchemaCrawlerUtility.buildERModel(catalog);

erModel.getEntities().forEach(entity ->
    System.out.println(entity.getFullName()));

erModel.getRelationships().forEach(relationship ->
    System.out.println(relationship.getFullName()));
```

SchemaCrawler infers entities and relationships from the schema metadata already present in the `Catalog`. That includes foreign keys, primary keys, unique indexes, and table shape. The result distinguishes meaningful model concepts such as:

- Strong entities and weak entities.
- Subtypes and their supertypes.
- One-to-one, one-to-many, and many-to-many relationships.
- Bridge tables, represented as many-to-many relationships rather than ordinary entities.
- Implicit relationships inferred from catalog metadata.
- Tables and references that could not be modeled.

This is an important distinction: a bridge table is not merely "a table with two foreign keys." SchemaCrawler's inference uses the surrounding metadata to determine whether the pattern actually represents a many-to-many relationship. That is why application code should reuse `ERModel` instead of recreating a quick-but-fragile join-table heuristic.

`ERModel` also gives you focused lookups:

```java
erModel.lookupEntity("PUBLIC.BOOKS.BOOKS")
    .ifPresent(entity -> System.out.println(entity.getEntityType()));

erModel.lookupRelationship("PUBLIC.BOOKS.BOOKAUTHORS")
    .ifPresent(relationship -> System.out.println(relationship.getCardinality()));
```

Relationship names are meaningful identifiers. Depending on the relationship, a name can correspond to a bridge table, a foreign key, or an implicit relationship. Use the model's lookup methods rather than inventing identifiers from table names.

### Use `ERModel` when...

- You need to explain the schema as a domain model, not just list its objects.
- You are drawing ER diagrams or exposing relationship-aware tooling.
- You need entity classification, cardinality, supertypes, or bridge-table reasoning.
- You are helping an AI agent or a developer understand the meaning behind foreign keys.

Use it for questions such as:

> Is this table a strong entity, a subtype, or a bridge table?
>
> What relationship does this foreign key represent?
>
> Which tables are not accounted for by the inferred data model?

One practical rule: do not use `ERModel` as a replacement for `Catalog`. It is a semantic interpretation of the catalog, not a second source of database facts. Keep the `Catalog` nearby when you need to inspect the actual columns, keys, or index definitions that support an inference.

## 3. `ImportanceModel`: find what matters and what belongs together

An ER model answers, "What does this relationship mean?" An importance model answers a different class of question:

> What should I understand first, what could this change affect, and which parts of this schema form a coherent domain?

SchemaCrawler's importance module builds an immutable `ImportanceModel` from a `Catalog`:

```java
import schemacrawler.importance.model.ImportanceModel;
import schemacrawler.importance.model.TableImportance;
import schemacrawler.importance.model.implementation.ImportanceModelBuilder;

ImportanceModel importanceModel = ImportanceModelBuilder.builder(catalog).build();

catalog.getTables().stream()
    .map(table -> new Object[] {
        table,
        table.<TableImportance>getAttribute(TableImportance.class.getName())
    })
    .sorted((left, right) ->
        ((TableImportance) left[1]).compareTo((TableImportance) right[1]))
    .forEach(entry -> {
      var table = (schemacrawler.schema.Table) entry[0];
      var importance = (TableImportance) entry[1];
      System.out.printf("%3d %s%n",
          importance.importanceScore(),
          table.getFullName());
    });
```

Behind that small API is a proper directed dependency graph, implemented with [JGraphT](https://jgrapht.org/). Vertices represent tables, views, routines, and synonyms. Typed edges represent:

- Foreign keys.
- Implied associations.
- View dependencies.
- Routine dependencies.
- Synonym resolution.

The catalog graph is exposed read-only through `getCatalogGraph()`, while `lookupByVertexId()` maps graph vertices back to their SchemaCrawler objects. That makes the graph useful both for built-in analysis and for your own JGraphT algorithms.

### Importance is more than "most foreign keys wins"

When the importance model is built, SchemaCrawler calculates topology metrics for every vertex:

- In-degree and out-degree.
- Betweenness centrality.
- Dependency reachability: what the object transitively depends on.
- Impact reachability: what can be reached when dependency edges are traversed backward.

For tables and views, it combines those signals with physical and ER-derived traits into a reproducible, catalog-relative score from 0 to 100. Structural signals contribute 50% of the score; entity role, attribute columns, row count, foreign key count, trigger count, and self-reference contribute the other 50%.

That blend avoids a classic graph-analysis trap. A bridge table can have high betweenness simply because it sits between two entities. The importance calculation knows that a bridge table is structurally useful without mistaking it for the business entity at the center of your system.

The computed `TableImportance` is stored as an attribute on each table, so you can reuse it without rebuilding your own scorecard.

### Clusters reveal domains hiding in plain sight

SchemaCrawler also detects table clusters: groups of related tables and views that often correspond to a functional area of the application.

```java
importanceModel.getTableClusters().forEach(tableCluster -> {
  System.out.printf("Anchor: %s%n", tableCluster.anchorVertexId());
  tableCluster.memberVertexIds().forEach(System.out::println);
});
```

The clustering process intentionally ignores dependency direction for this purpose. A customer table and an order table are closely related whether the foreign-key arrow points from orders to customers or the other way around. SchemaCrawler takes the table/view subgraph, treats it as undirected for affinity, and runs deterministic label-propagation clustering.

Only clusters with at least three members are reported. Within each one, members are ordered by importance, and the highest-ranked member becomes its anchor. The result is stable enough to use in reports, onboarding material, or an AI-assisted schema exploration workflow.

### Use `ImportanceModel` when...

- You inherited a large, undocumented database and need a sensible starting point.
- You need blast-radius analysis before changing a table, view, or routine.
- You want to identify central tables without over-rewarding thin bridge tables.
- You want to group a sprawling schema into likely business domains.
- You want to apply custom JGraphT traversals or graph algorithms to schema dependencies.

This is the model for questions such as:

> What are the five most important tables to learn first?
>
> What depends on this table, directly or transitively?
>
> Which tables belong to the same likely functional area?

## Pick the smallest lens that answers the question

Here is the cheat sheet:

| If you need to... | Start with... |
| --- | --- |
| Inspect columns, indexes, keys, routines, or database metadata | `Catalog` |
| Explain entity roles, cardinality, subtypes, or many-to-many relationships | `ERModel` |
| Rank central objects, analyze impact, find paths, or identify domains | `ImportanceModel` |

The models are complementary, not competing. The most effective workflow is usually:

```text
Catalog -> ERModel -> ImportanceModel
 facts     meaning    topology and priorities
```

Start with the catalog to establish what is real. Build the ER model when the shape of the schema needs interpretation. Build the importance model when the question becomes "where do I start?" or "what is connected to what?"

That progression turns raw JDBC metadata into something much more useful: a map of the database, a model of its relationships, and a guide to the parts that deserve your attention first.

For a deeper dive into scores, metrics, and the `importance` command, see [Rank Your Database Tables by Importance with SchemaCrawler](https://dev.to/sualeh/rank-your-database-tables-by-importance-with-schemacrawler-4j4m).
