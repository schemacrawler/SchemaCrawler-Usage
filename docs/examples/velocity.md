# Apache Velocity Templating Example

SchemaCrawler integrates with [Apache Velocity](https://velocity.apache.org/) to allow you to generate custom text output from your database schema using Velocity templates. You can use the full Velocity Template Language (VTL) to iterate over schemas, tables, and columns and produce any text format you need.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

1. Create a file called "tables.vm" with the contents shown below.
2. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command template \
    --templating-language=velocity \
    --template share/tables.vm \
    --output-file share/output.txt
```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started.md).

The output file will appear in your current working directory on the host.

## Resource Files

### `tables.vm`

```velocity
$catalog.crawlInfo

#foreach($schema in $catalog.schemas)
SET SCHEMA $schema.fullName;

#foreach($table in $catalog.getTables($schema))
#if ($table.tableType == "table")
CREATE TABLE $identifiers.quoteName($table)
(
  #foreach($column in $table.columns)
    $identifiers.quoteName($column) $column.columnDataType#if(!$column.isNullable()) NOT NULL#end#if($foreach.count < $table.columns.size()),#end
  #end
);

#end
#end
#end
```

> Place this file in your working directory. It will be accessible inside the container as `share/tables.vm`.

## How to Experiment

1. Modify `tables.vm` to change the output format — for example, produce HTML, CSV, or a custom SQL dialect.
2. Pass a different `.vm` template file via `--template share/<filename>.vm` to try alternate templates.
3. Explore other Velocity variables available on the `$catalog` object, such as `$catalog.tables`, to access additional schema metadata.
4. Adjust the `--info-level` flag (e.g., `detailed` or `maximum`) in the script to expose more schema information to the template.
