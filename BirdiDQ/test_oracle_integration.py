#!/usr/bin/env python3
"""
Test script for BirdiDQ Oracle integration
"""

import sys
import os
sys.path.append('great_expectations')

from connecting_data.database.oracle import ORACLE_CONNECTION_STRING, get_oracle_tables, read_oracle_tables

def test_oracle_integration():
    """Test the Oracle integration for BirdiDQ"""
    
    print("🧪 Testing BirdiDQ Oracle Integration")
    print("=" * 50)
    
    # Test 1: Connection String
    print("\n1. Checking Oracle Connection String...")
    if ORACLE_CONNECTION_STRING:
        print(f"✅ Oracle connection string found!")
        print(f"   Connection: {ORACLE_CONNECTION_STRING}")
    else:
        print("❌ Oracle connection string not found!")
        print("   Please check your .env file and ensure ORACLE_CONNECTION_STRING is set")
        return False
    
    # Test 2: Connection Test
    print("\n2. Testing Oracle Connection...")
    try:
        tables = get_oracle_tables()
        if tables:
            print(f"✅ Connection successful!")
            print(f"   Available tables: {tables}")
        else:
            print("⚠️  Connection successful but no tables found")
            print("   This might be normal if the database is empty")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Please ensure:")
        print("   1. Oracle Docker container is running")
        print("   2. Connection string is correct")
        print("   3. Oracle client libraries are installed")
        return False
    
    # Test 3: Data Reading (if tables exist)
    if tables:
        print("\n3. Testing Data Reading...")
        try:
            test_table = tables[0]  # Use first available table
            data = read_oracle_tables(test_table)
            print(f"✅ Data reading successful!")
            print(f"   Table: {test_table}")
            print(f"   Rows: {len(data)}")
            print(f"   Columns: {list(data.columns)}")
        except Exception as e:
            print(f"❌ Data reading failed: {e}")
            return False
    
    print("\n🎉 Oracle integration test completed!")
    return True

if __name__ == "__main__":
    # Check if .env file exists in main project directory
    env_path = '/Users/yavin/python_projects/ollama_jupyter/.env'
    if not os.path.exists(env_path):
        print("⚠️  Warning: .env file not found in main project directory!")
        print("   Please ensure your .env file exists at:")
        print("   /Users/yavin/python_projects/ollama_jupyter/.env")
        print("   With your Oracle connection string:")
        print("   ORACLE_CONNECTION_STRING=oracle+oracledb://system:oracle@localhost:1521/?service_name=FREEPDB1")
        print()
    
    success = test_oracle_integration()
    sys.exit(0 if success else 1)
