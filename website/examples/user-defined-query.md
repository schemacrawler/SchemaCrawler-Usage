# User Defined Queries Example

SchemaCrawler can execute arbitrary SQL per table using template variables that are automatically populated at runtime. This example demonstrates how to define and run custom per-table queries using the `tables.select` command configuration.

## Template Variables

When writing user-defined queries in "config/schemacrawler.config.properties", you can use the following built-in template variables:

| Variable | Description |
| --- | --- |
| `${tabletype}` | The type of the table (e.g., `TABLE`, `VIEW`) |
| `${table}` | The fully-qualified name of the current table |
| `${columns}` | A comma-separated list of column names for the current table |

For example, a query like the following will be executed once per table:

```sql
SELECT ${columns} FROM ${table} WHERE 1=0
```

This allows you to write a single query template that SchemaCrawler expands and runs against every table it processes.


## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

1. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command tables.select
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).

The "tables.select" query is already pre-defined in the "schemacrawler.config.properties" file. "schemacrawler.config.properties" is also read from the current working directory.



## How to Experiment

1. Try generating different output formats by adding `--output-format=html` and `--output-file share/output.html` to the command.
2. Modify "schemacrawler.config.properties" to define different `tables.select` queries using the `${tabletype}`, `${table}`, and `${columns}` template variables.
3. Write output to a file: `schemacrawler <connection-options> --info-level standard -c=tables.select --output-file share/file.txt`.
