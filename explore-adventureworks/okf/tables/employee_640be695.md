---
type: table
title: '"HumanResources"."Employee"'
description: Description of table
resource: catalog://tables/%22HumanResources%22.%22Employee%22
tags:
  - table
  - subtype
generated:
  at: 2026-09-21T02:04:08.061528054Z
  by: process:schemacrawler-v17.15.5
verified:
  at: 2026-09-21T02:04:08.836800073Z
  by: machine-confirmed:schemacrawler-v17.15.5
status: stable
shortTitle: Employee
intro: Description of table "HumanResources"."Employee"
showMiniToc: true
allowTitleToDifferFromFilename: true
schema: '"HumanResources"'
name: Employee
complete_type: table
counts:
  attribute_column_count: 15
  column_count: 16
  foreign_key_count: 1
  index_count: 6
  trigger_count: 0
entity_type: sub-type
---

# Table "HumanResources"."Employee"


## Metadata

- Type: Table
- Entity model type: Subtype
- Column count: 16
- Foreign key count: 1
- Trigger count: 0

## Columns

### "HumanResources"."Employee"

| Name | Type | Nullable | Default | Remarks | Auto-incremented | Generated |
| --- | --- | --- | --- | --- | --- | --- |
| BusinessEntityID | int4 | NOT NULL |  |  |  |  |
| NationalIDNumber | varchar\(15\) | NOT NULL |  |  |  |  |
| LoginID | varchar\(256\) | NOT NULL |  |  |  |  |
| OrganizationNode | text | NULL |  |  |  |  |
| OrganizationLevel | int4 | NULL |  |  |  |  |
| JobTitle | varchar\(50\) | NOT NULL |  |  |  |  |
| BirthDate | date | NOT NULL |  |  |  |  |
| MaritalStatus | bpchar\(1\) | NOT NULL |  |  |  |  |
| Gender | bpchar\(1\) | NOT NULL |  |  |  |  |
| HireDate | date | NOT NULL |  |  |  |  |
| SalariedFlag | bool | NOT NULL | true |  |  |  |
| VacationHours | int2 | NOT NULL | 0 |  |  |  |
| SickLeaveHours | int2 | NOT NULL | 0 |  |  |  |
| CurrentFlag | bool | NOT NULL | true |  |  |  |
| rowguid | uuid | NOT NULL | public\.uuid\_generate\_v4\(\) |  |  |  |
| ModifiedDate | timestamp | NOT NULL | CURRENT\_DATE |  |  |  |

## Primary Key

### PK_Employee_BusinessEntityID
| Name |
| --- |
| BusinessEntityID |

## Indexes

### IX_Employee_OrganizationNode



| Name | Type |
| --- | --- |
| OrganizationNode | ASC |
### AK_Employee_rowguid

unique index

| Name | Type |
| --- | --- |
| rowguid | ASC |
### AK_Employee_LoginID

unique index

| Name | Type |
| --- | --- |
| LoginID | ASC |
### AK_Employee_NationalIDNumber

unique index

| Name | Type |
| --- | --- |
| NationalIDNumber | ASC |
### IX_Employee_OrganizationLevel_OrganizationNode



| Name | Type |
| --- | --- |
| OrganizationLevel | ASC |
| OrganizationNode | ASC |

## Foreign Keys

### FK_Employee_Person_BusinessEntityID

"HumanResources"."Employee" ||--|| ["Person"."Person"](../tables/person_c91162ff.md)

- BusinessEntityID --> "Person"."Person"."BusinessEntityID"




## Attributes

| Attribute | Value |
| --- | --- |

## Diagram

```mermaid
---
config:
  theme: 'neutral'
---
erDiagram
HumanResources.Employee {
    int4 BusinessEntityID PK
    varchar NationalIDNumber
    varchar LoginID
    text OrganizationNode
    int4 OrganizationLevel
    varchar JobTitle
    date BirthDate
    bpchar MaritalStatus
    bpchar Gender
    date HireDate
    bool SalariedFlag
    int2 VacationHours
    int2 SickLeaveHours
    bool CurrentFlag
    uuid rowguid
    timestamp ModifiedDate
}
HumanResources.EmployeeDepartmentHistory {
    int4 BusinessEntityID PK
    int2 DepartmentID PK
    int2 ShiftID PK
    date StartDate PK
    date EndDate
    timestamp ModifiedDate
}
HumanResources.EmployeePayHistory {
    int4 BusinessEntityID PK
    timestamp RateChangeDate PK
    numeric Rate
    int2 PayFrequency
    timestamp ModifiedDate
}
HumanResources.JobCandidate {
    serial JobCandidateID PK
    int4 BusinessEntityID FK
    xml Resume
    timestamp ModifiedDate
}
Production.Document {
    varchar DocumentNode PK
    int4 DocumentLevel
    varchar Title
    int4 Owner FK
    bool FolderFlag
    varchar FileName
    varchar FileExtension
    bpchar Revision
    int4 ChangeNumber
    int2 Status
    text DocumentSummary
    bytea Document
    uuid rowguid
    timestamp ModifiedDate
}
Purchasing.PurchaseOrderHeader {
    serial PurchaseOrderID PK
    int2 RevisionNumber
    int2 Status
    int4 EmployeeID FK
    int4 VendorID FK
    int4 ShipMethodID FK
    timestamp OrderDate
    timestamp ShipDate
    numeric SubTotal
    numeric TaxAmt
    numeric Freight
    numeric TotalDue
    timestamp ModifiedDate
}
Sales.SalesPerson {
    int4 BusinessEntityID PK
    int4 TerritoryID FK
    numeric SalesQuota
    numeric Bonus
    numeric CommissionPct
    numeric SalesYTD
    numeric SalesLastYear
    uuid rowguid
    timestamp ModifiedDate
}
Person.Person {
    int4 BusinessEntityID PK
    bpchar PersonType
    varchar NameStyle
    varchar Title
    varchar FirstName
    varchar MiddleName
    varchar LastName
    varchar Suffix
    int4 EmailPromotion
    xml AdditionalContactInfo
    xml Demographics
    uuid rowguid
    timestamp ModifiedDate
}
HumanResources.EmployeeDepartmentHistory }|--|| HumanResources.Employee : "FK_EmployeeDepartmentHistory_Employee_BusinessEntityID"
HumanResources.EmployeePayHistory }|--|| HumanResources.Employee : "FK_EmployeePayHistory_Employee_BusinessEntityID"
HumanResources.JobCandidate }o--|| HumanResources.Employee : "FK_JobCandidate_Employee_BusinessEntityID"
Production.Document }|--|| HumanResources.Employee : "FK_Document_Employee_Owner"
Purchasing.PurchaseOrderHeader }|--|| HumanResources.Employee : "FK_PurchaseOrderHeader_Employee_EmployeeID"
Sales.SalesPerson ||--|| HumanResources.Employee : "FK_SalesPerson_Employee_BusinessEntityID"
HumanResources.Employee ||--|| Person.Person : "FK_Employee_Person_BusinessEntityID"
```

## Cross-References

### Referenced by
- ["HumanResources"."EmployeeDepartmentHistory"](../tables/employeedepartmenthistory_c3fff7b.md)
- ["HumanResources"."EmployeePayHistory"](../tables/employeepayhistory_b0475801.md)
- ["HumanResources"."JobCandidate"](../tables/jobcandidate_fb72ee2d.md)
- ["Production"."Document"](../tables/document_41c277e1.md)
- ["Purchasing"."PurchaseOrderHeader"](../tables/purchaseorderheader_c13bfa1b.md)
- ["Sales"."SalesPerson"](../tables/salesperson_4390b854.md)

### References
- ["Person"."Person"](../tables/person_c91162ff.md)

