# Use ChatGPT to Explore Your Database Schema

> **Deprecated:** The `aichat` command was removed from SchemaCrawler. The instructions below are historical and are not supported by current releases.

SchemaCrawler is a relational database exploration tool. It obtains database schema metadata such as tables, stored procedures, foreign keys, triggers and so on, and makes them available for search. The traditional way to use SchemaCrawler has been the command-line or an interactive shell. 

ChatGPT offers almost magical help with coding questions. You could use it to get help with SQL questions, but then you have to adapt that SQL to match your database tables and schemas.

What if ChatGPT could act as an expert on your database, and give you valid SQL that would work for you? Guess what - with a little help from SchemaCrawler, it can. You can use SchemaCrawler to "teach" ChatGPT what your database schema looks like.

SchemaCrawler is now integrated with ChatGPT models to provide an interactive way to interrogate your database schema metadata. When you start SchemaCrawler with the "aichat" command, you will have an interactive chat shell with ChatGPT, enhanced with information about your database metadata. 

You can try prompts such as the following ones:

- "List all schemas"
- "List all tables"
- "Describe the Track table"
- "Show me all the details of a table whose name is something like 'tra'"
- "What are the indexes on the Track table?"
- "What are the Track columns?"
- "What is the Track primary key?"
- "Show me the triggers on Track"
- "Find the parents of Track"
- "What are the dependents of Album?"

To quit the console, you can type something like:

- "I think I have everything I need"
or simply, "done", "exit" or "quit".

To start using this integration, you will need to create your own [OpenAI API key](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/). Then download a SQLite database called ["chinook-database-2.0.1.sqlite"](https://github.com/schemacrawler/chinook-database/releases/download/v16.11.7/chinook-database-2.0.1.sqlite) into your current directory.

Run this command in a bash shell:

```sh
docker run \
  --mount type=bind,source="${PWD}",target=/home/schcrwlr \
  --rm -it \
-e OPENAI_API_KEY=<<your-openai-api-key>> \
schemacrawler/schemacrawler:extra-latest \
/opt/schemacrawler/bin/schemacrawler.sh \
--server=sqlite \
--database=chinook-database-2.0.1.sqlite \
--info-level=standard \
--command=aichat
```

(If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick, and map the current directory differently.)

Once the Docker container starts up, enter some of the prompts above.

If you are willing to share your database metadata with OpenAI, the creators of ChatGPT, you can provide an additional `--use-metadata true` on the commandline, and then you can get SQL statements customized to your database.

You can then try prompts such as the following ones:

- "Get me the SQL statement to find all the tracks and their artists' names"
- "Get me the SQL statement to find the number of tracks for each artist, for artists that have more than 25 tracks, sorted by those who have the most"
- "What is the purpose or function of this database?"

After you have got this working, use the SchemaCrawler command-line to connect to your own database, and explore it using a natural language interface courtesy of ChatGPT.
