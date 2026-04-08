# Serialization Example

SchemaCrawler allows export of a full database schema to JSON or YAML via the `serialize` command. The serialized output can be used for offline analysis, schema comparison, or integration with other tooling.

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
    --command serialize \
    --output-format json \
    --output-file share/schema.json
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).

The schema will be exported to a file in the specified format in the current directory. You can use JSON or YAML formats. For details on formats, loading serialized catalogs offline, and format limitations, see [SchemaCrawler Serialization](../serialize.html).

## How to Experiment

1. Export to YAML instead of JSON.

2. Change `--info-level` to `detailed` or `maximum` to capture more schema detail in the serialized output.
3. Compare two serialized exports (e.g., from different database versions) using a standard diff tool to identify schema changes.
