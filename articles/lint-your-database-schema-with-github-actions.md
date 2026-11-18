# Lint Your Database Schema With GitHub Actions Workflows

Your project is probably moving to a DevOps model, and you are starting to check in infrastructure as code into your source code control system. This probably includes your database schema creation and migration scripts. As your development team makes changes to the database schema, wouldn't you like to flag schema design lints or non-adherence to both industry and project-specific standards and conventions?

A lot of database schema designers do not follow good design practices, simply because these are not documented well. Most programmers know about normalization, and take care to either normalize their tables, or deliberately denormalize them for performance reasons. However, what about "design smells", such as column names that are SQL reserved words, such as a column called `COUNT`? Or, foreign key and primary key columns that have different data types?

[SchemaCrawler](https://www.schemacrawler.com/) can lint your database schema. The [SchemaCrawler Action](https://github.com/marketplace/actions/schemacrawler-action-for-github-actions) integrates SchemaCrawler with GitHub Actions workflows, so you can generate a lint report for your database schema from your build pipeline.

It's easy. Take a look at the [example project](https://github.com/schemacrawler/SchemaCrawler-Action-Usage-Example), clone it, play with it. You will need to set up a directory called `.github/schemacrawler` in your project for additional Java jars and SchemaCrawler configuration. Then you can create a GitHub Action workflow and specify your SchemaCrawler command-line. You can put in secrets for your database username and password, and use those secrets with the SchemaCrawler Action. 

The database schema lint report is generated within the build pipeline, and you can find a way to copy it to a more useful place. The example project shows you how to make the diagram available as a build artifact in your GitHub repository. You may decide to use it to create a GitHub issue, post a Slack message, or to do something else with the report. If the lint report shows serious issues, you can fail your build pre-checks.

Once you set up your SchemaCrawler Action for GitHub Actions workflow, you will always have done a database schema lint based on the latest code check-in, and never have to worry about it again.

However, before you try this out, I would strongly suggest that you get familiar with the SchemaCrawler command-line. The best way to do this is to go through the [SchemaCrawler tutorials](https://killercoda.com/schemacrawler). Once you have gone through this, you will find it much easier to determine your SchemaCrawler command-line arguments.
