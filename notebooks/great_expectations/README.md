# Great Expectations Analysis Notebooks

## Overview

This directory contains Jupyter notebooks for analyzing Great Expectations data quality artifacts stored in JSON format.

## Notebooks

### 1. `validation_results_analysis.ipynb`

Analyzes validation results from Great Expectations runs.

**Features:**
- 📊 **Metadata Extraction**: Datasource, data asset, and validation run information
- 📈 **Statistics Analysis**: Overall success rates and counts
- 🔍 **Individual Results**: Detailed expectation results with success/failure status
- ❌ **Failure Analysis**: Focused view of failed expectations for remediation
- 📊 **Aggregated Summaries**: Statistics by expectation type and column
- 💾 **CSV Exports**: Export results for further analysis or reporting

**Data Source**: `BirdiDQ/gx/uncommitted/validations/` (JSON validation results)

### 2. `expectation_suites_analysis.ipynb`

Analyzes expectation suite definitions from Great Expectations.

**Features:**
- 📋 **Suite Metadata**: Name, version, expectation count, creation date
- 🔍 **Individual Expectations**: Detailed breakdown of all expectations
- 🐍 **Python Code Extraction**: Embedded implementation code from expectations
- ⚙️ **Execution Engine Info**: Which engine (Pandas, SQL, Spark) runs each expectation
- 🤖 **LLM-Generated Descriptions**: Uses Ollama (gpt-oss:20b) to generate human-readable descriptions for each expectation
- 📊 **Suite Summaries**: Aggregated views by suite and expectation type
- 📈 **Column Coverage**: Which columns have expectations and how many
- 🔧 **Parameter Analysis**: Range values, mostly parameters, value sets
- 🔄 **Suite Comparison**: Compare expectations across different suites
- 💾 **CSV Exports**: Export suite details for documentation

**Data Source**: `BirdiDQ/gx/expectations/` (JSON expectation suite definitions)

## Getting Started

### Prerequisites

Ensure you have the required packages installed:

```bash
pip install pandas jupyter matplotlib seaborn requests python-dotenv
```

**For LLM Description Generation** (in `expectation_suites_analysis.ipynb`):
- Uses Ollama Cloud API (no local installation required)
- Environment variables required in `.env` file:
  - `OLLAMA_CLOUD_BASE_URL=https://ollama.com`
  - `OLLAMA_CLOUD_MODEL=gpt-oss:20b`
  - `OLLAMA_API_KEY=<your_api_key>`

### Running the Notebook

1. **Activate your virtual environment:**
   ```bash
   cd /Users/yavin/python_projects/ollama_jupyter
   source venv/bin/activate
   ```

2. **Launch Jupyter:**
   ```bash
   # For validation results analysis
   jupyter notebook notebooks/great_expectations/validation_results_analysis.ipynb
   
   # For expectation suites analysis
   jupyter notebook notebooks/great_expectations/expectation_suites_analysis.ipynb
   ```

3. **Run all cells** to generate the analysis.

## Data Sources

The notebooks read from two main directories:

1. **Validation Results**: `BirdiDQ/gx/uncommitted/validations/`
   - JSON files generated after running validations
   - Contains actual test results (pass/fail)

2. **Expectation Suites**: `BirdiDQ/gx/expectations/`
   - JSON files defining data quality rules
   - Contains expectation definitions (what to test)

## Output

### Validation Results Notebook DataFrames:

1. **`metadata_df`**: High-level validation metadata
2. **`statistics_df`**: Validation statistics (success rates)
3. **`expectations_df`**: Individual expectation results
4. **`failed_expectations_df`**: Failed expectations only
5. **`expectation_type_summary`**: Aggregated by expectation type

### Expectation Suites Notebook DataFrames:

1. **`metadata_df`**: Suite metadata (name, version, count)
2. **`expectations_df`**: Individual expectation definitions
3. **`suite_summary`**: Aggregated by suite
4. **`expectation_type_summary`**: Aggregated by expectation type
5. **`column_coverage`**: Coverage analysis by column

### CSV Exports:

All DataFrames are automatically exported to:
```
/Users/yavin/python_projects/ollama_jupyter/notebooks/great_expectations/exports/
```

Files created:
- `validation_metadata.csv`
- `validation_statistics.csv`
- `expectation_results.csv`
- `expectation_type_summary.csv`
- `failed_expectations.csv` (if failures exist)

## Use Cases

### 1. **Data Quality Monitoring**
Track validation success rates over time to monitor data quality trends.

### 2. **Failure Investigation**
Quickly identify and analyze failed expectations to understand data quality issues.

### 3. **Reporting**
Generate CSV exports for stakeholder reports or dashboards.

### 4. **Expectation Optimization**
Analyze which expectation types are most/least successful to refine your data quality rules.

### 5. **Column-Level Analysis**
Identify which columns have the most quality issues.

## Example Queries

The notebook includes helper functions for quick data access:

```python
# Get all expectations for a specific column
get_expectations_by_column('column_name')

# Get all expectations of a specific type
get_expectations_by_type('expect_column_values_to_not_be_null')

# Get failed expectations for a specific column
get_failed_expectations_by_column('column_name')
```

## JSON File Structure

Great Expectations validation JSON files contain:

```json
{
  "evaluation_parameters": {},
  "meta": {
    "active_batch_definition": {...},
    "batch_markers": {...},
    "expectation_suite_name": "...",
    "validation_time": "..."
  },
  "statistics": {
    "evaluated_expectations": 132,
    "successful_expectations": 130,
    "unsuccessful_expectations": 2,
    "success_percent": 98.48
  },
  "results": [
    {
      "expectation_config": {...},
      "success": true,
      "result": {...}
    }
  ]
}
```

## Customization

You can customize the notebook to:

- Add additional visualizations
- Filter by specific date ranges
- Compare multiple validation runs
- Create custom aggregations
- Integrate with external reporting tools

## Troubleshooting

### No JSON files found
- Ensure validations have been run in the BirdiDQ application
- Check that the path in the notebook matches your installation

### Import errors
- Install missing packages: `pip install pandas jupyter matplotlib seaborn`

### Empty DataFrames
- Verify JSON files contain validation results
- Check the JSON structure matches the expected format

## Related Documentation

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [BirdiDQ Architecture](../../BirdiDQ/ARCHITECTURE.md)
- [BirdiDQ Quality Gates](../../BirdiDQ/ARCHITECTURE_QUALITY_GATES.md)

## Contributing

To add new analysis features:

1. Create a new cell in the notebook
2. Add appropriate markdown documentation
3. Test with sample validation results
4. Update this README with the new feature

---

**Created**: October 2025  
**Last Updated**: October 2025  
**Maintainer**: BirdiDQ Team
