#!/usr/bin/env python3
"""
Test script using the exact workflow provided by the user
"""

import sys
import os
sys.path.append('great_expectations')

from dotenv import load_dotenv
import ollama
from datetime import datetime

# Load environment variables from main project directory
load_dotenv('/Users/yavin/python_projects/ollama_jupyter/.env')

# Get environment variables
OLLAMA_CLOUD_BASE_URL = os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com')
OLLAMA_CLOUD_MODEL = os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')

print("🧪 Testing Ollama Connection (User's Workflow)")
print("=" * 50)

# Test connection to Ollama cloud service
if not OLLAMA_API_KEY:
    print("ERROR: Ollama API key not found in .env file!")
else:
    try:
        # Test cloud connection
        cloud_client = ollama.Client(
            host=OLLAMA_CLOUD_BASE_URL,
            headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'}
        )
        
        print("SUCCESS: Successfully connected to Ollama Cloud!")
        print(f"Connection time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Connected to: {OLLAMA_CLOUD_BASE_URL}")
        print(f"Cloud Model: {OLLAMA_CLOUD_MODEL}")
        print(f"API Key: {'Set' if OLLAMA_API_KEY else 'Not set'}")
        
        # request
        print("\nTesting cloud model availability...")
        try:
            response = cloud_client.generate(
                model=OLLAMA_CLOUD_MODEL,
                prompt="Hello",
                options={'num_predict': 10}
            )
            print(f"SUCCESS: Cloud model '{OLLAMA_CLOUD_MODEL}' is working!")
            print(f"Response: {response['response']}")
        except Exception as e:
            print(f"WARNING: Cloud model test failed: {e}")
            
    except Exception as e:
        print(f"ERROR: Failed to connect to Ollama Cloud: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your API key in the .env file")
        print("2. Verify your subscription at https://ollama.com")
        print("3. Check your internet connection")
