# Configuration Guide

This guide covers the configuration options for the Data Reporting Pipeline.

## Configuration Files

The pipeline uses JSON configuration files to control its behavior. The main configuration file is `pipeline_config.json`.

## Default Configuration

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

## Configuration Options

### Core Settings

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `validation_path` | string | Path to Great Expectations validation results directory | `../BirdiDQ/gx/uncommitted/validations` |
| `env_path` | string | Path to environment configuration file | `../.env` |
| `output_dir` | string | Output directory for generated reports | `.` (current directory) |

### AI Settings

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `ollama_timeout` | integer | Timeout for Ollama API calls in seconds | `120` |
| `ai_analysis` | boolean | Enable AI-powered analysis | `true` |

### Output Settings

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `pdf_generation` | boolean | Enable PDF report generation | `true` |
| `data_catalog` | boolean | Enable data catalog generation | `true` |

### Logging Settings

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `log_level` | string | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

## Environment Configuration

The pipeline reads additional configuration from environment files (`.env`).

### Required Environment Variables

```bash
# Ollama Cloud Configuration
OLLAMA_CLOUD_BASE_URL=https://ollama.com
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_api_key_here
```

### Optional Environment Variables

```bash
# Local Ollama Fallback
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LOCAL_MODEL=phi3:mini

# Database Configuration (if needed)
POSTGRES_CONNECTION_STRING=postgresql+psycopg2://user:pass@host:port/db
ORACLE_CONNECTION_STRING=oracle+oracledb://user:pass@host:port/service

# Application Settings
LOG_LEVEL=INFO
OUTPUT_DIR=notebooks/outputs
```

## Configuration Examples

### Basic Configuration

```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "env_path": "../.env",
  "output_dir": "reports"
}
```

### Advanced Configuration

```json
{
  "validation_path": "/path/to/validation/results",
  "env_path": "/path/to/.env",
  "output_dir": "/path/to/output",
  "ollama_timeout": 180,
  "pdf_generation": true,
  "ai_analysis": true,
  "data_catalog": true,
  "log_level": "DEBUG"
}
```

### Minimal Configuration

```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "output_dir": "minimal_output",
  "ai_analysis": false,
  "pdf_generation": false
}
```

## Command Line Overrides

You can override configuration settings using command line arguments:

```bash
# Override output directory
python data_reporting_pipeline.py --output-dir custom_reports

# Override validation path
python data_reporting_pipeline.py --validation-path /custom/path

# Override environment file
python data_reporting_pipeline.py --env-path /custom/.env

# Use custom configuration file
python data_reporting_pipeline.py --config custom_config.json
```

## Configuration Validation

The pipeline validates configuration settings and provides helpful error messages:

### Common Validation Errors

1. **Invalid JSON Syntax**
   ```
   Error: Invalid JSON in configuration file
   ```

2. **Missing Required Paths**
   ```
   Error: Validation path does not exist: /path/to/validations
   ```

3. **Invalid Log Level**
   ```
   Error: Invalid log level. Must be one of: DEBUG, INFO, WARNING, ERROR
   ```

## Best Practices

### 1. Use Relative Paths
```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "env_path": "../.env"
}
```

### 2. Organize Outputs
```json
{
  "output_dir": "reports/$(date +%Y%m%d)"
}
```

### 3. Enable Debug Logging for Development
```json
{
  "log_level": "DEBUG"
}
```

### 4. Disable Features When Not Needed
```json
{
  "pdf_generation": false,
  "ai_analysis": false
}
```

## Configuration Templates

### Development Configuration
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

### Production Configuration
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

### Testing Configuration
```json
{
  "validation_path": "../BirdiDQ/gx/uncommitted/validations",
  "env_path": "../.env",
  "output_dir": "test_output",
  "ollama_timeout": 30,
  "pdf_generation": false,
  "ai_analysis": false,
  "data_catalog": true,
  "log_level": "WARNING"
}
```

## Troubleshooting Configuration

### Common Issues

1. **Path Resolution Problems**
   - Use absolute paths for clarity
   - Verify path existence before running
   - Check file permissions

2. **Environment Variable Issues**
   - Verify `.env` file format
   - Check variable names and values
   - Ensure no extra spaces or quotes

3. **JSON Syntax Errors**
   - Validate JSON syntax using online tools
   - Check for missing commas or brackets
   - Verify string quoting

### Debug Configuration

Enable debug logging to troubleshoot configuration issues:

```json
{
  "log_level": "DEBUG"
}
```

This will show detailed information about:
- Configuration file loading
- Path resolution
- Environment variable loading
- Validation results
