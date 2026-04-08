# Diagram Example

The diagram example demonstrates integration of SchemaCrawler with [Graphviz](https://www.graphviz.org/) to generate visual entity-relationship diagrams of a database schema. Diagrams can be produced in a variety of output formats including PNG, PDF, and SVG.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

> Graphviz is included in the SchemaCrawler Docker image. No separate installation is needed.

1. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command schema \
    --output-file share/database-diagram.png
  ```

The output filename extension determines the output format — PNG, PDF, SVG, or others.

> Replace `<connection-options>` with the connection options for your chosen database. See [Getting Started](getting-started.md).

The diagram file will appear in your current working directory on the host.

## How to Experiment

1. Try different output formats by changing the file extension of the output argument.
2. Use grep options to restrict the diagram to specific tables. For example, to include only tables with columns matching `author`, add the following option - `--grep-columns=.*\.author.*`
3. Control display of foreign-key names, column ordinal numbers, and schema names by setting the following properties in `schemacrawler.config.properties`:

  ```properties
  schemacrawler.format.show_ordinal_numbers=true
  schemacrawler.format.hide_foreignkey_names=true
  schemacrawler.format.hide_weakassociation_names=true
  schemacrawler.format.show_unqualified_names=true
  ```

4. Pass custom Graphviz command-line options (for example, to increase output resolution) by adding the following to `config/schemacrawler.config.properties`:

  ```properties
  schemacrawler.graph.graphviz_opts=-Gdpi=300
  ```
