# SchemaCrawler Examples

Before running any example, follow the steps in
[Getting Started with SchemaCrawler Examples](getting-started-examples.md) to set up Docker,
start a database, and verify your connection.

## Examples

| Example | Description |
| --- | --- |
| [Command-Line](commandline.md) | Explore and document database schemas directly from the shell command line. |
| [Diagram](diagram.md) | Generate visual entity-relationship diagrams using Graphviz, in PNG, PDF, SVG, and other formats. |
| [Other Diagrams](other-diagrams.md) | Produce Mermaid, DBML, and PlantUML entity-relationship diagrams using Python scripts. |
| [Grep](grep.md) | Search a database schema for tables, columns, and routine parameters matching a regular expression. |
| [Lint](lint.md) | Identify potential database design issues such as missing primary keys, missing indexes, and naming inconsistencies. |
| [Dump](dump.md) | Export the full contents of a database in a diff-able HTML format for comparison across environments. |
| [Serialize](serialize.md) | Export a full database schema to JSON or YAML for offline analysis or integration with other tools. |
| [Offline Snapshot](offline.md) | Save a database schema snapshot and reconnect to it later without needing the original database. |
| [Attributes](attributes.md) | Enrich your schema with remarks and custom metadata loaded from a YAML file. |
| [Implicit Associations](implicit-associations.md) | Define logical foreign key relationships between tables that are not enforced at the database level. |
| [User Defined Queries](user-defined-query.md) | Execute custom per-table SQL queries using SchemaCrawler template variables. |
| [Database-Specific Queries](db-specific-query.md) | Run SQL specific to a particular database engine using named query commands. |
| [JavaScript Scripting](javascript.md) | Script against live database metadata using JavaScript, with access to the catalog and a live JDBC connection. |
| [Python Scripting](python.md) | Script against live database metadata using Python, with access to the catalog and a live JDBC connection. |
| [Apache Velocity Templating](velocity.md) | Generate custom text output from your database schema using Apache Velocity templates. |
| [Mustache Templating](mustache.md) | Generate custom text output from your database schema using logic-less Mustache templates. |
| [Thymeleaf Templating](thymeleaf.md) | Generate HTML output from your database schema using Thymeleaf natural templates. |
| [Chain](chain.md) | Run multiple SchemaCrawler commands in sequence from a single JavaScript script in one database pass. |
