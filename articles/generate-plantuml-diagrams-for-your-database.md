# Generate (Good Looking) PlantUML Diagrams for Your Database

[PlantUML](https://plantuml.com/) is a domain-specific language to allow you to describe UML and generate diagrams, including entity-relationship diagrams (ERD). You can learn syntax in minutes, but it may take you longer to represent your database. SchemaCrawler generates PlantUML ERD syntax from your existing database. Then you can see what it looks like in the [PlantUML online editor](https://www.planttext.com/), as well as make modifications.

Try it out. Make sure that you have [Docker](https://docs.docker.com/desktop/) installed on your system, or download [SchemaCrawler](https://www.schemacrawler.com/). Download a sample SQLite database called ["chinook-database-2.0.1.sqlite"](https://github.com/schemacrawler/chinook-database/releases/download/v16.11.7/chinook-database-2.0.1.sqlite) into your current directory.

Then run a command like:

```sh
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/bin/schemacrawler.sh \
--server=sqlite \
--database=share/chinook-database-2.0.1.sqlite \
--info-level=standard \
--command script \
--title "Chinook Database Schema" \
--script-language python \
--script plantuml.py
```

(If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick "`".)

Copy the output into the [PlantUML online editor](https://www.planttext.com/) and see what it looks like. Once you have got this working, you can connect to any database - whether Oracle, MySQL, PostgreSQL, Microsoft SQL Server, IBM DB2 or any other database that SchemaCrawler supports.

If you want to customize the script, grab the source from  of ["plantuml.py" from SchemaCrawler's GitHub repository](https://github.com/schemacrawler/SchemaCrawler/blob/50c46596368d499999c3a8e822f7db33bf5e68c7/schemacrawler-scripting/src/main/resources/scripts/plantuml.py), and modify it.

To learn about how to use SchemaCrawler, download the [SchemaCrawler distribution zip file](https://github.com/schemacrawler/SchemaCrawler/releases/) and go through the examples.
