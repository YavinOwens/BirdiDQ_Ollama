# Streamlit Data Upload Application

A user-friendly web application for uploading data files and running automated data quality validation using Great Expectations with Pandas execution engine.

## Features

### 📁 **Data Upload**
- Support for multiple file formats: CSV, Excel (XLSX/XLS), JSON, Parquet
- Automatic file format detection
- Real-time data preview and statistics

### 📊 **Data Analysis**
- Interactive data overview with key metrics
- Missing values heatmap visualization
- Data types and column information
- Statistical summaries

### 🔍 **Data Validation**
- **Missingness Data Assistant**: Automatically detects and analyzes missing data patterns
- **Onboarding Data Assistant**: Creates comprehensive data quality expectations
- **Automated Expectations**: Generates specialized expectations for your data
- **Validation Results**: Clear pass/fail indicators with detailed statistics

### 💾 **Results & Downloads**
- Validation summary with full statistics
- Download processed data in CSV format
- JSON summary for integration with other tools
- Timestamped results for tracking

## Quick Start

### 1. Install Dependencies
```bash
pip install -r streamlit_requirements.txt
```

### 2. Run the Application
```bash
streamlit run streamlit_data_upload_app.py
```

### 3. Open in Browser
The application will automatically open at `http://localhost:8501`

## Usage Guide

### Step 1: Upload Data
1. Click "Browse files" in the file upload section
2. Select your data file (CSV, Excel, JSON, or Parquet)
3. Wait for automatic data loading and preview

### Step 2: Review Data Overview
- Review row count, column count, and missing values
- Examine data statistics and distribution
- Check data types and column information
- Explore missing values heatmap

### Step 3: Run Validation
1. Click "🚀 Run Data Quality Validation"
2. Wait for Great Expectations processing (may take 30-60 seconds)
3. Review validation results:
   - **Missingness Analysis**: Identifies null/missing data patterns
   - **Onboarding Analysis**: Creates data quality expectations
   - **Pass/Fail Status**: Clear indicators for each validation

### Step 4: Download Results
- **Validation Summary**: JSON file with complete validation statistics
- **Processed Data**: Clean CSV file ready for further analysis

## Technical Details

### Execution Engine
- **Pandas**: Uses Pandas execution engine for optimal performance with small to medium datasets
- **Memory Efficient**: Processes data in-memory for fast validation
- **Cross-Platform**: Works on any system with Python support

### Great Expectations Integration
- **Data Assistants**: Automated expectation generation
- **Expectation Suites**: Organized validation rules
- **Checkpoints**: Automated validation execution
- **Statistics**: Comprehensive validation metrics

### Supported Data Types
- **Numeric**: Integer, Float, Decimal validation
- **Categorical**: String, Text, Category validation
- **DateTime**: Timestamp, Date, Time validation
- **Boolean**: True/False validation
- **Mixed**: Automatic type detection and validation

## Sample Expectations Generated

### Missingness Data Assistant
- `expect_column_values_to_not_be_null`
- `expect_column_values_to_be_null`
- `expect_column_values_to_be_unique`
- Column completeness expectations

### Onboarding Data Assistant
- `expect_column_values_to_be_between`
- `expect_column_values_to_be_in_set`
- `expect_column_values_to_match_regex`
- Statistical expectations (mean, median, std dev)
- Cardinality expectations

## File Format Examples

### CSV Format
```csv
name,age,city,salary
John,25,New York,50000
Jane,30,San Francisco,60000
```

### Excel Format
- Supports `.xlsx` and `.xls` files
- Multiple sheet support (first sheet used)
- Automatic data type detection

### JSON Format
```json
[
  {"name": "John", "age": 25, "city": "New York"},
  {"name": "Jane", "age": 30, "city": "San Francisco"}
]
```

### Parquet Format
- Optimal for large datasets
- Preserves data types accurately
- Fast loading performance

## Troubleshooting

### Common Issues

**File Upload Fails**
- Check file format is supported
- Ensure file is not corrupted
- Verify file size (recommended < 100MB)

**Validation Takes Too Long**
- Large files may take 1-2 minutes
- Consider using smaller sample datasets for testing
- Check system memory availability

**Memory Issues**
- Close other applications to free memory
- Use Parquet format for large files
- Consider data preprocessing before upload

### Error Messages

**"Error loading data"**
- File format not recognized
- File is corrupted or password protected
- Data encoding issues (try UTF-8)

**"Great Expectations initialization failed"**
- Check Great Expectations installation
- Verify configuration files exist
- Restart the application

## Advanced Usage

### Data Preparation Tips
- **Headers**: Ensure first row contains column names
- **Data Types**: Consistent formats within columns
- **Missing Values**: Consider how null values are represented
- **Encoding**: Use UTF-8 encoding for text data

### Best Practices
- **Sample Data**: Test with small datasets first
- **Regular Validation**: Run validation after data updates
- **Documentation**: Save validation summaries for audit trails
- **Integration**: Use JSON summaries for automated workflows

## Limitations

- **File Size**: Recommended < 100MB for optimal performance
- **Execution Engine**: Uses Pandas (not Spark) for processing
- **Web Interface**: Single user at a time
- **Temporary Storage**: Data is processed in-memory only

## Future Enhancements

- [ ] Support for Spark execution engine
- [ ] Multi-user collaboration features
- [ ] Custom expectation definitions
- [ ] Integration with data warehouses
- [ ] Automated data profiling reports
- [ ] Real-time data validation APIs

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Great Expectations documentation
3. Check Streamlit documentation for UI issues
4. Open an issue in the repository

---

**Built with ❤️ using BirdiDQ, Great Expectations, and Streamlit**
