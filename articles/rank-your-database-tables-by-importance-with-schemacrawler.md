# Rank Your Database Tables by Importance with SchemaCrawler

You've just been handed a database with 400 tables and no documentation. Where do you even start?

Most people start guessing. Maybe the table with the most rows? Maybe the one with the longest name, because surely someone spent a lot of time on it? Maybe just alphabetical order, because at least it's deterministic? None of these actually tell you which tables matter.

SchemaCrawler has a better answer: build a graph of your schema's dependencies, run some graph theory on it, blend in a bit of data-modeling common sense, and hand you a single ranked list. That's the `importance` command, and this article walks through why it exists, how the score is computed, and how you can plug it into an AI agent so it can explore your schema the same way an experienced engineer would.

## Why importance, not just size

Row count and column count are cheap proxies for "this table matters," but they're misleading. A `CUSTOMERS` table with a thousand rows and a dozen well-designed foreign keys pointing at it is probably far more important to your application's logic than a million-row `EVENT_LOG` table nobody queries directly. Size measures volume. It doesn't measure how central a table is to the way the rest of the schema depends on it.

What you actually want to know is: if I had to explain this schema to a new teammate, or if I had to change this table and needed to know what else might break, which tables would I need to understand first?

That's a graph problem, not a row-counting problem.

## Graph theory made accessible

SchemaCrawler builds a directed graph over your entire catalog: tables, views, routines, and synonyms are nodes, and foreign keys, view dependencies, routine table access, and synonym resolution become edges. Once that graph exists, some classic graph metrics fall out of it for free, computed once for every table and view:

- **In-degree** and **out-degree** — how many things point at this table, and how many things this table points at.
- **Betweenness centrality** — computed on an undirected view of the graph, this measures how often a table sits on the shortest path between two *other* tables. High betweenness means a table is a structural bridge — remove it, and other parts of the schema become harder to reach from each other.
- **Dependency reachability count** — how many other objects this table transitively depends on.
- **Impact reachability count** — how many other objects would be reachable (and therefore potentially affected) if you changed this table, by walking dependency edges backward into it.

If you've ever used a graph library like [JGraphT](https://jgrapht.org/) to analyze a social network or a road network, this will feel familiar — a database schema is just another kind of graph, and the same centrality and reachability concepts apply directly.

## Why centrality alone isn't enough — bridge tables versus real entities

Here's the catch: betweenness centrality, on its own, tends to reward **bridge tables** — the thin many-to-many association tables (think `BOOK_AUTHORS` linking `BOOKS` to `AUTHORS`) that sit between two other entities purely to connect them. A bridge table can have very high betweenness centrality simply because it's structurally in the middle of a lot of shortest paths, even though it might only have two or three foreign key columns and carry no meaningful business data of its own.

Meanwhile, a rich strong entity table like `BOOKS` — with real attribute columns, a solid primary key, indexes, and a well-understood business meaning — might have lower betweenness centrality just because it's not sitting *between* other tables in the graph.

If you rank purely by centrality, bridge tables can out-rank the tables that actually carry your business data. That's backwards from what most people mean when they ask "which tables are important."

SchemaCrawler fixes this by computing a **composite importance score** — an integer from 0 to 100 — that blends structural graph signals with data-modeling signals:

```text
structural half (50%): betweenness centrality, impact reachability, total degree
data-modeling half (50%): entity role, attribute column count, row count,
                          foreign key count, trigger count, self-referencing
```

The entity role term draws on SchemaCrawler's entity-relationship classification (strong entity, weak entity, subtype, non-entity) plus one graph-specific addition, `bridge_table`, and weights them so that strong and weak entities rank above bridge tables *within that term*:

```text
strong_entity  1.00
weak_entity    0.85
subtype        0.70
bridge_table   0.55
non_entity     0.30
unknown        0.10
```

Two dampeners then shave points off tables with design smells — no primary key (-15%) or no indexes at all (-10%) — because a table that's missing these fundamentals is less trustworthy as a "load-bearing" part of your schema, no matter how central it looks structurally.

The result: a genuinely central, richly-attributed entity table scores highest. A well-connected bridge table can still score respectably (structural signals are half the formula, after all), but it no longer beats out the entities it's connecting purely by an accident of graph position.

## Try it yourself

```shell
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=importance \
  --output-format=text \
  --output-file=share/importance.txt
```

Add `--table-filter='.*\.BOOKS.*'` with a regular expression to narrow the report to matching tables and views. Output is available as `text`, `json`, or `yaml`, sorted by importance score (descending), with betweenness centrality as a tie-breaker. Communities are calculated once when SchemaCrawler builds the schema graph, then reused in the report.

Here is an excerpt of what the output looks like in JSON format:

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

## Letting an AI agent use this directly

This is where it gets genuinely useful for AI-assisted workflows. The [SchemaCrawler AI MCP Server](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage) exposes these same metrics as tools an AI agent can call directly, without you having to explain your schema by hand:

- **`table_importance`** — returns graph importance metrics for tables and views, including dependency centrality, table counts, and traits. Accepts an optional regular expression filter (`table_name`) and an optional maximum table count (`max_tables`, defaulting to 5; pass 0 or a negative integer to return all tables).
- **`table_path`** — finds the shortest forward dependency path from one table or view to another, preferring foreign-key relationships and falling back to implied associations only when no formal foreign key exists.

Put these together, and an AI agent connected to your database through the MCP server can answer questions like "what are the five most important tables in this schema, and why?" or "what's the shortest dependency path from `ORDERS` to `SHIPPING_ADDRESSES`?" — grounded in actual graph analysis of your schema, not a guess based on table names. That turns a cold, undocumented database into something an AI coding assistant can reason about the same way a human engineer familiar with the system would.

## Where to go next

If you want the full formula, the complete weight tables, and sample JSON output, see the [graph metrics and importance page](https://www.schemacrawler.com/importance.html) on the SchemaCrawler website. If you want to see this in action against your own database, all you need is the `importance` command and a JDBC connection — no separate setup required.
