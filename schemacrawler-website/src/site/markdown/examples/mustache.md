# Mustache Templating Example

SchemaCrawler integrates with [Mustache](https://mustache.github.io/) to allow you to generate custom text output from your database schema using logic-less Mustache templates. Mustache's simple `{{variable}}` and `{{#section}}` syntax makes it easy to produce clean, readable output in any text format.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

1. Create a file called "tables.mustache" with the contents shown below.
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
    --templating-language=mustache \
    --template share/tables.mustache \
    --output-file share/output.txt
```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).

The output file will appear in your current working directory on the host.

## Resource Files

### `tables.mustache`

```handlebars
{{&catalog.crawlInfo}}

{{#catalog.tables}}
- {{&fullName}}
{{#columns}}
 - {{&name}}
{{/columns}}

{{/catalog.tables}}
```

> Place this file in your working directory. It will be accessible inside the container as `share/tables.mustache`.

## How to Experiment

1. Modify `tables.mustache` to change the output format — for example, produce Markdown, HTML, or CSV.
2. Pass a different `.mustache` template file via `--template share/<filename>.mustache` to try alternate templates.
3. Use `{{&variable}}` (triple-stash equivalent with `&`) for unescaped output, or `{{variable}}` for HTML-escaped output.
4. Adjust the `--info-level` flag (e.g., `detailed` or `maximum`) in the script to expose more schema metadata to the template.
