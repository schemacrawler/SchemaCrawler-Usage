# How to Get Database Metadata as Java POJOs

The Java Database Connectivity (JDBC) API enables access to data and metadata from standard relational database systems (RDBMS). However, an intrinsic mismatch exists between the object model of the application domain and the relational model of the database. The JDBC API's various statement classes, which enable execution of SQL statements, reflect the relational model of the database and its result set classes bring back tabular data. In addition, JDBC requires programmers to manage external resources, such as database connections, and handle exceptions.

Since the JDBC API so closely mimics the relational model, an ["impedance mismatch"](http://www.agiledata.org/essays/impedanceMismatch.html) occurs when programmers use it. Embedded SQL statements, try-catch-finally blocks, and mapping from tabular result sets into plain old Java objects (POJOs) all reflect this. However, excellent frameworks such as Hibernate largely hide the impedance mismatch from most application programmers.

Sometimes, however, programmers need to access database metadata in order to dynamically generate SQL statements when programmatically determining the capabilities of a given RDBMS or finding the names and types of tables and columns in the database. Since obtaining database metadata is not very common in applications, there are no good frameworks or APIs to obtain it, as there are for obtaining the data itself.
Sometimes, however, programmers need to access database metadata in order to dynamically generate SQL statements when programmatically determining the capabilities of a given RDBMS or finding the names and types of tables and columns in the database. Since obtaining database metadata is not very common in applications, there are no good frameworks or APIs to obtain it, as there are for obtaining the data itself.

Programmers can obtain database metadata using JDBC, but with the hammer of the raw JDBC API, everything looks like a nail—even database metadata. Programmers are still responsible for managing resources, mapping into object structures, and handling exceptions. The following section explains in more detail JDBC's shortcomings for database metadata retrieval.

# Drawbacks of JDBC for Obtaining Database Metadata

Obtaining database metadata via raw JDBC presents several issues. You first obtain database metadata from JDBC using static calls that return result sets with cryptic column names. For example, say you wanted to obtain a list of tables from the database. You would need to call `java.sql.DatabaseMetaData.getTables(String, String, String, String[])`, which would return a result set with the following columns:

- `TABLE_CAT`
- `TABLE_SCHEM`
- `TABLE_NAME`
- `TABLE_TYPE`
- `REMARKS`
- `TYPE_CAT`
- `TYPE_SCHEM`
- `TYPE_NAME`
- `SELF_REFERENCING_COL_NAME`
- `REF_GENERATION`

You would have to read through the Javadocs, find which call returns the information that you need, and then find out how to interpret the information that is returned — quite a task. You also would need to verify that the `getTables` call would not return any column information, and determine how to interpret the data columns: is `TABLE_TYPE` a string, an integer, or something else? What does it mean if the value is null? In addition, you would handle exceptions and manage resources, making sure you released the result set resources when you were done reviewing the results and closing the connection when appropriate.

Now, if you wanted more information about a table, such as the names and types of the columns, the primary key, indexes, grants and triggers, you would have to go through a series of equally cryptic calls until you finally drilled down into the data you'd been seeking.

You might assume that once you got used to programming with the JDBC API, you could churn out code very fast. That would be true if the API was consistent. For example, if you wanted to find the type of a table, you would look at the `TABLE_TYPE`, which would have a string value. Your next thought would be that you should look at `PROCEDURE_TYPE` to find procedures. Good guess, but what you get back is an integer, not a string. Next, for the column type, you would look for `COLUMN_TYPE`, right? No, because it doesn't exist. So maybe you could use `SQL_DATA_TYPE`, but this field, though it is returned, is unused for reasons known only to the API designers. Finally, you settle on `DATA_TYPE`, which is an integer that needs to be interpreted.

As another example, say you want to find all the catalogs in a database. So you call `getCatalogs()`, and it returns a result set with exactly one column. So far, so good. Now, if you wanted a list of string functions in the database, you would be tempted to call `getStringFunctions()` and then process the returned result set, right? Well, you get back the list of functions, separated by commas, as a single string. So much for consistency. The JDBC API has the idiosyncrasies of something that has been worked on by several people.

# Enter [SchemaCrawler](https://www.schemacrawler.com/)

The JDBC API is powerful, but using it is daunting, especially for novice programmers. It does not have to be this way. Wouldn't it be nice to have an API that delivered all the following:

- Table is an object that has a collection of Column objects, without requiring you to make additional calls.
- You could use a method like `getType()`, whether on a Column object, a Table object, or a Procedure object.
- Table types are enumerations instead of strings that leave you guessing.
- Lists are always `java.util.List`.
- You have the same convenience that you get with object-relational mapping tools, where you don't worry about resources or exception handling.
- You could navigate using standard Java methods from one Column object to its containing Table object, or from one Table object to another via a ForeignKey.

[SchemaCrawler](https://www.schemacrawler.com/) is just such an API. A free and open-source API available under the LGPL license, SchemaCrawler is written in Java, making it operating system agnostic. Since it leverages JDBC, it is also database independent. It deliberately doesn't have any RDBMS-specific code. That is the reason you won't find any triggers in it; there is no way to get trigger metadata using JDBC.

# SchemaCrawler in Action

Take a look at some sample code that demonstrates just how easy it is to use SchemaCrawler. This code assumes that you have a `javax.sql.DataSource` that is capable of handing out database connections on demand. Getting the database schema is a matter of one single call:

```java
final SchemaCrawlerOptions options = SchemaCrawlerOptionsBuilder.builder().toOptions();
final Catalog catalog = SchemaCrawlerUtility.getCatalog(getConnection(), options);
```

It is as simple as that. You get to decide how detailed you want the returned schema to be—with the basic schema information level, you get columns and tables but not indexes, for example. The schema information level determines how much time the getSchema call takes. You can filter out certain tables and columns with regular expressions that are more powerful than SQL regular expressions by setting the right `SchemaCrawlerOptions`. You can exclude tables of certain types, such as views, from the output schema.

Once you have the `Catalog` object, you can iterate through the schema and find all the tables and columns using standard Java idioms:

```java
for (final Schema schema : catalog.getSchemas())
{
  for (final Table table : catalog.getTables(schema))
  {
    System.out.print("o--> " + table);
    for (final Column column : table.getColumns())
    {
      System.out.println("     o--> " + column);
    }
  }
}
```

# Extend the API

If the simple code in the previous example is not sufficient for your needs, the SchemaCrawler API provides some well-defined extension points. 

Now, with all of that, go experiment!

