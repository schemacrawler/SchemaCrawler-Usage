# Getting Started with SchemaCrawler

## SchemaCrawler Installation

### Pre-requisites for Installation

- Install the latest version of [Java](https://www.oracle.com/java/technologies/)
- Optionally, install [Graphviz] if you want to create schema diagrams

### Cross-platform Installation

[There are multiple ways to download, install and use SchemaCrawler.](downloads.md)



## Getting Started

### Choose a path

Before downloading SchemaCrawler, read the [FAQs](faq.md) and browse the [resources](resources.md).

#### Explore or visualize

Start with [schema search](schemacrawler-grep.md) or [database diagrams](diagramming.md). Read [How to explore a new database](https://dev.to/sualeh/how-do-you-explore-a-new-database-1pge), [Explore Your Database Schema with SchemaCrawler](https://dev.to/sualeh/explore-your-database-schema-with-schemacrawler-5341), or follow a [dbdiagram.io](https://dev.to/sualeh/how-to-generate-dbdiagram-io-diagrams-for-your-database-431l) or [Mermaid diagram](https://dev.to/sualeh/how-to-generate-mermaid-diagrams-for-your-database-33bn) tutorial.

For a quick database-specific example, see how to visualize [MySQL](https://dev.to/sualeh/how-to-visualize-your-mysql-database-with-one-command-and-nothing-to-install-21cp), [PostgreSQL](https://dev.to/sualeh/how-to-visualize-your-postgresql-database-with-one-command-and-nothing-to-install-3e3j), or [SQLite](https://dev.to/sualeh/how-to-visualize-your-sqlite-database-with-one-command-and-nothing-to-install-1f4m) with one command.

#### Document

Compare [output formats](output.md) and [serialization](serialize.md), or generate navigable Markdown with [SchemaCrawler Scribe](scribe.md) and the [Scribe and Google OKF tutorial](https://dev.to/sualeh/schemacrawler-scribe-google-okf-ai-ready-database-docs-you-can-keep-in-git-2off). For a scripting-based walkthrough, see [Automatically Document Your Database in Markdown](https://dev.to/sualeh/automatically-document-your-database-in-markdown-elf).

#### Analyze

Use [graph metrics and table importance](importance.md) to prioritize tables, or [lint your schema](lint.md) for design issues. See [how to rank tables by importance](https://dev.to/sualeh/rank-your-database-tables-by-importance-with-schemacrawler-1gib) or [lint with GitHub Actions](https://dev.to/sualeh/lint-your-database-schema-with-github-actions-workflows-57cg).

#### Use AI assistance

Connect an AI client with the [SchemaCrawler AI MCP Server](mcpserver.md) and its [usage guide](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage), or try the [ChatGPT schema exploration tutorial](https://dev.to/sualeh/use-chatgpt-to-explore-your-database-schema-4mfm).


### Explore the Command-Line

Explore the SchemaCrawler command-line with a [live online tutorial](https://killercoda.com/schemacrawler). 
The tutorial works from within any browser with no software or plugins needed.

If you want to experiment locally, look at the [examples](examples/examples-index.md).


### Connecting To Your Database

Read information about [database support](database-support.md) carefully to understand how to connect to your database.


### How-tos

Once you start getting comfortable with SchemaCrawler, and need to know more about how to do
things, read the [how-tos](how-to.md) section.



## Advanced Topics

### Configuration

SchemaCrawler offers rich configuration options. Read about them on the [SchemaCrawler Configuration](config.md) page.


### SchemaCrawler Docker Image

You can use the official [SchemaCrawler Docker image](https://hub.docker.com/r/schemacrawler/schemacrawler/) from Docker Hub to reduce some of your
installation steps. It comes with [Graphviz] pre-installed, so you can generate schema diagrams.
For more information, see [information on the Docker image](docker-image.md).


### Building From Source Code

To use SchemaCrawler in your development projects, or to build SchemaCrawler from the source code, read
about [building](building.md).



[Python]: https://www.python.org/
[Graphviz]: https://www.graphviz.org/
[Apache Maven]: https://maven.apache.org/
[Apache ant]: https://ant.apache.org/
