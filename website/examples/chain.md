# Chain Example

SchemaCrawler allows you to run multiple SchemaCrawler commands in sequence ("chaining") from a single JavaScript script. The script uses a `chain` object to queue up commands with different output formats and file targets, then executes them all in one pass against the same database connection.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

1. Create a file called "chain.js" with the contents shown below.
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
    --script share/chain.js
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).

This produces two output files in your working directory on the host:
- `schema.txt` — a brief text summary of the schema
- `schema.png` — a visual PNG diagram of the schema

## Resource Files

### `chain.js`

Queues two SchemaCrawler commands via `chain.addNext(command, outputFormat, outputFile)` and then executes them with `chain.execute()`.

```javascript
var scCommands = function () {

  // Add command to run against the schema metadata
  // Arguments are:
  // 1. --command
  // 2. --output-format
  // 3. --output-file
  chain.addNext("brief", "text", "share/schema.txt");
  chain.addNext("schema", "png", "share/schema.png");

  // Execute the chain, and produce output
  chain.execute();
  
  print('Created files "schema.txt" and "schema.png" in the working directory on the host');
};

scCommands();
```

> Place this file in your working directory. It will be accessible inside the container as `share/chain.js`.

## How to Experiment

1. Add more `chain.addNext(...)` calls to produce additional outputs — for example, `chain.addNext("list", "text", "tables.txt")` to list all table names.
2. Change the output format of the `schema` command to `"html"` or `"svg"` to produce a different diagram format.
3. Change the command from `"brief"` to `"details"` to include full column and constraint information in the text output.
