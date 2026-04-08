# Thymeleaf Templating Example

SchemaCrawler integrates with [Thymeleaf](https://www.thymeleaf.org/) to allow you to generate HTML (or other XML-based) output from your database schema using Thymeleaf templates. Thymeleaf's natural templating approach means your template files are valid HTML that can be previewed in a browser even before processing.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

1. Create a file called "tables.thymeleaf" with the contents shown below.
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
    --templating-language=thymeleaf \
    --template share/tables.thymeleaf \
    --output-file share/output.html
```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).

The output file will appear in your current working directory on the host.

## Resource Files

### `tables.thymeleaf`

```xml
<!DOCTYPE html SYSTEM "http://www.thymeleaf.org/dtd/xhtml1-strict-thymeleaf-4.dtd">

<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:th="http://www.thymeleaf.org">

  <head>
    <title>SchemaCrawler Schema</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>

  <body>

    <pre th:text="${catalog.crawlInfo}">SchemaCrawler Information</pre>

    <span th:each="schema: ${catalog.schemas}">
      <h1 th:text="${schema.fullName}">Schema</h1>
        <span th:each="table: ${catalog.getTables(schema)}">
          <h2 th:text="${table.fullName}">Table</h2>
          <ol th:each="column: ${table.columns}">
            <li th:text="${column.name}">Columns</li>
          </ol>
        </span>
    </span>

  </body>

</html>
```

> Place this file in your working directory. It will be accessible inside the container as `share/tables.thymeleaf`.

## How to Experiment

1. Modify `tables.thymeleaf` to change the HTML structure or styling — for example, add a CSS stylesheet or render columns as a `<table>` element.
2. Pass a different `.thymeleaf` template file via `--template share/<filename>.thymeleaf` to try alternate templates.
3. Use additional Thymeleaf expressions such as `th:if` or `th:unless` to conditionally include schema elements (e.g., only tables of a certain type).
4. Adjust the `--info-level` flag (e.g., `detailed` or `maximum`) in the script to expose more schema metadata such as foreign keys and indexes.
