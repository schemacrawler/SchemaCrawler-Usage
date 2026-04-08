# Python Scripting Example

SchemaCrawler allows you to script against live database metadata using Python. Scripts have access to a `catalog` object (the SchemaCrawler catalog, with tables, columns, foreign keys, and more) and a `connection` object (a live JDBC database connection you can use to execute SQL).

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.html).

1. Create a file called "tables.py" with the contents shown below.
2. Run the command:

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command script \
    --script share/tables.py
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.html).

## Resource Files

### `tables.py`

Prints crawl info and lists each table along with its child (referencing) tables. Uses the `catalog` object directly.

```python
print(catalog.getCrawlInfo())

for table in catalog.getTables():
  print('')
  print(table.getFullName())
  for column in table.getColumns():
    print("  " + column.getName())
```

Place this file in your working directory. It will be accessible inside the container as `share/tables.py`.

## How to Experiment

1. Run `schemacrawler <connection-options> --info-level standard -c script --sort-tables=false --script share/droptables.py` to drop all tables. Restart the database server to restore them.
2. Modify `tables.py` to print additional metadata — for example, iterate over `table.columns` to list column names and types.
3. Use the `connection` object in your own scripts to run arbitrary SQL queries against the live database.
