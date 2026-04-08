# Database-Specific Queries Example

SchemaCrawler can execute arbitrary SQL, including SQL that is specific to a particular database engine. This example demonstrates how to run database-specific queries against an HyperSQL database using a named query command defined in the SchemaCrawler configuration.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.html).

1. Open a command shell in the `db-specific-query` example directory.
2. Run the example command:

  ```sh
  schemacrawler <connection-options> --info-level standard -c=hsqldb.tables
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.html).

3. To write output to a file:

  ```sh
  schemacrawler <connection-options> --info-level standard -c=hsqldb.tables --output-file share/output.txt
  ```

> The output file will appear in your current working directory on the host.

The `-c=hsqldb.tables` argument refers to a named query (`hsqldb.tables`) defined in `config/schemacrawler.config.properties`. This query uses HyperSQL-specific SQL syntax or system tables to retrieve table information in a way that differs from standard SQL.

## How to Experiment

1. Try generating different output formats by adding `--output-format=html` and `--output-file share/output.html` to the command.
2. Modify `config/schemacrawler.config.properties` to define different named queries targeting HyperSQL-specific system tables (e.g., `INFORMATION_SCHEMA.TABLES`).
3. Write output to a file: `schemacrawler <connection-options> --info-level standard -c=hsqldb.tables --output-file share/file.txt`.
4. Adapt the named query to a different database by changing the SQL to use that database's system catalog tables and updating the `--server` option accordingly.
