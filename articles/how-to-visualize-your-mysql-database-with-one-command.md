# How to Visualize Your MySql Database with One Command (and Nothing to Install)

Ever wondered what the tables in your MySql database look like, and how they are related to each other? Generate a diagram of your MySql database with one command. You can run this on any system that has Docker installed. 

On a Linux system, run a command like:

```sh
docker run \
--mount type=bind,source="$(pwd)",target=/home/schcrwlr \
--rm -it \
schemacrawler/schemacrawler \
/opt/schemacrawler/schemacrawler.sh \
--server mysql \
--host mysql-rfam-public.ebi.ac.uk \
--port 4497 \
--user rfamro \
--password= \
--database Rfam \
--info-level standard \
--command schema \
--output-file rfam.pdf
```

The command will generate an entity and relationship diagram of the [the Rfam database of the European Bioinformatics Institute](https://docs.rfam.org/en/latest/about-rfam.html). A file called "rfam.pdf" will be generated with the database schema, including foreign key relationships. 

If you are using PowerShell on Windows, replace the trailing backslash on each line with a back-tick, and map the current directory differently. Run this command:

```powershell
docker run `
--mount type=bind,source="${PWD}",target=/home/schcrwlr `
--rm -it `
schemacrawler/schemacrawler `
/opt/schemacrawler/schemacrawler.sh `
--server mysql `
--host mysql-rfam-public.ebi.ac.uk `
--port 4497 `
--user rfamro `
--password= `
--database Rfam `
--info-level standard `
--command schema `
--output-file rfam.pdf
```

You can generate PDF files, and other types of output too. Go through the [SchemaCrawler tutorials](https://killercoda.com/schemacrawler) to learn more SchemaCrawler commands. 
