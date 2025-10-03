#!/usr/bin/env python3
"""
Test script to verify Ollama LLM generates clean expectation code
Tests the complete workflow: Natural language -> Ollama -> GX expectation execution
"""

import sys
import os
import pandas as pd

# Add BirdiDQ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'BirdiDQ/great_expectations'))

from models.ollama_model import get_expectations, load_ollama_client, test_ollama_connection
from connecting_data.filesystem.pandas_filesystem import PandasFilesystemDatasource

print("=" * 80)
print("Testing Ollama Expectation Generation with Filesystem Data")
print("=" * 80)

# Step 1: Test Ollama Connection
print("\n[1/5] Testing Ollama connection...")
connection_test = test_ollama_connection()
if connection_test['status'] == 'error':
    print(f"✗ Ollama connection failed: {connection_test['error']}")
    sys.exit(1)
print(f"✓ Connected to Ollama (Model: {connection_test['model']})")

# Step 2: Load Ollama Client
print("\n[2/5] Loading Ollama client...")
try:
    client = load_ollama_client()
    print("✓ Ollama client loaded successfully")
except Exception as e:
    print(f"✗ Failed to load Ollama client: {e}")
    sys.exit(1)

# Step 3: Create Test DataFrame
print("\n[3/5] Creating test dataset...")
test_data = pd.DataFrame({
    'housing_median_age': [10, 15, 20, 25, 30, 5, 8, 12],
    'median_income': [3.5, 4.2, 5.1, 2.8, 6.3, 7.1, 3.9, 4.5],
    'total_rooms': [1500, 2000, 1800, 2200, 1600, 1900, 2100, 1700],
    'population': [800, 1200, 900, 1100, 850, 1000, 1150, 950]
})
print(f"✓ Created test dataset with {len(test_data)} rows and {len(test_data.columns)} columns")
print(f"  Columns: {', '.join(test_data.columns)}")

# Step 4: Test Natural Language to Code Generation
print("\n[4/5] Testing natural language to expectation code generation...")
test_cases = [
    {
        'description': "housing_median_age should not be below 6",
        'expected_method': 'expect_column_values_to_be_between'
    },
    {
        'description': "median_income should be greater than 0",
        'expected_method': 'expect_column_values_to_be_between'
    },
    {
        'description': "total_rooms should not be null",
        'expected_method': 'expect_column_values_to_not_be_null'
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n  Test {i}: {test_case['description']}")
    print(f"  Expected method: {test_case['expected_method']}")
    
    try:
        # Generate expectations using Ollama
        generated_code = get_expectations(
            test_case['description'],
            client=client,
            available_columns=list(test_data.columns)
        )
        
        print(f"  Generated code:")
        for line in generated_code.split('\n'):
            print(f"    {line}")
        
        # Verify the code is clean (no reasoning text)
        if any(keyword in generated_code.lower() for keyword in 
               ['we need', 'actually', 'wait:', 'so code:', 'but the', 'means']):
            print(f"  ✗ WARNING: Generated code contains reasoning text!")
        else:
            print(f"  ✓ Code is clean (no reasoning text)")
        
        # Verify expected method is present
        if test_case['expected_method'] in generated_code:
            print(f"  ✓ Contains expected method: {test_case['expected_method']}")
        else:
            print(f"  ✗ WARNING: Does not contain expected method: {test_case['expected_method']}")
            
    except Exception as e:
        print(f"  ✗ Failed to generate code: {e}")

# Step 5: Test Complete Workflow with GX
print("\n[5/5] Testing complete workflow with Great Expectations...")
try:
    # Create filesystem datasource
    dq_app = PandasFilesystemDatasource(
        datasource_name="test_housing",
        dataframe=test_data,
        filename="housing.csv"
    )
    print("✓ Created PandasFilesystemDatasource")
    
    # Verify table_name property
    assert hasattr(dq_app, 'table_name'), "Missing table_name property"
    print(f"✓ table_name property: {dq_app.table_name}")
    
    # Verify file_name property
    assert hasattr(dq_app, 'file_name'), "Missing file_name property"
    print(f"✓ file_name property: {dq_app.file_name}")
    
    # Test expectation execution
    test_description = "total_rooms should not be null"
    print(f"\n  Testing expectation: '{test_description}'")
    
    # Generate expectation code
    generated_code = get_expectations(
        test_description,
        client=client,
        available_columns=list(test_data.columns)
    )
    print(f"  Generated: {generated_code}")
    
    # Remove validator. prefix if present (run_expectation adds it)
    if generated_code.startswith('validator.'):
        generated_code = generated_code[len('validator.'):]
    
    # Run the expectation
    result = dq_app.run_expectation(generated_code)
    print(f"  ✓ Expectation executed successfully")
    print(f"  Result: {'PASSED' if result.success else 'FAILED'}")
    
except Exception as e:
    print(f"  ✗ Workflow test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("Testing Complete!")
print("=" * 80)

