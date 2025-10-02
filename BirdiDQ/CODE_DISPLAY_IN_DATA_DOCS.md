# Code Display in Data Docs

## ✅ **Yes! You Can Display Python Code in Data Docs**

Great Expectations Data Docs now display the **Python code** that generated each expectation in your validation suites!

---

## 📋 **What's Been Added**

### **New Feature: Code Display in Expectation Notes**

When you create expectations (either via LLM or Data Assistants), the Python code is automatically embedded in the expectation's metadata and displayed in the Data Docs HTML.

### **Location in Data Docs:**

1. Open Data Docs (click "Open Data Docs" button in Streamlit)
2. Navigate to an **Expectation Suite**
3. Click on any **individual expectation**
4. You'll see a **"Notes" section** with:
   - 📝 **Python Code** - The exact `validator.expect_*()` call
   - ⚙️ **Execution Engine** - PostgreSQL (SQL) or Oracle (Pandas)
   - ℹ️ **Additional context** about how the expectation is executed

---

## 🛠️ **Implementation Details**

### **How It Works:**

1. **Automatic Enhancement**
   - When an expectation is created in `run_expectation()`, it's passed through `enhance_expectation_with_code()`
   - This function adds a `meta` parameter with markdown-formatted notes
   - The notes contain the Python code and execution engine info

2. **Code Enhancement Function**
   ```python
   from helpers.code_display_enhancer import enhance_expectation_with_code
   
   # Original expectation
   line = 'validator.expect_column_values_to_be_unique(column="id")'
   
   # Enhanced with code display metadata
   enhanced = enhance_expectation_with_code(line, execution_engine="PostgreSQL (SQL)")
   # Result: validator.expect_column_values_to_be_unique(column="id", meta={...})
   ```

3. **Metadata Structure**
   ```python
   meta = {
       "notes": {
           "format": "markdown",
           "content": [
               """### 📝 Implementation Details
               
               **Python Code:**
               ```python
               validator.expect_column_values_to_be_unique(column="id")
               ```
               
               **Execution Engine:** PostgreSQL (SQL)
               
               ---
               *This expectation is executed using Great Expectations' PostgreSQL (SQL) execution engine.*
               """
           ]
       }
   }
   ```

### **Where It's Applied:**

- ✅ **PostgreSQL datasource** (`postgresql.py`)
  - Uses SQL execution engine
  - Code display shows `PostgreSQL (SQL)`
  
- ✅ **Oracle datasource** (`oracle.py`)
  - Uses Pandas execution engine (due to Oracle Client library limitations)
  - Code display shows `Oracle (Pandas)`

- ✅ **All LLM-generated expectations**
  - Automatically enhanced when executed

- ✅ **Data Assistants** (Onboarding, Missingness)
  - Not currently enhanced (could be added if needed)

---

## 🎨 **Example: What You'll See in Data Docs**

### **Before:**
```
Expectation: expect_column_values_to_be_unique

Column: transaction_id
```

### **After (with Code Display):**
```
Expectation: expect_column_values_to_be_unique

Column: transaction_id

Notes:
─────────────────────────────────────────
📝 Implementation Details

Python Code:
validator.expect_column_values_to_be_unique(column="transaction_id")

Execution Engine: PostgreSQL (SQL)

Note: The actual SQL query is generated dynamically by Great Expectations 
based on the expectation type and parameters.
─────────────────────────────────────────
```

---

## 💡 **SQL Query Display (Future Enhancement)**

### **Current State:**
- ✅ Python code is displayed
- ℹ️ Execution engine is identified
- ⚠️ **Actual SQL queries are NOT shown** (GX generates these internally and doesn't easily expose them)

### **Why SQL Queries Aren't Shown:**

Great Expectations:
1. Generates SQL dynamically based on the execution engine
2. Optimizes queries internally (batching, sampling, etc.)
3. Doesn't expose the generated SQL through public APIs

### **Workaround: Example SQL**

The `code_display_enhancer.py` module includes a `generate_sql_example()` function that can create **approximate** SQL examples for common expectations:

```python
from helpers.code_display_enhancer import generate_sql_example, extract_expectation_info

line = 'validator.expect_column_values_to_be_unique(column="id")'
info = extract_expectation_info(line)
sql = generate_sql_example(info['type'], info['column'], info['parameters'])

print(sql)
# Output:
# -- Check for duplicate values
# SELECT id, COUNT(*) as count
# FROM {table}
# GROUP BY id
# HAVING COUNT(*) > 1
```

**To enable example SQL in Data Docs**, modify the `enhance_expectation_with_code()` function to include this.

---

## 🔧 **Files Modified**

### **1. New File: `BirdiDQ/great_expectations/helpers/code_display_enhancer.py`**
- `enhance_expectation_with_code()` - Adds code display metadata
- `extract_expectation_info()` - Parses expectation parameters
- `generate_sql_example()` - Creates example SQL queries

### **2. Updated: `BirdiDQ/great_expectations/connecting_data/database/postgresql.py`**
- Imports `enhance_expectation_with_code`
- Enhances expectations before execution in `run_expectation()`
- Specifies execution engine as `"PostgreSQL (SQL)"`

### **3. Updated: `BirdiDQ/great_expectations/connecting_data/database/oracle.py`**
- Imports `enhance_expectation_with_code`
- Enhances expectations before execution in `run_expectation()`
- Specifies execution engine as `"Oracle (Pandas)"`

---

## 🧪 **Testing the Feature**

### **Test with PostgreSQL:**

1. Go to Streamlit app: http://localhost:8503
2. Select **PostgreSQL** tab
3. Choose **nyc_taxi_data**
4. Enter a natural language request:
   ```
   store_and_fwd_flag should only contain Y or N
   ```
5. Click **"Generate & Execute Expectations"**
6. Click **"Open Data Docs"**
7. Navigate to the expectation suite
8. Click on the expectation
9. **You should see** the Python code in the Notes section!

### **Test with Oracle:**

1. Select **Oracle** tab
2. Choose **TRANSACTIONS**
3. Enter a request:
   ```
   transaction_id must be unique
   ```
4. Follow same steps as PostgreSQL
5. Notes will show `Oracle (Pandas)` execution engine

---

## 📊 **Benefits**

1. **✅ Transparency** - Users can see exactly what code is running
2. **✅ Debugging** - Easier to troubleshoot failed expectations
3. **✅ Learning** - Helps users understand GX expectation syntax
4. **✅ Documentation** - Self-documenting validation rules
5. **✅ Reproducibility** - Copy-paste code to reproduce expectations

---

## 🔮 **Future Enhancements**

### **Potential Additions:**

1. **Actual SQL Queries**
   - If GX exposes SQL generation APIs in future versions
   - Or by hooking into the execution engine's query generation

2. **Execution Statistics**
   - Query execution time
   - Number of rows scanned
   - Performance metrics

3. **Visual SQL Explain Plans**
   - For SQL execution engines
   - Show how the database will execute the query

4. **Interactive Code Editor**
   - Edit expectation parameters directly in Data Docs
   - Re-run validations with modified expectations

5. **Code Export**
   - One-click export of all expectations as a Python script
   - Generate Jupyter notebooks from expectation suites

---

## 📚 **References**

- **Great Expectations Docs**: [Custom Expectations](https://docs.greatexpectations.io/docs/core/customize_expectations/)
- **UnexpectedRowsExpectation**: [Use SQL to Define Custom Expectations](https://docs.greatexpectations.io/docs/core/customize_expectations/use_sql_to_define_a_custom_expectation/)
- **Meta Parameter**: GX expectations accept a `meta` dict for custom metadata

---

## ❓ **FAQ**

**Q: Will this work with Data Assistants?**
A: Currently, Data Assistants generate expectations without code display. We could extend this feature to them if needed.

**Q: Can I customize the display format?**
A: Yes! Edit `code_display_enhancer.py` to modify the markdown template in `enhance_expectation_with_code()`.

**Q: Does this impact performance?**
A: Minimal impact - just adds metadata to expectations. No change to validation execution time.

**Q: Can I disable this feature?**
A: Yes - comment out the `enhance_expectation_with_code()` calls in `postgresql.py` and `oracle.py`.

---

**🎉 Enjoy your enhanced Data Docs with full code transparency!**

