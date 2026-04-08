# Dump Example

The dump example shows how to export the full contents of a database in a diff-able HTML format using the `dump` command. This is useful for comparing database states over time or across environments.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

1. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command dump \
    --output-format=html \
    --output-file share/dump.html
  ```

> Replace `<connection-options>` with the connection options for your chosen database. See [Getting Started](getting-started.md).

The output file will appear in your current working directory on the host and contain the full database contents in a structured, diff-friendly HTML format.

## How to Experiment

1. Use grep options to restrict the output to specific tables. For example, to include only tables with columns matching `author`, add the following option - `--grep-columns=.*\.author.*`

2. Change the `--info-level` to `detailed` or `maximum` to include more schema metadata alongside the data.
3. Open the output HTML file in a browser or diff it against another run to see what changed in the database.
