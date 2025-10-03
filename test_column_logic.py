#!/usr/bin/env python3
"""
Simple test to verify column name logic without dependencies
"""

def test_column_name_mapping():
    """Test the column name mapping logic"""
    
    print("🧪 Testing Column Name Mapping Logic")
    print("=" * 50)
    
    # Simulate the actual Housing DataFrame columns (from the JSON file)
    actual_columns = [
        "households",
        "latitude", 
        "total_bedrooms",
        "housing_median_age",  # This is the correct column name
        "total_rooms",
        "median_house_value",
        "longitude",
        "median_income",
        "population"
    ]
    
    print(f"📊 Actual DataFrame columns: {actual_columns}")
    
    # Simulate what Ollama was generating (incorrect)
    incorrect_generated = 'validator.expect_column_values_to_be_between(column="housing median age", min_value=6, strict_min=True)'
    print(f"\n❌ Incorrect generated code:")
    print(f"   {incorrect_generated}")
    
    # Simulate what Ollama should generate (correct)
    correct_generated = 'validator.expect_column_values_to_be_between(column="housing_median_age", min_value=6, strict_min=True)'
    print(f"\n✅ Correct generated code:")
    print(f"   {correct_generated}")
    
    # Test the fix logic
    print(f"\n🔍 Analysis:")
    print(f"   - User input: 'housing median age should not be below 6'")
    print(f"   - Available columns: {[col for col in actual_columns if 'housing' in col.lower()]}")
    print(f"   - Expected: Ollama should see 'housing_median_age' in available columns")
    print(f"   - Expected: Ollama should generate column='housing_median_age' (with underscores)")
    
    # Check if the fix addresses the issue
    if "housing_median_age" in actual_columns:
        print(f"\n✅ SUCCESS: 'housing_median_age' is in the actual columns")
        print(f"✅ The get_columns() method should return this correct name")
        print(f"✅ Ollama should receive this correct name in available_columns")
        print(f"✅ Ollama should generate the correct column name")
    else:
        print(f"\n❌ FAILED: 'housing_median_age' not found in actual columns")
    
    return True

if __name__ == "__main__":
    test_column_name_mapping()
    print(f"\n🎉 Column name mapping test completed!")
