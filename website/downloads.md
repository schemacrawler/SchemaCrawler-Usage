# SchemaCrawler Downloads

[![The Central Repository](https://img.shields.io/maven-central/v/us.fatehi/schemacrawler.svg)](https://central.sonatype.com/search?q=us.fatehi.schemacrawler&sort=name)
[![Main distribution](https://img.shields.io/github/downloads/schemacrawler/schemacrawler/total)](https://github.com/schemacrawler/SchemaCrawler-Installers/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/schemacrawler/schemacrawler.svg)](https://hub.docker.com/r/schemacrawler/schemacrawler/)


## Distributions and Downloads

SchemaCrawler is distributed in a variety of ways, to support various use cases.

If you would like to use SchemaCrawler without installing it, you can explore the SchemaCrawler command-line with a [live online tutorial](https://killercoda.com/schemacrawler). The tutorial works from within any browser with no software or plugins needed.

If you need to use SchemaCrawler locally, you have a number of options. You can install the SchemaCrawler Interactive Shell using platform-specific installers downloaded from [schemacrawler/SchemaCrawler-Installers](https://github.com/schemacrawler/SchemaCrawler-Installers). On Windows, SchemaCrawler is available via [Scoop](https://scoop.sh/), [Chocolatey](https://community.chocolatey.org/packages/schemacrawler), and [winget](https://docs.microsoft.com/en-us/windows/package-manager/). On macOS, SchemaCrawler is available via [Homebrew](https://brew.sh/). On Linux and macOS, SchemaCrawler is available via [SDKMan](https://sdkman.io/sdks#schemacrawler). Across all platforms, SchemaCrawler is available via [Docker](https://hub.docker.com/r/schemacrawler/schemacrawler/).

If you want to use SchemaCrawler as a library, and in your build, all jars are in the [Central Repository](https://central.sonatype.com/search?q=us.fatehi.schemacrawler&sort=name). They can be used as dependencies in [Gradle](https://gradle.org/) or [Apache Maven](https://maven.apache.org/) projects, or with any other build system that supports the Central Repository. SchemaCrawler reports can be incorporated into Apache Maven builds with the [SchemaCrawler Report Maven Plugin](https://github.com/schemacrawler/SchemaCrawler-Report-Maven-Plugin) and into the GitHub Actions workflow with the [SchemaCrawler Action](https://github.com/schemacrawler/SchemaCrawler-Action) or in [GitLab pipelines](https://gitlab.com/sualeh/schemacrawler-action-usage-example/-/pipelines). If you would like to extend SchemaCrawler with plugins for a certain database, create new database lints, or create a new command, use the [starter projects to create new SchemaCrawler plugins](https://github.com/schemacrawler/SchemaCrawler-Plugins-Starter) on GitHub.

[Pre-packaged SchemaCrawler Docker images](https://hub.docker.com/r/schemacrawler/) are available on Docker Hub. Refer to [schemacrawler/SchemaCrawler-AI-MCP-Server-Usage](https://github.com/schemacrawler/SchemaCrawler-AI-MCP-Server-Usage) for SchemaCrawler AI images. See the [Docker](#docker) section below for installation steps.

Additional SchemaCrawler database plugins are available from the [schemacrawler/SchemaCrawler-Database-Plugins](https://github.com/schemacrawler/SchemaCrawler-Database-Plugins) project.


## Installation on Windows

### Scoop

[![Scoop](https://img.shields.io/scoop/v/schemacrawler.svg)](https://github.com/ScoopInstaller/Main/blob/master/bucket/schemacrawler.json)

You can install SchemaCrawler on Windows using the [Scoop command-line installer](https://scoop.sh/). Follow these steps:

1. Install the [Scoop command-line installer](https://scoop.sh/)
2. Run  
   `scoop install schemacrawler`  
   from a PowerShell command-prompt
3. Run SchemaCrawler with `schemacrawler`

### Chocolatey

[![Chocolatey](https://img.shields.io/chocolatey/v/schemacrawler.svg)](https://community.chocolatey.org/packages/schemacrawler)

You can install SchemaCrawler on Windows using Chocolatey. Follow these steps:

1. Install [Chocolatey](https://chocolatey.org/install)
2. Run  
   `choco install schemacrawler -y`  
   from a PowerShell command-prompt with administrative privileges
3. Run SchemaCrawler with `schemacrawler`

The [Chocolatey SchemaCrawler package](https://community.chocolatey.org/packages/schemacrawler) is maintained by [Adrien Sales](https://www.linkedin.com/in/adrien-sales).

### Winget

You can install SchemaCrawler on Windows using the [Windows Package Manager (winget)](https://docs.microsoft.com/en-us/windows/package-manager/). Follow these steps:

1. Run  
   `winget install SchemaCrawler.SchemaCrawler --accept-package-agreements --accept-source-agreements`  
   from a command-prompt
2. Run SchemaCrawler with `schemacrawler`


## Installation on macOS

### Homebrew

You can install SchemaCrawler on macOS using [Homebrew](https://brew.sh/). Follow these steps:

1. Install [Homebrew](https://brew.sh/)
2. Add the SchemaCrawler tap and install SchemaCrawler:  
   ```
   brew tap schemacrawler/homebrew-tap
   brew install --formula schemacrawler
   ```
3. Run SchemaCrawler with `schemacrawler`


## Installation on Linux and macOS

### SDKMan

You can install SchemaCrawler on Linux and macOS using [SDKMan](https://sdkman.io/). Follow these steps:

1. Install [SDKMan](https://sdkman.io/install)
2. Install a [Java runtime](https://www.oracle.com/java/technologies/downloads/) (or use SDKMan to install it)
3. Run  
   `sdk install schemacrawler`  
   from a command-prompt
4. Run SchemaCrawler with `schemacrawler.sh`


## Cross-platform Installation

### Docker

[Pre-packaged SchemaCrawler Docker images](https://hub.docker.com/r/schemacrawler/schemacrawler/) are available on Docker Hub. Follow these steps:

1. Pull the SchemaCrawler Docker image:  
   `docker pull schemacrawler/schemacrawler:latest`
2. Run SchemaCrawler:  
   ```
   docker run --rm \
     --name schemacrawler \
     --volume "$(pwd):/home/schcrwlr/share" \
     schemacrawler/schemacrawler:latest \
     /opt/schemacrawler/bin/schemacrawler.sh --version
   ```

See [Docker Image](docker-image.md) for full documentation on using SchemaCrawler with Docker.


## Examples

SchemaCrawler examples are available on this website. The examples cover the command-line, diagramming, scripting, templating, lint, serialization, and more. See the [SchemaCrawler Examples](examples/examples-index.md) index to get started.

