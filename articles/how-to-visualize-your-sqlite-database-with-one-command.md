# How to Visualize Your SQLite Database with One Command (and Nothing to Install)

Ever wondered what the tables in your SQLite database look like, and how they are related to each other? Generate a diagram of your SQLite database with one command. You can run this on any system that has Docker installed. 

On a Linux system, run a command like:

```sh
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/schemacrawler.sh \
--server=sqlite \
--database=chinook-database-2.0.1.sqlite \
--info-level=standard \
--command=schema \
--output-file=output.png
```

The command assumes that a SQLite database called ["chinook-database-2.0.1.sqlite"](https://github.com/schemacrawler/chinook-database/releases/download/v16.11.7/chinook-database-2.0.1.sqlite) is in your current directory. A file called ["output.png"](https://github.com/schemacrawler/chinook-database/blob/master/chinook_schema_diagram.png) will be generated with the database schema, including foreign key relationships. 

If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick, and map the current directory differently. Run this command:

```powershell
docker run `
--mount type=bind,source="${PWD}",target=/home/schcrwlr `
--rm -it `
schemacrawler/schemacrawler `
/opt/schemacrawler/schemacrawler.sh `
--server=sqlite `
--database=chinook-database-2.0.1.sqlite `
--info-level=standard `
--command=schema `
--output-file=output.png
```

You can generate PDF files, and other types of output too. Go through the [SchemaCrawler tutorials](https://killercoda.com/schemacrawler) to learn more SchemaCrawler commands. 
