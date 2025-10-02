#!/usr/bin/env python3
"""
Test script for BirdiDQ Ollama integration
"""

import sys
import os
sys.path.append('great_expectations')

from models.ollama_model import test_ollama_connection, get_expectations, load_ollama_client

def test_ollama_integration():
    """Test the Ollama integration for BirdiDQ"""
    
    print("🧪 Testing BirdiDQ Ollama Integration")
    print("=" * 50)
    
    # Test 1: Connection Test
    print("\n1. Testing Ollama Connection...")
    connection_result = test_ollama_connection()
    
    if connection_result['status'] == 'success':
        print(f"✅ Connection successful!")
        print(f"   Model: {connection_result['model']}")
        print(f"   Response: {connection_result['response']}")
    else:
        print(f"❌ Connection failed: {connection_result['error']}")
        print("   Please check your .env file and OLLAMA_API_KEY")
        return False
    
    # Test 2: Expectation Generation
    print("\n2. Testing Expectation Generation...")
    test_prompt = "Check that none of the values in the address column match the pattern for an address starting with a digit"
    
    try:
        client = load_ollama_client()
        generated_code = get_expectations(test_prompt, client)
        
        print(f"✅ Expectation generated successfully!")
        print(f"   Input: {test_prompt}")
        print(f"   Generated Code:")
        print(f"   {generated_code}")
        
    except Exception as e:
        print(f"❌ Expectation generation failed: {e}")
        return False
    
    print("\n🎉 All tests passed! BirdiDQ is ready to use with Ollama.")
    return True

if __name__ == "__main__":
    # Check if .env file exists in main project directory
    env_path = '/Users/yavin/python_projects/ollama_jupyter/.env'
    if not os.path.exists(env_path):
        print("⚠️  Warning: .env file not found in main project directory!")
        print("   Please ensure your .env file exists at:")
        print("   /Users/yavin/python_projects/ollama_jupyter/.env")
        print("   With your Ollama API key:")
        print("   OLLAMA_CLOUD_BASE_URL=https://ollama.com")
        print("   OLLAMA_CLOUD_MODEL=gpt-oss:20b")
        print("   OLLAMA_API_KEY=your_api_key_here")
        print()
    
    success = test_ollama_integration()
    sys.exit(0 if success else 1)
