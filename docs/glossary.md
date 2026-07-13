# Glossary

Use this page to record terms and ideas that help you understand
professional analytics projects.

Pro-tip: Expand the VS Code **Outline** view (below the navigator on the right)
to see this file organization at-a-glance.

## Data Warehouse Concepts

### data warehouse

A data warehouse is a central repository designed for BI queries and reporting.
It stores historical data from multiple sources in a structured format
optimized for analysis rather than transaction processing.

### star schema

A star schema is a data warehouse design pattern with one central fact table
surrounded by dimension tables.
It is called a star schema because the diagram looks like a star.
Star schemas are optimized for fast analytical queries.

### fact table

A fact table stores measurable business events such as sales transactions.
Each row represents one event and includes numeric metrics and foreign keys
that link to dimension tables.
In this project, the sale table is the fact table.

### dimension table

A dimension table stores descriptive attributes about business entities.
Examples include customer, product, store, and date.
Dimension tables provide the context needed to interpret fact table metrics.

### grain

The grain of a fact table is the level of detail each row represents.
In this project, the grain is one sales transaction.
Defining the grain clearly is the most important decision in warehouse design.

### surrogate key

A surrogate key is an artificial primary key assigned by the warehouse,
separate from the natural key from the source system.
Surrogate keys protect the warehouse from changes in source system IDs.

## SQL and DuckDB

### SQL

SQL (Structured Query Language) is the standard language for
querying and manipulating relational databases.
SELECT, FROM, WHERE, GROUP BY, and JOIN are the most common SQL clauses.

### DuckDB

DuckDB is an in-process relational database designed for analytical workloads.
It can store data in a local `.duckdb` file and requires no separate database server.

### CREATE TABLE

`CREATE TABLE` is a SQL statement that defines a new table and its columns.
`CREATE TABLE IF NOT EXISTS` creates the table only when it does not already exist.
It does not update the schema of an existing table.

### INSERT

`INSERT` is a SQL statement that adds rows to a table.

### JOIN

A JOIN combines rows from two tables based on a matching column.
In this project, joining the sale table to the customer table
on CustomerID retrieves the region for each sale.

### foreign key constraint

A foreign key constraint enforces referential integrity in the database.
It prevents loading a sale with a CustomerID that does not exist
in the customer table.

## Loading and Verification

### row count verification

Row count verification checks that the number of rows loaded
matches the number of rows in the source.
It is the simplest and most important post-load check.
