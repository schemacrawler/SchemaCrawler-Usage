# Graph Metrics and Table Importance

## Overview

When you inherit or work with an unfamiliar database schema, not every table matters equally. Some tables are central to how data flows through the system; others are thin connector tables, lookups, or largely disconnected. SchemaCrawler builds an `ImportanceModel` containing a dependency graph from your schema's foreign keys, views, routines, and synonyms, then computes graph metrics and a composite importance score for every table and view. These metrics help you identify critical tables before a migration, understand the blast radius of a schema change, and prioritize which tables to document or review first.

This complements [entity-relationship (ER) modeling.](entity-modeling.md) Entity modeling classifies *what kind* of table something is (a strong entity, a weak entity, and so on); graph metrics and the importance score measure *how central* that table is in the overall schema, and combine the two views into a single ranking.

## Graph Metrics

SchemaCrawler builds a directed graph over the full catalog — tables, views, routines, and synonyms — with edges representing foreign keys, view dependencies, routine table/view access, and synonym resolution. From this graph, SchemaCrawler computes the following metrics for every table and view, once at startup:

- **In-Degree**: The number of incoming dependency edges (for example, foreign keys and view definitions that reference this table). A high in-degree suggests other objects rely on this table.
- **Out-Degree**: The number of outgoing dependency edges (for example, foreign keys this table declares to other tables). A high out-degree suggests this table depends on many others.
- **Betweenness Centrality**: How often a table lies on the shortest path between other pairs of tables, computed on an undirected view of the complete dependency graph. Tables with high betweenness centrality act as structural bridges or hubs connecting otherwise-distant parts of the schema.
- **Dependency Reachability Count**: The number of other objects reachable by following forward dependency edges from this table — a rough measure of how many prerequisites a table (or a change to it) depends on.
- **Impact Reachability Count**: The number of other objects reachable by following dependency edges backward into this table — a rough measure of how many other objects could be affected if this table changes.

## Table Metadata

In addition to graph metrics, SchemaCrawler collects data-modeling metadata for every table and view:

- **Entity model type**: One of `strong_entity`, `weak_entity`, `subtype`, `non_entity`, or `unknown`, as described in [entity-relationship modeling.](entity-modeling.md) The importance module adds one further classification, **`bridge_table`**, for tables that primarily exist to associate two other tables (typically composed mostly of foreign key columns), which is a graph-analysis concept rather than a general ER classification.
- **Table traits**: whether the table has no primary key, no foreign keys, no indexes, is self-referencing, has triggers, or is empty.
- **Table counts**: attribute (non-key, data-carrying) column count, total column count, foreign key count, index count, and trigger count.

## Composite Importance Score

Betweenness centrality alone rewards structural bridging, but says nothing about how much business data a table carries, or how central its data-modeling role is. A thin, two-column bridge table could otherwise outrank a richly-attributed strong entity purely by sitting on more shortest paths. SchemaCrawler addresses this by computing a single composite `importanceScore`, an integer between 0 and 100, that combines both kinds of signal.

### How the score is calculated

Each raw signal is normalized against the catalog-wide maximum for that signal, using a log-dampened scale (`log(1 + x) / log(1 + max)`), so a single outlier table does not compress every other table's score into a narrow band. A signal normalizes to zero when its catalog-wide maximum is zero. The normalized signals are then combined using the following weights:

```text
structural (50%):
  0.30 betweenness centrality
  0.15 impact reachability count
  0.05 in-degree + out-degree (total degree)

data-modeling (50%):
  0.15 entity-role weight
  0.13 attribute column count
  0.09 row count
  0.06 foreign key count
  0.05 trigger count
  0.02 self-referencing
```

Structural signals (betweenness, impact reachability, degree) make up half of the score, so a well-connected, central table or view scores highly regardless of its data-modeling role. Data-modeling signals make up the other half, so strong- and weak-entity tables are not automatically outranked by thin bridge tables.

### Entity-role weight

Within the data-modeling half of the formula, the entity model type contributes a weight:

| Entity model type | Weight |
|---|---|
| `strong_entity` | 1.00 |
| `weak_entity` | 0.85 |
| `subtype` | 0.70 |
| `bridge_table` | 0.55 |
| `non_entity` | 0.30 |
| unknown | 0.10 |

`strong_entity` and `weak_entity` tables always outrank `bridge_table` tables *within this one term* — but since structural signals are half of the total score, a highly-connected bridge table can still outrank a poorly-connected entity overall. This is intentional: entity role reflects data-modeling significance, while centrality and reachability reflect actual structural importance in the loaded schema.

### Dampening for missing primary keys or indexes

A table missing a primary key, or missing all indexes, is a data-modeling design smell rather than a sign of importance, so each condition *reduces* (never increases) the fully-weighted score:

```text
importanceScore = round(rawScore
  * (noPrimaryKey ? 0.85 : 1.0)   // -15%
  * (noIndexes    ? 0.90 : 1.0)) // -10%
```

Neither dampener reduces a table's score to zero on its own. The final score is rounded to the nearest whole number and clamped to the range `[0, 100]`.

## Domain Community Detection

In addition to individual table scores, SchemaCrawler detects functional domain clusters (groups of related tables and views) across the dependency graph using weighted Label Propagation clustering. Clusters are calculated once while the importance model is built and reused by report generation. Each cluster identifies an anchor table (the member vertex with the highest composite `importanceScore`) to act as the domain representative.

Community detection uses explicit affinity weights on schema graph dependencies:
- Foreign keys: `1.00`
- View dependencies: `0.80`
- Routine dependencies: `0.70`
- Implicit associations: `0.50`
- Synonym resolutions: `0.20`

## Running the `importance` Command

The `importance` command builds the importance model, computes all metrics, composite scores, and domain clusters, and produces a consolidated top-level report payload containing both `clusters` and `tables`.

By default, the report returns the top 5 tables. You can control the maximum number of tables returned using the `--max-tables` command-line option. Setting `--max-tables=0` (or a negative integer) returns all matching tables without limiting.

Supported `--output-format` values are `text`, `json`, and `yaml`. Reports are sorted by `importanceScore` descending, then by betweenness centrality descending (as a tie-break), then by table full name ascending.

To restrict the report to matching tables and views, provide a regular expression using the `table-filter` additional command-line option.
If no filter is specified, all tables and views are included.

### Sample report excerpt (JSON)

```json
{
  "clusters" : [ {
    "id" : "a61b0ea7-c688-3e35-ab3b-b7593f7fd788",
    "anchor_table_full_name" : "PUBLIC.BOOKS.BOOKS",
    "total_cluster_size" : 4,
    "member_table_full_names" : [ "PUBLIC.BOOKS.BOOKS", "PUBLIC.\"PUBLISHER SALES\".SALES", "PUBLIC.\"PUBLISHER SALES\".REGIONS", "PUBLIC.\"PUBLISHER SALES\".SALESDATA" ]
  } ],
  "tables" : [ {
    "table_full_name" : "PUBLIC.BOOKS.BOOKS",
    "table_importance" : {
      "importance_score" : 73,
      "table_traits" : {
        "self_referencing" : true,
        "entity_model_type" : "strong_entity"
      },
      "table_counts" : {
        "attribute_column_count" : 5,
        "column_count" : 7,
        "foreign_key_count" : 1,
        "index_count" : 3,
        "trigger_count" : 0
      },
      "importance_metrics" : {
        "in_degree" : 3,
        "out_degree" : 1,
        "betweenness_centrality" : 6.0,
        "dependency_reachability_count" : 0,
        "impact_reachability_count" : 2
      }
    }
  } ]
}
```

The top-level report payload groups domain `clusters` and ranked `tables` into a single object, so full domain structure and table rankings are available in one operation.
