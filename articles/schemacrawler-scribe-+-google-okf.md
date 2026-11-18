# SchemaCrawler Scribe + Google OKF: AI-Ready Database Docs You Can Keep in Git

If your database documentation is always behind production, this is for you.

**SchemaCrawler Scribe** generates structured database documentation directly from live schema metadata, using **[Google Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md)**.

The result is documentation that works for both developers and AI agents, without creating a second documentation workflow.

Source code: [SchemaCrawler/schemacrawler-scribe](https://github.com/schemacrawler/SchemaCrawler/tree/main/schemacrawler-scribe)

## The Problem SchemaCrawler Scribe Solves

Most teams end up in one of two modes:

1. Manual docs that drift from reality
2. Generated docs that are hard to read, hard to diff, or hard to reuse

SchemaCrawler Scribe targets the middle ground:

- readable Markdown that developers can review
- structured content that AI systems can parse
- plain text artifacts that belong in version control

This turns documentation into part of your engineering workflow, not a side task.

## What You Get With SchemaCrawler Scribe

- AI-agent-friendly database documentation
- Documentation generated directly from schema metadata
- Localized output (German, French, and more)
- Mermaid diagrams embedded in Markdown
- Artifacts that are both human-readable and machine-parseable
- Straightforward use in VS Code and other Markdown tooling

## Why Google OKF is a Strong Format for Database Docs

SchemaCrawler Scribe outputs in [Google Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md), which gives you one format that serves multiple use cases:

- **Human-friendly**: Markdown pages are readable in editors, code review tools, and docs portals
- **AI-friendly**: structured sections and metadata make extraction and grounding more reliable
- **Git-friendly**: text output is diffable, reviewable, and easy to version
- **Tool-friendly**: open format reduces lock-in and keeps migration options open
- **Team-friendly**: works well in Visual Studio Code and any Markdown-centric workflow

In short: one documentation artifact that supports people, automation, and long-term maintainability.

## If You Use SchemaSpy Today, This Will Feel Familiar

SchemaCrawler Scribe is in the same family of tooling as SchemaSpy: both crawl schema metadata and generate browsable documentation.

Like SchemaSpy-style documentation workflows, Scribe covers:

- per-table pages (columns, keys, constraints, triggers, references)
- cross-reference pages (what references what)
- routine documentation (functions and stored procedures)
- relationship visualization (Mermaid in Markdown)
- lint and anomaly reporting in generated output

So if your team already likes auto-generated schema docs and relationship views, SchemaCrawler Scribe keeps that experience while producing **Google OKF Markdown** artifacts that are easier to review in Git and consume with AI tooling.

## Usage

Run standard SchemaCrawler from the command line or Docker. Use the `scribe` command with `okf` output format.

Tips:

- Use `--title` to label the generated documentation set
- By default, output is zipped; add `--expanded-output` to generate a directory tree instead
- Add `--include-lint` to generate schema design issue reports

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

If you are using PowerShell, replace each trailing backslash with a backtick for line continuation.

## Also see

- [SchemaCrawler AI MCP Server](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage)
