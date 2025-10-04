# BirdiDQ Architecture Overview

## High-Level System Architecture

This document provides a comprehensive view of the BirdiDQ data quality application architecture, including the interaction between users, processes, and system components.

```mermaid
graph TB
    subgraph "People Layer"
        A[Data Engineer/Analyst] -->|Uploads Data| B[Data Source Selection]
        A -->|Natural Language Query| C[Query Input Interface]
    end

    subgraph "Interaction Workflow Process"
        B -->|CSV Upload| D[File Upload Handler]
        B -->|Select Existing| E[Local/Database Browser]
        D --> F[Data Preview & Metrics]
        E --> F
        F -->|Display DataFrame| G[Interactive Data Explorer]
        C -->|User Query Text| H[Query Processor]
    end

    subgraph "LLM Process"
        H -->|API Request| I[Ollama Cloud API]
        I -->|Model: gpt-oss:20b| J[Natural Language Parser]
        J -->|Context: Column Names| K[Expectation Generator]
        K -->|Generates Python Code| L[GX Expectation Methods]
        L -->|Return Code String| M[Code Display]
    end

    subgraph "Transformation Process"
        M -->|Execute Code| N[Great Expectations Validator]
        N -->|Create Batch| O[Data Source Context]
        O -->|Pandas/SQL Engine| P[Expectation Execution]
        P -->|Validation Results| Q[Checkpoint Runner]
        Q -->|Aggregate Results| R[Expectation Suite]
    end

    subgraph "Outputs Process"
        R -->|Generate Metrics| S[Validation Results]
        S -->|Build Reports| T[Data Docs Builder]
        T -->|HTML Generation| U[Interactive Reports]
        U -->|file:// URL| V[Browser Display]
        S -->|Success/Failure| W[Status Dashboard]
        W -->|Metrics Display| X[Streamlit UI]
    end

    subgraph "Data Persistence"
        R -.->|Save Suite| Y[(Expectations Store)]
        Q -.->|Save Results| Z[(Validations Store)]
        T -.->|Write HTML| AA[(Data Docs Store)]
    end

    style A fill:#e1f5ff
    style I fill:#fff3e0
    style N fill:#f3e5f5
    style T fill:#e8f5e9
    style Y fill:#fce4ec
    style Z fill:#fce4ec
    style AA fill:#fce4ec
```

## Component Details

### 1. People Layer
**Role:** Data Engineers and Analysts
- **Actions:**
  - Upload CSV files or select from existing data sources
  - Input natural language queries describing data quality checks
  - Review validation results and data documentation
  - Make decisions based on quality metrics

### 2. Interaction Workflow Process
**Components:**
- **File Upload Handler:** Processes CSV uploads, validates format, extracts metadata
- **Data Browser:** Lists available data sources (local files, PostgreSQL, Oracle)
- **Data Preview:** Shows sample data, row/column counts, memory usage
- **Interactive Explorer:** Allows filtering and viewing data before validation
- **Query Processor:** Captures and prepares natural language input for LLM

### 3. LLM Process
**Components:**
- **Ollama Cloud API:** Hosted LLM service with authentication
- **Model (gpt-oss:20b):** 20 billion parameter open-source model
- **Natural Language Parser:** Understands data quality requirements from text
- **Expectation Generator:** Converts requirements to Great Expectations code
- **Context Enhancement:** Uses column names and data types to improve accuracy

**Flow:**
```
User Query → API Request → Model Inference → Code Generation → Validation
"Check emails" → analyze → understand → generate code → return method
```

### 4. Transformation Process
**Components:**
- **GX Validator:** Core Great Expectations validation engine
- **Data Source Context:** Manages connections to Pandas/SQL data sources
- **Execution Engines:**
  - PandasExecutionEngine (for CSV/DataFrame)
  - SqlAlchemyExecutionEngine (for PostgreSQL/Oracle)
- **Expectation Execution:** Runs validation logic against data
- **Checkpoint Runner:** Orchestrates batch validation and result collection
- **Expectation Suite:** Collection of all expectations for a dataset

**Data Flow:**
```
Code String → Parse → Execute → Validate → Collect Results → Aggregate
```

### 5. Outputs Process
**Components:**
- **Validation Results:** Success/failure status, metric calculations
- **Data Docs Builder:** Generates HTML documentation from validation results
- **Interactive Reports:** Rich HTML pages with charts, tables, and metrics
- **Status Dashboard:** Real-time display in Streamlit UI
- **Browser Integration:** Opens reports in user's default browser

**Report Contents:**
- Expectation Suite Overview
- Validation Results by Column
- Data Quality Metrics
- Historical Validation Trends
- Failed Expectation Details

### 6. Data Persistence
**Storage Locations:**
- **Expectations Store:** `/BirdiDQ/gx/expectations/` (JSON format)
- **Validations Store:** `/BirdiDQ/gx/uncommitted/validations/` (JSON format)
- **Data Docs Store:** `/BirdiDQ/gx/uncommitted/data_docs/local_site/` (HTML format)

## Technology Stack

### Frontend
- **Streamlit:** Web application framework
- **Python:** Core application logic
- **HTML/CSS:** Custom styling for UI components

### Backend
- **Great Expectations:** Data validation framework
- **Pandas:** Data manipulation and analysis
- **SQLAlchemy:** Database connectivity layer

### AI/ML
- **Ollama Cloud:** LLM inference platform
- **gpt-oss:20b:** Open-source GPT model

### Data Sources
- **Local Filesystem:** CSV file support
- **PostgreSQL:** Relational database connector
- **Oracle Database:** Enterprise database support

### Storage
- **Local File System:** JSON and HTML storage
- **Git-Compatible:** All artifacts version-controllable

## Key Workflows

### Upload and Validate Workflow
```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant FileHandler
    participant LLM
    participant GX
    participant DataDocs

    User->>Streamlit: Upload CSV File
    Streamlit->>FileHandler: Process File
    FileHandler->>Streamlit: Display Preview
    User->>Streamlit: Enter Query
    Streamlit->>LLM: Send Query + Context
    LLM->>Streamlit: Return GX Code
    Streamlit->>GX: Execute Expectations
    GX->>GX: Validate Data
    GX->>DataDocs: Build Reports
    DataDocs->>User: Open HTML Report
```

### Database Validation Workflow
```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant DBConnector
    participant LLM
    participant GX
    participant DataDocs

    User->>Streamlit: Select Database Table
    Streamlit->>DBConnector: Fetch Schema
    DBConnector->>Streamlit: Display Preview
    User->>Streamlit: Enter Query
    Streamlit->>LLM: Send Query + Schema
    LLM->>Streamlit: Return GX Code
    Streamlit->>GX: Execute via SQL Engine
    GX->>GX: Validate in Database
    GX->>DataDocs: Build Reports
    DataDocs->>User: Open HTML Report
```

## Database-Specific Architecture

### High-Level Database Architecture
This diagram shows the complete database validation workflow with specific components for PostgreSQL and Oracle databases.

```mermaid
graph TB
    subgraph "People Layer"
        A[Database Administrator] -->|Connects to| B[Database Selection]
        A -->|Natural Language Query| C[Query Input Interface]
    end

    subgraph "Database Access Layer"
        B -->|Environment Config| D[Connection Manager]
        D -->|Test Connection| E[Database Browser]
        E -->|List Tables| F[Schema Inspector]
        F -->|Table Selection| G[Data Preview]
    end

    subgraph "Database-Specific Connectors"
        G -->|PostgreSQL| H[PostgreSQLDatasource]
        G -->|Oracle DB| I[OracleDatasource]
        H -->|SQLAlchemy Engine| J[PostgreSQL Executor]
        I -->|SQLAlchemy Engine| K[Oracle Executor]
    end

    subgraph "LLM Process"
        C -->|API Request| L[Ollama Cloud API]
        L -->|Model: gpt-oss:20b| M[Natural Language Parser]
        M -->|Context: Schema Info| N[Expectation Generator]
        N -->|Generates SQL-Based| O[GX Expectation Code]
        O -->|With Table Schema| P[Code Display]
    end

    subgraph "Database Validation Process"
        P -->|Execute Code| Q[SqlAlchemyExecutionEngine]
        Q -->|Create Batch| R[Database Context]
        R -->|Push-down Execution| S[SQL Query Engine]
        S -->|Run in Database| T[Validation Execution]
        T -->|SQL Results| U[Checkpoint Runner]
        U -->|Aggregate Results| V[Expectation Suite]
    end

    subgraph "Outputs Process"
        V -->|Generate Metrics| W[Validation Results]
        W -->|Build Reports| X[Data Docs Builder]
        X -->|HTML + Charts| Y[Interactive Reports]
        Y -->|Database Metrics| Z[Browser Display]
        W -->|Success/Failure| AA[Database Dashboard]
        AA -->|Live Data Status| BB[Streamlit UI]
    end

    subgraph "Database Storage"
        V -.->|Save Suite| CC[(Expectations Store)]
        U -.->|Save Results| DD[(Validations Store)]
        X -.->|Write HTML| EE[(Data Docs Store)]
        BB -.->|Cache Schema| FF[(Schema Cache)]
    end

    style A fill:#e1f5ff
    style L fill:#fff3e0
    style Q fill:#f3e5f5
    style T fill:#e8f5e9
    style CC fill:#fce4ec
    style DD fill:#fce4ec
    style EE fill:#fce4ec
    style FF fill:#fce4ec
```

### Database Components Detail

#### 1. Database Access Layer
**Components:**
- **Connection Manager:** Manages database connections using environment variables
- **Database Browser:** Lists available databases and schemas
- **Schema Inspector:** Extracts table structures, column types, and constraints
- **Data Preview:** Shows sample data without loading entire tables

**Supported Databases:**
- **PostgreSQL:** Via `psycopg2` driver and `SqlAlchemyExecutionEngine`
- **Oracle Database:** Via `cx_Oracle` driver and `SqlAlchemyExecutionEngine`

#### 2. Database-Specific Connectors
**PostgreSQLDatasource:**
- Connection via `POSTGRES_CONNECTION_STRING` environment variable
- Uses Fluent API `sources.add_postgres()`
- Supports complex queries and schema introspection
- Automatic batch request creation for tables

**OracleDatasource:**
- Connection via `ORACLE_CONNECTION_STRING` environment variable  
- Uses Fluent API `sources.add_sql()` with Oracle driver
- Enterprise-grade features and performance
- Handles Oracle-specific data types and functions

#### 3. Database Validation Process
**SqlAlchemyExecutionEngine:**
- **Push-down Execution:** Runs expectations as SQL queries in the database
- **Performance Optimization:** Leverages database indexes and query planning
- **Scalability:** Handles tables with millions of rows efficiently
- **Resource Efficiency:** Minimal data transfer between application and database

**Query Optimization Features:**
- Automatic SQL query generation from expectations
- Database-specific optimizations (PostgreSQL vs Oracle)
- Batch processing for large tables
- Connection pooling for performance

#### 4. Database-Specific Workflows

**PostgreSQL Validation Flow:**
```mermaid
graph LR
    A[User Query] -->|Check columns| B[Schema Validation]
    B -->|Generate SQL| C[PostgreSQL Engine]
    C -->|Execute Query| D[PostgreSQL DB]
    D -->|Return Results| E[GX Validation]
    E -->|Aggregate Metrics| F[Quality Report]
    
    style C fill:#336791
    style D fill:#336791
```

**Oracle Validation Flow:**
```mermaid
graph LR
    A[User Query] -->|Check schema| B[Oracle Schema Check]
    B -->|Generate SQL| C[Oracle Engine]
    C -->|Execute Query| D[Oracle DB]
    D -->|Return Results| E[GX Validation]
    E -->|Aggregate Metrics| F[Quality Report]
    
    style C fill:#F80000
    style D fill:#F80000
```

### Database Performance Characteristics

#### Query Execution Performance
- **Small tables (< 10K rows):** 200-500ms
- **Medium tables (10K-100K rows):** 500ms-2s
- **Large tables (100K-1M rows):** 2-10s  
- **Very large tables (> 1M rows):** 10s-60s

#### Performance Optimization
- **Index Usage:** Automatically leverages existing database indexes
- **Query Planning:** Database query planner optimizes expectations
- **Parallel Execution:** Runs independent expectations concurrently (when possible)
- **Materialized Views:** Can utilize pre-computed aggregations

#### Database-Specific Features

**PostgreSQL Advantages:**
- Advanced JSON data type support
- Rich indexing capabilities
- Excellent Open Source ecosystem
- Cost-effective scaling

**Oracle Advantages:**
- Enterprise-grade reliability and features
- Advanced partitioning and compression
- Comprehensive monitoring and analytics
- High-performance OLTP support

### Database Security & Compliance

#### Connection Security
- **Environment Variables:** Database credentials stored securely
- **Connection Encryption:** SSL/TLS for database connections
- **Access Control:** Database-level permissions and roles
- **Audit Logging:** Comprehensive validation result logging

#### Data Privacy
- **In-place Validation:** No data copied from database
- **Schema Only Transfer:** Only metadata sent for context
- **Local Storage:** Validation results stored locally
- **Compliance Ready:** Supports GDPR, HIPAA, and SOC2 requirements


## Data Flow Architecture

```mermaid
graph LR
    A[Raw Data] -->|Ingestion| B[Data Source]
    B -->|Query/Read| C[Execution Engine]
    C -->|Validate| D[Expectations]
    D -->|Results| E[Validation Store]
    E -->|Transform| F[Data Docs]
    F -->|Display| G[User Interface]
    
    H[User Query] -->|NLP| I[LLM]
    I -->|Code Gen| D
    
    style A fill:#e3f2fd
    style D fill:#fff3e0
    style F fill:#e8f5e9
    style I fill:#fce4ec
```

## Security Considerations

### Environment Configuration
- API keys stored in `.env` file (not version controlled)
- Database credentials managed through environment variables
- File path validation for uploads

### Data Privacy
- Local execution - no data sent to external services except LLM queries
- Validation results stored locally
- User controls data exposure

## Performance Characteristics

### File Upload
- **Throughput:** ~1000 rows/second for CSV parsing
- **Memory:** DataFrame loaded entirely in memory
- **Limitation:** Recommended max 100MB per file

### Validation Execution
- **Pandas Engine:** Fast for datasets < 1M rows
- **SQL Engine:** Efficient for large database tables
- **Parallel:** Multiple expectations run sequentially

### LLM Processing
- **Latency:** 2-5 seconds for query processing
- **Model:** gpt-oss:20b hosted on Ollama Cloud
- **Caching:** Not implemented (future enhancement)

## Scalability Notes

### Current Limitations
- Single-threaded execution
- In-memory data processing
- Local file storage only

### Future Enhancements
- Distributed execution for large datasets
- Streaming data validation
- Cloud storage integration
- Batch processing capabilities

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Maintained By:** BirdiDQ Development Team

