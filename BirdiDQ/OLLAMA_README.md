# BirdiDQ with Ollama Integration

This is a modified version of [BirdiDQ](https://github.com/BirdiD/BirdiDQ) that replaces the Falcon LLM with Ollama for natural language to Great Expectations conversion.

## Changes Made

### 1. Replaced Falcon Model with Ollama
- **Removed**: `falcon_model.py` dependencies (transformers, peft, torch, etc.)
- **Added**: `ollama_model.py` with Ollama cloud integration
- **Updated**: `app.py` to use Ollama instead of Falcon
- **Updated**: `requirements.txt` to remove heavy ML dependencies

### 2. New Ollama Model Implementation
The `ollama_model.py` provides:
- `load_ollama_client()`: Initialize Ollama client with cloud configuration
- `get_expectations(prompt, client, model_name)`: Convert natural language to GE expectations
- `test_ollama_connection()`: Test Ollama connectivity

### 3. Environment Configuration
Create a `.env` file with the following variables:
```bash
OLLAMA_CLOUD_BASE_URL=https://ollama.com
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_ollama_api_key_here
```

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv birdidq_env
   source birdidq_env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with your Ollama API key
5. Run the application:
   ```bash
   streamlit run great_expectations/app.py
   ```

## Benefits of Using Ollama

1. **Lighter Dependencies**: No need for PyTorch, transformers, or CUDA
2. **Cloud-based**: No local GPU requirements
3. **Faster Setup**: No model downloading or fine-tuning required
4. **Better Performance**: Cloud-based inference is typically faster
5. **Easier Maintenance**: No model version management

## Usage

The application works exactly like the original BirdiDQ:
1. Select your data source (Local File System, PostgreSQL, or Oracle)
2. Choose a table
3. Describe your data quality checks in natural language
4. The Ollama model will generate Great Expectations code
5. View results and data documentation

## Example Queries

- "Ensure that at least 80% of the values in the country column are not null"
- "Check that none of the values in the address column match the pattern for an address starting with a digit"
- "Verify that all prices are positive numbers"

## Original BirdiDQ

This modification is based on the original [BirdiDQ](https://github.com/BirdiD/BirdiDQ) project, which leverages Great Expectations for data quality validation with natural language queries.
