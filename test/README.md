# Data Reporting Pipeline

This directory contains a comprehensive data reporting pipeline that replicates the end-to-end process from the `validation_analysis.ipynb` notebook as a standalone Python script.

## Overview

The Data Reporting Pipeline provides automated data quality analysis and reporting capabilities for Great Expectations validation results. It combines data processing, AI-powered analysis, and professional report generation into a single, executable pipeline.

## Features

- **Automated Data Processing**: Loads and processes Great Expectations validation JSON files
- **AI-Powered Analysis**: Uses Ollama Cloud (gpt-oss:20b) for intelligent insights and executive summaries
- **Professional Reporting**: Generates markdown and PDF reports suitable for C-level executives
- **Data Catalog Generation**: Creates comprehensive data asset and expectation suite catalogs
- **Comprehensive Error Handling**: Robust error handling with detailed logging
- **Configurable Pipeline**: Flexible configuration through JSON files and command-line arguments

## Files

### Core Pipeline
- `data_reporting_pipeline.py` - Main pipeline script
- `pipeline_config.json` - Default configuration file
- `pipeline_requirements.txt` - Required Python packages

### Testing
- `test_pipeline.py` - Comprehensive test suite for the pipeline
- `README.md` - This documentation file

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r pipeline_requirements.txt
   ```

2. **Configure Environment**:
   - Ensure your `.env` file is properly configured with Ollama Cloud settings
   - Update `pipeline_config.json` if needed

## Usage

### Basic Usage

```bash
# Run with default configuration
python data_reporting_pipeline.py

# Run with custom output directory
python data_reporting_pipeline.py --output-dir /path/to/output

# Run with custom validation path
python data_reporting_pipeline.py --validation-path /path/to/validations

# Run with custom configuration file
python data_reporting_pipeline.py --config custom_config.json
```

### Command Line Options

- `--config CONFIG_FILE`: Path to configuration JSON file
- `--output-dir OUTPUT_DIR`: Output directory for generated reports
- `--validation-path VALIDATION_PATH`: Path to validation results directory
- `--env-path ENV_PATH`: Path to environment configuration file

### Configuration File

The pipeline can be configured using a JSON file:

```json
{
  "validation_path": "BirdiDQ/gx/uncommitted/validations",
  "env_path": ".env",
  "output_dir": "notebooks/great_expectations",
  "ollama_timeout": 120,
  "pdf_generation": true,
  "ai_analysis": true,
  "data_catalog": true,
  "log_level": "INFO"
}
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_pipeline.py

# Run specific test
python test_pipeline.py --test analyzer
python test_pipeline.py --test full

# Available test options:
# - analyzer: Test ValidationAnalyzer class
# - init: Test pipeline initialization
# - loading: Test data loading functionality
# - metrics: Test quality metrics calculation
# - ai: Test AI insights generation
# - catalog: Test data catalog generation
# - report: Test report generation
# - full: Test complete pipeline
# - all: Run all tests (default)
```

## Output Files

The pipeline generates several output files:

### Reports
- `validation_analysis_report_professional.md` - Professional markdown report with AI executive summary
- `validation_analysis_report_professional.pdf` - Professional PDF report (if weasyprint is available)

### Data Catalog
- `data_catalog.json` - Structured data catalog in JSON format

### Logs
- `data_reporting_pipeline.log` - Detailed execution log

## Pipeline Components

### 1. ValidationAnalyzer
- Loads Ollama configuration from environment
- Handles API communication with Ollama Cloud
- Provides fallback mechanisms for local Ollama

### 2. DataReportingPipeline
- Main pipeline orchestrator
- Coordinates all processing steps
- Manages output generation and file handling

### 3. Data Processing
- Loads validation JSON files recursively
- Processes expectations into structured DataFrame
- Calculates comprehensive quality metrics

### 4. AI Analysis
- Generates AI-powered insights using Ollama Cloud
- Creates professional executive summaries
- Provides fallback analysis when AI is unavailable

### 5. Report Generation
- Creates professional markdown reports
- Generates PDF reports with A4 formatting
- Includes data catalog summaries

## Error Handling

The pipeline includes comprehensive error handling:

- **API Failures**: Graceful fallback to local Ollama or static analysis
- **File Errors**: Detailed error logging for missing or corrupted files
- **PDF Generation**: Optional PDF generation with clear error messages
- **Configuration**: Validation of configuration parameters

## Logging

The pipeline provides detailed logging:

- **File Logging**: All logs saved to `data_reporting_pipeline.log`
- **Console Output**: Real-time progress updates
- **Error Tracking**: Detailed error messages with context
- **Performance Metrics**: Execution time and performance ratings

## Performance

Typical execution times:
- **Small Dataset** (< 100 expectations): 5-10 seconds
- **Medium Dataset** (100-1000 expectations): 10-30 seconds
- **Large Dataset** (> 1000 expectations): 30+ seconds

Performance depends on:
- Number of validation files
- Ollama Cloud API response time
- PDF generation complexity

## Troubleshooting

### Common Issues

1. **Ollama API Errors**:
   - Check API key configuration in `.env`
   - Verify Ollama Cloud connectivity
   - Pipeline will fallback to local Ollama or static analysis

2. **PDF Generation Failures**:
   - Install weasyprint: `pip install weasyprint`
   - Check system dependencies for PDF generation
   - Pipeline will continue without PDF output

3. **File Not Found Errors**:
   - Verify validation path exists
   - Check file permissions
   - Ensure JSON files are valid

4. **Configuration Errors**:
   - Validate JSON configuration syntax
   - Check environment file format
   - Verify all required parameters

### Debug Mode

Enable debug logging by setting log level to DEBUG in configuration:

```json
{
  "log_level": "DEBUG"
}
```

## Integration

The pipeline can be integrated into:

- **CI/CD Pipelines**: Automated data quality reporting
- **Scheduled Jobs**: Regular data quality monitoring
- **Data Workflows**: Part of larger data processing pipelines
- **Monitoring Systems**: Integration with alerting systems

## Dependencies

### Required
- Python 3.8+
- pandas
- numpy
- requests
- python-dotenv

### Optional
- weasyprint (for PDF generation)
- markdown (for enhanced markdown processing)

## License

This pipeline is part of the Great Expectations Validation Analysis system and follows the same licensing terms.

## Support

For issues or questions:
1. Check the log files for detailed error messages
2. Run the test suite to identify specific problems
3. Verify configuration and environment setup
4. Review the troubleshooting section above
