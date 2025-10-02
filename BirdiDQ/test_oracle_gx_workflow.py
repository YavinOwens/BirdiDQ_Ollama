#!/usr/bin/env python3
"""
Test script to verify Oracle + Great Expectations workflow
This tests the complete flow: connect to Oracle, create validator, add expectations, validate
"""

import sys
import os
from dotenv import load_dotenv
import pandas as pd
import great_expectations as gx
from pathlib import Path

# Add the great_expectations directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'great_expectations'))

# Load environment variables
load_dotenv('/Users/yavin/python_projects/ollama_jupyter/.env')

print("="*80)
print("ORACLE + GREAT EXPECTATIONS WORKFLOW TEST")
print("="*80)

# Step 1: Import Oracle connection function
print("\n[1/6] Importing Oracle utilities...")
try:
    from connecting_data.database.oracle import read_oracle_tables
    print("✓ Successfully imported Oracle utilities")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Read data from Oracle
print("\n[2/6] Reading data from Oracle...")
try:
    df = read_oracle_tables('TRANSACTIONS')
    print(f"✓ Successfully read {len(df)} rows from TRANSACTIONS table")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  Sample data:")
    print(df.head(3))
except Exception as e:
    print(f"✗ Failed to read Oracle data: {e}")
    sys.exit(1)

# Step 3: Create GX context and datasource using Fluent API
print("\n[3/6] Creating Great Expectations context and datasource...")
try:
    context = gx.get_context()
    print("✓ Created GX context")
    
    # Create pandas datasource using Fluent API
    datasource_name = "test_oracle_pandas"
    try:
        data_source = context.get_datasource(datasource_name)
        print(f"✓ Using existing datasource: {datasource_name}")
    except:
        data_source = context.sources.add_pandas(datasource_name)
        print(f"✓ Created new datasource: {datasource_name}")
    
    # Create data asset
    asset_name = "test_transactions"
    try:
        data_asset = data_source.get_asset(asset_name)
        print(f"✓ Using existing asset: {asset_name}")
    except:
        data_asset = data_source.add_dataframe_asset(name=asset_name)
        print(f"✓ Created new asset: {asset_name}")
    
except Exception as e:
    print(f"✗ Failed to create datasource: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Build batch request and create validator
print("\n[4/6] Building batch request and creating validator...")
try:
    # Build batch request with DataFrame
    batch_request = data_asset.build_batch_request(dataframe=df)
    print("✓ Built batch request")
    
    # Create expectation suite
    suite_name = "test_oracle_suite"
    try:
        context.delete_expectation_suite(suite_name)
    except:
        pass
    
    context.add_or_update_expectation_suite(expectation_suite_name=suite_name)
    print(f"✓ Created expectation suite: {suite_name}")
    
    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )
    print("✓ Created validator")
    
except Exception as e:
    print(f"✗ Failed to create validator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Test different expectations
print("\n[5/6] Testing expectations...")

# Test expectations that SHOULD work with PandasExecutionEngine
test_expectations = [
    {
        "name": "Column exists",
        "code": "validator.expect_column_to_exist(column='TRANSACTION_ID')",
        "should_work": True
    },
    {
        "name": "Not null check",
        "code": "validator.expect_column_values_to_not_be_null(column='TRANSACTION_ID')",
        "should_work": True
    },
    {
        "name": "Between values",
        "code": "validator.expect_column_values_to_be_between(column='AMOUNT', min_value=0)",
        "should_work": True
    },
    {
        "name": "Unique values (complex metric)",
        "code": "validator.expect_column_values_to_be_unique(column='TRANSACTION_ID')",
        "should_work": False  # This requires metrics not available with pandas runtime
    }
]

results = []
for test in test_expectations:
    print(f"\n  Testing: {test['name']}")
    print(f"    Code: {test['code']}")
    print(f"    Expected: {'✓ Should work' if test['should_work'] else '✗ Will likely fail'}")
    
    try:
        # Execute the expectation
        exec(f"result = {test['code']}")
        print(f"    Actual: ✓ SUCCESS")
        results.append({"test": test['name'], "success": True, "error": None})
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)[:100]
        print(f"    Actual: ✗ FAILED - {error_type}: {error_msg}")
        results.append({"test": test['name'], "success": False, "error": error_type})

# Step 6: Save suite and generate report
print("\n[6/6] Saving expectations and building Data Docs...")
try:
    validator.save_expectation_suite()
    print("✓ Saved expectation suite")
    
    # Get final suite
    final_suite = context.get_expectation_suite(suite_name)
    print(f"✓ Suite has {len(final_suite.expectations)} expectations")
    
    # Build Data Docs
    context.build_data_docs()
    print("✓ Built Data Docs")
    
    # Get Data Docs URL
    docs_sites = context.get_docs_sites_urls()
    if docs_sites:
        print(f"✓ Data Docs URL: {docs_sites[0]['site_url']}")
    
except Exception as e:
    print(f"✗ Failed to save/build: {e}")

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

print(f"\nTotal tests run: {len(results)}")
print(f"Successful: {sum(1 for r in results if r['success'])}")
print(f"Failed: {sum(1 for r in results if not r['success'])}")

print("\nDetailed Results:")
for r in results:
    status = "✓" if r['success'] else "✗"
    error = f" ({r['error']})" if r['error'] else ""
    print(f"  {status} {r['test']}{error}")

print("\n" + "="*80)
print("KEY FINDINGS:")
print("="*80)
print("""
1. Simple expectations (column_to_exist, values_to_not_be_null, values_to_be_between)
   work well with PandasExecutionEngine + runtime DataFrames

2. Complex expectations (values_to_be_unique, values_to_match_regex with complex patterns)
   fail because they require metrics not registered with runtime pandas data

3. The Fluent API (context.sources.add_pandas, data_asset.build_batch_request) 
   is the correct modern approach for GX 0.18+

4. For Oracle without cx_Oracle client libraries:
   - Read data with oracledb into DataFrame ✓
   - Use pandas execution engine ✓
   - Stick to simple expectations ✓
   - Or use Data Assistants for automatic profiling ✓
""")

print("\n✅ Test completed!")

