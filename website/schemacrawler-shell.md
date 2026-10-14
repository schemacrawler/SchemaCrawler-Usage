# SchemaCrawler Interactive Shell

SchemaCrawler Interactive Shell is an interactive shell environment that allows you to work with your database metadata.

The easiest way to learn how to use the SchemaCrawler Interactive Shell is by doing the 
[live online tutorial](https://killercoda.com/schemacrawler). The tutorial works from within 
any browser with no software or plugins needed.

You can connect to a database, load the schema metadata catalog, and then execute commands against the metadata.

In order to use SchemaCrawler Interactive Shell, download the [latest SchemaCrawler distribution](https://www.schemacrawler.com/downloads.html#running-examples-locally/).
Unzip it, and follow instructions in the `shell` example included with the distribution. 
You can start the SchemaCrawler Interactive Shell from the command-line with a `--shell` argument. You can also download [platform-specific SchemaCrawler installers](https://github.com/schemacrawler/SchemaCrawler-Installers/releases/) to use the SchemaCrawler Interactive Shell.

Once the SchemaCrawler Interactive Shell starts up, you will get the `schemacrawler>` command-prompt, and you can interact with SchemaCrawler using shell commands.

Example shell commands look like:

```sh
help
connect --server <server> --host <host> --user <host> --password <password> --database <database>
load --info-level maximum
execute --command list
```

Results of command output can be redirected into a file. You can also generate schema diagrams.
The schema metadata remains loaded as long as the shell is open, even if the database connection is closed.


## Loading and Selecting Metadata

The shell keeps the loaded catalog as a baseline for commands. Grep and
filter changes select from that baseline on the next execution; they do not
require another load. Changes to live load or limit options require `load`
before executing again. For details, see the
[execution pipeline](schemacrawler-execution-pipeline.md).

Use `help connect`, `help load`, `help limit`, `help grep`, `help filter`,
and `help execute` for shell-specific command options. `help commands` and
`help loaders` list the available commands and catalog loaders.



The live online tutorial on the [interactive shell](https://killercoda.com/schemacrawler/scenario/schemacrawler-shell) walks you through these concepts to help you understand them.
