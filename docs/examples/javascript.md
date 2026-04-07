# JavaScript Scripting Example

SchemaCrawler allows you to script against live database metadata using JavaScript. Scripts have access to a `catalog` object (the SchemaCrawler catalog, accessible via methods like `catalog.getTables()`) and a `connection` object (a live JDBC database connection you can use to execute SQL).

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

1. Create a file called "tables.js" with the contents shown below.
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
    --script share/tables.js
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started.md).

## Resource Files

### `tables.js`

Prints crawl info and lists each table along with its child (referencing) tables. Uses `catalog.getCrawlInfo()` and `catalog.getTables()`.

```javascript
var printChildren = function()
{
  var forEach = Array.prototype.forEach;

  print(catalog.getCrawlInfo());

  forEach.call(catalog.getTables(), function(table)
  {
    print('');
    print(table.getFullName());
    var children = table.getDependentTables();
    forEach.call(children, function(childTable)
    {
      print("  [child] " + childTable.getFullName());
    });
  });
};

printChildren();
```

> Place this file in your working directory. It will be accessible inside the container as `share/tables.js`.

### `droptables.js`

Drops all tables in the database in reverse order using the `connection` object to execute SQL statements. Uses both `catalog` (to enumerate tables) and `connection` (to execute `DROP` statements).

```javascript
var dropTables = function()
{
  var statement = connection.createStatement();
  var tables = catalog.getTables().toArray();
  for (var i = (tables.length - 1); i >= 0; i--)
  {
    var table = tables[i];
    var tableType = table.getType().toString().toUpperCase();
    var sql = "DROP " + tableType + " " + table.getFullName();
    print("Executing SQL: " + sql);
    try
    {
      statement.executeUpdate(sql);
    } catch (e)
    {
      print("Exception: " + e.getMessage());
      print("(Not dropping table due to exception)");
      print("");
    }
  }
};

print("NOTE: Restart the database server after running this script, since tables will be dropped!");
dropTables();
```

> Place this file in your working directory. It will be accessible inside the container as `share/droptables.js`.

## How to Experiment

1. Run `schemacrawler <connection-options> --info-level standard -c script --sort-tables=false --script share/droptables.js` to drop all tables. Restart the database server to restore them.
2. Modify `tables.js` to print additional metadata — for example, iterate over `table.getColumns()` to list column names and types.
3. Intentionally introduce a JavaScript error to observe how SchemaCrawler reports scripting exceptions.
4. Use the `connection` object in your own scripts to run arbitrary SQL queries against the live database.
