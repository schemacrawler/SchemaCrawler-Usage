# SchemaCrawler Execution Pipeline

SchemaCrawler separates loading database metadata from filtering it into a catalog projection for an individual command. The distinction matters in both the command-line and the [interactive shell](schemacrawler-shell.md).

## Live Database

1. **Connect.** SchemaCrawler opens the configured live database connection.
2. **Load.** A load crawls metadata and publishes a baseline catalog. Load
   options determine which metadata is retrieved. Limit options bound the
   objects available from the live crawl.
3. **Filter and project.** Each command applies its current limit, filter,
   and grep options to the loaded catalog and uses the resulting projection.
   This post-load filtering does not retrieve more metadata or change the
   retained baseline.
4. **Execute.** The command sees its projection. Another command can
   create a different projection from the retained baseline.

In the interactive shell, changing grep or filter settings affects the next `execute` command and does not require another `load`. For example:

```text
load --info-level maximum
grep --grep-tables .*\.BOOKS
filter --parents 1 --no-empty-tables
execute --command list
```

The grep and filter settings narrow the projection from the existing baseline. The `--no-empty-tables` filter excludes tables whose row count is known to be zero; a table with an unknown row count remains eligible. Row counts must already have been loaded.

Changing live load or limit options makes the loaded catalog stale. Run `load` again before executing commands so the baseline reflects those crawl settings. A projection cannot add objects that were not loaded.

## Offline Catalog

An offline catalog is deserialized with the active database object membership stored in its snapshot. Commands then apply their current limit, filter, and grep settings to that loaded catalog to create a projection; projections do not rewrite the snapshot or permanently remove objects from its baseline. A current limit can narrow a command's projection, but it cannot retrieve objects absent from the serialized catalog.

In the interactive shell, changing load or limit options still requires `load` before the next execution; for an offline connection, this reloads the snapshot rather than crawling a live database. Changing grep or filter options does not require another `load`.

For repeatable broad offline queries, serialize the desired metadata and membership into the snapshot using the meximum info-level. Current crawl settings do not expand or re-crawl an offline catalog.

See [offline catalog snapshots](offline.md), [grep](schemacrawler-grep.md),
and [shell commands](schemacrawler-shell.md) for usage details.
