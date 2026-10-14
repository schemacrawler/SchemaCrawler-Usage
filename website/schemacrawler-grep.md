# SchemaCrawler Grep

SchemaCrawler is a command-line tool that allows you to search your database
for tables and columns that match a regular expression, much like the standard
[grep](https://en.wikipedia.org/wiki/Grep) tool.

The SchemaCrawler command-line allows limiting tables, views, columns, stored
procedure and function based on regular expressions, in addition to the grep
functionality. This can be useful, say, when you want to search through your
schema to find all tables that have a CUSTOMER_ID column, for example.

Grep is applied when selecting objects for a command, after metadata is
loaded. In the interactive shell, changing grep settings affects the next
execution without reloading the baseline. See the
[execution pipeline](schemacrawler-execution-pipeline.md) for how grep,
filters, live limits, and offline snapshots interact.

To find tables with certain names, run SchemaCrawler with command-line options
similar to 
`--info-level=standard --command=list --grep-columns=.*\\..*CUSTOMER.*\\..*` 
This will find table with names that have "CUSTOMER" in them.

To find tables with certain column names, run SchemaCrawler with command-line
options similar to 
`--info-level=standard --command=list --grep-columns=.*\\.CUSTOMER_ID` 
This will find all tables that have a CUSTOMER_ID column.

For more details, see the [grep example](examples/grep.md) for a hands-on walkthrough.
