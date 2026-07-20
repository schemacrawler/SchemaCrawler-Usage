# SchemaCrawler Scribe

SchemaCrawler Scribe helps you turn database structure into documentation that is easy to read and easy to share.

SchemaCrawler Scribe generates documentation in [Google OKF format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md), so your schema knowledge lives in plain text files rather than in a locked-in format. 

Google OKF is lightweight and portable. It uses Markdown with YAML front matter, so people can read it in tools they already use, such as Visual Studio Code, while AI systems can still parse it cleanly. That makes it a good fit for teams that want documentation that is both human-friendly and machine-friendly. Because the output is plain text, you can store it in Git, review changes in pull requests, and keep it under version control like any other project asset.

SchemaCrawler Scribe is useful when you want database documentation that stays close to the data model. Instead of maintaining separate documentation by hand, you can generate a structured documentation tree that reflects tables, relationships, and other database concepts in a format that is simple to browse and update.

## Benefits

- **[SchemaCrawler Scribe](https://www.schemacrawler.com/scribe.html)** produces clean, navigable Markdown documentation from live database metadata, packaged as a [Google OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) bundle.
**[Google OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) output** is cross‑linked Markdown with YAML frontmatter, readable by humans as well as AI agents, making the schema navigable as a knowledge graph and fully diff‑friendly in Git.
- **Supports all major relational databases** including PostgreSQL, MySQL, MariaDB, Oracle, Microsoft SQL Server, IBM DB2, Snowflake, SQLite, and more.
- **[GitHub Docs frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)** is included in every generated page, allowing the OKF bundle to be turned into a full website using standard static‑site tools like Hugo or Jekyll on GitHub Pages.
- **Cross‑linked schema navigation**: tables, columns, routines, and foreign keys become Markdown links, with auto‑generated directory indexes for easy browsing.
- **Mermaid diagrams** are embedded directly into Markdown to visualize relationships and structure.
- **Comprehensive schema coverage**: tables, columns, keys, constraints, routines, triggers, references, cross‑reference pages, and optional lint or anomaly reports.
- **Localized output** supports multiple languages for international teams.
- **Git‑native workflow**: everything is plain text, diff‑friendly, and ideal for version control. It is deterministically generated for the same database schema.


## Usage

Run a standard SchemaCrawler command-line or Docker container. Connect to a database of your choice. Use the `scribe` command and `okf` output format. It is a good idea to provide a title with `--title`. By default, a zip file is created, but `--expanded-output` will produce a directory structure. `--include-lint` show design issues with the database in a separate report.

```sh
docker run \
  --mount type=bind,source="$(pwd)",target=/home/schcrwlr/share \
  --rm -it \
  schemacrawler/schemacrawler \
  /opt/schemacrawler/bin/schemacrawler.sh \
  --server=sqlite \
  --database=sc.db \
  --info-level=maximum \
  --command scribe \
  --output-format okf \
  --title "Books Database" \
  --expanded-output \
  --include-lint \
  --load-row-counts \
  --output-file=share/schema
```

Use backtick (`) instead of backslash (\) for command-line continuations in PowerShell.

## Also See

- [SchemaCrawler AI MCP Server](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage)
