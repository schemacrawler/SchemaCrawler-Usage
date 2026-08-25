# SchemaSpy Adapter

SchemaCrawler provides a SchemaSpy adapter so teams can keep familiar
SchemaSpy-style command usage while generating modern SchemaCrawler Scribe
documentation in OKF format.

## Why this adapter is provided

- **Migration compatibility:** existing runbooks that use SchemaSpy flags like
  `-t`, `-db`, `-host`, `-u`, and `-p` can continue to work.
- **Modern output target:** the adapter runs SchemaCrawler Scribe and produces
  OKF output (`index.md`, table pages, cross-references) that is Git-friendly
  and AI-readable.
- **Operational continuity:** teams can adopt SchemaCrawler incrementally,
  without rewriting all invocation scripts up front.

## How to use it

Use the `schemaspy` launcher from a SchemaCrawler distribution or Docker image.

```sh
schemaspy \
  -t sqlite \
  -db ./sc.db \
  -u sa \
  -p "" \
  -o ./schema-output.zip
```

You can list supported SchemaSpy database types:

```sh
schemaspy -dbhelp
```

The adapter translates options and runs SchemaCrawler with command `scribe`
and output format `okf`.

## Docker usage

In the SchemaCrawler Docker image, both `schemacrawler` and `schemaspy` are
available:

```sh
docker run --rm -it schemacrawler/schemacrawler schemaspy -dbhelp
```

## Expected output

By default, output is a ZIP artifact. For a successful run, expect OKF content
such as:

- `index.md`
- `tables/*.md`
- `cross-references/index.md`

## Current compatibility notes

- Some SchemaSpy options are translated to SchemaCrawler equivalents.
- Some options are accepted as compatibility no-ops.
- Unsupported options fail with explicit guidance.
