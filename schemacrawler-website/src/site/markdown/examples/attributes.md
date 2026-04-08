# Attributes Example

SchemaCrawler allows you to enrich your schema with remarks and custom metadata by loading table and column attributes from a YAML file. This is useful when the database itself does not store remarks, or when you want to annotate the schema externally without modifying the database.

## How to Run

Before running this example, complete the setup in [Getting Started](getting-started-examples.html).

1. Create a file called "attributes.yaml" with the contents shown below.
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
    --attributes-file share/attributes.yaml
  ```

> Replace with the connection options for your chosen database. See [Getting Started](getting-started-examples.html).

SchemaCrawler will load the schema and overlay the remarks and attributes defined in `attributes.yaml` onto the output.

To save output to a file, an additional `--output-file share/output.txt`.


## Resource Files

### `attributes.yaml`

```yaml
name: catalog
tables:
- catalog: null
  schema: books
  name: authors
  remarks:
  - "Overwritten remarks authors table"
  columns:
  - name: firstname
    remarks:
    - Overwritten remarks for firstname at line 1
    - Overwritten remarks firstname at line 2
    attributes:
      tag1: tagvalue1
  - name: lastname
    remarks:
    - Overwritten remarks for lastname
```

> Place this file in your working directory. It will be accessible inside the container as `share/attributes.yaml`.

(Modify this overrides file appropriately for the other databases.)


## How to Experiment

- Add remarks to more tables and columns in `attributes.yaml` and rerun the command to see them appear in the schema output.
- Add custom key-value `attributes` to any table or column — these are passed through as metadata in the schema output.
- Look at the `implicit-associations` example to see how you can define foreign key relationships that are not enforced at the database level.
