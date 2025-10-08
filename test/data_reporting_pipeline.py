#!/usr/bin/env python3
"""
Great Expectations Data Reporting Pipeline

This script replicates the end-to-end process from the validation_analysis.ipynb notebook
as a standalone Python script for automated data quality reporting.

Features:
- Automated data loading and processing
- AI-powered analysis with Ollama Cloud
- Professional PDF report generation
- Data catalog creation
- Mermaid diagram generation
- Comprehensive error handling and logging

Usage:
    python data_reporting_pipeline.py [--config CONFIG_FILE] [--output-dir OUTPUT_DIR]

Author: Great Expectations Validation Analysis System
Version: 1.0
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
import requests
from dotenv import dotenv_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_reporting_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ValidationAnalyzer:
    """Main analyzer class for Great Expectations validation results"""
    
    def __init__(self, validation_path: str, env_path: str = ".env", config: Optional[Dict] = None):
        """Initialize the validation analyzer"""
        self.validation_path = Path(validation_path)
        self.results_data = []
        self.analysis_results = {}
        self.config = config or {}
        
        # Load environment configuration
        self._load_environment_config(env_path)
        
        logger.info(f"Validation Analyzer initialized")
        logger.info(f"Ollama URL: {self.ollama_url}")
        logger.info(f"Ollama Model: {self.ollama_model}")
        logger.info(f"API Key configured: {'Yes' if self.ollama_api_key and self.ollama_api_key != 'your_api_key_here' else 'No'}")
        logger.info(f"Validation path: {self.validation_path}")
        logger.info(f"Path exists: {self.validation_path.exists()}")
    
    def _load_environment_config(self, env_path: str):
        """Load Ollama configuration from environment file or config fallback"""
        env_file = Path(env_path)
        logger.info(f"Looking for environment file at: {env_file.absolute()}")
        logger.info(f"Environment file exists: {env_file.exists()}")
        
        # Try to load from environment file first
        if env_file.exists():
            env_vars = dotenv_values(env_file)
            logger.info(f"Loaded environment variables: {list(env_vars.keys())}")
            
            # Use Ollama Cloud settings from .env file
            self.ollama_url = env_vars.get("OLLAMA_CLOUD_BASE_URL", "https://ollama.com")
            self.ollama_model = env_vars.get("OLLAMA_CLOUD_MODEL", "gpt-oss:20b")
            self.ollama_api_key = env_vars.get("OLLAMA_API_KEY", "")
            
            logger.info(f"API Key from env: {self.ollama_api_key[:10]}..." if self.ollama_api_key else "No API key found")
            
            # Fallback to local if cloud is not configured
            if not self.ollama_api_key or self.ollama_api_key == "your_api_key_here":
                logger.warning("No valid API key found in env file, falling back to local Ollama")
                self.ollama_url = env_vars.get("OLLAMA_BASE_URL", "http://localhost:11434")
                self.ollama_model = env_vars.get("OLLAMA_LOCAL_MODEL", "phi3:mini")
                self.ollama_api_key = ""
            else:
                logger.info("Using Ollama Cloud configuration from env file")
        else:
            # Fallback to config file settings
            logger.warning(f"Environment file not found at {env_file.absolute()}, trying config file fallback")
            ollama_config = self.config.get('ollama_config', {})
            
            if ollama_config.get('api_key') and ollama_config.get('api_key') != 'your_api_key_here':
                logger.info("Using Ollama Cloud configuration from config file")
                self.ollama_url = ollama_config.get('cloud_url', 'https://ollama.com')
                self.ollama_model = ollama_config.get('cloud_model', 'gpt-oss:20b')
                self.ollama_api_key = ollama_config.get('api_key', '')
            else:
                logger.warning("No valid API key in config file, using local Ollama defaults")
                self.ollama_url = ollama_config.get('local_url', 'http://localhost:11434')
                self.ollama_model = ollama_config.get('local_model', 'phi3:mini')
                self.ollama_api_key = ""
    
    def ollama_infer(self, prompt: str, model: Optional[str] = None, 
                    url: Optional[str] = None, timeout: int = 120) -> Optional[str]:
        """Send a prompt to Ollama and return the response"""
        model = model or self.ollama_model
        url = url or self.ollama_url
        
        # Prepare headers
        headers = {"Content-Type": "application/json"}
        
        # Add API key if available (for Ollama Cloud)
        if self.ollama_api_key and self.ollama_api_key != "your_api_key_here":
            headers["Authorization"] = f"Bearer {self.ollama_api_key}"
        
        try:
            response = requests.post(
                f"{url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.Timeout:
            logger.error(f"Ollama request timed out after {timeout} seconds")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            return None


class DataReportingPipeline:
    """Main pipeline class for data quality reporting"""
    
    def __init__(self, config: Dict):
        """Initialize the data reporting pipeline"""
        self.config = config
        self.analyzer = ValidationAnalyzer(
            validation_path=config.get('validation_path', 'BirdiDQ/gx/uncommitted/validations'),
            env_path=config.get('env_path', '/Users/yavin/python_projects/ollama_jupyter/.env'),
            config=config
        )
        self.output_dir = Path(config.get('output_dir', '.'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data containers
        self.validation_files = []
        self.df = None
        self.quality_metrics = {}
        self.data_catalog = {}
        self.ai_insights = ""
        self.data_summary = {}
        
        logger.info("Data Reporting Pipeline initialized")
    
    def load_validation_files(self) -> List[Dict]:
        """Load all validation JSON files from the directory structure"""
        logger.info("Loading validation files...")
        validation_files = []
        
        # Find all JSON files in the validation directory
        for json_file in self.analyzer.validation_path.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    validation_files.append({
                        'file_path': str(json_file),
                        'data': data,
                        'timestamp': data.get('meta', {}).get('validation_time', ''),
                        'suite_name': data.get('meta', {}).get('expectation_suite_name', ''),
                        'run_id': data.get('meta', {}).get('run_id', {}).get('run_name', ''),
                        'data_asset': data.get('meta', {}).get('active_batch_definition', {}).get('data_asset_name', '')
                    })
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
        
        self.validation_files = validation_files
        logger.info(f"Loaded {len(validation_files)} validation files")
        return validation_files
    
    def process_validation_results(self) -> pd.DataFrame:
        """Process validation results into structured data"""
        logger.info("Processing validation results...")
        processed_data = []
        
        for file_info in self.validation_files:
            data = file_info['data']
            results = data.get('results', [])
            
            for result in results:
                expectation_config = result.get('expectation_config', {})
                exception_info = result.get('exception_info', {})
                
                processed_data.append({
                    'file_path': file_info['file_path'],
                    'timestamp': file_info['timestamp'],
                    'suite_name': file_info['suite_name'],
                    'run_id': file_info['run_id'],
                    'data_asset': file_info['data_asset'],
                    'expectation_type': expectation_config.get('expectation_type', ''),
                    'column': expectation_config.get('kwargs', {}).get('column', 'table-level'),
                    'success': result.get('success', False),
                    'exception_raised': exception_info.get('raised_exception', False),
                    'exception_message': exception_info.get('exception_message', ''),
                    'result': result.get('result', {}),
                    'meta': expectation_config.get('meta', {})
                })
        
        self.df = pd.DataFrame(processed_data)
        logger.info(f"Processed {len(self.df)} individual expectations")
        logger.info(f"Unique expectation suites: {self.df['suite_name'].nunique()}")
        logger.info(f"Unique expectation types: {self.df['expectation_type'].nunique()}")
        return self.df
    
    def calculate_quality_metrics(self) -> Dict:
        """Calculate comprehensive data quality metrics"""
        logger.info("Calculating quality metrics...")
        metrics = {}
        
        # Overall success rate
        metrics['overall_success_rate'] = self.df['success'].mean()
        
        # Success rate by expectation suite
        suite_metrics = self.df.groupby('suite_name').agg({
            'success': ['count', 'sum', 'mean'],
            'exception_raised': 'sum'
        }).round(3)
        suite_metrics.columns = ['total_expectations', 'successful_expectations', 'success_rate', 'exceptions']
        metrics['suite_metrics'] = suite_metrics
        
        # Success rate by expectation type
        type_metrics = self.df.groupby('expectation_type').agg({
            'success': ['count', 'sum', 'mean'],
            'exception_raised': 'sum'
        }).round(3)
        type_metrics.columns = ['total_expectations', 'successful_expectations', 'success_rate', 'exceptions']
        metrics['type_metrics'] = type_metrics
        
        # Column-level analysis
        column_metrics = self.df[self.df['column'] != 'table-level'].groupby('column').agg({
            'success': ['count', 'sum', 'mean'],
            'exception_raised': 'sum'
        }).round(3)
        column_metrics.columns = ['total_expectations', 'successful_expectations', 'success_rate', 'exceptions']
        metrics['column_metrics'] = column_metrics
        
        # Exception analysis
        exception_df = self.df[self.df['exception_raised'] == True]
        metrics['exception_count'] = len(exception_df)
        metrics['exception_rate'] = len(exception_df) / len(self.df)
        
        self.quality_metrics = metrics
        
        logger.info(f"Overall Success Rate: {metrics['overall_success_rate']:.2%}")
        logger.info(f"Exception Rate: {metrics['exception_rate']:.2%}")
        logger.info(f"Total Expectations Analyzed: {len(self.df)}")
        
        return metrics
    
    def generate_ai_insights(self) -> Tuple[str, Dict]:
        """Generate AI-powered insights using Ollama Cloud with fallback"""
        logger.info("Generating AI insights with Ollama Cloud...")
        
        # Prepare data summary for AI analysis
        data_summary = {
            'total_expectations': len(self.df),
            'overall_success_rate': self.quality_metrics['overall_success_rate'],
            'exception_rate': self.quality_metrics['exception_rate'],
            'suite_count': self.df['suite_name'].nunique(),
            'expectation_types': self.df['expectation_type'].nunique(),
            'date_range': f"{self.df['timestamp'].min()} to {self.df['timestamp'].max()}",
            'top_failing_suites': self.quality_metrics['suite_metrics'].nsmallest(3, 'success_rate').to_dict(),
            'top_failing_types': self.quality_metrics['type_metrics'].nsmallest(3, 'success_rate').to_dict()
        }
        
        prompt = f"""
        You are a data quality expert analyzing Great Expectations validation results. 

        Data Summary:
        - Total Expectations: {data_summary['total_expectations']}
        - Overall Success Rate: {data_summary['overall_success_rate']:.2%}
        - Exception Rate: {data_summary['exception_rate']:.2%}
        - Number of Suites: {data_summary['suite_count']}
        - Number of Expectation Types: {data_summary['expectation_types']}
        - Date Range: {data_summary['date_range']}

        Top Failing Suites:
        {data_summary['top_failing_suites']}

        Top Failing Expectation Types:
        {data_summary['top_failing_types']}

        Please provide:
        1. **Executive Summary**: Key findings and overall data quality assessment
        2. **Critical Issues**: Most important problems that need immediate attention
        3. **Trends Analysis**: Patterns and trends observed in the data
        4. **Recommendations**: Specific actionable recommendations to improve data quality
        5. **Risk Assessment**: Potential risks and their impact
        6. **Next Steps**: Prioritized action items

        Format your response as a professional data quality report with clear sections and actionable insights.
        """
        
        ai_response = self.analyzer.ollama_infer(prompt)
        
        # Use fallback if AI is unavailable
        if ai_response is None:
            logger.warning("Ollama Cloud unavailable, using fallback analysis...")
            ai_response = self._generate_fallback_analysis()
        
        self.ai_insights = ai_response
        self.data_summary = data_summary
        
        logger.info("AI Analysis Complete!")
        return ai_response, data_summary
    
    def _generate_fallback_analysis(self) -> str:
        """Generate fallback analysis when AI is unavailable"""
        fallback_analysis = f"""
## Executive Summary
Based on the analysis of {len(self.df)} data quality expectations across {self.df['suite_name'].nunique()} validation suites, the overall data quality success rate is {self.quality_metrics['overall_success_rate']:.2%}.

## Critical Issues
- **Exception Rate**: {self.quality_metrics['exception_rate']:.2%} of expectations raised exceptions
- **Lowest Performing Suite**: {self.quality_metrics['suite_metrics'].nsmallest(1, 'success_rate').index[0]} with {self.quality_metrics['suite_metrics'].nsmallest(1, 'success_rate')['success_rate'].iloc[0]:.2%} success rate
- **Most Problematic Expectation Type**: {self.quality_metrics['type_metrics'].nsmallest(1, 'success_rate').index[0]} with {self.quality_metrics['type_metrics'].nsmallest(1, 'success_rate')['success_rate'].iloc[0]:.2%} success rate

## Trends Analysis
- **Date Range**: {self.df['timestamp'].min()} to {self.df['timestamp'].max()}
- **Total Expectations**: {len(self.df)}
- **Successful Expectations**: {self.df['success'].sum()}
- **Failed Expectations**: {len(self.df) - self.df['success'].sum()}

## Recommendations
1. **Immediate Action**: Address suites with success rates below 80%
2. **Expectation Review**: Review and update failing expectation types
3. **Monitoring**: Implement daily monitoring for critical data assets
4. **Process Improvement**: Establish data quality governance processes

## Risk Assessment
- **High Risk**: Suites with success rates below 70% require immediate attention
- **Medium Risk**: Suites with success rates between 70-85% need monitoring
- **Low Risk**: Suites with success rates above 85% are performing well

## Next Steps
1. Prioritize fixing the lowest performing suite
2. Review expectation configurations for failing types
3. Implement automated monitoring and alerting
4. Schedule regular data quality reviews
"""
        return fallback_analysis
    
    def generate_data_catalog(self) -> Dict:
        """Generate comprehensive data catalog from validation results"""
        logger.info("Generating data catalog...")
        
        catalog = {
            "metadata": {
                "generated_on": datetime.now().isoformat(),
                "total_validation_files": len(self.validation_files),
                "analysis_period": f"{self.df['timestamp'].min()} to {self.df['timestamp'].max()}",
                "great_expectations_version": "0.18.22"
            },
            "data_assets": {},
            "expectation_suites": {},
            "data_quality_summary": {
                "overall_success_rate": self.quality_metrics['overall_success_rate'],
                "exception_rate": self.quality_metrics['exception_rate'],
                "total_expectations": len(self.df)
            }
        }
        
        # Process each validation file to extract data asset information
        for file_info in self.validation_files:
            data = file_info['data']
            suite_name = file_info['suite_name']
            data_asset = file_info['data_asset']
            
            # Extract batch definition information
            batch_def = data.get('meta', {}).get('active_batch_definition', {})
            batch_spec = data.get('meta', {}).get('batch_spec', {})
            
            # Initialize data asset entry if not exists
            if data_asset not in catalog["data_assets"]:
                catalog["data_assets"][data_asset] = {
                    "name": data_asset,
                    "type": batch_spec.get('type', 'unknown'),
                    "table_name": batch_spec.get('table_name', ''),
                    "schema_name": batch_spec.get('schema_name', ''),
                    "datasource": batch_def.get('datasource_name', ''),
                    "data_connector": batch_def.get('data_connector_name', ''),
                    "validation_runs": [],
                    "columns": {},
                    "expectation_suites": []
                }
            
            # Add validation run information
            run_info = {
                "run_id": file_info['run_id'],
                "timestamp": file_info['timestamp'],
                "suite_name": suite_name,
                "expectation_count": len(data.get('results', [])),
                "success_rate": sum(1 for r in data.get('results', []) if r.get('success', False)) / len(data.get('results', [])) if data.get('results') else 0
            }
            
            catalog["data_assets"][data_asset]["validation_runs"].append(run_info)
            
            # Add suite to data asset
            if suite_name not in catalog["data_assets"][data_asset]["expectation_suites"]:
                catalog["data_assets"][data_asset]["expectation_suites"].append(suite_name)
            
            # Extract column information from expectations
            for result in data.get('results', []):
                expectation_config = result.get('expectation_config', {})
                column = expectation_config.get('kwargs', {}).get('column', 'table-level')
                
                if column != 'table-level' and column not in catalog["data_assets"][data_asset]["columns"]:
                    catalog["data_assets"][data_asset]["columns"][column] = {
                        "name": column,
                        "expectation_types": [],
                        "quality_metrics": {
                            "total_expectations": 0,
                            "successful_expectations": 0,
                            "success_rate": 0.0,
                            "exceptions": 0
                        }
                    }
                
                if column != 'table-level':
                    exp_type = expectation_config.get('expectation_type', '')
                    if exp_type not in catalog["data_assets"][data_asset]["columns"][column]["expectation_types"]:
                        catalog["data_assets"][data_asset]["columns"][column]["expectation_types"].append(exp_type)
            
            # Initialize expectation suite entry
            if suite_name not in catalog["expectation_suites"]:
                catalog["expectation_suites"][suite_name] = {
                    "name": suite_name,
                    "data_assets": [],
                    "expectation_types": [],
                    "quality_metrics": {
                        "total_expectations": 0,
                        "successful_expectations": 0,
                        "success_rate": 0.0,
                        "exceptions": 0
                    }
                }
            
            # Add data asset to suite
            if data_asset not in catalog["expectation_suites"][suite_name]["data_assets"]:
                catalog["expectation_suites"][suite_name]["data_assets"].append(data_asset)
        
        # Calculate quality metrics for columns and suites
        for data_asset_name, asset_info in catalog["data_assets"].items():
            for column_name, column_info in asset_info["columns"].items():
                column_df = self.df[(self.df['data_asset'] == data_asset_name) & (self.df['column'] == column_name)]
                if not column_df.empty:
                    column_info["quality_metrics"] = {
                        "total_expectations": len(column_df),
                        "successful_expectations": column_df['success'].sum(),
                        "success_rate": column_df['success'].mean(),
                        "exceptions": column_df['exception_raised'].sum()
                    }
        
        for suite_name, suite_info in catalog["expectation_suites"].items():
            suite_df = self.df[self.df['suite_name'] == suite_name]
            if not suite_df.empty:
                suite_info["quality_metrics"] = {
                    "total_expectations": len(suite_df),
                    "successful_expectations": suite_df['success'].sum(),
                    "success_rate": suite_df['success'].mean(),
                    "exceptions": suite_df['exception_raised'].sum()
                }
                suite_info["expectation_types"] = suite_df['expectation_type'].unique().tolist()
        
        self.data_catalog = catalog
        
        logger.info(f"Data assets cataloged: {len(catalog['data_assets'])}")
        logger.info(f"Expectation suites cataloged: {len(catalog['expectation_suites'])}")
        
        return catalog
    
    def generate_ai_executive_summary(self) -> str:
        """Generate AI-powered executive summary following professional standards"""
        logger.info("Generating AI-powered executive summary...")
        
        # Extract key metrics for summary
        overall_success = self.quality_metrics['overall_success_rate']
        exception_rate = self.quality_metrics['exception_rate']
        total_expectations = len(self.df)
        
        # Get top failing expectation types for summary
        failing_types = self.quality_metrics['type_metrics'].nsmallest(3, 'success_rate')
        
        # Generate AI-powered executive summary
        executive_summary_prompt = f"""
        You are a senior data quality consultant writing an executive summary for a Great Expectations validation analysis report.
        
        Data Quality Context:
        - Total Expectations: {total_expectations}
        - Overall Success Rate: {overall_success:.2%}
        - Exception Rate: {exception_rate:.2%}
        - Expectation Types: {self.data_summary['expectation_types']}
        - Validation Suites: {self.data_summary['suite_count']}
        - Critical Issues: {len(failing_types[failing_types['success_rate'] < 0.8])} expectation types below 80% success rate
        
        Top Failing Expectation Types:
        {failing_types.to_dict()}
        
        Write a professional executive summary that follows these guidelines:
        
        1. **Problem Statement**: Define the data quality challenge being addressed
        2. **Solution Approach**: Explain how Great Expectations addresses the problem
        3. **Key Findings**: Present the most critical insights from the analysis
        4. **Business Impact**: Highlight the value and benefits of the data quality program
        5. **Call to Action**: Provide clear next steps for decision-makers
        
        Requirements:
        - Write for C-level executives and decision-makers
        - Use clear, simple language (15-year-old reading level)
        - Keep to 500-800 words maximum
        - Focus on business value and strategic importance
        - Include specific metrics and actionable recommendations
        - Avoid technical jargon
        - Create urgency for immediate action
        
        Format as a professional executive summary suitable for a board presentation.
        """
        
        ai_executive_summary = self.analyzer.ollama_infer(executive_summary_prompt)
        
        # Fallback executive summary if AI is unavailable
        if ai_executive_summary is None:
            logger.warning("AI unavailable, using fallback executive summary...")
            ai_executive_summary = f"""
            ## Executive Summary
            
            This Great Expectations validation analysis reveals critical insights into our data quality program's performance across {self.data_summary['suite_count']} validation suites monitoring {total_expectations} data quality expectations.
            
            **Key Findings:**
            Our data quality program demonstrates strong overall performance with a {overall_success:.2%} success rate, indicating robust data governance processes. However, {len(failing_types[failing_types['success_rate'] < 0.8])} expectation types require immediate attention due to success rates below 80%.
            
            **Business Impact:**
            The current data quality metrics suggest reliable data for most analytical workloads, but specific expectation failures could impact downstream analytics and reporting accuracy. Immediate remediation of failing expectations is recommended to maintain data trust and prevent potential business impact.
            
            **Recommendation:**
            Prioritize fixing expectation types with success rates below 80% to ensure comprehensive data quality coverage and maintain stakeholder confidence in our data assets.
            """
        
        return ai_executive_summary
    
    def generate_professional_report(self) -> str:
        """Generate professional markdown report with AI executive summary"""
        logger.info("Generating professional report...")
        
        # Generate AI executive summary
        ai_executive_summary = self.generate_ai_executive_summary()
        
        # Extract key metrics
        overall_success = self.quality_metrics['overall_success_rate']
        exception_rate = self.quality_metrics['exception_rate']
        total_expectations = len(self.df)
        failing_types = self.quality_metrics['type_metrics'].nsmallest(3, 'success_rate')
        
        report = f"""# Great Expectations Validation Analysis Report

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Analysis Period:** {self.data_summary['date_range']}

## Executive Summary

{ai_executive_summary}

## Critical Findings

### Top Issues Requiring Attention
"""
        
        # Add critical issues
        for idx, (exp_type, metrics) in enumerate(failing_types.iterrows(), 1):
            if metrics['success_rate'] < 0.8:
                report += f"{idx}. **{exp_type}**: {metrics['success_rate']:.1%} success rate ({metrics['successful_expectations']}/{metrics['total_expectations']} expectations)\n"
        
        report += f"""
## Data Quality Analysis

### Overall Performance Metrics

| Metric | Value |
|--------|-------|
| Total Expectations | {total_expectations} |
| Overall Success Rate | {overall_success:.2%} |
| Exception Rate | {exception_rate:.2%} |
| Expectation Types | {self.data_summary['expectation_types']} |
| Validation Suites | {self.data_summary['suite_count']} |

### Suite Performance

| Suite Name | Expectations | Success Rate | Exceptions |
|------------|-------------|--------------|------------|
"""
        
        # Add suite metrics
        for suite, metrics in self.quality_metrics['suite_metrics'].iterrows():
            report += f"| {suite} | {metrics['total_expectations']} | {metrics['success_rate']:.2%} | {metrics['exceptions']} |\n"
        
        report += f"""
### Expectation Type Performance

| Expectation Type | Count | Success Rate | Exceptions |
|------------------|-------|--------------|------------|
"""
        
        # Add type metrics
        for exp_type, metrics in self.quality_metrics['type_metrics'].iterrows():
            report += f"| {exp_type} | {metrics['total_expectations']} | {metrics['success_rate']:.2%} | {metrics['exceptions']} |\n"
        
        report += f"""
## AI-Powered Analysis

{self.ai_insights}

## Data Catalog Summary

### Data Assets Overview

| Asset Name | Type | Table | Schema | Datasource | Columns | Suites |
|------------|------|-------|--------|------------|---------|--------|
"""
        
        # Add data catalog information
        if self.data_catalog:
            for asset_name, asset_info in self.data_catalog['data_assets'].items():
                report += f"| {asset_name} | {asset_info['type']} | {asset_info['table_name']} | {asset_info['schema_name']} | {asset_info['datasource']} | {len(asset_info['columns'])} | {len(asset_info['expectation_suites'])} |\n"
        
        report += f"""
### Expectation Suites Overview

| Suite Name | Total Expectations | Success Rate | Exceptions | Data Assets |
|------------|-------------------|--------------|------------|-------------|
"""
        
        # Add expectation suites information
        if self.data_catalog:
            for suite_name, suite_info in self.data_catalog['expectation_suites'].items():
                report += f"| {suite_name} | {suite_info['quality_metrics']['total_expectations']} | {suite_info['quality_metrics']['success_rate']:.2%} | {suite_info['quality_metrics']['exceptions']} | {len(suite_info['data_assets'])} |\n"
        
        report += f"""
## Recommendations

Based on the analysis, the following actions are recommended:

1. **Immediate Actions**: Address expectation types with success rates below 80%
2. **Monitoring**: Implement daily monitoring for critical data assets
3. **Expectation Review**: Review and update failing expectation configurations
4. **Process Improvement**: Establish data quality governance processes

## Technical Details

- **Analysis Engine**: Great Expectations v0.18.22
- **AI Analysis**: Ollama LLM (gpt-oss:20b)
- **Data Source**: Validation results from BirdiDQ/gx/uncommitted/validations
- **Report Generated**: {datetime.now().isoformat()}

---
*This report was automatically generated by the Great Expectations Validation Analysis system.*
"""
        
        return report
    
    def generate_pdf_report(self, report_content: str, filename: str = "validation_analysis_report.pdf") -> Optional[Path]:
        """Generate PDF report from markdown content with proper A4 formatting"""
        try:
            from markdown import markdown
            from weasyprint import HTML, CSS
            
            # Convert markdown to HTML
            html_content = markdown(report_content, extensions=['tables', 'codehilite'])
            
            # Enhanced CSS styling for A4 format
            css_content = """
            @page {
                size: A4;
                margin: 2cm;
                @top-center {
                    content: "Great Expectations Validation Analysis Report";
                    font-size: 10px;
                    color: #666;
                }
                @bottom-center {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    color: #666;
                }
            }
            
            body {
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                color: #333;
                font-size: 11px;
            }
            
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                page-break-after: avoid;
                font-size: 18px;
            }
            
            h2 {
                color: #34495e;
                margin-top: 25px;
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
                page-break-after: avoid;
                font-size: 14px;
            }
            
            h3 {
                color: #7f8c8d;
                margin-top: 20px;
                page-break-after: avoid;
                font-size: 12px;
            }
            
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                font-size: 9px;
                page-break-inside: avoid;
            }
            
            th, td {
                border: 1px solid #ddd;
                padding: 4px 6px;
                text-align: left;
                word-wrap: break-word;
            }
            
            th {
                background-color: #f2f2f2;
                font-weight: bold;
                font-size: 9px;
            }
            
            code {
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 9px;
            }
            
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                font-size: 9px;
                page-break-inside: avoid;
            }
            """
            
            # Create HTML document
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Great Expectations Validation Analysis Report</title>
                <style>{css_content}</style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Generate PDF
            output_path = self.output_dir / filename
            HTML(string=full_html).write_pdf(str(output_path))
            
            logger.info(f"PDF report saved to: {output_path}")
            return output_path
            
        except ImportError as e:
            logger.error(f"PDF generation requires additional packages: {e}")
            logger.error("Install with: pip install weasyprint markdown")
            return None
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return None
    
    def save_data_catalog(self) -> Path:
        """Save data catalog as JSON"""
        catalog_path = self.output_dir / "data_catalog.json"
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(self.data_catalog, f, indent=2, default=str)
        
        logger.info(f"Data catalog JSON saved to: {catalog_path}")
        return catalog_path
    
    def run_pipeline(self) -> Dict[str, Path]:
        """Run the complete data reporting pipeline"""
        logger.info("Starting data reporting pipeline...")
        start_time = time.time()
        
        try:
            # Step 1: Load validation files
            self.load_validation_files()
            
            # Step 2: Process validation results
            self.process_validation_results()
            
            # Step 3: Calculate quality metrics
            self.calculate_quality_metrics()
            
            # Step 4: Generate AI insights
            self.generate_ai_insights()
            
            # Step 5: Generate data catalog
            self.generate_data_catalog()
            
            # Step 6: Generate professional report
            professional_report = self.generate_professional_report()
            
            # Step 7: Save outputs
            outputs = {}
            
            # Save markdown report
            markdown_path = self.output_dir / "validation_analysis_report_professional.md"
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(professional_report)
            outputs['markdown_report'] = markdown_path
            logger.info(f"Markdown report saved to: {markdown_path}")
            
            # Save data catalog
            catalog_path = self.save_data_catalog()
            outputs['data_catalog'] = catalog_path
            
            # Generate PDF report
            pdf_path = self.generate_pdf_report(professional_report, "validation_analysis_report_professional.pdf")
            if pdf_path:
                outputs['pdf_report'] = pdf_path
            
            # Calculate execution time
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info("=" * 80)
            logger.info("DATA REPORTING PIPELINE COMPLETE!")
            logger.info("=" * 80)
            logger.info(f"Execution time: {duration:.2f} seconds")
            logger.info(f"Total expectations processed: {len(self.df)}")
            logger.info(f"Overall success rate: {self.quality_metrics['overall_success_rate']:.2%}")
            logger.info("=" * 80)
            
            return outputs
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise


def load_config(config_file: Optional[str] = None) -> Dict:
    """Load configuration from file or use defaults"""
    if config_file and Path(config_file).exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    
    # Default configuration - works from both root and test directory
    return {
        'validation_path': 'BirdiDQ/gx/uncommitted/validations',
        'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
        'output_dir': '.',
        'ollama_timeout': 120
    }


def main():
    """Main entry point for the data reporting pipeline"""
    parser = argparse.ArgumentParser(description='Great Expectations Data Reporting Pipeline')
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--output-dir', type=str, help='Output directory for reports')
    parser.add_argument('--validation-path', type=str, help='Path to validation results')
    parser.add_argument('--env-path', type=str, help='Path to environment file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.output_dir:
        config['output_dir'] = args.output_dir
    if args.validation_path:
        config['validation_path'] = args.validation_path
    if args.env_path:
        config['env_path'] = args.env_path
    
    try:
        # Initialize and run pipeline
        pipeline = DataReportingPipeline(config)
        outputs = pipeline.run_pipeline()
        
        print("\n" + "=" * 80)
        print("PIPELINE EXECUTION SUCCESSFUL!")
        print("=" * 80)
        print("Generated outputs:")
        for output_type, output_path in outputs.items():
            print(f"  • {output_type}: {output_path}")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
