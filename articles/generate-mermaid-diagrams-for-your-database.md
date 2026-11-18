# Generate Mermaid Diagrams for Your Database

[mermaid](https://mermaid-js.github.io/mermaid/#/) describes itself as a "Markdownish syntax" for generating entity-relationship diagrams. You can learn syntax in minutes, but it may take you longer to represent your database. SchemaCrawler generates mermaid syntax from your existing database. Then you can see what it looks like in the [mermaid live editor](https://mermaid-js.github.io/mermaid-live-editor/), as well as make modifications.

Try it out. Make sure that you have [Docker](https://docs.docker.com/desktop/) installed on your system, or download [SchemaCrawler](https://www.schemacrawler.com/). Download a sample SQLite database called ["northwind.db"](https://github.com/jpwhite3/northwind-SQLite3/blob/4f56e7f5906dfd23b25244c5bfe8fb5da6402efd/dist/northwind.db) into your current directory.

Then run a command like:

```sh
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/bin/schemacrawler.sh \
--server=sqlite \
--database share/northwind.db \
--info-level standard \
--command script \
--script-language python \
--script mermaid.py \
--title "Northwind Database" \
--output-file share/northwind.mmd
```

(If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick "`".)

Copy the output into the [Mermaid live editor](https://mermaid.ai/) and see what it looks like. Once you have got this working, you can connect to any database - whether Oracle, MySQL, PostgreSQL, Microsoft SQL Server, IBM DB2 or any other database that SchemaCrawler supports.

If you want to customize the script, grab the source of ["mermaid.py" from SchemaCrawler's GitHub repository](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/mermaid.py) and edit it.

To learn about how to use SchemaCrawler, see [the website](https://www.schemacrawler.com/).
