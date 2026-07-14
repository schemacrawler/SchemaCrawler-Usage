# SchemaCrawler Scribe

SchemaCrawler Scribe helps you turn database structure into documentation that is easy to read and easy to share.

SchemaCrawler Scribe generates documentation in [Google OKF format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md), so your schema knowledge lives in plain text files rather than in a locked-in format.

Google OKF is lightweight and portable. It uses Markdown with YAML front matter, so people can read it in tools they already use, such as Visual Studio Code, while AI systems can still parse it cleanly. That makes it a good fit for teams that want documentation that is both human-friendly and machine-friendly.

SchemaCrawler Scribe is useful when you want database documentation that stays close to the data model. Instead of maintaining separate documentation by hand, you can generate a structured documentation tree that reflects tables, relationships, and other database concepts in a format that is simple to browse and update.

Because the output is plain text, you can store it in Git, review changes in pull requests, and keep it under version control like any other project asset.

## Benefits

- Allow AI agents to advise you on SQL and database information
- Generate documentation directly from schema metadata
- Keep documentation versioned with source code
- Produce human-readable and machine-parseable artifacts
- Use generated documentation in Visual Studio Code or other Markdown-based tooling

## Also See

- [SchemaCrawler AI MCP Server](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage)
