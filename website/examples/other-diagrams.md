# Other Diagrams Example

SchemaCrawler can generate diagrams in formats beyond its built-in GraphViz generated output by combining its `script` command with small Python scripts. This example shows how to produce [Mermaid](https://mermaid-js.github.io/mermaid/#/entityRelationshipDiagram), [DBML for dbdiagram.io](https://dbdiagram.io/home), and [PlantUML](http://www.plantuml.com/plantuml/umla) entity-relationship diagrams.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.md).

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).


### Mermaid ER Diagram

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command script \
    --script mermaid.py \
    --output-file share/output.mmd
  ```

The output file `output.mmd` will appear in your working directory on the host. Paste its contents into the [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor) to view the diagram.


### DBML for dbdiagram.io

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command script \
    --script dbml.py \
    --output-file share/output.dbml
```

The output file `output.dbml` will appear in your working directory on the host. Paste its contents into [dbdiagram.io](https://dbdiagram.io/d) to view and share the diagram.


### PlantUML ER Diagram

  ```sh
  schemacrawler \
    --server postgresql \
    --host postgresql \
    --database schemacrawler \
    --user schemacrawler \
    --password schemacrawler \
    --info-level standard \
    --command script \
    --script plantuml.py \
    --output-file share/output.puml
```

The output file `output.puml` will appear in your working directory on the host. Paste its contents into the [PlantUML online server](http://www.plantuml.com/plantuml/umla) to render the diagram.

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.md).


## Resource Files

The script command passes SchemaCrawler's in-memory catalog model to a Python script. The Python script then walks the catalog's tables and relationships and emits the diagram source text to stdout.

### Python Scripts

The three Python scripts (`mermaid.py`, `dbml.py`, `plantuml.py`) each receive the SchemaCrawler catalog as a scripting context and emit diagram source in their respective formats:

| Script | Output format | View at |
|---|---|---|
| `mermaid.py` | Mermaid `erDiagram` syntax | [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor) |
| `dbml.py` | DBML (Database Markup Language) | [dbdiagram.io](https://dbdiagram.io/d) |
| `plantuml.py` | PlantUML `@startuml` entity diagram | [PlantUML server](http://www.plantuml.com/plantuml/umla) |

Each script iterates over the filtered tables (`AUTHORS` and `BOOKS` in the `PUBLIC.BOOKS` schema) and their foreign-key relationships, then serialises them in the target notation.

> Place each script file in your working directory. It will be accessible inside the container as `share/mermaid.py`, `share/dbml.py`, or `share/plantuml.py`.

## How to Experiment

1. Modify the `--schemas` and `--tables` filter options in the run command to include more (or fewer) tables in the diagram.
2. Edit the Python scripts to customise the diagram output — for example, adding column data types to the Mermaid diagram or changing the DBML colour theme.
3. Add a new Python script to emit a different diagram format (e.g., [Graphviz DOT](https://graphviz.org/), [Nomnoml](https://nomnoml.com/)) and run it the same way: `schemacrawler <connection-options> ... --script share/myformat.py > share/output.txt`.
