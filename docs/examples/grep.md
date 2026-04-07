# Grep Example

This example shows how to search a database schema for tables, columns, and routine parameters that match a regular expression — similar to how `grep` works on text files, but applied to database metadata.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

1. Find tables that contain columns matching a regular expression (e.g., columns named `publisher`). Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command schema \
    --grep-columns=.*\.publisher
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started.md).

2. Find routines that have parameters matching a regular expression (e.g., parameters named `two`). Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command schema \
    ---tables= \
    --routines ".*" \
    --grep-parameters=.*\.two
  ```

`--tables=` (empty value) suppresses table output so only routine results are shown.

## How to Experiment

1. Combine `--grep-columns` with `--tables` to restrict the search to specific tables:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command schema \
      --no-info \
      --tables=.*authors.* \
      --grep-columns=.*\.name
  ```

2. Use `--grep-def` to search for a pattern in table or column definitions (remarks or comments).
