# Explore Your Database Schema with SchemaCrawler

How do you explore a new database? Chances are that you have started a new job, and are quickly trying to get up to speed on how the data is laid out. Or, you are a consultant, trying to look worth the money, and speak intelligently about a client’s schema design. Maybe you just returned from vacation, and want to see what changes other developers have made to the database.

SchemaCrawler allows you to get to the heart of what you need very quickly. Let us say that you know that there is a piece of the application that deals with customers. You would expect that there would be columns called "customer" or something like that. You can ask SchemaCrawler to connect to the database, and use a regular expression such as `.*CUSTOMER.*`, to find all tables that have a column with the word "customer" in it. Then, you can find related tables, based on foreign key relationships. Finally, you can graph the result in a database diagram. Using this technique, you will find that you are very quickly able to get schema information that you are interested in – usually in a matter of minutes. SchemaCrawler is unique in the features that it offers for this kind of drill-down.

In a large database, you can have hundreds of tables. Most people try to print out this entire schema in the form of a diagram, and paste it on a blank wall for reference. This is not a productive way of getting to information, particularly in the modern age where people are used to Google searches. SchemaCrawler is a sort of "Google search" for database metadata. Then, instead of having one giant diagram on the wall, you would have many smaller diagrams, created on demand, for the particular research task at hand.

Consider the case when you came back from vacation, and the developers had been very active. You would not be able to find any of the new tables and columns that they would have created on the diagram on your wall. However, if you had saved your SchemaCrawler command-line from before your vacation, all you would have to do would be to rerun SchemaCrawler, and you would get a brand new diagram. SchemaCrawler would have found and accounted for all of the new tables and columns that you were not going to know about.

Here are some concrete examples, using Microsoft's AdventureWorks database:
Search for tables that have a column called `VendorID` (use `--grep-columns=.*\.VendorID`)

```sh
schemacrawler --server=sqlserver --host=**** --database=AdventureWorks --schemas=AdventureWorks\..* --user=**** --password=**** --info-level=standard --table-types=TABLE --grep-columns=.*\.VendorID --command=schema
```

Then, to plot a database diagram of tables that have a column called `VendorID`, with related tables (use `--parents=1 --children=1`)

```sh
schemacrawler --server=sqlserver --host=**** --database=AdventureWorks --schemas=AdventureWorks\..* --user=**** --password=**** --info-level=standard --table-types=TABLE --grep-columns=.*\.VendorID --command=schema --parents=1 --children=1 --only-matching --output-format=pdf
```

(You can use [SchemaCrawler live tutorials](https://killercoda.com/schemacrawler) to see this in action.)

SchemaCrawler is intended to be a database schema exploration tool, serving many types of users.

For programmers, there is a rich Java API for metadata about database objects, and integration with Maven repositories. You can script with a number of scripting languages, such as JavaScript, Python, Ruby, Scala, Groovy and so on. For continuous builds, you can use SchemaCrawler with GitHub Actions or GitLab workflows, and there is ant and Maven build integration, along with reports for Maven-generated sites. Programmers can also build plugins for lint, and extend support for database specific metadata.

QA engineers can automate database tests by outputting expected results for metadata as well as data in SchemaCrawler's easy to diff format, and compare against their test runs. This technique can be used to compare schemas between development and production servers as well, and also help keep track of schema changes over time.

Database architects and DBAs can quickly explore the structure of a database, using powerful grep functionality based on regular expressions. Then, they can use the results of their search to create ERDs. SchemaCrawler's ERDs are very useful when schemas keep changing. You do not need to know what the changes are, but you can simply rerun the same SchemaCrawler command to find out. For example, if a team member added a new customer related column to a table when you were on vacation, you could add it to your database diagram simply by rerunning a SchemaCrawler command that searches for all tables with columns called `CUSTOMER_ID`. Of course, database architects would find the lint capability really useful to keep track of poor schema design practices, and even add some of their own custom linters.

Visit the [SchemaCrawler website](https://www.schemacrawler.com/) to learn more about SchemaCrawler. Use [SchemaCrawler live tutorials](https://killercoda.com/schemacrawler) to get a feel for what is possible.
