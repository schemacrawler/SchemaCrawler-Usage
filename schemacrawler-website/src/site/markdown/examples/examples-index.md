# SchemaCrawler Examples

Before running any example, follow the steps in
[Getting Started with SchemaCrawler Examples](getting-started-examples.html) to set up Docker,
start a database, and verify your connection.

## Examples

| Example | Description |
| --- | --- |
| [Command-Line](commandline.html) | Explore and document database schemas directly from the shell command line. |
| [Diagram](diagram.html) | Generate visual entity-relationship diagrams using Graphviz, in PNG, PDF, SVG, and other formats. |
| [Other Diagrams](other-diagrams.html) | Produce Mermaid, DBML, and PlantUML entity-relationship diagrams using Python scripts. |
| [Grep](grep.html) | Search a database schema for tables, columns, and routine parameters matching a regular expression. |
| [Lint](lint.html) | Identify potential database design issues such as missing primary keys, missing indexes, and naming inconsistencies. |
| [Dump](dump.html) | Export the full contents of a database in a diff-able HTML format for comparison across environments. |
| [Serialize](serialize.html) | Export a full database schema to JSON or YAML for offline analysis or integration with other tools. |
| [Offline Snapshot](offline.html) | Save a database schema snapshot and reconnect to it later without needing the original database. |
| [Attributes](attributes.html) | Enrich your schema with remarks and custom metadata loaded from a YAML file. |
| [Implicit Associations](implicit-associations.html) | Define logical foreign key relationships between tables that are not enforced at the database level. |
| [User Defined Queries](user-defined-query.html) | Execute custom per-table SQL queries using SchemaCrawler template variables. |
| [Database-Specific Queries](db-specific-query.html) | Run SQL specific to a particular database engine using named query commands. |
| [JavaScript Scripting](javascript.html) | Script against live database metadata using JavaScript, with access to the catalog and a live JDBC connection. |
| [Python Scripting](python.html) | Script against live database metadata using Python, with access to the catalog and a live JDBC connection. |
| [Apache Velocity Templating](velocity.html) | Generate custom text output from your database schema using Apache Velocity templates. |
| [Mustache Templating](mustache.html) | Generate custom text output from your database schema using logic-less Mustache templates. |
| [Thymeleaf Templating](thymeleaf.html) | Generate HTML output from your database schema using Thymeleaf natural templates. |
| [Chain](chain.html) | Run multiple SchemaCrawler commands in sequence from a single JavaScript script in one database pass. |
