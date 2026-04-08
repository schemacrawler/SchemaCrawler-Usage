# SchemaCrawler Website Deployment

This document describes how to set up and deploy the SchemaCrawler website at
[https://www.schemacrawler.com/](https://www.schemacrawler.com/).

---

## Overview

The website is built as a Maven project at the root of this repository. The build:

1. Stages website markdown sources and static resources.
2. Runs JUnit tests that generate diagrams and HTML variations (requires Graphviz).
3. Converts all Markdown files to HTML using a templated header and footer.
4. Produces the finished website in `target/_website/`.

The `publish-website.yml` GitHub Actions workflow builds the website and deploys it to
GitHub Pages on every version tag push (`v*`) or manual trigger.

---

## One-Time GitHub Repository Setup

### 1. Enable GitHub Pages

1. Go to the repository **Settings → Pages**.
2. Under **Build and deployment**, set the source to **GitHub Actions**.
3. Do **not** select a branch — the deployment is driven entirely by the workflow.

### 2. Configure the Custom Domain

1. In **Settings → Pages → Custom domain**, enter `www.schemacrawler.com` and click **Save**.
2. Confirm that `src/site/resources/CNAME` contains exactly:
   ```
   www.schemacrawler.com
   ```
   This file is copied into the website output so GitHub Pages enforces the custom domain.
3. Enable **Enforce HTTPS** once the domain is verified.

### 3. DNS Configuration

At your DNS provider, add the following records to point `www.schemacrawler.com` at GitHub Pages:

| Type  | Host  | Value                    |
|-------|-------|--------------------------|
| CNAME | `www` | `schemacrawler.github.io` |

For the apex domain (`schemacrawler.com`), add `A` records pointing to GitHub Pages IP addresses:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

DNS changes may take up to 24 hours to propagate. GitHub will verify the domain automatically.

---

## Required Repository Permissions

The `publish-website.yml` workflow requires the following permissions, which are already set in
the workflow file:

| Permission     | Level  | Purpose                                    |
|----------------|--------|--------------------------------------------|
| `contents`     | `read` | Check out the repository                   |
| `pages`        | `write`| Upload pages artifact and create deployment|
| `id-token`     | `write`| OIDC authentication for Pages deployment   |

No additional GitHub secrets are needed for website deployment.

---

## Required GitHub Secrets (for dependency builds)

The website build depends on artifacts from sibling repositories built using
`sualeh/build-maven-dependency`. That action uses the `GITHUB_TOKEN` automatically provided
by Actions — no extra secrets are required.

---

## Build Dependency Order

The website JUnit tests require SchemaCrawler artifacts to be available in the local Maven
repository. The workflow builds them in this order before building the website:

1. **SchemaCrawler-Core** — `us.fatehi:schemacrawler:17.10.0`
   Repository: `schemacrawler/SchemaCrawler-Core`
2. **SchemaCrawler** — `us.fatehi:schemacrawler-commandline:17.10.0`
   Repository: `schemacrawler/SchemaCrawler`
3. **SchemaCrawler-Database-Plugins** — `us.fatehi:schemacrawler-trino:17.10.0`
   Repository: `schemacrawler/SchemaCrawler-Database-Plugins`
4. **SchemaCrawler-Usage** (this repository) — builds the website

---

## Triggering a Deployment

The single `publish-website.yml` workflow runs in two modes:

### CI (every push and pull request)
Every push to any branch and every PR targeting `main` runs the full build and tests, but
does **not** deploy to GitHub Pages.

### Deploy (on version tag or manual)
Push a Git tag matching `v*` (e.g., `v17.10.0`) to trigger a full build **and** deploy:
```bash
git tag v17.10.0
git push --follow-tags origin v17.10.0
```

Or go to **Actions → Build and Publish Website → Run workflow** and click **Run workflow**
to manually trigger a deploy from any branch.

---

## Local Build

To build the website locally (requires Java 17, Maven, and Graphviz):

```bash
# Build SchemaCrawler dependencies into local Maven repo first (one-time):
# (or install from Maven Central if the version is released)

# Then build the website:
mvn clean test

# The website output is in:
#   target/_website/
```

Open `target/_website/index.html` in a browser to preview the site.

---

## Website Structure

| Path | Purpose |
|------|---------|
| `src/site/markdown/` | Markdown source for all website pages |
| `src/site/markdown/examples/` | Example documentation pages |
| `src/site/resources/` | Static assets: CSS, images, `CNAME`, `.nojekyll` |
| `src/site/header.include` | HTML header template (nav, Bootstrap, SEO) |
| `src/site/footer.include` | HTML footer template (analytics, copyright) |
| `src/assembly/website.xml` | Ant script that stages markdown and resources |
| `src/main/java/` | Example Java code (API usage examples) |
| `src/main/resources/config/` | SchemaCrawler config files staged into the website |
| `src/test/java/` | JUnit tests that generate website images/diagrams and validate examples |
| `target/_website/` | Built website output (uploaded to GitHub Pages) |
