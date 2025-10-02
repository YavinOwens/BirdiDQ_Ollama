# Ollama Jupyter - Data Validation & AI Integration Project

A comprehensive data validation platform that integrates Streamlit for interactive web-based data quality checks, leverages the latest Great Expectations 0.18.x (Fluent API) for robust data validation, and utilizes Ollama LLM (gpt-oss:20b model) for natural language-driven expectation generation and validation.

## 📋 Table of Contents
- [Use Cases](#-use-cases)
- [References & Credits](#-references--credits)
- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Documentation](#-documentation)
- [High-Level Architecture](#-high-level-architecture)
- [Configuration](#-configuration)
- [Technical Details](#-technical-details)
- [License & Contributing](#-license--contributing)

---

## 🎯 Use Cases

| Use Case | Tool/Component | Purpose | Target Audience |
|----------|----------------|---------|-----------------|
| **Data Exploration** | Jupyter notebooks | Learn GX patterns, test Ollama integration | Data engineers, developers |
| **Production Validation** | BirdiDQ Streamlit app | Team-based data quality checks with natural language | Data analysts, business users |
| **Natural Language QA** | Ollama LLM integration | Generate validation rules from plain English | Non-technical stakeholders |
| **Database Monitoring** | Scheduled checkpoint runs | Continuous data quality monitoring | Data engineers, DevOps |
| **Custom Reporting** | Enhanced Data Docs | Branded reports with embedded code | Data governance teams |

## 📖 References & Credits

### External Documentation
- **Great Expectations:** https://docs.greatexpectations.io/
- **Ollama:** https://ollama.com/docs
- **Streamlit:** https://docs.streamlit.io/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Oracle:** https://docs.oracle.com/

### Related Projects
- **BirdiDQ Original:** https://github.com/BirdiD/BirdiDQ
- **Great Expectations GitHub:** https://github.com/great-expectations/great_expectations

### 🏆 Credits
- **Great Expectations Team** - Data validation framework
- **Ollama Team** - LLM inference platform
- **BirdiDQ Original Authors** - Base Streamlit application
- **Streamlit Team** - Web application framework

### Getting Help
1. Check the [WORKFLOW.md](WORKFLOW.md) guide
2. Review troubleshooting docs in `BirdiDQ/` directory
3. Check Great Expectations documentation
4. Review terminal output for specific errors

---

## 🎯 Overview

### What is This Project?

This project provides two main components for data quality validation:

1. **BirdiDQ Streamlit App** - Production-ready web application for natural language data quality checks
2. **Jupyter Notebooks** - Experimental environment for testing Great Expectations patterns and Ollama LLM integration

### Core Technologies
- **Great Expectations 0.18+** - Data validation framework with Fluent API
- **Ollama Cloud** - LLM integration (`gpt-oss:20b` model) for natural language processing
- **Streamlit** - Interactive web application framework
- **PostgreSQL & Oracle** - Database connectivity with SQL/Pandas execution engines

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL access (Oracle optional)
- Ollama API key for LLM features

### Installation

1. **Clone and setup environment:**
```bash
git clone <repository_url>
cd ollama_jupyter
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
# Create .env file in project root
cp env_template.txt .env
# Edit .env with your credentials (see Configuration section)
```

3. **Run the application:**
```bash
# Option 1: Streamlit App (Production)
cd BirdiDQ
streamlit run great_expectations/app.py --server.port 8503

# Option 2: Jupyter Notebooks (Experimentation)
jupyter notebook
```

4. **Access the application:**
- **Streamlit App:** http://localhost:8503
- **Jupyter:** http://localhost:8888

---

## 📊 Key Features

### BirdiDQ Streamlit Application
- ✅ **Natural Language Processing** - Convert plain English to Great Expectations code
- ✅ **Multi-Database Support** - PostgreSQL (SQL engine) & Oracle (Pandas engine)
- ✅ **Data Assistants** - Automated profiling (Onboarding & Missingness)
- ✅ **Custom Data Docs** - Enhanced with Python and SQL code display
- ✅ **Interactive Preview** - Explore data before validation
- ✅ **Email Notifications** - Alert data owners about quality issues
- ✅ **Real-time Validation** - Immediate feedback on data quality

### Jupyter Notebooks
- ✅ **GX Fluent API Patterns** - Examples and best practices
- ✅ **Data Assistant Workflows** - Automated expectation generation
- ✅ **Checkpoint Management** - Validation orchestration
- ✅ **Ollama Streaming** - Real-time LLM responses
- ✅ **Performance Benchmarking** - Optimization testing

---

## 📚 Documentation

### 🎯 Getting Started
- **[WORKFLOW.md](WORKFLOW.md)** - **START HERE!** Complete step-by-step workflow guide with screenshots
  - Database and table selection
  - Data preview and exploration
  - Natural language input examples
  - Validation results interpretation
  - Data Docs navigation and analysis

### 🔄 Migration & Planning
- **[MIGRATION_PLAN.md](MIGRATION_PLAN.md)** - Comprehensive migration strategy from GX 0.18.x to 0.24+
  - Current vs. target architecture analysis
  - Breaking changes identification and mitigation
  - 6-week phased migration plan
  - Specific code changes and examples
  - Risk assessment and success metrics

### 📖 BirdiDQ Application Guides
Located in `BirdiDQ/` directory:

#### Setup & Integration
- **[BirdiDQ/README.md](BirdiDQ/README.md)** - BirdiDQ overview and original documentation
- **[BirdiDQ/OLLAMA_README.md](BirdiDQ/OLLAMA_README.md)** - Ollama integration setup guide
- **[BirdiDQ/INTEGRATION_SUMMARY.md](BirdiDQ/INTEGRATION_SUMMARY.md)** - Complete integration overview and metrics

#### Feature Guides
- **[BirdiDQ/CODE_DISPLAY_IN_DATA_DOCS.md](BirdiDQ/CODE_DISPLAY_IN_DATA_DOCS.md)** - Python code display in Data Docs
- **[BirdiDQ/SQL_CODE_DISPLAY.md](BirdiDQ/SQL_CODE_DISPLAY.md)** - SQL code display for PostgreSQL
- **[BirdiDQ/DATA_ASSISTANT_CODE_DISPLAY.md](BirdiDQ/DATA_ASSISTANT_CODE_DISPLAY.md)** - Data Assistant code display
- **[BirdiDQ/COLUMN_NAME_FIX.md](BirdiDQ/COLUMN_NAME_FIX.md)** - LLM column name awareness improvements

#### Troubleshooting
- **[BirdiDQ/DATA_ASSISTANT_FIX.md](BirdiDQ/DATA_ASSISTANT_FIX.md)** - Data Assistant API migration (GX 0.18+)
- **[BirdiDQ/DATA_ASSISTANT_VALIDATION_FIX.md](BirdiDQ/DATA_ASSISTANT_VALIDATION_FIX.md)** - Suite validation fixes
- **[BirdiDQ/DATA_DOCS_VALIDATION_FIX.md](BirdiDQ/DATA_DOCS_VALIDATION_FIX.md)** - Data Docs display fixes
- **[BirdiDQ/EXECUTION_REFINEMENT.md](BirdiDQ/EXECUTION_REFINEMENT.md)** - Expectation execution improvements

### 🖼️ Visual Resources
- **Workflow Screenshots:** `birdidq_vs2_imgs/` directory
  - `01_select_database.png` - Database selection interface
  - `02_select_table.png` - Table selection dropdown
  - `03_data_preview.png` - Data preview and exploration
  - `04_natural_language_input.png` - Natural language input interface
  - `05_validation_results.png` - Validation execution results
  - `06_data_docs.png` - Data Docs HTML reports

---

## 🏗️ High-Level Architecture

The following diagram illustrates how the key components integrate to provide natural language data quality validation:

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface"
        UI[Streamlit Web App<br/>Port 8503]
        JN[Jupyter Notebooks<br/>Port 8888]
    end
    
    %% Application Layer
    subgraph "BirdiDQ Application"
        APP[Streamlit App<br/>app.py]
        CONN[Database Connectors<br/>PostgreSQL & Oracle]
        HELP[Helper Modules<br/>Code Display & Utils]
    end
    
    %% LLM Integration
    subgraph "LLM Processing"
        OLLAMA[Ollama Cloud API<br/>gpt-oss:20b Model]
        NATLANG[Natural Language<br/>Input Processing]
        GXCODE[Great Expectations<br/>Code Generation]
    end
    
    %% Data Validation Engine
    subgraph "Great Expectations Framework"
        GX[GX Context<br/>Fluent API 0.18.x]
        EXPECT[Expectation Suites<br/>JSON Files]
        CHECK[Checkpoints<br/>Validation Orchestration]
        DOCS[Data Docs<br/>HTML Reports]
    end
    
    %% Data Sources
    subgraph "Data Sources"
        PG[(PostgreSQL Database<br/>NYC Taxi Data<br/>SQL Execution Engine)]
        ORACLE[(Oracle 19c Database<br/>TRANSACTIONS Table<br/>Pandas Execution Engine)]
        LOCAL[Local Files<br/>CSV/Excel<br/>Pandas Engine]
    end
    
    %% Infrastructure
    subgraph "Infrastructure"
        DOCKER[Docker Container<br/>Oracle 19c]
        FILES[File System<br/>Expectations & Checkpoints]
    end
    
    %% User Interactions
    UI --> APP
    JN --> APP
    
    %% Application Flow
    APP --> CONN
    APP --> NATLANG
    APP --> HELP
    
    %% LLM Processing Flow
    NATLANG --> OLLAMA
    OLLAMA --> GXCODE
    GXCODE --> GX
    
    %% Great Expectations Flow
    GX --> EXPECT
    GX --> CHECK
    CHECK --> DOCS
    HELP --> DOCS
    
    %% Data Connections
    CONN --> PG
    CONN --> ORACLE
    CONN --> LOCAL
    
    %% Infrastructure Connections
    ORACLE --> DOCKER
    EXPECT --> FILES
    CHECK --> FILES
    DOCS --> FILES
    
    %% Styling
    classDef userInterface fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef application fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef llm fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef gx fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef infra fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    
    class UI,JN userInterface
    class APP,CONN,HELP application
    class OLLAMA,NATLANG,GXCODE llm
    class GX,EXPECT,CHECK,DOCS gx
    class PG,ORACLE,LOCAL data
    class DOCKER,FILES infra
```

### Architecture Flow Description

1. **User Interface Layer**
   - **Streamlit Web App** (Port 8503): Production interface for team-based data quality validation
   - **Jupyter Notebooks** (Port 8888): Experimental environment for testing patterns

2. **Application Layer**
   - **Streamlit App**: Main application orchestrating all components
   - **Database Connectors**: Handle PostgreSQL, Oracle, and local file connections
   - **Helper Modules**: Enhance Data Docs with code display and utility functions

3. **LLM Processing**
   - **Ollama Cloud API**: Processes natural language input using `gpt-oss:20b` model
   - **Natural Language Processing**: Converts user requirements to structured expectations
   - **Code Generation**: Produces valid Great Expectations Fluent API code

4. **Great Expectations Framework**
   - **GX Context**: Manages validation context and configuration
   - **Expectation Suites**: Store validation rules as JSON files
   - **Checkpoints**: Orchestrate validation execution and reporting
   - **Data Docs**: Generate HTML reports with embedded code examples

5. **Data Sources**
   - **PostgreSQL**: Production database with SQL execution engine
   - **Oracle 19c**: Local Docker container with Pandas execution engine
   - **Local Files**: CSV/Excel files processed with Pandas

6. **Infrastructure**
   - **Docker Container**: Isolated Oracle 19c database environment
   - **File System**: Persistent storage for GX artifacts and configurations

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root (use `env_template.txt` as reference):

```env
# Ollama Cloud Configuration
OLLAMA_CLOUD_BASE_URL=https://ollama.com
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_api_key_here

# Database Connections
POSTGRES_CONNECTION_STRING=postgresql+psycopg2://user:password@host:port/database
ORACLE_CONNECTION_STRING=oracle+oracledb://user:password@host:port/?service_name=SERVICE

# Optional: Email Configuration (for data owner notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Optional: Application Settings
LOG_LEVEL=INFO
OUTPUT_DIR=notebooks/outputs
```

### Configuration Files
- **[env_template.txt](env_template.txt)** - Project-wide environment template
- **[BirdiDQ/environment_config.txt](BirdiDQ/environment_config.txt)** - BirdiDQ-specific template
- **[BirdiDQ/LICENSE](BirdiDQ/LICENSE)** - Apache License 2.0

### Database Setup

#### PostgreSQL
- **Purpose:** Production Great Expectations workshop database
- **Connection:** Configure `POSTGRES_CONNECTION_STRING` in `.env`
- **Sample Dataset:** NYC taxi data
- **Execution Engine:** SQL (direct database queries)

#### Oracle (Optional)
- **Purpose:** Local testing with Oracle 19c
- **Setup:** Run `scripts/setup_oracle.sh` to create Docker container
- **Connection:** Configure `ORACLE_CONNECTION_STRING` in `.env`
- **Sample Dataset:** TRANSACTIONS table
- **Execution Engine:** Pandas (in-memory DataFrame)

---

## 🔧 Technical Details

### Software Requirements

#### Core Dependencies
```
great-expectations>=0.18.0    # Data validation framework (Fluent API)
ollama>=0.1.0                 # LLM integration
streamlit>=1.28.0             # Web application framework
pandas>=1.5.0                 # Data manipulation
sqlalchemy==1.4.49            # Database ORM (BirdiDQ specific)
psycopg2-binary>=2.9.0        # PostgreSQL driver
oracledb>=3.0.0               # Oracle driver (optional)
python-dotenv>=1.0.0          # Environment management
streamlit-extras>=0.3.0       # Streamlit enhancements
plotly>=5.0.0                 # Interactive visualizations
```

#### Development Dependencies
```
jupyter>=1.0.0                # Notebook environment
ipykernel>=6.0.0              # Jupyter kernel
```

See `requirements.txt` and `BirdiDQ/requirements.txt` for complete lists.

### LLM Integration

#### Ollama Configuration
- **Model:** `gpt-oss:20b` (cloud-based reasoning model)
- **Purpose:** Natural language to Great Expectations code generation
- **Features:**
  - Streaming responses
  - Reasoning mode support
  - Error handling with retries
  - Column name awareness

#### Alternative Models
- **Falcon-7B** (deprecated, still in codebase) - Fine-tuned model
- **OpenAI GPT-3** (optional) - Fine-tuned on custom data

### Great Expectations Features

#### Execution Engines
- **PostgreSQL:** SQL execution engine (database-level validation)
- **Oracle:** Pandas execution engine (in-memory validation)
- **Local Files:** Pandas execution engine (CSV/Excel files)

#### Data Assistants
- **Onboarding Assistant** - Comprehensive data profiling
- **Missingness Assistant** - Null value analysis

#### Custom Enhancements
- **Code Display** - Python and SQL code embedded in Data Docs
- **Column Awareness** - LLM knows actual column names
- **Metadata Enhancement** - Implementation details in validation results

### Output Locations
- **Streamlit App:** http://localhost:8503
- **Data Docs:** `BirdiDQ/gx/uncommitted/data_docs/local_site/index.html`
- **Notebook Outputs:** `notebooks/great_expectations/outputs/`
- **Expectation Suites:** `BirdiDQ/gx/expectations/`
- **Checkpoints:** `BirdiDQ/gx/checkpoints/`
- **Validation Results:** `BirdiDQ/gx/uncommitted/validations/`

---

## 🧪 Testing

### Run Streamlit App
```bash
cd BirdiDQ
streamlit run great_expectations/app.py --server.port 8503
# Access at http://localhost:8503
```

### Run Jupyter Notebooks
```bash
jupyter notebook notebooks/great_expectations/demo.ipynb
# Access at http://localhost:8888
```

### Test Database Connections
```bash
cd BirdiDQ
python test_oracle_integration.py
python test_ollama_integration.py
```

### Verify Installation
```bash
# Test Python imports
python -c "import great_expectations; import ollama; import streamlit; print('All imports successful')"

# Test Ollama connection
python -c "from BirdiDQ.great_expectations.models.ollama_model import test_ollama_connection; print(test_ollama_connection())"
```

---

## 📄 License & Contributing

### License
Educational and demonstration purposes. See individual component licenses:
- **BirdiDQ:** Apache License 2.0 ([BirdiDQ/LICENSE](BirdiDQ/LICENSE))
- **Great Expectations:** Apache License 2.0
- **This Project:** Educational use

### Contributing
This is a personal development project. The BirdiDQ component is based on the open-source BirdiDQ project with custom enhancements including:
- Ollama LLM integration
- Code display in Data Docs
- SQL example generation
- Column name awareness
- Enhanced error handling

---

**Last Updated:** October 2025  
**Version:** 2.0 (Enhanced with Ollama Cloud Integration)  
**Great Expectations Version:** 0.18.x (Fluent API)
