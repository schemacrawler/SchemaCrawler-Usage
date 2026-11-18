# How to Document Your Cassandra Database with One Command (and Nothing to Install)

Ever wondered what the tables in your Cassandra database look like? Generate a text file of your Cassandra database with one command. You can run this on any system that has Docker installed.

For now, create a Cassandra database in a Docker container. Later you can use the same technique to conect to your own Cassandra database. Create two Docker Compose files for the Cassandra and SchemaCrawler containers. Also create one more with the CQL database creation script.

Then open a command shell in the same folder that you created these files, and run:

```sh
docker-compose -f schemacrawler.yml -f cassandra.yml up -d
```

Wait for a while for the containers to start up, and then connect into the Cassandra container by running:

```sh
docker exec -it cassandra bash
```

In the Cassandra container shell, run the script to create a sample database, and exit the shell:

```sh
cqlsh -f /share/database.cql
exit
```

Now that the Cassandra database is created, connect into the SchemaCrawler container by running:

```sh
docker exec -it schemacrawler bash
```

In the SchemaCrawler container shell, run SchemaCrawler against the Cassandra database to see your table. Run:

```sh
schemacrawler \
  --url jdbc:cassandra://cassandra:9042/store \
  --user cassandra --password cassandra \
  --info-level minimum \
  --command list
```

After you have got this working, you can alter the command to show more details of the database. For example, you can run:

```sh
schemacrawler \
  --url jdbc:cassandra://cassandra:9042/store \
  --user cassandra --password cassandra \
  --info-level standard \
  --command schema
```

You can save the output with an additional `--output-file /share/schema.txt` argument, and the file will be created in your local directory. `schemacrawler help` will give you more information, as well as the [SchemaCrawler website](https://www.schemacrawler.com/). Now you are ready to connect to your own database. If you need help on how to construct the connection URL, take a look at [ing-bank/cassandra-jdbc-wrapper](https://github.com/ing-bank/cassandra-jdbc-wrapper).
