#!/usr/bin/env python3
"""
Test script for the Data Reporting Pipeline

This script tests the data reporting pipeline functionality and validates
that all components work correctly.

Usage:
    python test_pipeline.py [--config CONFIG_FILE]
"""

import argparse
import json
import sys
from pathlib import Path

# Add the test directory to the path so we can import the pipeline
sys.path.insert(0, str(Path(__file__).parent))

from data_reporting_pipeline import DataReportingPipeline, ValidationAnalyzer


def test_validation_analyzer():
    """Test the ValidationAnalyzer class"""
    print("Testing ValidationAnalyzer...")
    
    try:
        analyzer = ValidationAnalyzer(
            validation_path="../BirdiDQ/gx/uncommitted/validations",
            env_path="/Users/yavin/python_projects/ollama_jupyter/.env"
        )
        
        print(f"✅ ValidationAnalyzer initialized successfully")
        print(f"   Ollama URL: {analyzer.ollama_url}")
        print(f"   Ollama Model: {analyzer.ollama_model}")
        print(f"   Validation Path: {analyzer.validation_path}")
        print(f"   Path Exists: {analyzer.validation_path.exists()}")
        
        return True
        
    except Exception as e:
        print(f"❌ ValidationAnalyzer test failed: {e}")
        return False


def test_pipeline_initialization():
    """Test pipeline initialization"""
    print("\nTesting Pipeline Initialization...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        print(f"✅ Pipeline initialized successfully")
        print(f"   Output Directory: {pipeline.output_dir}")
        print(f"   Config: {pipeline.config}")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline initialization test failed: {e}")
        return False


def test_data_loading():
    """Test data loading functionality"""
    print("\nTesting Data Loading...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Test loading validation files
        validation_files = pipeline.load_validation_files()
        
        if validation_files:
            print(f"✅ Data loading successful")
            print(f"   Loaded {len(validation_files)} validation files")
            
            # Test processing validation results
            df = pipeline.process_validation_results()
            
            if not df.empty:
                print(f"✅ Data processing successful")
                print(f"   Processed {len(df)} expectations")
                print(f"   Unique suites: {df['suite_name'].nunique()}")
                print(f"   Unique types: {df['expectation_type'].nunique()}")
                
                return True
            else:
                print(f"❌ Data processing failed: Empty DataFrame")
                return False
        else:
            print(f"❌ Data loading failed: No validation files found")
            return False
            
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False


def test_quality_metrics():
    """Test quality metrics calculation"""
    print("\nTesting Quality Metrics...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Load and process data
        pipeline.load_validation_files()
        pipeline.process_validation_results()
        
        # Calculate quality metrics
        metrics = pipeline.calculate_quality_metrics()
        
        print(f"✅ Quality metrics calculation successful")
        print(f"   Overall Success Rate: {metrics['overall_success_rate']:.2%}")
        print(f"   Exception Rate: {metrics['exception_rate']:.2%}")
        print(f"   Suite Metrics: {len(metrics['suite_metrics'])} suites")
        print(f"   Type Metrics: {len(metrics['type_metrics'])} types")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality metrics test failed: {e}")
        return False


def test_ai_insights():
    """Test AI insights generation"""
    print("\nTesting AI Insights...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Load and process data
        pipeline.load_validation_files()
        pipeline.process_validation_results()
        pipeline.calculate_quality_metrics()
        
        # Generate AI insights
        ai_insights, data_summary = pipeline.generate_ai_insights()
        
        print(f"✅ AI insights generation successful")
        print(f"   AI Response Length: {len(ai_insights)} characters")
        print(f"   Data Summary Keys: {list(data_summary.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI insights test failed: {e}")
        return False


def test_data_catalog():
    """Test data catalog generation"""
    print("\nTesting Data Catalog...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Load and process data
        pipeline.load_validation_files()
        pipeline.process_validation_results()
        pipeline.calculate_quality_metrics()
        
        # Generate data catalog
        catalog = pipeline.generate_data_catalog()
        
        print(f"✅ Data catalog generation successful")
        print(f"   Data Assets: {len(catalog['data_assets'])}")
        print(f"   Expectation Suites: {len(catalog['expectation_suites'])}")
        print(f"   Metadata: {catalog['metadata']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data catalog test failed: {e}")
        return False


def test_report_generation():
    """Test report generation"""
    print("\nTesting Report Generation...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Load and process data
        pipeline.load_validation_files()
        pipeline.process_validation_results()
        pipeline.calculate_quality_metrics()
        pipeline.generate_ai_insights()
        pipeline.generate_data_catalog()
        
        # Generate professional report
        report = pipeline.generate_professional_report()
        
        print(f"✅ Report generation successful")
        print(f"   Report Length: {len(report)} characters")
        print(f"   Contains Executive Summary: {'Executive Summary' in report}")
        print(f"   Contains AI Analysis: {'AI-Powered Analysis' in report}")
        print(f"   Contains Data Catalog: {'Data Catalog Summary' in report}")
        
        return True
        
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False


def test_full_pipeline():
    """Test the complete pipeline"""
    print("\nTesting Full Pipeline...")
    
    try:
        config = {
            'validation_path': '../BirdiDQ/gx/uncommitted/validations',
            'env_path': '/Users/yavin/python_projects/ollama_jupyter/.env',
            'output_dir': 'test_output'
        }
        
        pipeline = DataReportingPipeline(config)
        
        # Run the complete pipeline
        outputs = pipeline.run_pipeline()
        
        print(f"✅ Full pipeline execution successful")
        print(f"   Generated Outputs:")
        for output_type, output_path in outputs.items():
            print(f"     • {output_type}: {output_path}")
            if output_path.exists():
                print(f"       File exists: ✅")
            else:
                print(f"       File exists: ❌")
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        return False


def main():
    """Run all tests"""
    parser = argparse.ArgumentParser(description='Test the Data Reporting Pipeline')
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--test', type=str, choices=[
        'analyzer', 'init', 'loading', 'metrics', 'ai', 'catalog', 'report', 'full', 'all'
    ], default='all', help='Specific test to run')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("DATA REPORTING PIPELINE TEST SUITE")
    print("=" * 80)
    
    tests = []
    
    if args.test in ['analyzer', 'all']:
        tests.append(('ValidationAnalyzer', test_validation_analyzer))
    
    if args.test in ['init', 'all']:
        tests.append(('Pipeline Initialization', test_pipeline_initialization))
    
    if args.test in ['loading', 'all']:
        tests.append(('Data Loading', test_data_loading))
    
    if args.test in ['metrics', 'all']:
        tests.append(('Quality Metrics', test_quality_metrics))
    
    if args.test in ['ai', 'all']:
        tests.append(('AI Insights', test_ai_insights))
    
    if args.test in ['catalog', 'all']:
        tests.append(('Data Catalog', test_data_catalog))
    
    if args.test in ['report', 'all']:
        tests.append(('Report Generation', test_report_generation))
    
    if args.test in ['full', 'all']:
        tests.append(('Full Pipeline', test_full_pipeline))
    
    # Run tests
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Total Tests: {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
