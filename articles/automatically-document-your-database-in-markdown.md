# Automatically Document Your Database in Markdown

Use SchemaCrawler to generate Markdown documentation from your existing database. You can tweak the output to your heart's content using Python scripting. (SchemaCrawler also supports JavaScript and Ruby scripting.)

Try it out. Make sure that you have [Docker](https://docs.docker.com/desktop/) installed on your system, or download [SchemaCrawler](https://www.schemacrawler.com/). Download a sample SQLite database called ["chinook-database-2.0.1.sqlite"](https://github.com/schemacrawler/chinook-database/releases/download/v16.11.7/chinook-database-2.0.1.sqlite) into your current directory.

Grab the Python script of ["markdown.py" from SchemaCrawler's GitHub repository](https://github.com/schemacrawler/SchemaCrawler/blob/50c46596368d499999c3a8e822f7db33bf5e68c7/schemacrawler-scripting/src/main/resources/scripts/markdown.py), and save it in your local directory.

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
--script share/markdown.py
```

(If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick "`".)

Once you have got this working, you can connect to any database - whether Oracle, MySQL, PostgreSQL, Microsoft SQL Server, IBM DB2 or any other database that SchemaCrawler supports.

You can build the DBML generation in a GitHub Action or GitLab build too. An example is in the [schemacrawler/SchemaCrawler-Action-Usage-Example](https://github.com/schemacrawler/SchemaCrawler-Action-Usage-Example) repository.


-----

To learn about how to use SchemaCrawler, download the [SchemaCrawler distribution zip file](https://github.com/schemacrawler/SchemaCrawler/releases/) and go through the examples.
