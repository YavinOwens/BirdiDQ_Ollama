#!/bin/bash

echo "🚀 Setting up BirdiDQ with Ollama Integration"
echo "=============================================="

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment detected!"
    echo "   Please activate your virtual environment first:"
    echo "   source venv/bin/activate"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Using existing virtual environment: $VIRTUAL_ENV"

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists in main project directory
if [ ! -f "/Users/yavin/python_projects/ollama_jupyter/.env" ]; then
    echo "⚠️  Warning: .env file not found in main project directory!"
    echo "   Please ensure your .env file exists at:"
    echo "   /Users/yavin/python_projects/ollama_jupyter/.env"
    echo "   With your Ollama API key and PostgreSQL connection string."
else
    echo "✅ Found .env file in main project directory"
fi

# Test the integration
echo "🧪 Testing Ollama integration..."
python test_ollama_integration.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run BirdiDQ:"
echo "1. Edit .env file with your API keys"
echo "2. Run: streamlit run great_expectations/app.py"
echo ""
echo "🌐 The app will be available at http://localhost:8501"
