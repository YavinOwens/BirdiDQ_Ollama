# Data Reporting Pipeline Documentation

This directory contains the complete data reporting pipeline system for Great Expectations validation analysis.

## 📁 Directory Structure

```
test/
├── data_reporting_pipeline.py      # Main pipeline script
├── pipeline_config.json            # Configuration file
├── pipeline_requirements.txt       # Python dependencies
├── test_pipeline.py                # Test suite
├── example_usage.py                # Usage examples
├── README.md                       # Main documentation
├── docs/                           # Additional documentation
│   ├── installation.md
│   ├── configuration.md
│   ├── usage_guide.md
│   └── troubleshooting.md
├── examples/                       # Example configurations
│   ├── basic_config.json
│   ├── advanced_config.json
│   └── custom_config.json
├── outputs/                        # Generated reports (created when pipeline runs)
│   ├── validation_analysis_report_professional.md
│   ├── validation_analysis_report_professional.pdf
│   ├── data_catalog.json
│   └── data_reporting_pipeline.log
└── templates/                      # Report templates
    ├── executive_summary_template.md
    └── pdf_styles.css
```

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
pip install -r pipeline_requirements.txt

# Verify installation
python test_pipeline.py --test analyzer
```

### 2. Basic Usage
```bash
# Run with default configuration
python data_reporting_pipeline.py

# Run with custom output directory
python data_reporting_pipeline.py --output-dir custom_reports

# Run with custom configuration
python data_reporting_pipeline.py --config pipeline_config.json
```

### 3. Test the Pipeline
```bash
# Run all tests
python test_pipeline.py

# Run specific test
python test_pipeline.py --test full
```

## 📊 Generated Outputs

When the pipeline runs successfully, it generates the following files in the `outputs/` directory:

### Reports
- **`validation_analysis_report_professional.md`** - Professional markdown report with AI executive summary
- **`validation_analysis_report_professional.pdf`** - Professional PDF report (if weasyprint is available)

### Data Catalog
- **`data_catalog.json`** - Structured data catalog in JSON format

### Logs
- **`data_reporting_pipeline.log`** - Detailed execution log

## 🔧 Configuration

The pipeline can be configured using the `pipeline_config.json` file:

```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "env_path": "../.env",
  "output_dir": ".",
  "ollama_timeout": 120,
  "pdf_generation": true,
  "ai_analysis": true,
  "data_catalog": true,
  "log_level": "INFO"
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `validation_path` | Path to Great Expectations validation results | `../BirdiDQ/gx/uncommitted/validations` |
| `env_path` | Path to environment configuration file | `../.env` |
| `output_dir` | Output directory for generated reports | `.` (current directory) |
| `ollama_timeout` | Timeout for Ollama API calls (seconds) | `120` |
| `pdf_generation` | Enable PDF report generation | `true` |
| `ai_analysis` | Enable AI-powered analysis | `true` |
| `data_catalog` | Enable data catalog generation | `true` |
| `log_level` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

## 🤖 AI Features

The pipeline includes advanced AI capabilities:

### Executive Summary Generation
- **Target Audience**: C-level executives and decision-makers
- **Language Level**: 15-year-old reading level
- **Length**: 500-800 words maximum
- **Focus**: Business value and strategic importance
- **Format**: Professional board presentation style

### AI Analysis Components
1. **Problem Statement**: Defines the data quality challenge
2. **Solution Approach**: Explains how Great Expectations addresses the problem
3. **Key Findings**: Presents critical insights from the analysis
4. **Business Impact**: Highlights value and benefits
5. **Call to Action**: Provides clear next steps for decision-makers

### Fallback Mechanisms
- **Ollama Cloud Unavailable**: Falls back to local Ollama
- **Local Ollama Unavailable**: Falls back to static analysis
- **PDF Generation Fails**: Continues with markdown output
- **Configuration Errors**: Uses default settings with warnings

## 📈 Performance Metrics

Typical execution times:
- **Small Dataset** (< 100 expectations): 5-10 seconds
- **Medium Dataset** (100-1000 expectations): 10-30 seconds
- **Large Dataset** (> 1000 expectations): 30+ seconds

Performance depends on:
- Number of validation files
- Ollama Cloud API response time
- PDF generation complexity
- System resources

## 🔍 Troubleshooting

### Common Issues

1. **Ollama API Errors**
   - Check API key configuration in `.env`
   - Verify Ollama Cloud connectivity
   - Pipeline will fallback to local Ollama or static analysis

2. **PDF Generation Failures**
   - Install weasyprint: `pip install weasyprint`
   - Check system dependencies for PDF generation
   - Pipeline will continue without PDF output

3. **File Not Found Errors**
   - Verify validation path exists
   - Check file permissions
   - Ensure JSON files are valid

4. **Configuration Errors**
   - Validate JSON configuration syntax
   - Check environment file format
   - Verify all required parameters

### Debug Mode

Enable debug logging:
```json
{
  "log_level": "DEBUG"
}
```

## 🔗 Integration

The pipeline can be integrated into:

- **CI/CD Pipelines**: Automated data quality reporting
- **Scheduled Jobs**: Regular data quality monitoring
- **Data Workflows**: Part of larger data processing pipelines
- **Monitoring Systems**: Integration with alerting systems

## 📚 Additional Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Usage Guide](docs/usage_guide.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## 🆘 Support

For issues or questions:
1. Check the log files for detailed error messages
2. Run the test suite to identify specific problems
3. Verify configuration and environment setup
4. Review the troubleshooting section above

## 📄 License

This pipeline is part of the Great Expectations Validation Analysis system and follows the same licensing terms.
