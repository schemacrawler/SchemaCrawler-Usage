# Getting Started with SchemaCrawler Examples

Before running any of the examples in this directory, follow the steps below to set up your environment and verify that everything is working.

## Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed.
- All example commands are run **inside the SchemaCrawler Docker container**.

> If you prefer to install SchemaCrawler locally instead of using Docker, see the
> [SchemaCrawler downloads page](https://www.schemacrawler.com/downloads.html) for instructions.
> The `schemacrawler` command used in the examples is available in both Docker and local installs.


## Step 1 — Start a Database

The examples use a test database with a Books schema. Follow the instructions in
[`../docker-compose/README.md`](../docker-compose/README.md) to:

Choose a database (for example, PostgreSQL). Change your working directory to the "docker-compose" folder. Start the SchemaCrawler container and the database container with Docker Compose:

```sh
docker compose -f schemacrawler.yaml -f postgresql.yaml up -d
```


## Step 2 — Connect to the SchemaCrawler Container

Open a shell inside the running SchemaCrawler container:

```sh
docker exec -it schemacrawler bash
```

All subsequent `schemacrawler` commands in the examples are run from this shell prompt inside the container.


## Step 3 — Set Up the Test Schema

The examples use a test database with a Books schema. Follow the instructions in
[`../docker-compose/README.md`](../docker-compose/README.md) to:

```sh
/opt/schemacrawler/testdb.sh \
  --url "jdbc:postgresql://postgresql:5432/schemacrawler?ApplicationName=SchemaCrawler" \
  --user schemacrawler \
  --password schemacrawler
```

(Modify the command as needed for PowerShell or other shell.)

> The `../docker-compose/README.md` file has the exact setup commands for every supported database.
> All examples will use PostgreSQL, but can be adapted to any other database, and for a local SchemaCrawler install.


## Step 4 — Verify the Connection

Before following any specific example, confirm that SchemaCrawler can connect to your database and list its objects:

```sh
schemacrawler \
  --server postgresql \
  --host postgresql \
  --database schemacrawler \
  --user schemacrawler \
  --password schemacrawler \
  --info-level minimum \
  --command list
```

> Replace the connection options with those for your chosen database.
> See [`../docker-compose/README.md`](../docker-compose/README.md) for the connection options for each database.

You should see a list of tables in the Books schema. You are now ready to follow any of the examples.

## Step 5 — Try Out the Examples

Start with the most basic example, ["commandline"](commandline.md).


## Working with Output Files

Some examples produce output files (diagrams, serialized schemas, reports). The SchemaCrawler container mounts your **current working directory** (the directory where you ran `docker compose up`) to `/home/schcrwlr/share` inside the container.

To write an output file so that it is accessible on your host machine, use the `share/` prefix:

```sh
schemacrawler \
  ... \
  --output-file share/output.png
```

The file `output.png` will appear in your current working directory on the host.

## Working with Script and Template Files

Some examples use Python scripts, JavaScript scripts, or template files (Velocity, Mustache, Thymeleaf). To make these files accessible inside the container, place them in your current working directory on the host. They will be available inside the container under `share/`:

```sh
schemacrawler \
  ... \
  --script share/tables.py
```

```sh
schemacrawler \
  ... \
  --template share/tables.vm
```

## Tear Down

When you are done, stop and remove the containers:

```sh
docker compose -f schemacrawler.yaml -f postgresql.yaml down -t0
```
