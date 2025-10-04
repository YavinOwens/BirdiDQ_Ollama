import ollama
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from main project directory
# Use absolute path to ensure reliability
env_path = '/Users/yavin/python_projects/ollama_jupyter/.env'
load_dotenv(env_path)

def load_ollama_client():
    """
    Initialize and return Ollama client with cloud configuration
    Returns:
        ollama.Client: Configured Ollama client
    """
    try:
        # Get configuration from environment variables
        cloud_url = os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com')
        api_key = os.getenv('OLLAMA_API_KEY')
        
        if not api_key:
            raise ValueError("OLLAMA_API_KEY not found in environment variables")
        
        # Create client with cloud configuration
        client = ollama.Client(
            host=cloud_url,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        
        return client
    except Exception as e:
        print(f"Error initializing Ollama client: {e}")
        raise

def get_expectations(prompt, client=None, model_name=None, available_columns=None):
    """
    Convert natural language query to great expectation methods using Ollama
    
    Params:
        prompt (str): Natural language query
        client (ollama.Client): Ollama client instance (optional)
        model_name (str): Model name to use (optional)
        available_columns (list): List of actual column names from the data (optional)
    
    Returns:
        str: Generated Great Expectations code
    """
    import time
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Initialize client if not provided
            if client is None:
                client = load_ollama_client()
            
            # Get model name from environment or use default
            if model_name is None:
                model_name = os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
            
            # Create a more specific prompt for Great Expectations
            system_prompt = """You are an expert in Great Expectations data validation library.
            Convert the following natural language description into Python code using the validator.expect_*() format.
            
            CRITICAL INSTRUCTIONS:
            - Return ONLY executable Python code using validator.expect_*() methods
            - NO explanations, NO thinking process, NO markdown, NO comments
            - Use the format: validator.expect_column_values_to_be_unique(column="column_name")
            - Each expectation on a new line
            - Do NOT use expectation_suite.add_expectation()
            - Do NOT import anything
            - Use EXACT column names as provided in the available columns list
            - Column names are CASE-SENSITIVE - use them EXACTLY as shown
            
            Example 1:
            Input: "Check that none of the values in the address column match the pattern for an address starting with a digit"
            Output: validator.expect_column_values_to_not_match_regex(column="address", regex=r"^\\d")
            
            Example 2:
            Input: "transaction_id should be unique and customer_id should not be null"
            Output: validator.expect_column_values_to_be_unique(column="transaction_id")
            validator.expect_column_values_to_not_be_null(column="customer_id")
            
            Example 3:
            Input: "amount should be greater than 0"
            Output: validator.expect_column_values_to_be_between(column="amount", min_value=0, strict_min=True)
            """
            
            # Add available columns if provided
            if available_columns:
                columns_str = ", ".join(f'"{col}"' for col in available_columns)
                system_prompt += f"\n\nIMPORTANT - Available columns in this dataset: {columns_str}\n"
                system_prompt += "You MUST use these exact column names (case-sensitive) in your expectations.\n"
            
            system_prompt += "\nNatural language description:"
            full_prompt = f"{system_prompt}\n{prompt}"
            
            # Generate response using Ollama
            response = client.generate(
                model=model_name,
                prompt=full_prompt,
                options={
                    'temperature': 0.3,
                    'top_p': 0.9,
                    'num_predict': 200
                }
            )
            
            # Extract the response text
            generated_code = response.get('response', '').strip()
            
            # Clean up the response to extract just the code
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()
            
            # Additional cleaning: Extract only validator.expect_* lines
            # This filters out reasoning/thinking text
            lines = generated_code.split('\n')
            validator_lines = []
            
            for line in lines:
                line = line.strip()
                # Only include lines that start with validator.expect_
                # or are continuation lines (for multi-line expectations)
                if line.startswith('validator.expect_'):
                    validator_lines.append(line)
                elif validator_lines and line and not any(keyword in line.lower() for keyword in 
                    ['we need', 'actually', 'wait', 'so code:', 'but', 'output:', 'means', 'they\'d use', 'should use']):
                    # This might be a continuation line (e.g., multi-line expectation)
                    validator_lines.append(line)
            
            # If we found validator lines, use those
            if validator_lines:
                generated_code = '\n'.join(validator_lines)
            
            # If the generated code still contains reasoning keywords, try to extract the last validator call
            reasoning_keywords = ['we need to produce', 'actually', 'wait:', 'so code:', 'but the', 'means']
            if any(keyword in generated_code.lower() for keyword in reasoning_keywords):
                # Find all validator.expect_ patterns
                import re
                validator_pattern = r'validator\.expect_[a-z_]+\([^)]*\)'
                matches = re.findall(validator_pattern, generated_code, re.IGNORECASE)
                if matches:
                    # Use the last complete match (usually the final answer)
                    generated_code = '\n'.join(matches)
            
            return generated_code
            
        except Exception as e:
            error_msg = str(e)
            print(f"Attempt {attempt + 1} failed: {error_msg}")
            
            # Check if it's a 502 error or similar API issue
            if "502" in error_msg or "upstream error" in error_msg.lower() or "bad gateway" in error_msg.lower():
                if attempt < max_retries - 1:
                    print(f"API error detected, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    print("Max retries reached for API error")
                    # Return a valid expectation as fallback
                    raise Exception(f"Ollama API error after {max_retries} attempts: {error_msg}")
            else:
                # Non-API error, raise immediately
                raise Exception(f"Error generating expectation: {error_msg}")
    
    # If we get here, all retries failed
    raise Exception(f"Ollama API error: upstream error (status code: 502) after {max_retries} attempts")

def test_ollama_connection():
    """
    Test the Ollama connection and return status
    Returns:
        dict: Connection status and model information
    """
    try:
        client = load_ollama_client()
        model_name = os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
        
        # Test with a simple prompt
        test_response = client.generate(
            model=model_name,
            prompt="Hello, are you working?",
            options={'num_predict': 10}
        )
        
        return {
            'status': 'success',
            'model': model_name,
            'response': test_response['response'],
            'message': 'Ollama connection successful'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Ollama connection failed'
        }
