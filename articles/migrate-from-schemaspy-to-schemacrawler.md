---
title: Migrate from SchemaSpy to SchemaCrawler Without Rewriting Your Runbooks
published: false
description: Keep your familiar SchemaSpy command line while generating Git-friendly, AI-readable Google OKF database documentation with SchemaCrawler.
tags: database, devops, github, opensource
canonical_url: https://www.schemacrawler.com/migrate-from-schemaspy-to-schemacrawler.html
cover_image:
---

If you already use SchemaSpy to document a database, moving to SchemaCrawler does not have to mean replacing every script at once.

The latest SchemaCrawler release includes a SchemaSpy-compatible shim. It accepts common SchemaSpy command-line arguments, connects to the database, and runs SchemaCrawler Scribe to produce documentation in Google Open Knowledge Format (OKF).

That gives you a gradual migration path: keep the command-line shape your team knows, while changing the output from a generated website bundle to a set of Markdown files that can live in Git.

## Start with the SchemaSpy command you already have

The shim is called `schemaspy` and is included in the SchemaCrawler Docker image and the other SchemaCrawler installers.

For example, a SchemaSpy command for a SQLite database might look like this:

```sh
schemaspy \
  -t sqlite \
  -db ./sc.db \
  -u sa \
  -p "" \
  -o ./schema-output.zip
```

With SchemaCrawler installed, the same command produces an OKF bundle. The adapter translates the SchemaSpy options and invokes SchemaCrawler Scribe behind the scenes.

You can use the Docker image without installing Java locally:

```sh
docker run --rm -it \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  schemacrawler/schemacrawler \
  schemaspy \
  -t sqlite \
  -db /home/schcrwlr/sc.db \
  -u sa \
  -p "" \
  -o share/schema-output.zip
```

On Windows PowerShell, use a backtick instead of a backslash for line continuation. The Docker mount makes the database and generated ZIP available in your current directory.

To see the database types supported by the adapter, run:

```sh
schemaspy -dbhelp
```

In Docker:

```sh
docker run --rm -it schemacrawler/schemacrawler schemaspy -dbhelp
```

The shim is intended to make migration practical, not to promise that every SchemaSpy-specific option has an identical meaning. Supported options are translated, compatibility options may be accepted as no-ops, and unsupported options report an explicit error. Check the adapter documentation when converting a more specialized command.

## What Google OKF changes

SchemaSpy's usual output is a browser-oriented HTML report. That is useful when someone wants to click through a schema, but HTML is not always convenient as a source artifact. It is difficult to review meaningfully in a pull request, search with ordinary text tools, or give to another tool without first scraping the pages.

Google OKF uses Markdown files with YAML frontmatter and links between related documents. A generated bundle contains files such as:

```text
index.md
tables/
  authors.md
  books.md
cross-references/
  index.md
```

The exact tree depends on the database, but the important property is that the documentation is ordinary text. Developers can open it in Visual Studio Code, review it in GitHub, and diff one schema snapshot against another.

The pages can include:

- tables, columns, keys, constraints, triggers, and references
- routines such as functions and stored procedures
- cross-reference pages for relationships
- Mermaid diagrams embedded in Markdown
- optional lint reports for schema design issues

The YAML frontmatter also makes each document easier for static-site generators and indexing tools to understand. For an AI agent, the result is a collection of small, named, linked documents instead of one opaque report. For a developer, it is still just Markdown.

## Run Scribe directly when you are ready

Once the compatibility shim is working, you can switch to SchemaCrawler's native command line. This makes the output options explicit and gives you access to SchemaCrawler features such as linting and row counts.

Here is a Docker example that writes an expanded OKF directory instead of a ZIP file:

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=/home/schcrwlr/sc.db \
  --info-level=maximum \
  --command scribe \
  --output-format okf \
  --title "Books Database" \
  --expanded-output \
  --include-lint \
  --load-row-counts \
  --output-file=share/schema.zip
```

The compatibility command is a good first step. The native command is a good long-term choice for a new automation job.

## Check the documentation into GitHub

An OKF directory is a natural build artifact for a documentation repository. A simple repository layout might be:

```text
.
├── .github/workflows/schema-docs.yml
├── schema/
│   ├── index.md
│   ├── tables/
│   └── cross-references/
└── README.md
```

You can generate the files on a schedule or whenever your schema migrations are merged. Commit the generated Markdown to a branch, or publish it as the Pages source from a dedicated documentation repository.

Checking in generated output has a useful side effect: schema changes become visible in ordinary pull requests. A changed column, new foreign key, or removed table appears as a text diff. The database remains the source of truth, while Git records how its documented shape changed over time.

Do not commit database passwords or connection strings containing secrets. Store credentials in GitHub Actions secrets and pass them to the container as environment variables or workflow inputs.

## Publish the OKF bundle with GitHub Pages

GitHub Pages can publish Markdown content using Jekyll. Because OKF pages include YAML frontmatter, the generated directory can be used as the source for a Pages site. A minimal workflow can generate the documentation and deploy it:

```yaml
name: Publish schema documentation

on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate OKF documentation
        run: |
          mkdir -p public
          docker run --rm \
            --mount type=bind,source="$PWD",target=/home/schcrwlr/share \
            schemacrawler/schemacrawler \
            /opt/schemacrawler/bin/schemacrawler.sh \
            --server=sqlite \
            --database=/home/schcrwlr/share/sc.db \
            --info-level=maximum \
            --command scribe \
            --output-format okf \
            --title "Books Database" \
            --expanded-output \
            --include-lint \
            --output-file=/home/schcrwlr/share/public

      - name: Configure Pages
        uses: actions/configure-pages@v5

      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: public
          destination: _site

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: _site

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

For a database that is not a file in the repository, replace the SQLite connection with your database server and provide the connection values through GitHub Actions secrets. You may also choose to commit the generated `schema` directory and use a separate Pages workflow that publishes that checked-in directory.

After enabling GitHub Pages for the repository, the workflow publishes `index.md` as the entry point and keeps the links to table and cross-reference pages intact. The result is a browsable schema reference at the same URL your team can use in tickets, pull requests, and onboarding notes.

## A practical migration sequence

You do not need to change everything in one pull request:

1. Replace the SchemaSpy executable with the SchemaCrawler `schemaspy` shim.
2. Confirm that your database connection and filtering options produce the expected OKF bundle.
3. Add the generated Markdown to a Git repository and review the first schema diff.
4. Publish the directory with GitHub Pages if a hosted reference site is useful.
5. Move mature scripts to the native `scribe` command and add options such as `--include-lint`.

SchemaSpy and SchemaCrawler both work with relational database metadata over JDBC, so the database connection remains familiar. The main change is what you do with the result: instead of treating documentation as a report to regenerate and distribute, you can treat it as structured source material that belongs in your repository.

## Learn more

- [SchemaCrawler](https://www.schemacrawler.com/)
- [SchemaCrawler Scribe](https://www.schemacrawler.com/scribe.html)
- [SchemaSpy Adapter](https://www.schemacrawler.com/schemaspy-adapter.html)
- [Google Open Knowledge Format specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
