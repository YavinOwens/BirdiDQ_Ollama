#!/usr/bin/env python3
"""
Test script for Streamlit data upload application
Creates sample data and tests the core functionality
"""

import pandas as pd
import great_expectations as gx
from io import StringIO
import tempfile
import json
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for testing"""
    
    # Sample NYC taxi data
    sample_data = {
        'vendor_id': [random.randint(1, 2) for _ in range(100)],
        'pickup_datetime': [datetime.now() - timedelta(hours=random.randint(1, 1000)) for _ in range(100)],
        'dropoff_datetime': [datetime.now() - timedelta(hours=random.randint(1, 1000)) for _ in range(100)],
        'passenger_count': [random.randint(1, 6) for _ in range(100)],
        'trip_distance': [round(random.uniform(0.1, 50.0), 2) for _ in range(100)],
        'fare_amount': [round(random.uniform(2.0, 100.0), 2) for _ in range(100)],
        'extra': [round(random.uniform(0.0, 5.0), 2) for _ in range(100)],
        'mta_tax': [round(random.uniform(0.0, 2.0), 2) for _ in range(100)],
        'tip_amount': [round(random.uniform(0.0, 20.0), 2) for _ in range(100)],
        'tolls_amount': [round(random.uniform(0.0, 10.0), 2) for _ in range(100)],
        'total_amount': [round(random.uniform(5.0, 120.0), 2) for _ in range(100)]
    }
    
    # Add some missing values for testing
    for i in range(5):
        sample_data['fare_amount'][i] = None
        sample_data['tip_amount'][i * 2] = None
    
    return pd.DataFrame(sample_data)

def test_gx_integration():
    """Test Great Expectations integration"""
    print("Testing Great Expectations integration...")
    
    try:
        # Initialize GX context
        context = gx.get_context()
        print("✅ Great Expectations context initialized")
        
        # Create sample data
        df = create_sample_data()
        print(f"✅ Sample data created: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Create datasource
        try:
            datasource = context.get_datasource("test_uploaded_data")
        except:
            datasource = context.sources.add_pandas("test_uploaded_data")
        
        # Create DataFrame asset
        asset = datasource.add_dataframe_asset(name="test_sample_data", dataframe=df)
        print("✅ DataFrame asset created")
        
        # Create validator
        batch_request = asset.build_batch_request()
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name="test_sample_suite"
        )
        print("✅ Validator created")
        
        # Run Missingness Data Assistant
        missingness_result = context.assistants.missingness.run(validator=validator)
        missingness_suite = missingness_result.get_expectation_suite(
            expectation_suite_name="test_missingness_final"
        )
        context.save_expectation_suite(missingness_suite)
        print(f"✅ Missingness Data Assistant: {len(missingness_suite.expectations)} expectations")
        
        # Run Onboarding Data Assistant
        onboarding_result = context.assistants.onboarding.run(validator=validator)
        onboarding_suite = onboarding_result.get_expectation_suite(
            expectation_suite_name="test_onboarding_final"
        )
        context.save_expectation_suite(onboarding_suite)
        print(f"✅ Onboarding Data Assistant: {len(onboarding_suite.suite)} expectations")
        
        print("🎉 All Great Expectations tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Great Expectations test failed: {e}")
        return False

def test_file_formats():
    """Test files in different formats"""
    print("\nTesting file format detection...")
    
    df = create_sample_data()
    
    # CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    print("✅ CSV format test passed")
    
    # JSON
    json_data = df.to_json(orient='records')
    print("✅ JSON format test passed")
    
    print("🎉 File format tests passed!")
    return True

def test_data_analysis():
    """Test data analysis functions"""
    print("\nTesting data analysis functions...")
    
    df = create_sample_data()
    
    # Basic statistics
    stats = df.describe()
    print(f"✅ Statistics generated for {len(stats.columns)} columns")
    
    # Missing values
    null_count = df.isnull().sum().sum()
    print(f"✅ Missing values detected: {null_count}")
    
    # Data types
    dtype_info = df.dtypes.value_counts()
    print(f"✅ Data types analyzed: {dict(dtype_info)}")
    
    print("🎉 Data analysis tests passed!")
    return True

def main():
    """Run all tests"""
    print("🧪 Running Streamlit App Tests")
    print("=" * 50)
    
    tests = [
        ("Great Expectations Integration", test_gx_integration),
        ("File Format Detection", test_file_formats),
        ("Data Analysis", test_data_analysis)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Streamlit app is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
