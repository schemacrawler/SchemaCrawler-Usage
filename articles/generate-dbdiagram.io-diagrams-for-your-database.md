# Generate dbdiagram.io Diagrams for Your Database

[dbdiagram.io](https://dbdiagram.io/home) from [Holistics](https://www.holistics.io/) is an online tool to allow you to draw database schema diagrams online using their own [Database Markup Language (DBML)](https://www.dbml.org/home/). You can learn syntax in minutes, but it may take you longer to represent your database. SchemaCrawler generates DBML syntax from your existing database. Then you can see what it looks like in the [dbdiagram.io online editor](https://dbdiagram.io/d), as well as make modifications. The advantage of having the DBML file is that you can use the [DBML CLI](https://www.dbml.org/cli/) to generate DDL  to create the database in a variety of dialects, including MySQL and PostgreSQL.

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
--script-language python \
--script dbml.py
```

(If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick "`".)

Copy the output into the [dbdiagram.io online editor](https://dbdiagram.io/d) and see what it looks like. Once you have got this working, you can connect to any database - whether Oracle, MySQL, PostgreSQL, Microsoft SQL Server, IBM DB2 or any other database that SchemaCrawler supports. And if you like, you can download the [DBML CLI](https://www.dbml.org/cli/) to generate DDL  to create the database.

You can build the DBML generation in a GitHub Action or GitLab build too. An example is in the [schemacrawler/SchemaCrawler-Action-Usage-Example](https://github.com/schemacrawler/SchemaCrawler-Action-Usage-Example) repository.

If you want to customize the script, grab the source from  of ["dbml.py" from SchemaCrawler's GitHub repository]([https://github.com/schemacrawler/SchemaCrawler/blob/master/schemacrawler-scripting/src/test/resources/dbml.py](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/dbml.py)).

To learn about how to use SchemaCrawler, download the [SchemaCrawler distribution zip file](https://github.com/schemacrawler/SchemaCrawler/releases/) and go through the examples.
