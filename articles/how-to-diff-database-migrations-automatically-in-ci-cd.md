# How to Diff Database Migrations Automatically in CI/CD

Database regressions rarely start with application code. They start when a migration changes a column type, removes an index, or introduces a nullable relationship that your code assumed was mandatory. The pull request looks fine, tests pass, and then production fails because the shape of the database drifted.

You can catch this in CI/CD by generating a text snapshot of your schema and diffing it as part of every pull request.

[SchemaCrawler](https://www.schemacrawler.com/) is a practical fit for this workflow because it outputs stable, diff-friendly schema text and runs cleanly in GitHub Actions through the [SchemaCrawler Action](https://github.com/schemacrawler/SchemaCrawler-Action) (which uses Docker) or the [SchemaCrawler Local Action](https://github.com/schemacrawler/SchemaCrawler-Local-Action) (which installs SchemaCrawler on your runner).

The approach below gives you two protections:

- A readable schema diff in your build logs.
- A failed CI check when the schema changes unexpectedly.

## Step 1: Generate Diff-Friendly Schema Snapshots Locally

Start by proving the workflow on your machine. Use two SQLite files (for example, before and after applying a migration) and compare the generated schema snapshots. Let us say that the files are called "database-before.db" and "database-after.db" on your local file system.

```sh
# Schema Before Migration
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/bin/schemacrawler.sh \
--server=sqlite \
--database=share/database-before.db \
--info-level=standard \
--command=schema \
--output-format=text \
--output-file=share/schema-before.txt

# Schema After Migration
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/bin/schemacrawler.sh \
--server=sqlite \
--database=share/database-after.db \
--info-level=standard \
--command=schema \
--output-format=text \
--output-file=share/schema-after.txt

# Diff
diff -u schema-before.txt schema-after.txt
```

If you are using PowerShell on Windows, replace each trailing backslash with a back-tick.

The output is plain text, so your diffs are reviewable in pull requests and easy to archive as artifacts.

## Step 2: Add Schema Diff to GitHub Actions

Now automate the same check in CI/CD. The workflow below runs on pull requests, generates one schema snapshot from the base branch and one from the PR branch, then fails if they differ.

It uses [schemacrawler/SchemaCrawler-Action](https://github.com/schemacrawler/SchemaCrawler-Action) to run SchemaCrawler in the pipeline. You can also use [SchemaCrawler Local Action](https://github.com/schemacrawler/SchemaCrawler-Local-Action).

```yaml
name: Detect Database Schema Drift

on:
  pull_request:
    branches: [ main ]

jobs:
  schema-diff:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout PR branch
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # In a real project, replace this with your migration/build step
      # that creates the database file used for comparison.

      - id: schema-head
        name: Generate schema snapshot (PR)
        uses: schemacrawler/SchemaCrawler-Action@v18.0.3
        with:
          entrypoint: /schemacrawler.sh
          args: >
            --server=sqlite
            --database=/home/schcrwlr/sc.db
            --info-level=standard
            --command=schema
            --output-format=text
            --output-file=schema-pr.txt

      - name: Checkout base branch commit
        run: git checkout ${{ github.event.pull_request.base.sha }}

      # Run your base-branch migration/build step here as well.

      - id: schema-base
        name: Generate schema snapshot (base)
        uses: schemacrawler/SchemaCrawler-Action@v18.0.3
        with:
          entrypoint: /schemacrawler.sh
          args: >
            --server=sqlite
            --database=/home/schcrwlr/sc.db
            --info-level=standard
            --command=schema
            --output-format=text
            --output-file=schema-base.txt

      - name: Diff schema snapshots
        run: |
          git checkout ${{ github.sha }}
          if ! diff -u schema-base.txt schema-pr.txt > schema.diff; then
            echo "Schema drift detected between base and PR."
            cat schema.diff
            exit 1
          fi

      - name: Upload schema diff artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: schema-diff
          path: schema.diff
          if-no-files-found: ignore
```

## Step 3: Make the Differences Actionable

A failing check is useful only if developers can fix it quickly. Use these conventions:

- Keep the diff in CI logs so reviewers can see what changed.
- Upload `schema.diff` as a build artifact for larger diffs.
- Decide policy per repository: just produce an informative report without failing, or fail on every schema change, or fail only when specific objects change.

If your schema changes are expected, the PR should include both migration code and reviewer-approved schema diff output. If a diff is unexpected, you have caught a regression before merge.

This is the core CI/CD hook:

> Catch database schema regressions in pull requests before they reach production.

## Notes for Production Databases

For PostgreSQL, MySQL, SQL Server, Oracle, and other JDBC databases, keep the same pattern and change only connection options. The strongest setup is:

1. Provision an ephemeral database in CI.
2. Apply base branch migrations and snapshot schema.
3. Apply PR branch migrations and snapshot schema.
4. Diff snapshots and fail on unexpected changes.

You can start with SQLite to validate the workflow and then switch to your production engine without changing the review model.

If you want a ready-made starting point, look at the [SchemaCrawler Action usage example](https://github.com/schemacrawler/SchemaCrawler-Action-Usage-Example) and adapt the workflow to your migration process.
