#!/bin/bash
# Docker Compose startup script for Ollama Jupyter project

echo "🐳 Starting Ollama Jupyter Docker Environment"
echo "=============================================="

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker Compose is available"

# Start services
echo "🚀 Starting Oracle and PostgreSQL databases..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."

# Wait for PostgreSQL
echo "📊 Waiting for PostgreSQL..."
while ! docker exec postgres_gx pg_isready -U try_gx &> /dev/null; do
    echo "   Still waiting for PostgreSQL..."
    sleep 5
done
echo "✅ PostgreSQL is ready!"

# Wait for Oracle
echo "🗄️  Waiting for Oracle..."
while ! docker exec oracle19c sqlplus -s system/oracle@//localhost:1521/XE <<< "SELECT 1 FROM DUAL;" &> /dev/null; do
    echo "   Still waiting for Oracle..."
    sleep 10
done
echo "✅ Oracle is ready!"

echo ""
echo "🎉 All services are running!"
echo ""
echo "📋 Connection Information:"
echo "=========================="
echo ""
echo "Oracle Database:"
echo "  Host: localhost"
echo "  Port: 1521"
echo "  Service: FREEPDB1"
echo "  Username: system"
echo "  Password: oracle"
echo ""
echo "PostgreSQL Database:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: gx_example_db"
echo "  Username: try_gx"
echo "  Password: try_gx"
echo ""
echo "🚀 Next Steps:"
echo "1. Start Jupyter: jupyter notebook notebooks/great_expectations/"
echo "2. Run the Great Expectations workflows"
echo "3. Stop services: docker-compose down"
echo ""
echo "📊 To view logs: docker-compose logs"
echo "🛑 To stop: docker-compose down"
