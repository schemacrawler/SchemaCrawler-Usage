---
type: report
title: Database Schema Diagram
description: Diagram of the entire database schema
generated:
  at: 2026-09-21T02:04:08.061528054Z
  by: process:schemacrawler-v17.15.5
verified:
  at: 2026-09-21T02:04:08.998058569Z
  by: machine-confirmed:schemacrawler-v17.15.5
status: stable
shortTitle: Database Schema Diagram
intro: Diagram of the entire database schema
showMiniToc: false
allowTitleToDifferFromFilename: true
---

# Diagram


```mermaid
---
title: Database Schema
config:
  theme: base
---
erDiagram

  classDef strong_entity stroke:#283593;
  classDef subtype stroke:#1976D2;
  classDef weak_entity stroke:#1976D2;
  classDef unknown stroke:#AAAAAA;
  classDef non_entity stroke:#AAAAAA;

  "HumanResources.Employee":::subtype {
    string NationalIDNumber
    string LoginID
    string OrganizationNode
    integer OrganizationLevel
    string JobTitle
    date BirthDate
    string MaritalStatus
    string Gender
    date HireDate
    bool SalariedFlag
    integer VacationHours
    integer SickLeaveHours
    bool CurrentFlag
    other rowguid
    timestamp ModifiedDate
  }

  "Person.BusinessEntity":::strong_entity {
    other rowguid
    timestamp ModifiedDate
  }

  "Person.Person":::subtype {
    string PersonType
    string NameStyle
    string Title
    string FirstName
    string MiddleName
    string LastName
    string Suffix
    integer EmailPromotion
    other AdditionalContactInfo
    other Demographics
    other rowguid
    timestamp ModifiedDate
  }


  "HumanResources.Employee"  ||--||  "Person.Person" : "foreign key"
```
