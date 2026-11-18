# How to Visualize Your PostgreSQL Database with One Command (and Nothing to Install)

Ever wondered what the tables in your PostgreSQL database look like, and how they are related to each other? Generate a diagram of your PostgreSQL database with one command. You can run this on any system that has Docker installed. 

On a Linux system, run a command like:

```sh
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/schemacrawler.sh \
--server postgresql \
--host castor.db.elephantsql.com \
--user yourusername \
--password yourpassword \
--database yourdatabase \
--info-level standard \
--command schema \
--output-file output.png
```

The command assumes that you have created a sample database on the excellent [ElephantSQL](https://www.elephantsql.com/) service, including some tables and foreign keys. You will need to obtain the username, password and database name of your ElephantSQL instance. A file called "output.png" will be generated with the database schema, including foreign key relationships. 

If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick, and map the current directory differently. Run this command:

```powershell
docker run `
--mount type=bind,source="${PWD}",target=/home/schcrwlr `
--rm -it `
schemacrawler/schemacrawler `
/opt/schemacrawler/schemacrawler.sh `
--server postgresql `
--host castor.db.elephantsql.com `
--user yourusername `
--password yourpassword `
--database yourdatabase `
--info-level standard `
--command schema `
--output-file output.png
```

You can generate PDF files, and other types of output too. Go through the [SchemaCrawler tutorials](https://killercoda.com/schemacrawler) to learn more SchemaCrawler commands. 
