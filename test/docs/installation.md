# Installation Guide

This guide covers the installation and setup of the Data Reporting Pipeline.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Access to Great Expectations validation results
- Ollama Cloud API key (optional, for AI features)

## Step 1: Install Python Dependencies

```bash
# Navigate to the test directory
cd /Users/yavin/python_projects/ollama_jupyter/test

# Install required packages
pip install -r pipeline_requirements.txt
```

### Required Packages

The following packages are required for basic functionality:

- `pandas>=1.5.0` - Data processing
- `numpy>=1.21.0` - Numerical operations
- `requests>=2.28.0` - API communication
- `python-dotenv>=0.19.0` - Environment configuration

### Optional Packages

The following packages are optional but recommended:

- `weasyprint>=57.0` - PDF generation
- `markdown>=3.4.0` - Enhanced markdown processing

## Step 2: Configure Environment

### Create Environment File

Create a `.env` file in the parent directory (`/Users/yavin/python_projects/ollama_jupyter/.env`):

```bash
# Ollama Configuration
OLLAMA_CLOUD_BASE_URL=https://ollama.com
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_api_key_here

# Local Ollama (fallback)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LOCAL_MODEL=phi3:mini
```

### Verify Configuration

```bash
# Test the configuration
python test_pipeline.py --test analyzer
```

## Step 3: Verify Installation

### Run Test Suite

```bash
# Run all tests
python test_pipeline.py

# Run specific tests
python test_pipeline.py --test init
python test_pipeline.py --test loading
python test_pipeline.py --test full
```

### Expected Output

You should see output similar to:

```
================================================================================
DATA REPORTING PIPELINE TEST SUITE
================================================================================
Testing ValidationAnalyzer...
✅ ValidationAnalyzer initialized successfully
   Ollama URL: https://ollama.com
   Ollama Model: gpt-oss:20b
   Validation Path: ../BirdiDQ/gx/uncommitted/validations
   Path Exists: True

Testing Pipeline Initialization...
✅ Pipeline initialized successfully
   Output Directory: .
   Config: {'validation_path': '../BirdiDQ/gx/uncommitted/validations', ...}

...

================================================================================
TEST SUMMARY
================================================================================
Tests Passed: 8
Tests Failed: 0
Total Tests: 8
🎉 All tests passed!
```

## Step 4: Test Pipeline Execution

### Run Example

```bash
# Run the example usage script
python example_usage.py
```

### Manual Test

```bash
# Run the pipeline with default settings
python data_reporting_pipeline.py
```

## Troubleshooting Installation

### Common Issues

1. **Permission Errors**
   ```bash
   # Fix permission issues
   chmod +x data_reporting_pipeline.py
   chmod +x test_pipeline.py
   chmod +x example_usage.py
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r pipeline_requirements.txt
   ```

3. **Python Version Issues**
   ```bash
   # Check Python version
   python --version
   
   # Should be 3.8 or higher
   ```

4. **Path Issues**
   ```bash
   # Verify you're in the correct directory
   pwd
   # Should show: /Users/yavin/python_projects/ollama_jupyter/test
   ```

### Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] Environment file configured
- [ ] Validation path exists
- [ ] Test suite passes
- [ ] Pipeline runs successfully

## Next Steps

After successful installation:

1. **Configure the pipeline** for your specific needs
2. **Run the test suite** to verify functionality
3. **Execute the pipeline** to generate reports
4. **Review generated outputs** in the outputs directory
5. **Integrate into your workflow** as needed

## Support

If you encounter issues during installation:

1. Check the troubleshooting section above
2. Review the log files for error messages
3. Verify all prerequisites are met
4. Run the test suite for detailed diagnostics
