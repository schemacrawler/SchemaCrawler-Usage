/*
 * SchemaCrawler
 * http://www.schemacrawler.com
 * Copyright (c) 2000-2026, Sualeh Fatehi <sualeh@hotmail.com>.
 * All rights reserved.
 * SPDX-License-Identifier: EPL-2.0
 */

package com.example;

import static schemacrawler.filter.CatalogSearcher.search;
import static schemacrawler.filter.NamedObjectFilters.nameRegex;
import static schemacrawler.filter.NamedObjectFilters.tableTypes;

import java.util.Collection;
import java.util.logging.Level;
import schemacrawler.filter.NamedObjectFilter;
import schemacrawler.schema.Catalog;
import schemacrawler.schema.Column;
import schemacrawler.schema.SimpleTableType;
import schemacrawler.schema.Table;
import schemacrawler.schemacrawler.LimitOptionsBuilder;
import schemacrawler.schemacrawler.LoadOptionsBuilder;
import schemacrawler.schemacrawler.SchemaCrawlerOptions;
import schemacrawler.schemacrawler.SchemaCrawlerOptionsBuilder;
import schemacrawler.schemacrawler.SchemaInfoLevelBuilder;
import schemacrawler.tools.utility.SchemaCrawlerUtility;
import us.fatehi.utility.datasource.DatabaseConnectionSource;
import us.fatehi.utility.datasource.DatabaseConnectionSources;
import us.fatehi.utility.datasource.MultiUseUserCredentials;
import us.fatehi.utility.logging.LoggingConfig;

/**
 * Demonstrates how to use {@link schemacrawler.filter.CatalogSearcher} to find named objects (for
 * example, tables or columns) in an already-loaded {@link Catalog}, instead of writing custom code
 * to loop over and filter the catalog's collections by hand.
 *
 * <p>{@code CatalogSearcher} is a thin, read-only wrapper around a catalog. It does not go back to
 * the database, and it never changes what {@link Catalog#getTables()} (or the other {@code
 * getXxx()} methods) return - it simply applies one or more {@link NamedObjectFilter}s to the
 * catalog's existing, in-memory contents, and returns matches as a new, independent collection.
 * This makes it well-suited to code that needs to select a subset of an already-crawled catalog -
 * for example, "only the tables whose name matches this pattern" or "only columns of a particular
 * name, across every table" - without re-crawling the database, and without repeating the
 * inclusion/exclusion logic that may have already been used (or deliberately not used) at crawl
 * time.
 *
 * <p>Use {@code CatalogSearcher} instead of {@code SchemaCrawlerOptions} inclusion rules when: the
 * catalog has already been crawled (and possibly needs to be searched more than once, in different
 * ways, without re-crawling); the search criteria is only relevant to how a single report or tool
 * presents its output, not to what should be loaded into memory in the first place; or several
 * independent searches need to share the same, already-loaded catalog.
 */
public final class CatalogSearcherExample {

  public static void main(final String[] args) throws Exception {

    // Set log level
    new LoggingConfig(Level.OFF);

    // Create the options - crawl every table, since filtering is done afterwards, with
    // CatalogSearcher, rather than at crawl time with inclusion rules
    final LimitOptionsBuilder limitOptionsBuilder =
        LimitOptionsBuilder.builder().includeAllTables();
    final LoadOptionsBuilder loadOptionsBuilder =
        LoadOptionsBuilder.builder()
            // Set what details are required in the schema - this affects the
            // time taken to crawl the schema
            .withSchemaInfoLevel(SchemaInfoLevelBuilder.standard());
    final SchemaCrawlerOptions options =
        SchemaCrawlerOptionsBuilder.newSchemaCrawlerOptions()
            .withLimitOptions(limitOptionsBuilder.toOptions())
            .withLoadOptions(loadOptionsBuilder.toOptions());

    // Get the schema definition
    final DatabaseConnectionSource dataSource = getDataSource();
    final Catalog catalog = SchemaCrawlerUtility.getCatalog(dataSource, options);

    // Find tables using a compound filter - see findForeignKeyTables() below - rather than
    // looping over catalog.getTables() and checking each table by hand
    for (final Table table : findForeignKeyTables(catalog)) {
      System.out.println("o--> " + table);
      for (final Column column : table.getColumns()) {
        System.out.println("     o--> " + column);
      }
    }
  }

  /**
   * Finds ordinary (non-view) tables whose name ends in "_FK" - that is, tables that are named to
   * indicate they contain foreign keys - by combining two independent, reusable {@link
   * NamedObjectFilter}s into one compound filter.
   *
   * <p>Since {@link NamedObjectFilter} extends {@link java.util.function.Predicate}, individual
   * filters can be combined using the standard predicate combinators - {@code and}, {@code or}, and
   * {@code negate} - rather than SchemaCrawler needing its own, parallel set of combinator methods.
   * This keeps {@link schemacrawler.filter.NamedObjectFilters} itself small: it only needs to
   * supply individual, named building blocks (by table type, by regular expression, by inclusion
   * rule, and so on), and any Boolean combination of them can then be expressed with plain Java, as
   * shown here.
   *
   * @param catalog the already-loaded catalog to search; not modified by this method
   * @return tables of type "table" whose name ends in "_FK", in catalog order; never null, but
   *     empty if nothing matches
   */
  private static Collection<Table> findForeignKeyTables(final Catalog catalog) {
    // A compound filter, built by combining two independent filters with `and()`. Each half is
    // still a plain, reusable filter on its own - `tableTypes("table")` could equally be used by
    // itself, or combined differently, for example with `or()` or `negate()`.
    //
    // `Predicate.and()` returns a `Predicate<Table>`, not a `NamedObjectFilter<Table>`, so the
    // result is adapted back to `NamedObjectFilter<Table>` with a method reference - `::test` -
    // rather than needing a new, parallel "compound filter" type. `NamedObjectFilter` is a
    // functional interface with the same single abstract method as `Predicate` (`test`), so this
    // adaptation is just a matter of matching method signatures, not a change in behavior.
    final NamedObjectFilter<Table> foreignKeyTables =
        tableTypes(SimpleTableType.table).and(nameRegex(".*_FK"))::test;

    return search(catalog).findTables(foreignKeyTables);
  }

  private static DatabaseConnectionSource getDataSource() {
    final String connectionUrl = "jdbc:sqlite::resource:test.db";
    return DatabaseConnectionSources.newDatabaseConnectionSource(
        connectionUrl, new MultiUseUserCredentials("", ""));
  }
}
