# Offline Snapshot Example

This example demonstrates how to save a database schema to a compressed offline snapshot file, and how to later reconnect to that snapshot as though it were a live database — without needing the original database to be running.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

1. Create an offline snapshot from the live database. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level maximum \
    --command serialize \
    --output-format ser \
    --output-file share/offline.ser
   ```

This produces a compressed serialized snapshot file named "offline.ser". For details on snapshot formats, limitations, and requirements, see [SchemaCrawler Offline Catalog Snapshot](../offline.html).

When creating an offline database, prefer to use `maximum` info-level.

2. Use the offline snapshot — no live database connection required. Run the command:

   ```sh
   schemacrawler \
     --server offline \
     --database share/offline.ser \
     --info-level standard \
     --command=schema
   ```

## How to Experiment

1. Try other SchemaCrawler commands against the offline snapshot, such as `list`, `brief`, or `details`:

   ```sh
   schemacrawler \
     --server offline \
     --database share/offline.ser \
     --info-level standard \
     --command details
   ```

2. Generate an HTML or text report from the offline snapshot:

   ```sh
   schemacrawler \
     --server offline \
     --database share/offline.ser \
     --info-level standard \
     --command schema \
     --output-format html \
     --output-file share/output.html
   ```

3. Use the offline snapshot with the [grep](grep.md) options to search metadata without a live connection:

   ```sh
   schemacrawler \
     --server offline \
     --database share/offline.ser \
     --info-level standard \
     --command=details \
     --no-info \
     --grep-columns ".*\.publisher"
   ```

4. Use the offline snapshot with [lint](lint.md) to find design issues without a live database:

   ```sh
   schemacrawler \
     --server offline \
     --database share/offline.ser \
     --info-level standard \
     --command=lint
   ```
