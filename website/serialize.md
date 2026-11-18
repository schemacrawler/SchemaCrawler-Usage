# SchemaCrawler Serialization

SchemaCrawler can serialize schema metadata for applications or offline work. Java serialization is tied to the Java and SchemaCrawler versions that created it; use it for version-matched snapshots, such as resuming work in the Interactive Shell without reconnecting to the database.
SchemaCrawler does not offer deserialization using formats other than Java
serialization.

SchemaCrawler's three programmatic models, the `Catalog`, `ERModel`, and `ImportanceModel`, are all serializable. For an overview of each model and when to use it, see [SchemaCrawler Has Three Programmatic Models](https://dev.to/sualeh/schemacrawler-has-three-programmatic-models-here-is-when-to-use-each-one-2gb1).

SchemaCrawler needs [Jackson](https://github.com/FasterXML/jackson) jars on the 
classpath to serialize to JSON and YAML, and these can be downloaded with the 
download tool provided with the SchemaCrawler download.


## How to Serialize a Catalog

SchemaCrawler serialization can be run using the 
`--command=serialize` command-line option. The serialized schema metadata model
will be saved to a file.

For a hands-on walkthrough, see the [serialize example](examples/serialize.md).

Serialization can produce binary Java serialization, [JSON](snapshot-examples/snapshot.json), or [YAML](snapshot-examples/snapshot.yaml) using `--output-format`. Use JSON or YAML when another application needs structured metadata; these formats are version-specific and contain identifiers that make them unsuitable for diffs. If your goal is human-readable, navigable documentation rather than serialized metadata, use [SchemaCrawler Scribe](scribe.md).


## How to Load a Serialized Catalog

When you use Java serialization (`--output-format=ser`) to serialize database
metadata to a file, you can load a serialized metadata using the [`offline`](offline.md)
server type. Please make sure that you use the same version of SchemaCrawler to 
create serialized snapshots and to load those offline catalog snapshots.
 