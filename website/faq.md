<!-- markdownlint-disable MD024 -->
# SchemaCrawler - Frequently Asked Questions

## General

1. [What is SchemaCrawler?](#whats-schemacrawler)
2. [What does SchemaCrawler output look like?](#output)
3. [What are the SchemaCrawler commands?](#commands)
4. [What does a SchemaCrawler configuration file look like?](#config)

## Supported Platforms

1. [What databases does SchemaCrawler work with?](#supported-databases)
2. [What Java version does SchemaCrawler work with?](#supported-java)
3. [What operating systems does SchemaCrawler work with?](#supported-os)
4. [Can SchemaCrawler be used with ant?](#ant)
5. [Can SchemaCrawler be used with Apache Maven?](#maven)

## SchemaCrawler Database Diagrams

1. [What is a SchemaCrawler database diagram?](#diagrams)
2. [What does a SchemaCrawler database diagram look like?](#diagram-output)

## SchemaCrawler Grep

1. [What is SchemaCrawler Grep?](#whats-schemacrawler-grep)
2. [What does SchemaCrawler Grep output look like?](#grep-output)
3. [What are the SchemaCrawler Grep commands?](#grepcommands)
4. [What does a SchemaCrawler configuration file look like?](#config)

## SchemaCrawler Features

1. [What is SchemaCrawler Lint?](#schema-lint)
2. [What are implicit associations?](#implicit-associations)
3. [Can SchemaCrawler be used with scripting languages?](#scripting)
4. [Can SchemaCrawler be used programmatically?](#api)
5. [Can SchemaCrawler be used integrated with other programs?](#integrations)

## Distribution

1. [Where is SchemaCrawler available?](#availability)
2. [Is technical support available?](#tech-support)
3. [Is SchemaCrawler free?](#cost)


## General

---------

### <a name="whats-schemacrawler">What is SchemaCrawler?</a>

SchemaCrawler is an open-source Java API that makes working with database metadata as easy as working with plain old Java objects.
SchemaCrawler is also a command-line tool to output your database schema and data in a readable form. The output is designed to be [diff-ed](https://en.wikipedia.org/wiki/Diff) with previous versions of your database schema.

---------

### <a name="output">What does SchemaCrawler output look like?</a>

SchemaCrawler can produce [plain text,](snapshot-examples/snapshot.txt)
[HTML5,](snapshot-examples/snapshot.md)
[HTML5 with embedded diagrams](snapshot-examples/snapshot.svg.md),
[JavaScript object notation (JSON)](snapshot-examples/snapshot.json) or
[YAML](snapshot-examples/snapshot.yaml) output. Compare the [output formats](output.md) and [serialization guidance](serialize.md), or follow the [serialization example](examples/serialize.md) for JSON and YAML.

---------

### <a name="commands">What are the SchemaCrawler commands?</a>

Try the [live command-line tutorial](https://killercoda.com/schemacrawler) in a browser, or install SchemaCrawler and run `schemacrawler --help` for command and option details. Follow the [command-line recipe](how-to.md#command-line) and [runnable example](examples/commandline.md); see [configuration](config.md) for settings.

---------

### <a name="config">What does a SchemaCrawler configuration file look like?</a>

An example of a [SchemaCrawler configuration file.](config/schemacrawler.config.properties)

---------


## Supported Platforms

---------

### <a name="supported-databases">What databases does SchemaCrawler work with?</a>

SchemaCrawler supports any database for which there is a JDBC database driver available. SchemaCrawler has been tested with various databases, and JDBC drivers. For more information, see [Database System Support.](database-support.md)

---------

### <a name="supported-java">What Java version does SchemaCrawler work with?</a>

SchemaCrawler works with Java SE 17 or better.

---------

### <a name="supported-os">What operating systems does SchemaCrawler work with?</a>

SchemaCrawler works with any operating system that supports Java SE 17 or better.

---------

### <a name="ant">Can SchemaCrawler be used with ant?</a>

Yes, the SchemaCrawler command-line can be called from ant, using the exec task.

---------

### <a name="maven">Can SchemaCrawler be used with Apache Maven?</a>

Yes SchemaCrawler can be used in a Apache Maven project as an API, or to generate Apache Maven reports in your projects. In order to use SchemaCrawler in your Apache Maven projects, simply add a dependency to SchemaCrawler in your pom.xml.
_For more details, see the [plugins](plugins.md) page._

Using the [SchemaCrawler Report Maven Plugin](https://github.com/schemacrawler/SchemaCrawler-Report-Maven-Plugin), 
you can generate a SchemaCrawler report along with other reports for your Apache Maven generated site.

---------


## SchemaCrawler Database Diagrams

---------

### <a name="diagrams">What is a SchemaCrawler database diagram?</a>

SchemaCrawler uses [Graphviz](https://www.graphviz.org/) to generate entity-relationship diagrams, and [Grep](schemacrawler-grep.md) to filter schema objects. See the [diagramming guide](diagramming.md) and its [runnable example](examples/diagram.md).

---------

### <a name="diagram-output">What does a SchemaCrawler database diagram look like?</a>

An example of a SchemaCrawler database diagram:
[![An example of a SchemaCrawler database diagram](diagram-examples/diagram.png)](diagram-examples/diagram.png "SchemaCrawler database diagram")

---------

## SchemaCrawler Grep

---------

### <a name="whats-schemacrawler-grep">What is SchemaCrawler Grep?</a>

SchemaCrawler Grep searches schema objects with regular expressions. See the [Grep reference](schemacrawler-grep.md) and [runnable example](examples/grep.md).

---------

### <a name="grep-output">What does SchemaCrawler Grep output look like?</a>

Grep returns the normal SchemaCrawler output, filtered to matching objects; see the [Grep reference](schemacrawler-grep.md) and [example](examples/grep.md).

---------

### <a name="grepcommands">What are the SchemaCrawler Grep commands?</a>

See the [Grep reference](schemacrawler-grep.md), the [filtering recipe](how-to.md#excluded-tables-or-columns), and the [Grep example](examples/grep.md).

---------

### <a name="config">What does a SchemaCrawler configuration file look like?</a>

The SchemaCrawler Grep configuration file is the same as the [SchemaCrawler configuration file.](config/schemacrawler.config.properties)

---------


## SchemaCrawler Features

---------

### <a name="schema-lint">What is SchemaCrawler Lint?</a>

SchemaCrawler Lint finds potential schema design issues with `--command=lint`. See the [Lint reference](lint.md) and [runnable example](examples/lint.md).

---------

### <a name="implicit-associations">What are implicit associations?</a>

Implicit Associations infer relationships between tables when the database has no foreign key. See the [feature reference](implicit-associations.md) and [runnable example](examples/implicit-associations.md).

---------

### <a name="scripting">Can SchemaCrawler be used with scripting languages?</a>

SchemaCrawler supports Python and JavaScript scripts. See the [scripting reference](scripting.md) and the [Python](examples/python.md) and [JavaScript](examples/javascript.md) examples.

---------

### <a name="api">Can SchemaCrawler be used programmatically?</a>

SchemaCrawler provides Java objects for database metadata. Read [How to Get Database Metadata as Java POJOs](https://dev.to/sualeh/how-to-get-database-metadata-as-java-pojos-24li), browse the [Javadocs](https://javadoc.io/doc/us.fatehi/schemacrawler/), or see the [API code examples](code-examples.md).

---------

### <a name="integrations">Can SchemaCrawler be used integrated with other programs?</a>

Use the [Java API](how-to.md#api) to integrate SchemaCrawler with other programs, or generate custom output with [Velocity](https://velocity.apache.org/). See the [Velocity recipe](how-to.md#velocity) and [runnable example](examples/velocity.md).


</dl>


## Distribution

### <a name="availability">Where is SchemaCrawler available?</a>

SchemaCrawler is available from the [Downloads page](downloads.md).

---------

### <a name="tech-support">Is technical support available?</a>

Yes. Please see [Support and Consulting](consulting.md) for details.

---------

### <a name="cost">Is SchemaCrawler free?</a>

See [SchemaCrawler license](license.md) for details.
