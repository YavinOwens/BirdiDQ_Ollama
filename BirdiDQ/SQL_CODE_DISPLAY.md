# SQL Code Display in Data Docs

## ✅ **Updated: Now Shows Both Python & SQL!**

Great Expectations Data Docs now display **both Python code and approximate SQL queries** for expectations!

---

## 📊 **What You'll See in Data Docs**

### **For PostgreSQL Expectations (SQL Engine):**

When you open an expectation in Data Docs, you'll see:

```markdown
### 📝 Implementation Details

**Python Code:**
```python
validator.expect_column_values_to_match_regex(column="store_and_fwd_flag", regex=r"^[NY]$")
```

**Execution Engine:** PostgreSQL (SQL)

**Approximate SQL Query:**
```sql
-- Check store_and_fwd_flag values NOT matching pattern
-- Pattern: r"^[NY]$"
SELECT store_and_fwd_flag, COUNT(*) as non_matching_count
FROM {table}
WHERE store_and_fwd_flag !~ '^[NY]$'
GROUP BY store_and_fwd_flag;
```

**Note:** This is a simplified example. Great Expectations generates optimized SQL with batching, sampling, and additional logic.
```

### **For Oracle Expectations (Pandas Engine):**

```markdown
### 📝 Implementation Details

**Python Code:**
```python
validator.expect_column_values_to_be_unique(column="TRANSACTION_ID")
```

**Execution Engine:** Oracle (Pandas)

---
*This expectation is executed using Great Expectations' Oracle (Pandas) execution engine.*
```

---

## 🎯 **SQL vs Python Execution**

### **PostgreSQL - SQL Execution:**
- ✅ **Runs actual SQL** against the database
- ✅ **Shows approximate SQL** in Data Docs
- 🚀 **Memory efficient** - doesn't load entire table
- ⚡ **Database-optimized** - leverages PostgreSQL indexes

### **Oracle - Pandas Execution:**
- ⚠️ **Loads data into Python** as DataFrame
- ❌ **No SQL shown** (not running SQL)
- 💾 **Memory intensive** for large tables
- 🐍 **Pure Python** validation logic

**Why the difference?**
- PostgreSQL has native GX Fluent API support (`context.sources.add_postgres()`)
- Oracle requires client libraries that weren't working, so we use Pandas as a workaround

---

## 📝 **Supported SQL Examples**

The code display now includes SQL examples for these common expectations:

| Expectation | SQL Example Shown |
|-------------|------------------|
| `expect_column_values_to_be_unique` | `SELECT column, COUNT(*) ... HAVING COUNT(*) > 1` |
| `expect_column_values_to_not_be_null` | `SELECT COUNT(*) ... WHERE column IS NULL` |
| `expect_column_values_to_be_between` | `SELECT COUNT(*) ... WHERE column NOT BETWEEN min AND max` |
| `expect_column_values_to_match_regex` | `SELECT column, COUNT(*) ... WHERE column !~ 'pattern'` |
| `expect_column_values_to_not_match_regex` | `SELECT column, COUNT(*) ... WHERE column ~ 'pattern'` |
| `expect_column_values_to_be_in_set` | `SELECT column, COUNT(*) ... WHERE column NOT IN (values)` |
| `expect_column_min_to_be_between` | `SELECT MIN(column) FROM {table}` |
| `expect_column_max_to_be_between` | `SELECT MAX(column) FROM {table}` |
| `expect_column_mean_to_be_between` | `SELECT AVG(column) FROM {table}` |
| `expect_column_distinct_values_to_be_in_set` | `SELECT DISTINCT column ... WHERE column NOT IN (values)` |
| `expect_column_to_exist` | `SELECT column_name FROM information_schema.columns` |

---

## 🔍 **Important Caveats**

### **These are APPROXIMATE examples, not exact SQL:**

1. **GX's Actual SQL is More Complex**
   - Includes batching logic
   - Adds sampling for large tables
   - Optimizes for performance
   - Handles edge cases (NULL, special characters, etc.)
   - Uses parameterized queries

2. **SQL is Generated Dynamically**
   - Great Expectations doesn't expose the exact SQL through public APIs
   - SQL varies based on:
     - Database type (PostgreSQL, MySQL, Snowflake, etc.)
     - GX version
     - Configuration settings
     - Batch size and sampling

3. **These Examples Are Educational**
   - Help you understand *what* the expectation is checking
   - Show the *general approach* GX uses
   - Useful for debugging and learning
   - **NOT meant to be copy-pasted for production use**

---

## 🧪 **Test It Now**

### **Try with PostgreSQL:**

1. Open Streamlit: **http://localhost:8503**
2. Go to **PostgreSQL** tab
3. Select **nyc_taxi_data**
4. Enter a request:
   ```
   store_and_fwd_flag should only contain Y or N
   ```
5. Click **"Generate & Execute Expectations"**
6. Click **"Open Data Docs"**
7. Navigate to the expectation
8. **You'll see both Python code AND SQL!**

### **What You'll See:**

**Python:**
```python
validator.expect_column_values_to_match_regex(column="store_and_fwd_flag", regex=r"^[NY]$")
```

**SQL:**
```sql
-- Check store_and_fwd_flag values NOT matching pattern
-- Pattern: r"^[NY]$"
SELECT store_and_fwd_flag, COUNT(*) as non_matching_count
FROM {table}
WHERE store_and_fwd_flag !~ '^[NY]$'
GROUP BY store_and_fwd_flag;
```

---

## 🛠️ **How It Works**

### **1. Enhancement Function:**
```python
from helpers.code_display_enhancer import enhance_expectation_with_code

# Original expectation
line = 'validator.expect_column_values_to_be_unique(column="id")'

# Enhanced with code display metadata (including SQL for PostgreSQL)
enhanced = enhance_expectation_with_code(line, execution_engine="PostgreSQL (SQL)")
```

### **2. Parameter Extraction:**
```python
from helpers.code_display_enhancer import extract_expectation_info

info = extract_expectation_info(line)
# Returns: {
#   'type': 'expect_column_values_to_be_unique',
#   'column': 'id',
#   'parameters': {}
# }
```

### **3. SQL Generation:**
```python
from helpers.code_display_enhancer import generate_sql_example

sql = generate_sql_example(info['type'], info['column'], info['parameters'])
# Returns appropriate SQL template for the expectation type
```

---

## 🎨 **Customization**

Want to add more SQL examples or modify existing ones?

Edit `BirdiDQ/great_expectations/helpers/code_display_enhancer.py`:

```python
def generate_sql_example(expectation_type: str, column: str, parameters: Dict[str, Any]) -> str:
    sql_templates = {
        'expect_column_values_to_be_unique': f"""
-- Your custom SQL example here
SELECT {column}, COUNT(*) as duplicate_count
FROM {{{{table}}}}
GROUP BY {column}
HAVING COUNT(*) > 1;
""",
        # Add more templates...
    }
```

---

## 🔮 **Future: Actual SQL Capture**

### **Why We Can't Show Exact SQL (Yet):**

Great Expectations generates SQL internally during metric calculation, but:
1. It's not exposed through public APIs
2. It's deeply embedded in the execution engine
3. Different databases use different SQL dialects
4. The SQL includes internal GX optimizations

### **Potential Solutions:**

1. **Database Query Logging**
   - Enable PostgreSQL query logging
   - Capture queries during expectation execution
   - Parse logs to extract GX-generated SQL
   - Display in Data Docs

2. **GX Engine Hooks**
   - If GX adds public APIs in future versions
   - Hook into the execution engine
   - Capture SQL before execution

3. **SQL Explain Plans**
   - For databases that support it
   - Show query execution plans
   - Useful for performance optimization

---

## 📊 **Benefits**

### **For PostgreSQL Users:**

✅ **Full Transparency** - See both Python and SQL
✅ **Educational** - Learn SQL patterns for data validation
✅ **Debugging** - Understand what's being checked
✅ **Performance Insights** - See how queries are structured
✅ **Database-Specific** - SQL adapts to expectation type

### **For Oracle Users:**

✅ **Python Code Shown** - See the expectation logic
ℹ️ **No SQL** (because it's not running SQL)
✅ **Engine Clarity** - Clearly labeled as "Pandas" execution

---

## ❓ **FAQ**

**Q: Is this the exact SQL that Great Expectations runs?**
A: No, these are simplified examples. GX's actual SQL is more complex and optimized.

**Q: Can I copy this SQL and run it directly?**
A: You can try, but you'll need to replace `{table}` with your actual table name and add proper error handling. The examples are meant to be educational.

**Q: Why don't I see SQL for Oracle expectations?**
A: Oracle expectations use Pandas (Python) execution, not SQL, so there's no SQL to show.

**Q: Can I add my own SQL examples for custom expectations?**
A: Yes! Edit `code_display_enhancer.py` and add your expectation type to the `sql_templates` dictionary.

**Q: Will this slow down my validations?**
A: No! The SQL examples are generated once when the expectation is created and stored in metadata. There's no performance impact during validation.

**Q: What if my expectation type isn't in the SQL templates?**
A: The code will show a generic SQL comment indicating that GX generates SQL for that expectation type. You can add a specific template if needed.

---

## 📚 **Related Documentation**

- `CODE_DISPLAY_IN_DATA_DOCS.md` - General code display feature
- `BirdiDQ/great_expectations/helpers/code_display_enhancer.py` - Implementation
- Great Expectations SQL Expectations: https://docs.greatexpectations.io/docs/core/customize_expectations/use_sql_to_define_a_custom_expectation/

---

**🎉 Enjoy your enhanced Data Docs with full SQL transparency for PostgreSQL!**

