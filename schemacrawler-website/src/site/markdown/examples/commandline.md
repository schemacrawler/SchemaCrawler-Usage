# Command-Line Example

This example demonstrates how to use SchemaCrawler directly from the shell command line to explore and document database schemas.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.html).

1. Get a list of all available command-line options:

   ```sh
   schemacrawler --help
   ```

2. List all database objects:

   ```sh
   schemacrawler \
     --server postgresql \
     --host postgresql \
     --database schemacrawler \
     --user schemacrawler \
     --password schemacrawler \
     --info-level minimum \
     --command list
   ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.html).


## How to Experiment

1. Explore the [grep](grep.html) example to search schema objects by regular expression.
2. Explore the [lint](lint.html) example to detect database design issues.
3. Explore the [offline](offline.html) example to save and reuse a database snapshot.
4. Try different `--info-level` values: `minimum`, `standard`, `detailed`, `maximum`.
5. Edit `config/schemacrawler.config.properties` to customize output options.
