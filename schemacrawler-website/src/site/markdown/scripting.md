# SchemaCrawler Database Scripting

SchemaCrawler is a command-line tool that allows you to script against your
database, using JavaScript or [Python](https://www.python.org/).
(SchemaCrawler supports any scripting language supported on the JDK.) Database
meta-data is provided to your script, as the "database" object, and you can
use any of the API methods to obtain details about your schema. A live
database connection is provided to your script as the "connection" object. You
can use standard JDBC to script against the database.

For hands-on examples, see:
- [JavaScript Scripting](examples/javascript.html)
- [Python Scripting](examples/python.html)
- [Apache Velocity Templating](examples/velocity.html)
- [Mustache Templating](examples/mustache.html)
- [Thymeleaf Templating](examples/thymeleaf.html)

An hypothetical example of SchemaCrawler JavaScript support is in the
following script, which attempts to drop all the tables in the database.

```javascript
var dropTables = function()
{
  println(catalog.schemaCrawlerInfo);
  println(catalog.databaseInfo);
  println(catalog.jdbcDriverInfo);
  var statement = connection.createStatement();
  var tables = catalog.tables.toArray();
  for ( var i = (tables.length - 1); i &gt;= 0; i--)
  {
    var table = tables[i];
    var sql = &quot;DROP &quot; + table.type + &quot; &quot; + table.fullName;
    println(&quot;Executing SQL: &quot; + sql);
    try
    {
      statement.executeUpdate(sql);
    } catch (e)
    {
      println(&quot;&quot;);
      println(e.message);
      println(&quot;(Not dropping any more tables, due to exception)&quot;);
      return;
    }
  }
};

dropTables();      
```

**Security Note:** SchemaCrawler's scripting and templating functionality allows arbitrary script execution. Do not distribute the `schemacrawler-scripting` jar in production or include this dependency unless explicitly needed.
