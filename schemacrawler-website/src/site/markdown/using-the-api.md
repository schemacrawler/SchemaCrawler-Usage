# Using the SchemaCrawler API

## Overview

The SchemaCrawler API is a much simpler alternative to using JDBC metadata. The API example demonstrates the use of the SchemaCrawler API to create a data source, and obtain database metadata. 


## Example Code

- [An example of using the SchemaCrawler API to obtain database metadata in a plain Java
object model.](https://github.com/schemacrawler/SchemaCrawler-Usage/blob/main/schemacrawler-examplecode/src/main/java/com/example/ApiExample.java#L36-L52)
- [An example of using the SchemaCrawler API to generate a description of database metadata in an
HTML file.](https://github.com/schemacrawler/SchemaCrawler-Usage/blob/main/schemacrawler-examplecode/src/main/java/com/example/ExecutableExample.java#L37-L61)
- [An example of using the SchemaCrawler API to obtain result-set metadata.](https://github.com/schemacrawler/SchemaCrawler-Usage/blob/main/schemacrawler-examplecode/src/main/java/com/example/ResultSetExample.java#L40-L52)


### How to Experiment

1. Try uncommenting the code block in `com.example.ApiExample.java` that modifies the default options. 
2. Read the [SchemaCrawler javadoc](https://javadoc.io/doc/us.fatehi/schemacrawler/), and 
   edit `com.example.ApiExample.java` to print more details. 
3. Make changes to `com.example.ExecutableExample.java` to produce different types of output.
