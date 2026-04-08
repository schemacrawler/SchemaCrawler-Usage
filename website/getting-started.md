# Getting Started with SchemaCrawler

## SchemaCrawler Installation

### Pre-requisites for Installation

- Install the latest version of [Java](https://www.oracle.com/java/technologies/)
- Optionally, install [Graphviz] if you want to create schema diagrams

### Cross-platform Installation

[There are multiple ways to download, install and use SchemaCrawler.](downloads.md)



## Getting Started

### FAQs

Before downloading SchemaCrawler, be sure to read the [FAQs](faq.md) and take a look at the [resources](resources.md).

Watch the video on [How to explore a new database](https://dev.to/sualeh/how-do-you-explore-a-new-database-1pge) to understand the power of SchemaCrawler, and to give you some ideas of how to use it. Also read [Explore Your Database Schema with SchemaCrawler](https://dev.to/sualeh/explore-your-database-schema-with-schemacrawler-5341), [How to Get Database Metadata as Java POJOs](https://dev.to/sualeh/how-to-get-database-metadata-as-java-pojos-24li) and [Lint Your Database Schema With GitHub Actions Workflows](https://dev.to/sualeh/lint-your-database-schema-with-github-actions-workflows-57cg).

SchemaCrawler can [generate diagrams of your database schema](diagramming.md), and export them to other tools. Take a look at [How to Generate dbdiagram.io Diagrams for Your Database](https://dev.to/sualeh/how-to-generate-dbdiagram-io-diagrams-for-your-database-431l)
and [How to Generate Mermaid Diagrams for Your Database](https://dev.to/sualeh/how-to-generate-mermaid-diagrams-for-your-database-33bn) to see how you can continue to evolve your database design. If you want continuous ingtegration, see how you can [Generate Database Diagrams With GitHub Actions Workflows](https://dev.to/sualeh/generate-database-diagrams-with-github-actions-workflows-4l96).

And finally, here are some other quick getting started articles:

- [How to Visualize Your MySql Database with One Command (and Nothing to Install)](https://dev.to/sualeh/how-to-visualize-your-mysql-database-with-one-command-and-nothing-to-install-21cp)
- [How to Visualize Your PostgreSQL Database with One Command (and Nothing to Install)](https://dev.to/sualeh/how-to-visualize-your-postgresql-database-with-one-command-and-nothing-to-install-3e3j)
- [How to Visualize Your SQLite Database with One Command (and Nothing to Install)](https://dev.to/sualeh/how-to-visualize-your-sqlite-database-with-one-command-and-nothing-to-install-1f4m)
- [Automatically Document Your Database in Markdown](https://dev.to/sualeh/automatically-document-your-database-in-markdown-elf)


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
