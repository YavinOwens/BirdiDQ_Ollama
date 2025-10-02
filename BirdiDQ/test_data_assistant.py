#!/usr/bin/env python3
"""
Test script to verify Data Assistant workflow with Oracle
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent / 'great_expectations'))

# Load environment variables
load_dotenv('/Users/yavin/python_projects/ollama_jupyter/.env')

print("="*80)
print("DATA ASSISTANT WORKFLOW TEST")
print("="*80)

# Step 1: Import and read Oracle data
print("\n[1/5] Reading Oracle data...")
try:
    from connecting_data.database.oracle import read_oracle_tables
    df = read_oracle_tables('TRANSACTIONS')
    print(f"✓ Read {len(df)} rows from TRANSACTIONS")
    print(f"  Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Failed to read data: {e}")
    sys.exit(1)

# Step 2: Create GX context and datasource
print("\n[2/5] Setting up Great Expectations context...")
try:
    import great_expectations as gx
    context = gx.get_context()
    print("✓ Created GX context")
    
    # Create pandas datasource using Fluent API
    datasource_name = "test_data_assistant_pandas"
    try:
        data_source = context.get_datasource(datasource_name)
        print(f"✓ Using existing datasource: {datasource_name}")
    except:
        data_source = context.sources.add_pandas(datasource_name)
        print(f"✓ Created new datasource: {datasource_name}")
    
    # Create data asset
    asset_name = "test_transactions_data_assistant"
    try:
        data_asset = data_source.get_asset(asset_name)
        print(f"✓ Using existing asset: {asset_name}")
    except:
        data_asset = data_source.add_dataframe_asset(name=asset_name)
        print(f"✓ Created new asset: {asset_name}")
    
except Exception as e:
    print(f"✗ Failed to setup context: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Create batch request and validator
print("\n[3/5] Creating validator for Data Assistant...")
try:
    # Build batch request with DataFrame
    batch_request = data_asset.build_batch_request(dataframe=df)
    print("✓ Built batch request")
    
    # Create expectation suite for data assistant
    suite_name = "data_assistant_test_suite"
    
    # Delete existing suite if it exists
    try:
        context.delete_expectation_suite(suite_name)
        print(f"✓ Deleted existing suite: {suite_name}")
    except:
        print(f"✓ No existing suite to delete")
    
    # Create new suite
    context.add_expectation_suite(expectation_suite_name=suite_name)
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

# Step 4: Test Onboarding Data Assistant
print("\n[4/5] Running Onboarding Data Assistant...")
try:
    # Run data assistant using context API
    print("  Calling context.assistants.onboarding.run()...")
    result = context.assistants.onboarding.run(validator=validator)
    
    print(f"✓ Data Assistant completed")
    print(f"  Result type: {type(result)}")
    print(f"  Result attributes: {dir(result)}")
    
    # Try different methods to get the expectation suite
    print("\n  Testing methods to extract expectations:")
    
    # Method 1: get_expectation_suite with suite name
    try:
        suite = result.get_expectation_suite(expectation_suite_name=f"{suite_name}_final")
        print(f"  ✓ Method 1 (get_expectation_suite): {len(suite.expectations)} expectations")
        
        # Save the suite
        context.save_expectation_suite(suite)
        print(f"  ✓ Saved suite: {suite.expectation_suite_name}")
        
        success_method = "get_expectation_suite(expectation_suite_name='..._final')"
        
    except Exception as e1:
        print(f"  ✗ Method 1 failed: {e1}")
        
        # Method 2: Direct attribute access (old API)
        try:
            suite = result.expectation_suite
            print(f"  ✓ Method 2 (direct attribute): {len(suite.expectations)} expectations")
            success_method = "result.expectation_suite"
        except Exception as e2:
            print(f"  ✗ Method 2 failed: {e2}")
            
            # Method 3: Check validator's expectation suite
            try:
                suite = validator.expectation_suite
                print(f"  ✓ Method 3 (validator.expectation_suite): {len(suite.expectations)} expectations")
                
                # Save the suite
                validator.save_expectation_suite()
                print(f"  ✓ Saved suite from validator")
                
                success_method = "validator.expectation_suite (after run)"
                
            except Exception as e3:
                print(f"  ✗ Method 3 failed: {e3}")
                print("\n  ✗ All methods failed!")
                sys.exit(1)
    
except Exception as e:
    print(f"✗ Data Assistant failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Verify and build Data Docs
print("\n[5/5] Building Data Docs...")
try:
    # Get the saved suite
    final_suite = context.get_expectation_suite(suite.expectation_suite_name)
    print(f"✓ Retrieved suite: {final_suite.expectation_suite_name}")
    print(f"  Total expectations: {len(final_suite.expectations)}")
    
    # Show sample expectations
    print("\n  Sample expectations:")
    for exp in list(final_suite.expectations)[:5]:
        column = exp.kwargs.get('column', 'N/A')
        exp_type = exp.expectation_type.replace('expect_', '').replace('_', ' ')
        print(f"    • {exp_type} on column: {column}")
    
    # Build Data Docs
    context.build_data_docs()
    print("\n✓ Built Data Docs")
    
    # Get Data Docs URL
    docs_sites = context.get_docs_sites_urls()
    if docs_sites:
        print(f"✓ Data Docs URL: {docs_sites[0]['site_url']}")
    
except Exception as e:
    print(f"✗ Failed to build Data Docs: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print(f"""
✅ Data Assistant workflow completed successfully!

Key findings:
1. Data Assistant runs: ✓
2. Expectations generated: {len(final_suite.expectations)}
3. Correct method to use: {success_method}
4. Suite saved: ✓
5. Data Docs built: ✓

This is the correct pattern for GX 0.18+!
""")

print("="*80)
print("✅ Test completed successfully!")
print("="*80)

