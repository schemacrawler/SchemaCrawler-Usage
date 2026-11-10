# SchemaCrawler Configuration

SchemaCrawler is highly configurable. You can choose which database schema metadata to retrieve, which can affect crawl time, and configure the output of SchemaCrawler commands. SchemaCrawler uses the [lightbend/config](https://github.com/lightbend/config) library, so refer to its documentation for property overrides.


## Configuration

SchemaCrawler provides command-line options for commonly used configuration, such as `--no-info` to hide database information in the output. These options and many more can also be set in the SchemaCrawler configuration file. See the complete [schemacrawler.config.properties](config/schemacrawler.config.properties) example. Command-line options take precedence over configuration files.

Configuration settings are loaded in this order:

1. Built-in default values
2. A `schemacrawler.config` resource on the classpath, in Java properties
   (`.properties`), JSON (`.json`), or HOCON (`.conf`) format
3. A similarly named file specified with `-Dconfig.file=<path>` or
   `--config-file=<path>`
4. Individual Java system properties such as
   `-Dschemacrawler.format.hide_primarykey_names=true`
5. Command-line options such as `--no-info`

For more information about configuration loading, see the [lightbend/config](https://github.com/lightbend/config) documentation. The main SchemaCrawler distribution provides complete configuration files in the `config/` directory and places them on the classpath.

## External Runtime Settings

These external settings are used by SchemaCrawler Core, the command-line entry point, and diagram plugins. They are separate from the `schemacrawler.*` configuration options described below, and they are not all environment variables. The seven non-AI settings use canonical `SC_*` names and alternate `SCHCRWLR_*` aliases.

## Sources and Precedence

An **environment variable** is inherited by the Java process. A **system property** is supplied to the JVM, for example `java -DSC_SINGLE_THREADED=true ...`. Exporting a variable does not set a system property. A common prefix does not imply common source support.

For settings that support both sources, resolution is:

1. System property
2. Environment variable
3. Default value

Within a source, the canonical name takes precedence over its alternate alias; source precedence is evaluated first, so an alias system property takes precedence over a canonical environment variable.

Property-only settings use the system property and documented default. Boolean values are stripped and parsed case-insensitively: only `true` enables them; other values mean false. Invalid integer values use the documented default before range clamping.

## Core and Command-Line Settings

| Setting | Alias | Owner and supported sources | Default and accepted values |
| --- | --- | --- | --- |
| `SC_SINGLE_THREADED` | `SCHCRWLR_SINGLE_THREADED` | Core scheduler and connection-source selection: property then environment. | `false`. Boolean; `true` runs loading tasks on the main thread. For connection-source selection, `true` selects a single connection rather than the multi-connection source. Both use the same resolution, so an environment-only value affects both. |
| `SC_LOAD_MAX_THREADS` | `SCHCRWLR_LOAD_MAX_THREADS` | Core scheduler: property then environment. | `5`. Integer, clamped to 1 through 10. Only used by the multithreaded runner; one worker is not the same as main-thread loading. |
| `SC_LOAD_TIMEOUT_SECONDS` | `SCHCRWLR_LOAD_TIMEOUT_SECONDS` | Core scheduler: property then environment. | `3600`. Integer seconds per batch of loading tasks, not the overall crawl. Zero or negative disables the timeout. |
| `SC_WITHOUT_DATABASE_PLUGIN` | `SCHCRWLR_WITHOUT_DATABASE_PLUGIN` | Core connector selection: property only. | Empty/unset: no exemption. One database-system identifier, such as `oracle`, exempts that database from the required-plugin check. It does not install a connector or JDBC driver. |
| `SC_EXIT_WITH_EXCEPTION` | `SCHCRWLR_EXIT_WITH_EXCEPTION` | Command-line entry point: property only. | `false`. Boolean; `true` throws `SystemExitException` on an unsuccessful run instead of calling `System.exit`. Successful runs are unchanged. |

For example, set the scheduler's worker count using PowerShell:

```powershell
$env:SC_LOAD_MAX_THREADS = "3"
```

For a property-only setting, pass the name to the JVM before its main class or `-jar` argument, for example `-DSC_EXIT_WITH_EXCEPTION=true`. Follow the launcher instructions for supplying JVM options; do not assume an application argument will become a system property.

## Graphviz Configuration

These property-only settings control the diagram plugin's Graphviz behavior. They support the alternate `SCHCRWLR_*` aliases shown below.

| Setting | Alias | Owner and supported sources | Default and accepted values |
| --- | --- | --- | --- |
| `SC_GRAPHVIZ_OPTS` | `SCHCRWLR_GRAPHVIZ_OPTS` | Diagram plugin: property only. | Empty/unset: no extra options. String of extra Graphviz command-line options, split into arguments by the existing list parser. Nonblank explicit `schemacrawler.graph.graphviz_opts` configuration wins over both external names. |
| `SC_GRAPHVIZ_PROC_DISABLE` | `SCHCRWLR_GRAPHVIZ_PROC_DISABLE` | Diagram plugin: property only. | `false`. Boolean; `true` makes the Graphviz availability check return false without launching `dot`. |

Pass a property-only setting to the JVM before its main class or `-jar` argument, for example `-DSC_GRAPHVIZ_PROC_DISABLE=true`. Follow the launcher instructions for supplying JVM options; do not assume an application argument will become a system property.

## Color Map

SchemaCrawler allows you to override colors assigned to schemas in HTML output and diagrams. See the [schemacrawler.colormap.properties](config/schemacrawler.colormap.properties) example. The configuration is loaded by default from a file with the `schemacrawler.colormap` stem, following precedence similar to the configuration loading order above. Override color map properties with keys prefixed by `schemacrawler.format.color_map`.


## Configuration Via the API

All configuration options available through files can also be set programmatically with the SchemaCrawler API. See the examples in the `schemacrawler-examplecode` folder of the [SchemaCrawler-Usage](https://github.com/schemacrawler/SchemaCrawler-Usage) project.


## Lint Configuration

See details on configuring lints on the [lints page](lint.md).


## Extending Metadata With Attributes

See how to extend SchemaCrawler metadata with table and column metadata and [implicit associations](implicit-associations.md) using [attributes](attributes.md).


## Data Dictionary Extensions

See how to extend SchemaCrawler with [Data Dictionary Extensions](data-dictionary-extensions.md).


## SchemaCrawler AI MCP Server Settings

For SchemaCrawler AI MCP Server connection and server environment settings, see the [SchemaCrawler-AI-MCP-Server-Usage GitHub repository](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage).
