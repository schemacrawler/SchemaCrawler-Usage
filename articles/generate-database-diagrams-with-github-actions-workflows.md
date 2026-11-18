# Generate Database Diagrams With GitHub Actions Workflows

Your project is probably moving to a DevOps model, and you are starting to check in infrastructure as code into your source code control system. This probably includes your database schema creation and migration scripts. As your development team makes changes to the database schema, they would like to see what the latest database schema diagram looks like.

[SchemaCrawler](https://www.schemacrawler.com/) can generate database schema diagrams as PNG files that you can include with your documentation. The [SchemaCrawler Action](https://github.com/marketplace/actions/schemacrawler-action-for-github-actions) integrates SchemaCrawler with GitHub Actions workflows, so you can generate a diagram from your build pipeline.

It's easy. Take a look at the [example project](https://github.com/schemacrawler/SchemaCrawler-Action-Usage-Example), clone it, play with it. You will need to set up a directory called `.github/schemacrawler` in your project for additional Java jars and SchemaCrawler configuration. Then you can create a GitHub Action workflow and specify your SchemaCrawler command-line. You can put in secrets for your database username and password, and use those secrets with the SchemaCrawler Action. 

The database diagram is generated within the build pipeline, and you can find a way to copy it to a more useful place. The example project shows you how to make the diagram available as a build artifact in your GitHub repository. You may decide to check it into your Wiki, upload it to a website, or to do something else with the diagram. 

Once you set up your SchemaCrawler Action for GitHub Actions workflow, you will always have a database schema diagram based on the latest code check-in, and never have to wonder if it up to date.

However, before you try this out, I would strongly suggest that you get familiar with the SchemaCrawler command-line. The best way to do this is to go through the [SchemaCrawler tutorials](https://killercoda.com/schemacrawler). Once you have gone through this, you will find it much easier to determine your SchemaCrawler command-line arguments.
