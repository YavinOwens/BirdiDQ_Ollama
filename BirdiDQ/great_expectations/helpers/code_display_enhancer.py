"""
Great Expectations Code Display Enhancer
=========================================

Enhances expectation metadata to display Python code and SQL in Data Docs.
"""

import re
from typing import Dict, Any


def enhance_expectation_with_code(expectation_line: str, execution_engine: str = "SQL", return_meta: bool = False):
    """
    Enhance an expectation with metadata to display the Python code in Data Docs.
    
    Args:
        expectation_line: The expectation code line (e.g., 'validator.expect_column_values_to_be_unique(column="id")')
        execution_engine: The execution engine being used ("SQL", "Pandas", etc.)
        return_meta: If True, return a tuple of (enhanced_line, meta_dict) instead of just the line
    
    Returns:
        If return_meta=False: Enhanced expectation line with meta parameter
        If return_meta=True: Tuple of (enhanced_line, meta_dict)
    
    Example:
        Input:  'validator.expect_column_values_to_be_unique(column="id")'
        Output: 'validator.expect_column_values_to_be_unique(column="id", meta={...})'
    """
    
    # Skip if not a validator expectation
    if "validator.expect_" not in expectation_line:
        return (expectation_line, None) if return_meta else expectation_line
    
    # Skip if already has meta (avoid duplication)
    if "meta=" in expectation_line:
        return (expectation_line, None) if return_meta else expectation_line
    
    # Create the code display content
    code_display = f"""### 📝 Implementation Details

**Python Code:**
```python
{expectation_line}
```

**Execution Engine:** {execution_engine}
"""
    
    # For SQL execution engine, add example SQL query
    if "SQL" in execution_engine:
        # Extract expectation info and generate SQL example
        info = extract_expectation_info(expectation_line)
        if info['type'] and info['column']:
            sql_example = generate_sql_example(info['type'], info['column'], info['parameters'])
            code_display += f"""

**Approximate SQL Query:**
```sql
{sql_example}
```

**Note:** This is a simplified example. Great Expectations generates optimized SQL with batching, sampling, and additional logic.
"""
        else:
            code_display += """

**Note:** The actual SQL query is generated dynamically by Great Expectations based on the expectation type and parameters.
"""
    else:
        code_display += f"""

---
*This expectation is executed using Great Expectations' {execution_engine} execution engine.*
"""
    
    # Create meta dictionary
    meta_dict = {
        "notes": {
            "format": "markdown",
            "content": [code_display]
        }
    }
    
    # Insert meta parameter before closing parenthesis
    # Handle both cases: with and without trailing parenthesis
    expectation_line = expectation_line.rstrip()
    
    if expectation_line.endswith(')'):
        # Insert before the last closing parenthesis
        insert_pos = expectation_line.rfind(')')
        # Use placeholder {...} that will be replaced with actual dict
        enhanced_line = (
            expectation_line[:insert_pos] + 
            ", meta={...}" + 
            expectation_line[insert_pos:]
        )
    else:
        # No closing parenthesis (shouldn't happen, but handle it)
        enhanced_line = expectation_line + ", meta={...})"
    
    # Return based on return_meta flag
    if return_meta:
        return (enhanced_line, meta_dict)
    else:
        # For backward compatibility, replace placeholder with dict string representation
        enhanced_line = enhanced_line.replace('{...}', str(meta_dict))
        return enhanced_line


def extract_expectation_info(expectation_line: str) -> Dict[str, Any]:
    """
    Extract information from an expectation line for display purposes.
    
    Args:
        expectation_line: The expectation code line
    
    Returns:
        Dictionary with expectation details (type, column, parameters)
    """
    info = {
        'type': None,
        'column': None,
        'parameters': {}
    }
    
    # Extract expectation type
    type_match = re.search(r'validator\.(expect_\w+)', expectation_line)
    if type_match:
        info['type'] = type_match.group(1)
    
    # Extract column name
    column_match = re.search(r'column=["\']([^"\']+)["\']', expectation_line)
    if column_match:
        info['column'] = column_match.group(1)
    
    # Extract other parameters (simplified - doesn't handle all cases)
    param_patterns = {
        'min_value': r'min_value=([^,)]+)',
        'max_value': r'max_value=([^,)]+)',
        'regex': r'regex=r?["\']([^"\']+)["\']',
        'value_set': r'value_set=(\[[^\]]+\])',
        'mostly': r'mostly=([0-9.]+)'
    }
    
    for param_name, pattern in param_patterns.items():
        param_match = re.search(pattern, expectation_line)
        if param_match:
            info['parameters'][param_name] = param_match.group(1)
    
    return info


def generate_sql_example(expectation_type: str, column: str, parameters: Dict[str, Any]) -> str:
    """
    Generate an example SQL query that approximates what GX might generate.
    
    Note: This is a SIMPLIFIED example. GX's actual SQL is more complex and
    handles many edge cases, batching, sampling, etc.
    
    Args:
        expectation_type: The expectation type (e.g., 'expect_column_values_to_be_unique')
        column: The column name
        parameters: Additional parameters from the expectation
    
    Returns:
        Example SQL query string
    """
    
    sql_templates = {
        'expect_column_values_to_be_unique': f"""
-- Check for duplicate values in {column}
SELECT {column}, COUNT(*) as duplicate_count
FROM {{{{table}}}}
GROUP BY {column}
HAVING COUNT(*) > 1;
""",
        
        'expect_column_values_to_not_be_null': f"""
-- Check for NULL values in {column}
SELECT COUNT(*) as null_count
FROM {{{{table}}}}
WHERE {column} IS NULL;
""",
        
        'expect_column_values_to_be_between': f"""
-- Check {column} values outside range
SELECT COUNT(*) as out_of_range_count
FROM {{{{table}}}}
WHERE {column} NOT BETWEEN {parameters.get('min_value', 'MIN')} AND {parameters.get('max_value', 'MAX')};
""",
        
        'expect_column_values_to_match_regex': f"""
-- Check {column} values NOT matching pattern
-- Pattern: {parameters.get('regex', 'PATTERN')}
SELECT {column}, COUNT(*) as non_matching_count
FROM {{{{table}}}}
WHERE {column} !~ '{parameters.get('regex', 'PATTERN')}'
GROUP BY {column};
""",
        
        'expect_column_values_to_not_match_regex': f"""
-- Check {column} values matching pattern (should NOT match)
-- Pattern: {parameters.get('regex', 'PATTERN')}
SELECT {column}, COUNT(*) as matching_count
FROM {{{{table}}}}
WHERE {column} ~ '{parameters.get('regex', 'PATTERN')}'
GROUP BY {column};
""",
        
        'expect_column_values_to_be_in_set': f"""
-- Check {column} values NOT in allowed set
-- Allowed values: {parameters.get('value_set', '[VALUES]')}
SELECT {column}, COUNT(*) as invalid_count
FROM {{{{table}}}}
WHERE {column} NOT IN {parameters.get('value_set', '(VALUES)')}
GROUP BY {column};
""",
        
        'expect_column_values_to_be_of_type': f"""
-- Type validation is typically handled at the schema level
-- GX will query column metadata or attempt casting
SELECT COUNT(*) as type_mismatch_count
FROM {{{{table}}}}
WHERE NOT ({column}::text ~ '^[0-9]+$');  -- Example for integer check
""",
        
        'expect_column_min_to_be_between': f"""
-- Check if minimum value of {column} is in range
SELECT MIN({column}) as min_value
FROM {{{{table}}}};
-- Then verify: min_value BETWEEN {parameters.get('min_value', 'MIN')} AND {parameters.get('max_value', 'MAX')}
""",
        
        'expect_column_max_to_be_between': f"""
-- Check if maximum value of {column} is in range
SELECT MAX({column}) as max_value
FROM {{{{table}}}};
-- Then verify: max_value BETWEEN {parameters.get('min_value', 'MIN')} AND {parameters.get('max_value', 'MAX')}
""",
        
        'expect_column_mean_to_be_between': f"""
-- Check if mean of {column} is in range
SELECT AVG({column}) as mean_value
FROM {{{{table}}}};
-- Then verify: mean_value BETWEEN {parameters.get('min_value', 'MIN')} AND {parameters.get('max_value', 'MAX')}
""",
        
        'expect_column_distinct_values_to_be_in_set': f"""
-- Check for distinct values NOT in allowed set
SELECT DISTINCT {column}
FROM {{{{table}}}}
WHERE {column} NOT IN {parameters.get('value_set', '(VALUES)')};
""",
        
        'expect_column_to_exist': f"""
-- Check if column exists (via metadata query)
SELECT column_name
FROM information_schema.columns
WHERE table_name = '{{{{table}}}}'
  AND column_name = '{column}';
""",
    }
    
    return sql_templates.get(
        expectation_type,
        f"""
-- SQL query generated by Great Expectations
-- Expectation type: {expectation_type}
-- Column: {column}
SELECT COUNT(*) FROM {{{{table}}}} WHERE <expectation_logic>;
"""
    ).strip()

