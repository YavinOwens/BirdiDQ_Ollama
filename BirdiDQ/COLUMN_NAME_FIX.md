# Column Name Awareness Fix

## Problem
The LLM was generating expectations with incorrect column names:
- User query: "transaction_id should be unique"
- LLM generated: `validator.expect_column_values_to_be_unique(column="transition_id")` ❌ (typo!)
- Actual column name: `TRANSACTION_ID` (uppercase)

This caused validation failures with the error:
```
MetricResolutionError: The column "transition_id" in BatchData does not exist.
```

## Root Cause
The LLM (Ollama gpt-oss:20b) was:
1. Making typos ("transition" instead of "transaction")
2. Not respecting case sensitivity (lowercase vs uppercase)
3. Not aware of the actual available columns in the dataset

## Solution

### 1. Enhanced LLM Prompt
Updated `ollama_model.py` to:
- Accept `available_columns` parameter
- Include actual column names in the prompt
- Emphasize case sensitivity
- Show exact column names to the LLM

**Before:**
```python
def get_expectations(prompt, client=None, model_name=None):
    system_prompt = """...
    Use validator.expect_*() format
    """
```

**After:**
```python
def get_expectations(prompt, client=None, model_name=None, available_columns=None):
    system_prompt = """...
    - Use EXACT column names as provided
    - Column names are CASE-SENSITIVE
    """
    
    if available_columns:
        columns_str = ", ".join(f'"{col}"' for col in available_columns)
        system_prompt += f"\n\nIMPORTANT - Available columns: {columns_str}\n"
        system_prompt += "You MUST use these exact column names.\n"
```

### 2. Column Retrieval Method
Added `get_columns()` method to `OracleDatasource`:
```python
def get_columns(self):
    """Get list of column names from the table"""
    if self._columns_cache is None:
        df = read_oracle_tables(self.table_name)
        self._columns_cache = list(df.columns)
    return self._columns_cache
```

### 3. Integration in Streamlit App
Updated `app.py` to pass columns to LLM:
```python
# Get available columns from the datasource
available_columns = None
try:
    if hasattr(DQ_APP, 'get_columns'):
        available_columns = DQ_APP.get_columns()
except:
    pass

# Generate expectations with column information
nltoge = get_expectations(checks_input, client, available_columns=available_columns)
```

## Example Improved Prompt

**User Input:** "transaction id should be unique"

**LLM Receives:**
```
You are an expert in Great Expectations...

CRITICAL INSTRUCTIONS:
- Use EXACT column names as provided in the available columns list
- Column names are CASE-SENSITIVE - use them EXACTLY as shown

Example 1: ...
Example 2: ...

IMPORTANT - Available columns in this dataset: 
"TRANSACTION_ID", "CUSTOMER_ID", "PRODUCT_ID", "AMOUNT", "QUANTITY", "TIMESTAMP", "PAYMENT_METHOD", "REGION", "IS_FRAUDULENT", "CUSTOMER_AGE", "PRODUCT_CATEGORY"

You MUST use these exact column names (case-sensitive) in your expectations.

Natural language description:
transaction id should be unique
```

**LLM Generates:**
```python
validator.expect_column_values_to_be_unique(column="TRANSACTION_ID")
```
✅ Correct column name!

## Benefits

1. **Eliminates Typos**: LLM can copy exact column names from the list
2. **Handles Case Sensitivity**: LLM sees uppercase columns and uses them correctly
3. **Prevents Column Not Found Errors**: LLM knows what columns actually exist
4. **Better User Experience**: Users can use natural language without worrying about exact casing
5. **Works with Any Database**: Same approach for Oracle, PostgreSQL, Pandas, etc.

## Testing

### Before Fix:
```
User: "transaction id should be unique"
Generated: validator.expect_column_values_to_be_unique(column="transition_id")
Result: ❌ Column "transition_id" does not exist
```

### After Fix:
```
User: "transaction id should be unique"
LLM sees: Available columns: "TRANSACTION_ID", ...
Generated: validator.expect_column_values_to_be_unique(column="TRANSACTION_ID")
Result: ✅ Expectation runs successfully
```

## Files Modified

1. **`models/ollama_model.py`**
   - Added `available_columns` parameter to `get_expectations()`
   - Enhanced prompt to include column names
   - Emphasized case sensitivity

2. **`connecting_data/database/oracle.py`**
   - Added `get_columns()` method
   - Added `_columns_cache` for performance

3. **`app.py`**
   - Retrieve columns from datasource
   - Pass columns to `get_expectations()`

## Next Steps

- PostgreSQL datasource should also implement `get_columns()` method
- Pandas datasource already has `df.columns` accessible
- Consider fuzzy matching as fallback if LLM still makes minor errors

## Key Learnings

1. **LLMs need context**: Providing actual column names dramatically improves accuracy
2. **Case sensitivity matters**: Database columns are often uppercase, but users type lowercase
3. **Error messages are helpful**: The "column does not exist" error quickly identified the issue
4. **Clean execution works**: The refined execution approach correctly detected and reported the error

