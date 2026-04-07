# Implicit Associations Example

SchemaCrawler allows you to define *implicit associations* — foreign key relationships between columns in different tables that are not enforced at the database level. These are logical relationships that exist in your data model but have not been declared as formal foreign key constraints in the database schema. By loading them from a YAML file using the `--attributes-file` switch, SchemaCrawler can include them in diagrams and schema output as if they were real foreign keys.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started.md).

1. Create a file called "implicit-associations.yaml" with the contents shown below.
2. Run the command:

```sh
schemacrawler \
  --server postgresql \
  --host postgresql \
  --database schemacrawler \
  --user schemacrawler \
  --password schemacrawler \
  --info-level standard \
  --command schema \
  --attributes-file share/implicit-associations.yaml \
  --output-file share/implicit-associations.png
```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started.md).

Open `implicit-associations.png` to view the schema diagram. The implicit associations defined in the YAML file will appear as relationships in the diagram, alongside any real foreign keys in the database.

## Resource Files

### `implicit-associations.yaml`

```yaml
name: catalog
implicit-associations:
- name: ref_1
  referenced-table:
    catalog: null
    schema: books
    name: authors
  referencing-table:
    catalog: null
    schema: books
    name: books
  column-references:
    id: id
  remarks:
  - "Inserted reference ref_1"
  - "(This is not a real foreign key)"
- name: ref_2
  referenced-table:
    catalog: null
    schema: books
    name: person
  referencing-table:
    catalog: private
    schema: company
    name: employees
  column-references:
    name: name
  remarks:
  - "Inserted reference ref_2"
  - "(Referenced table does not exist)"
```

> Place this file in your working directory. It will be accessible inside the container as `share/implicit-associations.yaml`.

(Modify this overrides file appropriately for the other databases.)


## How to Experiment

- Modify `implicit-associations.yaml` to add or remove associations between tables and rerun the command to see the diagram update.
- Add `remarks` to each association entry to document why the relationship exists.
- Use multiple `column-references` entries to define composite implicit foreign keys, as shown in the `multi_remarks_reference` example above.
