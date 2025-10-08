# Usage Guide

This guide covers how to use the Data Reporting Pipeline effectively.

## Basic Usage

### Command Line Interface

The pipeline provides a command line interface with several options:

```bash
# Basic usage with default configuration
python data_reporting_pipeline.py

# Use custom configuration file
python data_reporting_pipeline.py --config custom_config.json

# Override specific settings
python data_reporting_pipeline.py --output-dir reports --validation-path /path/to/validations
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--config` | Path to configuration JSON file | `--config pipeline_config.json` |
| `--output-dir` | Output directory for reports | `--output-dir /path/to/reports` |
| `--validation-path` | Path to validation results | `--validation-path /path/to/validations` |
| `--env-path` | Path to environment file | `--env-path /path/to/.env` |

## Programmatic Usage

### Basic Example

```python
from data_reporting_pipeline import DataReportingPipeline

# Configuration
config = {
    'validation_path': '../BirdiDQ/gx/uncommitted/validations',
    'env_path': '../.env',
    'output_dir': 'reports'
}

# Initialize and run pipeline
pipeline = DataReportingPipeline(config)
outputs = pipeline.run_pipeline()

# Access generated files
print("Generated outputs:")
for output_type, output_path in outputs.items():
    print(f"  {output_type}: {output_path}")
```

### Advanced Example

```python
from data_reporting_pipeline import DataReportingPipeline
import json

# Load configuration from file
with open('custom_config.json', 'r') as f:
    config = json.load(f)

# Initialize pipeline
pipeline = DataReportingPipeline(config)

# Run individual steps
pipeline.load_validation_files()
pipeline.process_validation_results()
pipeline.calculate_quality_metrics()
pipeline.generate_ai_insights()
pipeline.generate_data_catalog()

# Generate custom report
report = pipeline.generate_professional_report()

# Save to custom location
with open('custom_report.md', 'w') as f:
    f.write(report)
```

## Configuration Examples

### Development Setup

```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "env_path": "../.env",
  "output_dir": "dev_output",
  "ollama_timeout": 60,
  "pdf_generation": false,
  "ai_analysis": true,
  "data_catalog": true,
  "log_level": "DEBUG"
}
```

### Production Setup

```json
{
  "validation_path": "/data/validations",
  "env_path": "/config/.env",
  "output_dir": "/reports",
  "ollama_timeout": 120,
  "pdf_generation": true,
  "ai_analysis": true,
  "data_catalog": true,
  "log_level": "INFO"
}
```

## Output Files

### Generated Reports

The pipeline generates several output files:

#### Markdown Report
- **File**: `validation_analysis_report_professional.md`
- **Content**: Professional analysis report with AI executive summary
- **Format**: Markdown with tables and structured sections

#### PDF Report
- **File**: `validation_analysis_report_professional.pdf`
- **Content**: Professional PDF version of the markdown report
- **Format**: A4 format with clean styling (no grey backgrounds)

#### Data Catalog
- **File**: `data_catalog.json`
- **Content**: Structured data catalog in JSON format
- **Usage**: Programmatic access to data asset information

#### Log File
- **File**: `data_reporting_pipeline.log`
- **Content**: Detailed execution log
- **Usage**: Debugging and monitoring

### Report Structure

The generated reports include:

1. **Executive Summary** - AI-generated summary for C-level executives
2. **Critical Findings** - Top issues requiring attention
3. **Data Quality Analysis** - Comprehensive metrics and performance data
4. **AI-Powered Analysis** - Intelligent insights and recommendations
5. **Data Catalog Summary** - Overview of data assets and expectation suites
6. **Recommendations** - Actionable next steps
7. **Technical Details** - System information and metadata

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# GitHub Actions example
name: Data Quality Report
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday at 9 AM

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd test
          pip install -r pipeline_requirements.txt
      - name: Generate report
        run: |
          cd test
          python data_reporting_pipeline.py --output-dir reports
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: data-quality-reports
          path: test/reports/
```

### Scheduled Execution

```bash
#!/bin/bash
# Daily data quality report script

# Set variables
SCRIPT_DIR="/Users/yavin/python_projects/ollama_jupyter/test"
OUTPUT_DIR="/reports/$(date +%Y%m%d)"
LOG_FILE="/logs/pipeline_$(date +%Y%m%d).log"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run pipeline
cd "$SCRIPT_DIR"
python data_reporting_pipeline.py \
  --output-dir "$OUTPUT_DIR" \
  --config pipeline_config.json \
  2>&1 | tee "$LOG_FILE"

# Send notification
if [ $? -eq 0 ]; then
    echo "Data quality report generated successfully" | mail -s "Daily Data Quality Report" admin@company.com
else
    echo "Data quality report generation failed" | mail -s "Daily Data Quality Report - ERROR" admin@company.com
fi
```

### Python Script Integration

```python
import subprocess
import json
from datetime import datetime
from pathlib import Path

def generate_daily_report():
    """Generate daily data quality report"""
    
    # Configuration
    config = {
        'validation_path': '../BirdiDQ/gx/uncommitted/validations',
        'env_path': '../.env',
        'output_dir': f'reports/{datetime.now().strftime("%Y%m%d")}',
        'log_level': 'INFO'
    }
    
    # Save configuration
    config_file = 'daily_config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Run pipeline
    try:
        result = subprocess.run([
            'python', 'data_reporting_pipeline.py',
            '--config', config_file
        ], capture_output=True, text=True, check=True)
        
        print("Report generated successfully!")
        print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    finally:
        # Clean up
        Path(config_file).unlink(missing_ok=True)

if __name__ == "__main__":
    generate_daily_report()
```

## Testing and Validation

### Run Test Suite

```bash
# Run all tests
python test_pipeline.py

# Run specific tests
python test_pipeline.py --test analyzer
python test_pipeline.py --test full
python test_pipeline.py --test ai
```

### Validate Outputs

```python
from pathlib import Path
import json

def validate_outputs(output_dir="."):
    """Validate that all expected outputs were generated"""
    
    expected_files = [
        'validation_analysis_report_professional.md',
        'validation_analysis_report_professional.pdf',
        'data_catalog.json',
        'data_reporting_pipeline.log'
    ]
    
    missing_files = []
    for file in expected_files:
        if not Path(output_dir) / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    
    # Validate JSON structure
    try:
        with open(Path(output_dir) / 'data_catalog.json', 'r') as f:
            catalog = json.load(f)
        
        required_keys = ['metadata', 'data_assets', 'expectation_suites']
        for key in required_keys:
            if key not in catalog:
                print(f"Missing key in data catalog: {key}")
                return False
                
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in data catalog: {e}")
        return False
    
    print("All outputs validated successfully!")
    return True

# Usage
validate_outputs()
```

## Best Practices

### 1. Use Version Control
- Keep configuration files in version control
- Track changes to pipeline settings
- Document configuration decisions

### 2. Monitor Performance
- Log execution times
- Monitor resource usage
- Set up alerts for failures

### 3. Organize Outputs
- Use date-based directories
- Archive old reports
- Maintain consistent naming

### 4. Error Handling
- Implement retry logic
- Set up fallback mechanisms
- Monitor for failures

### 5. Security
- Secure API keys
- Limit file permissions
- Audit access logs

## Troubleshooting

### Common Issues

1. **Pipeline Fails to Start**
   - Check Python version (3.8+)
   - Verify dependencies are installed
   - Check configuration file syntax

2. **No Output Files Generated**
   - Verify output directory permissions
   - Check validation path exists
   - Review log files for errors

3. **AI Analysis Fails**
   - Check Ollama API key
   - Verify network connectivity
   - Review timeout settings

4. **PDF Generation Fails**
   - Install weasyprint: `pip install weasyprint`
   - Check system dependencies
   - Verify CSS styling

### Debug Mode

Enable debug logging for detailed troubleshooting:

```json
{
  "log_level": "DEBUG"
}
```

This provides detailed information about:
- Configuration loading
- File processing
- API calls
- Error conditions
