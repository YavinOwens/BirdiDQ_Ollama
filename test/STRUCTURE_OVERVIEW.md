# Data Reporting Pipeline - Complete Documentation Structure

## 📁 Directory Structure

```
/Users/yavin/python_projects/ollama_jupyter/test/
├── 📄 Core Pipeline Files
│   ├── data_reporting_pipeline.py      # Main pipeline script (915 lines)
│   ├── pipeline_config.json            # Default configuration
│   ├── pipeline_requirements.txt       # Python dependencies
│   └── README.md                       # Main documentation
│
├── 🧪 Testing & Examples
│   ├── test_pipeline.py                # Comprehensive test suite
│   └── example_usage.py                # Usage examples and demonstrations
│
├── 📚 Documentation
│   └── docs/
│       ├── README.md                   # Documentation overview
│       ├── installation.md             # Installation guide
│       ├── configuration.md             # Configuration guide
│       ├── usage_guide.md              # Usage guide
│       └── troubleshooting.md          # Troubleshooting guide
│
├── ⚙️ Configuration Examples
│   └── examples/
│       ├── basic_config.json           # Basic configuration
│       ├── advanced_config.json        # Advanced configuration
│       └── custom_config.json          # Custom configuration
│
├── 🎨 Templates
│   └── templates/
│       ├── executive_summary_template.md # AI executive summary template
│       └── pdf_styles.css               # PDF styling template
│
└── 📊 Generated Outputs (created when pipeline runs)
    └── outputs/
        ├── validation_analysis_report_professional.md
        ├── validation_analysis_report_professional.pdf
        ├── data_catalog.json
        └── data_reporting_pipeline.log
```

## 🚀 Quick Start Commands

### Installation
```bash
cd /Users/yavin/python_projects/ollama_jupyter/test
pip install -r pipeline_requirements.txt
```

### Basic Usage
```bash
# Run with default configuration
python data_reporting_pipeline.py

# Run with custom configuration
python data_reporting_pipeline.py --config examples/basic_config.json

# Run with custom output directory
python data_reporting_pipeline.py --output-dir custom_reports
```

### Testing
```bash
# Run all tests
python test_pipeline.py

# Run specific tests
python test_pipeline.py --test full
python test_pipeline.py --test ai
```

### Examples
```bash
# Run usage examples
python example_usage.py
```

## 📋 File Descriptions

### Core Pipeline Files

| File | Description | Lines |
|------|-------------|-------|
| `data_reporting_pipeline.py` | Main pipeline script with complete functionality | 915 |
| `pipeline_config.json` | Default configuration file | 10 |
| `pipeline_requirements.txt` | Required Python packages | 15 |
| `README.md` | Main documentation and overview | 200+ |

### Testing & Examples

| File | Description | Purpose |
|------|-------------|---------|
| `test_pipeline.py` | Comprehensive test suite | Validation and debugging |
| `example_usage.py` | Usage examples and demonstrations | Learning and reference |

### Documentation

| File | Description | Content |
|------|-------------|---------|
| `docs/README.md` | Documentation overview | Structure and quick start |
| `docs/installation.md` | Installation guide | Step-by-step setup |
| `docs/configuration.md` | Configuration guide | All options and examples |
| `docs/usage_guide.md` | Usage guide | Command line and programmatic usage |
| `docs/troubleshooting.md` | Troubleshooting guide | Common issues and solutions |

### Configuration Examples

| File | Description | Use Case |
|------|-------------|----------|
| `examples/basic_config.json` | Basic configuration | Standard usage |
| `examples/advanced_config.json` | Advanced configuration | Production environments |
| `examples/custom_config.json` | Custom configuration | Specialized requirements |

### Templates

| File | Description | Purpose |
|------|-------------|---------|
| `templates/executive_summary_template.md` | AI executive summary template | Consistent AI output |
| `templates/pdf_styles.css` | PDF styling template | Professional PDF formatting |

## 🎯 Key Features

### ✅ AI-Powered Analysis
- **Ollama Cloud Integration** with gpt-oss:20b model
- **Professional Executive Summary** generation for C-level executives
- **Fallback Mechanisms** when AI is unavailable
- **Strategic Recommendations** and business impact analysis

### ✅ Data Processing
- **Automated Data Loading** from Great Expectations validation files
- **Comprehensive Quality Metrics** calculation
- **Data Catalog Generation** with detailed asset information
- **Exception Handling** and error recovery

### ✅ Professional Reporting
- **Markdown Report Generation** with consistent formatting
- **PDF Report Generation** with A4 formatting and clean styling
- **No Grey Backgrounds** - clean, professional appearance
- **Executive-Ready Format** suitable for board presentations

### ✅ Pipeline Features
- **Command Line Interface** with flexible options
- **Configuration Management** via JSON files
- **Comprehensive Logging** with file and console output
- **Error Handling** with graceful fallbacks
- **Performance Monitoring** with execution timing

## 📊 Generated Outputs

When the pipeline runs successfully, it generates:

### Reports
- **`validation_analysis_report_professional.md`** - Professional markdown report with AI executive summary
- **`validation_analysis_report_professional.pdf`** - Professional PDF report (if weasyprint is available)

### Data Catalog
- **`data_catalog.json`** - Structured data catalog in JSON format

### Logs
- **`data_reporting_pipeline.log`** - Detailed execution log

## 🔧 Configuration Options

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

## 🚀 Usage Examples

### Command Line
```bash
# Basic usage
python data_reporting_pipeline.py

# Custom configuration
python data_reporting_pipeline.py --config examples/advanced_config.json

# Custom output directory
python data_reporting_pipeline.py --output-dir /path/to/reports
```

### Programmatic
```python
from data_reporting_pipeline import DataReportingPipeline

config = {
    'validation_path': '../BirdiDQ/gx/uncommitted/validations',
    'env_path': '../.env',
    'output_dir': 'reports'
}

pipeline = DataReportingPipeline(config)
outputs = pipeline.run_pipeline()
```

## 📈 Performance

Typical execution times:
- **Small Dataset** (< 100 expectations): 5-10 seconds
- **Medium Dataset** (100-1000 expectations): 10-30 seconds
- **Large Dataset** (> 1000 expectations): 30+ seconds

## 🔍 Troubleshooting

### Quick Diagnostics
```bash
# Check system status
python --version
pwd
ls -la data_reporting_pipeline.py

# Run tests
python test_pipeline.py --test analyzer
python test_pipeline.py --test full
```

### Common Issues
1. **Missing Dependencies**: `pip install -r pipeline_requirements.txt`
2. **Permission Errors**: `chmod +x *.py`
3. **Path Issues**: Check validation path exists
4. **API Errors**: Verify Ollama API key in `.env`

## 📚 Documentation

- **Installation**: See `docs/installation.md`
- **Configuration**: See `docs/configuration.md`
- **Usage**: See `docs/usage_guide.md`
- **Troubleshooting**: See `docs/troubleshooting.md`

## 🎉 Success!

The Data Reporting Pipeline is now fully configured and ready for use. All documentation and outputs will be saved in the `/Users/yavin/python_projects/ollama_jupyter/test` folder as requested.

**Next Steps:**
1. Run the test suite to verify functionality
2. Execute the pipeline to generate reports
3. Review generated outputs in the outputs directory
4. Integrate into your workflow as needed
