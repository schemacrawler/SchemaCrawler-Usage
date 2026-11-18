# Reverse Engineer Any Database into dbdiagram.io, PlantUML, Mermaid, or QuickDBD - Then Keep Designing

Most database diagram tools stop at documentation. They connect to your database, inspect the schema, and generate a report or a picture. That is useful, but it does not help if your next step is design work.

*What if you want to start from an existing database, open the result in a design tool, add a few new tables, adjust relationships, and then turn that updated design back into SQL?*

> **[SchemaCrawler](https://www.schemacrawler.com/) supports that workflow.**

SchemaCrawler can connect to any database with a JDBC driver and generate editable output in **four** useful formats:

- **DBML** for [dbdiagram.io](https://dbdiagram.io/home)
- **PlantUML** for [PlantText](https://www.planttext.com/), IntelliJ, and other PlantUML tools
- **Mermaid** for GitHub, GitLab, Notion, and the [Mermaid Live Editor](https://mermaid.live/)
- **QuickDBD** for [QuickDatabaseDiagrams.com](https://app.quickdatabasediagrams.com/#/)

That gives you a practical round-trip workflow:

1. **Connect** to an existing database
2. **Export** the schema into DBML, PlantUML, Mermaid or QuickDBD
3. **Edit** the design in the tool you already use
4. **Generate DDL** from the updated design when you need SQL again

SchemaSpy is strong when you want a browsable HTML report for stakeholders. But HTML is the end of the line. You can read it, click through it, and share it, but you cannot open it in a design tool and keep working. If you need reverse engineer -> edit design -> generate DDL, **[SchemaCrawler](https://www.schemacrawler.com/)** is the better fit.

In this article, I will use the Northwind sample SQLite database for all examples.

---

## Step 1: Connect

Make sure you have [Docker](https://docs.docker.com/desktop/) installed. Then download the [Northwind sample SQLite database](https://github.com/jpwhite3/northwind-SQLite3/blob/4f56e7f5906dfd23b25244c5bfe8fb5da6402efd/dist/northwind.db?raw=true) into your current directory.

All commands below mount your current directory into the SchemaCrawler container, so the generated files are written back to your machine.

If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick "`".

---

## Step 2: Export

### Export to DBML for dbdiagram.io

DBML is the best choice if you want to keep designing and later generate SQL from the updated model.

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=script \
  --script-language=python \
  --script=dbml.py \
  --output-file=share/northwind.dbml
```

Open [dbdiagram.io](https://dbdiagram.io/d), paste in the contents of `northwind.dbml`, and you immediately have an editable diagram based on the live database.

### Export to PlantUML

PlantUML is a good choice if your team keeps diagrams in source control or already uses PlantUML in docs and architecture notes.

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=script \
  --script-language=python \
  --script=plantuml.py \
  --title="Northwind Database Schema" \
  --output-file=share/northwind.puml
```

Open `northwind.puml` in [PlantText](https://www.planttext.com/) or your IDE and keep editing.

### Export to Mermaid

Mermaid is the best choice if you want diagrams that render directly in Markdown-based tools such as GitHub, GitLab, and Notion.

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=script \
  --script-language=python \
  --script=mermaid.py \
  --title="Northwind Database Schema" \
  --output-file=share/northwind.mmd
```

Paste `northwind.mmd` into the [Mermaid Live Editor](https://mermaid.live/) or commit it straight into your documentation.

### Export to QuickDBD

QuickDBD is a good choice when you want fast, text-first schema editing in a dedicated diagram editor.

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=script \
  --script-language=python \
  --script=quickdbd.py \
  --title="Northwind Database Schema" \
  --output-file=share/northwind.quickdbd
```

Paste `northwind.quickdbd` into [QuickDatabaseDiagrams.com](https://app.quickdatabasediagrams.com/#/) to continue editing.

---

## Step 3: Edit

This is the part most reverse-engineering tools do not support well.

Once you have exported the live schema into an editable design language, you are no longer stuck with a read-only report. You can continue designing.

For example, imagine that after reverse-engineering northwind you want to add a table for storing playlist tags.

In DBML, you could extend the exported design with something like:

```dbml
Table PlaylistTag {
  PlaylistTagId integer [pk]
  PlaylistId integer [not null]
  TagName varchar [not null]
}

Ref: PlaylistTag.PlaylistId > Playlist.PlaylistId
```

That is the key distinction in this workflow:

- you start from what is actually in production
- you bring that schema into an editable format
- you extend the design instead of redrawing it from scratch

The same idea works with PlantUML, Mermaid, and QuickDBD. Add entities, adjust relationships, rename columns, or reorganize sections of the model for clarity. SchemaCrawler gets you to a clean starting point from a live database instead of forcing you to recreate the schema by hand.

---

## Step 4: Generate DDL

DBML is especially useful because it can be turned back into SQL.

Install the DBML CLI:

```sh
npm install -g @dbml/cli
```

Then generate SQL from your updated design:

```sh
dbml2sql northwind.dbml --postgres
```

Or for MySQL:

```sh
dbml2sql northwind.dbml --mysql
```

Now you have a full round-trip flow:

- reverse engineer from a live database
- edit the design in a modeling tool
- generate SQL from the updated design

That is a much more useful workflow than producing a static HTML report and stopping there.

---

## Worked Example: northwind from Live Database to Editable Design

Here is the full DBML flow in one sequence.

### 1. Export northwind to DBML

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=share/northwind.db \
  --info-level=standard \
  --command=script \
  --script-language=python \
  --script=dbml.py \
  --output-file=share/northwind.dbml
```

### 2. Open the result in dbdiagram.io

Paste the contents of `northwind.dbml` into [dbdiagram.io](https://dbdiagram.io/d).

### 3. Extend the model

Add new tables, fields, and relationships directly in DBML.

### 4. Generate SQL

```sh
dbml2sql northwind.dbml --postgres
```

At that point you have gone from a real database to an editable design and back into SQL without manually redrawing anything.

---

## When to Choose Each Output Format

- **Choose DBML** if you want the strongest design-tool workflow and the option to generate SQL later.
- **Choose PlantUML** if your team prefers text-based diagrams in source control or already uses PlantUML in architecture docs.
- **Choose Mermaid** if you want diagrams that live directly inside Markdown, GitHub, GitLab, or internal docs.
- **Choose QuickDBD** if you want rapid text-based editing in the QuickDatabaseDiagrams editor and an easy way to iterate on schema shape.

You do not need to choose only one forever. The same database can be exported to all four, depending on what the next step in your workflow looks like.

---

## Why This Matters

Reverse engineering is only half the job.

Developers often inherit an existing database and need to answer more than "what tables are there?" They need to ask:

- what should we add next?
- how do we model the next feature without breaking what exists?
- how do we propose changes in a format that is easy to review?
- how do we get from the current schema to future DDL with less manual work?

SchemaCrawler helps because it starts with the live database and produces output you can keep working with.

That is the real value of DBML, PlantUML, Mermaid, and QuickDBD export. Not just nicer diagrams, but a better workflow.

---

## Try It Yourself

Start with the northwind sample database and generate one of the editable formats above. Once you have the workflow working locally, switch the connection to PostgreSQL, MySQL, SQL Server, Oracle, DB2, or any other JDBC database supported by SchemaCrawler.

If you want to customize the generated output, you can find and edit the built-in scripts:

- [dbml.py](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/dbml.py)
- [plantuml.py](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/plantuml.py)
- [mermaid.py](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/mermaid.py)
- [quickdbd.py](https://github.com/schemacrawler/SchemaCrawler/blob/main/schemacrawler-scripting/src/main/resources/scripts/quickdbd.py)
