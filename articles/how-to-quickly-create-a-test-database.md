# How to Quickly Create a Test Database

Chinook is an open source test database (schema and data) that was created as an alternative to Microsoft's Northwind database. For a while now, [Luis Rocha](https://github.com/lerocha) has provided scripts to create this database with his [lerocha/chinook-database](https://github.com/lerocha/chinook-database) project. These scripts support building Chinook for Microsoft SQL Server, Oracle, MySQL, PostgreSQL and IBM DB2. However, this project has not been updated in a few years, and the scripts are in different formats and encodings. 

[schemacrawler/chinook-database](https://github.com/schemacrawler/chinook-database) builds on the earlier project. The project has an automatic build using GitHub Actions, which pulls scripts from [lerocha/chinook-database](https://github.com/lerocha/chinook-database), cleans them up, and converts them all to UTF-8 with consistent line-endings. Then are are repacked and redistributed in various ways - as a Java jar file for use in Java programs or in tests with database in [Testcontainers](https://www.testcontainers.org/). The SQLite database can be directly download from the [project site](https://github.com/schemacrawler/chinook-database/releases). But probably the best way to use the package it is use the Docker image from [schemacrawler/chinook-database](https://github.com/schemacrawler/chinook-database) to create the Chinook database on a database of your choice, whether the database server is running on a separate host or within a Docker container itself.


## Create Chinook Database

Using [schemacrawler/chinook-database](https://github.com/schemacrawler/chinook-database) is very simple. The Chinook database Docker image is [published on Docker Hub](https://hub.docker.com/r/schemacrawler/chinook-database). Pull the latest Docker image, and run it using a command like:

```sh
docker run -it schemacrawler/chinook-database /bin/bash
```

and then from the shell run `chinook-database-creator` with a command like:

```sh
chinook-database-creator \
--url "jdbc:postgresql://localhost:5432/database" \
--user ***** --password *****
```

The command uses JDBC internally, so your may want to refer to the [JDBC connection URL documentation for each database](https://www.baeldung.com/java-jdbc-url-format).
 

## Create Chinook Database with Server Running in Docker Compose

You can use `chinook-database-creator` with Docker Compose to create the Chinook database in any container that is running a database. First, create a Docker Compose file with the following contents, and name it "chinook-database.yml".

```yaml
version: '3.7'

services:

  chinook-database:
    image: schemacrawler/chinook-database
    container_name: chinook-database
    stdin_open: true
    tty: true

  postgresql:
    image: postgres
    container_name: postgres
    ports:
      - target: 5432
        published: 5432
        protocol: tcp
        mode: host
    environment:
      POSTGRES_DB: schemacrawler
      POSTGRES_USER: schemacrawler
      POSTGRES_PASSWORD: schemacrawler
```

Then, start the database server and the Chinook database container with:

```sh
docker-compose -f chinook-database.yml up -d
docker exec -it chinook-database /bin/bash
```

and in the shell, create the database with:

```sh
chinook-database-creator \
--url "jdbc:postgresql://postgresql:5432/schemacrawler" \
--user schemacrawler \
--password schemacrawler
```

(Don't forget to clean up.)

```sh
docker-compose -f chinook-database.yml down
```

You can do something similar with any of the supported databases, Microsoft SQL Server, Oracle, MySQL, PostgreSQL and IBM DB2. And that is how easy it is to create a sample Chinook database. 
