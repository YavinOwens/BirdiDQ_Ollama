# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Data Reporting Pipeline.

## Quick Diagnostics

### Check System Status

```bash
# Verify Python version
python --version
# Should be 3.8 or higher

# Check if you're in the right directory
pwd
# Should show: /Users/yavin/python_projects/ollama_jupyter/test

# Verify files exist
ls -la data_reporting_pipeline.py pipeline_config.json
```

### Run Basic Tests

```bash
# Test analyzer initialization
python test_pipeline.py --test analyzer

# Test data loading
python test_pipeline.py --test loading

# Test full pipeline
python test_pipeline.py --test full
```

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: Missing Dependencies
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
# Install dependencies
pip install -r pipeline_requirements.txt

# Or install individually
pip install pandas numpy requests python-dotenv
```

#### Problem: Permission Denied
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Make scripts executable
chmod +x data_reporting_pipeline.py
chmod +x test_pipeline.py
chmod +x example_usage.py

# Or run with python explicitly
python data_reporting_pipeline.py
```

#### Problem: Python Version Too Old
```
SyntaxError: invalid syntax
```

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.8+ if needed
# On macOS with Homebrew:
brew install python@3.9

# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.9
```

### 2. Configuration Issues

#### Problem: Invalid JSON Configuration
```
json.decoder.JSONDecodeError: Expecting ',' delimiter
```

**Solution:**
```bash
# Validate JSON syntax
python -m json.tool pipeline_config.json

# Common JSON errors:
# - Missing commas between objects
# - Unquoted strings
# - Trailing commas
# - Mismatched brackets
```

#### Problem: Path Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: '../BirdiDQ/gx/uncommitted/validations'
```

**Solution:**
```bash
# Check if path exists
ls -la ../BirdiDQ/gx/uncommitted/validations

# Use absolute path if needed
python data_reporting_pipeline.py --validation-path /absolute/path/to/validations
```

#### Problem: Environment File Issues
```
KeyError: 'OLLAMA_API_KEY'
```

**Solution:**
```bash
# Check .env file exists
ls -la ../.env

# Verify .env file format
cat ../.env

# Should contain:
# OLLAMA_CLOUD_BASE_URL=https://ollama.com
# OLLAMA_CLOUD_MODEL=gpt-oss:20b
# OLLAMA_API_KEY=your_api_key_here
```

### 3. Data Loading Issues

#### Problem: No Validation Files Found
```
Loaded 0 validation files
```

**Solution:**
```bash
# Check validation directory structure
find ../BirdiDQ/gx/uncommitted/validations -name "*.json" | head -5

# Verify Great Expectations setup
ls -la ../BirdiDQ/gx/uncommitted/validations/

# Check file permissions
ls -la ../BirdiDQ/gx/uncommitted/validations/*/
```

#### Problem: Invalid JSON Files
```
json.decoder.JSONDecodeError: Invalid control character
```

**Solution:**
```bash
# Validate JSON files
python -c "
import json
import glob
for file in glob.glob('../BirdiDQ/gx/uncommitted/validations/**/*.json', recursive=True):
    try:
        with open(file, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f'Invalid JSON in {file}: {e}')
"
```

### 4. AI Analysis Issues

#### Problem: Ollama API Timeout
```
requests.exceptions.Timeout: HTTPConnectionPool timeout
```

**Solution:**
```bash
# Increase timeout in configuration
# Edit pipeline_config.json:
{
  "ollama_timeout": 180
}

# Or test Ollama connection manually
curl -X POST https://ollama.com/api/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"model": "gpt-oss:20b", "prompt": "test", "stream": false}'
```

#### Problem: Unauthorized API Call
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**Solution:**
```bash
# Check API key in .env file
grep OLLAMA_API_KEY ../.env

# Verify API key format
# Should be: OLLAMA_API_KEY=your_actual_api_key_here

# Test API key manually
curl -X POST https://ollama.com/api/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACTUAL_API_KEY" \
  -d '{"model": "gpt-oss:20b", "prompt": "test", "stream": false}'
```

#### Problem: AI Analysis Falls Back to Static
```
⚠️ AI unavailable, using fallback executive summary...
```

**Solution:**
```bash
# Check network connectivity
ping ollama.com

# Verify API key is valid
# Check .env file format
# Ensure no extra spaces or quotes around API key
```

### 5. PDF Generation Issues

#### Problem: PDF Generation Fails
```
ImportError: Missing optional dependency 'weasyprint'
```

**Solution:**
```bash
# Install weasyprint
pip install weasyprint

# On macOS, you may need system dependencies:
brew install cairo pango gdk-pixbuf libffi

# On Ubuntu/Debian:
sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev
```

#### Problem: PDF Styling Issues
```
PDF generated but formatting is incorrect
```

**Solution:**
```bash
# Check CSS styling in the pipeline
# Verify weasyprint version
pip show weasyprint

# Test with minimal PDF
python -c "
from weasyprint import HTML, CSS
html = HTML(string='<h1>Test</h1>')
css = CSS(string='h1 { color: red; }')
html.write_pdf('test.pdf', stylesheets=[css])
"
```

### 6. Performance Issues

#### Problem: Pipeline Runs Slowly
```
Pipeline execution time: 300+ seconds
```

**Solution:**
```bash
# Enable debug logging to identify bottlenecks
# Edit pipeline_config.json:
{
  "log_level": "DEBUG"
}

# Check system resources
top
df -h

# Consider reducing timeout for faster failure
{
  "ollama_timeout": 60
}
```

#### Problem: Memory Issues
```
MemoryError: Unable to allocate array
```

**Solution:**
```bash
# Check available memory
free -h

# Process smaller batches
# Consider disabling PDF generation temporarily
{
  "pdf_generation": false
}
```

## Debug Mode

### Enable Debug Logging

```json
{
  "log_level": "DEBUG"
}
```

### Debug Output Example

```
2025-01-07 10:30:15 - DEBUG - Loading configuration from pipeline_config.json
2025-01-07 10:30:15 - DEBUG - Validation path: ../BirdiDQ/gx/uncommitted/validations
2025-01-07 10:30:15 - DEBUG - Path exists: True
2025-01-07 10:30:15 - DEBUG - Found 5 JSON files
2025-01-07 10:30:15 - DEBUG - Processing file: validation_001.json
2025-01-07 10:30:15 - DEBUG - Loaded 132 expectations
2025-01-07 10:30:16 - DEBUG - Calculating quality metrics
2025-01-07 10:30:16 - DEBUG - Overall success rate: 0.9621
2025-01-07 10:30:16 - DEBUG - Generating AI insights
2025-01-07 10:30:16 - DEBUG - Calling Ollama API
2025-01-07 10:30:45 - DEBUG - AI response received (29 seconds)
```

## Log Analysis

### Check Log Files

```bash
# View recent log entries
tail -f data_reporting_pipeline.log

# Search for errors
grep -i error data_reporting_pipeline.log

# Search for warnings
grep -i warning data_reporting_pipeline.log

# Count log entries by level
grep -c "INFO\|DEBUG\|WARNING\|ERROR" data_reporting_pipeline.log
```

### Common Log Patterns

#### Successful Execution
```
2025-01-07 10:30:15 - INFO - Data Reporting Pipeline initialized
2025-01-07 10:30:16 - INFO - Loaded 5 validation files
2025-01-07 10:30:17 - INFO - Processed 132 individual expectations
2025-01-07 10:30:18 - INFO - Overall Success Rate: 96.21%
2025-01-07 10:30:45 - INFO - AI Analysis Complete!
2025-01-07 10:30:46 - INFO - Data assets cataloged: 1
2025-01-07 10:30:47 - INFO - Pipeline execution successful
```

#### Failed Execution
```
2025-01-07 10:30:15 - ERROR - Validation path does not exist: /invalid/path
2025-01-07 10:30:16 - ERROR - Pipeline initialization failed
```

## Recovery Procedures

### Reset Configuration

```bash
# Backup current configuration
cp pipeline_config.json pipeline_config.json.backup

# Restore default configuration
cat > pipeline_config.json << EOF
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
EOF
```

### Clean Output Directory

```bash
# Remove old outputs
rm -rf outputs/
mkdir outputs

# Or clean specific files
rm -f *.md *.pdf *.json *.log
```

### Reinstall Dependencies

```bash
# Uninstall and reinstall
pip uninstall -r pipeline_requirements.txt -y
pip install -r pipeline_requirements.txt

# Or force reinstall
pip install --force-reinstall -r pipeline_requirements.txt
```

## Getting Help

### Self-Diagnosis Checklist

- [ ] Python version is 3.8 or higher
- [ ] All dependencies are installed
- [ ] Configuration file is valid JSON
- [ ] Validation path exists and contains JSON files
- [ ] Environment file exists and contains required variables
- [ ] Output directory is writable
- [ ] Network connectivity to Ollama Cloud
- [ ] API key is valid and properly formatted

### When to Seek Additional Help

If you've tried the solutions above and still have issues:

1. **Collect Information:**
   - Python version: `python --version`
   - Operating system: `uname -a`
   - Error messages: Copy full error output
   - Log files: Include relevant log entries
   - Configuration: Share your config file (remove sensitive data)

2. **Reproduce the Issue:**
   - Run the test suite: `python test_pipeline.py`
   - Try minimal configuration
   - Test individual components

3. **Document the Problem:**
   - What you were trying to do
   - What happened instead
   - Steps to reproduce
   - System information
   - Error messages and logs
