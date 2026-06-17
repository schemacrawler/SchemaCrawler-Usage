# Auto-commit Settings for Database Transactions

## Context and Problem Statement

Determine the most appropriate auto-commit settings for SchemaCrawler and manage database transactions. SchemaCrawler mostly needs read-only access to the database, but will need to commit occasionally — specifically when creating the test database, and when passing in a connection to the scripting context for running arbitrary user scripts. Some database plugins, such as the Oracle plugin, may also need to run SQL queries before the schema is crawled.


## Considered Options

1. The JDBC specification states that by default, a JDBC driver should create a new database connection with auto-commit set to true, giving implicit database transactions. However, to avoid the vagaries of JDBC drivers, it may be better to explicitly disable auto-commit and commit explicitly when needed.
2. Do not change the default auto-commit setting, but decide to commit after checking that auto-commit mode is off. This approach relies on the JDBC driver giving an accurate value for the auto-commit setting, and that the driver or database will not expect transactions to be managed by the client.


## Decision Outcome

In previous versions of SchemaCrawler, the test schema creator explicitly turned off auto-commit mode and explicitly committed each DDL or SQL statement. The test framework behaved in the same way, masking the behavior of the Oracle plugin which had to execute some SQL. From 16.16.9 onwards, SchemaCrawler does not explicitly set the auto-commit mode, either in the test schema creator or in the Oracle plugin. Commits are done where needed after checking if the auto-commit mode is off.
