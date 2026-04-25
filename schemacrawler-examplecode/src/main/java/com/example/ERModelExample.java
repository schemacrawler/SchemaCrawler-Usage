/*
 * SchemaCrawler
 * http://www.schemacrawler.com
 * Copyright (c) 2000-2026, Sualeh Fatehi <sualeh@hotmail.com>.
 * All rights reserved.
 * SPDX-License-Identifier: EPL-2.0
 */

package com.example;

import java.util.Collection;
import java.util.logging.Level;
import schemacrawler.ermodel.model.ERModel;
import schemacrawler.ermodel.model.Entity;
import schemacrawler.ermodel.model.EntityAttribute;
import schemacrawler.ermodel.model.Relationship;
import schemacrawler.schema.Catalog;
import schemacrawler.schemacrawler.LimitOptionsBuilder;
import schemacrawler.schemacrawler.LoadOptionsBuilder;
import schemacrawler.schemacrawler.SchemaCrawlerOptions;
import schemacrawler.schemacrawler.SchemaCrawlerOptionsBuilder;
import schemacrawler.schemacrawler.SchemaInfoLevelBuilder;
import schemacrawler.tools.utility.SchemaCrawlerUtility;
import us.fatehi.utility.LoggingConfig;
import us.fatehi.utility.datasource.DatabaseConnectionSource;
import us.fatehi.utility.datasource.DatabaseConnectionSources;
import us.fatehi.utility.datasource.MultiUseUserCredentials;

public final class ERModelExample {

  public static void main(final String[] args) throws Exception {

    // Set log level
    new LoggingConfig(Level.OFF);

    // Create the options
    final LimitOptionsBuilder limitOptionsBuilder =
        LimitOptionsBuilder.builder()
            .includeTables(tableFullName -> !tableFullName.contains("_PK"));
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
    final ERModel erModel = SchemaCrawlerUtility.buildERModel(catalog);

    for (final Entity entity : erModel.getEntities()) {
      System.out.printf("o--> %s (%s)%n", entity, entity.getType());
      final Collection<EntityAttribute> entityAttributes = entity.getEntityAttributes();
      for (final EntityAttribute entityAttribute : entityAttributes) {
        System.out.printf("       - %s (%s)%n", entityAttribute, entityAttribute.getType());
      }
      for (final Relationship relationship : entity.getRelationships()) {
        System.out.printf("     o--> %s (%s)%n", relationship, relationship.getType());
      }
    }
  }

  private static DatabaseConnectionSource getDataSource() {
    final String connectionUrl = "jdbc:sqlite::resource:test.db";
    return DatabaseConnectionSources.newDatabaseConnectionSource(
        connectionUrl, new MultiUseUserCredentials("", ""));
  }
}
