#!/bin/bash
# Oracle 19c Database Setup Script for Great Expectations Demo

echo "Setting up Oracle 19c database for Great Expectations demo"
echo "============================================================="

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker is not running. Please start Docker first."
    exit 1
fi

echo "[OK] Docker is running"

# Check if Oracle container already exists
if docker ps -a --format "table {{.Names}}" | grep -q "oracle19c"; then
    echo "[INFO] Oracle container already exists"
    
    # Check if it's running
    if docker ps --format "table {{.Names}}" | grep -q "oracle19c"; then
        echo "[OK] Oracle container is already running"
    else
        echo "[INFO] Starting existing Oracle container..."
        docker start oracle19c
        echo "[OK] Oracle container started"
    fi
else
    echo "[INFO] Creating new Oracle 19c container..."
    
    # Pull Oracle Database Free image (publicly available)
    echo "[INFO] Pulling Oracle Database Free image..."
    docker pull gvenzl/oracle-free:slim-faststart
    
    # Create and start Oracle container
    echo "[INFO] Starting Oracle container..."
    docker run -d --name oracle19c \
        -p 1521:1521 \
        -e ORACLE_PASSWORD=oracle \
        gvenzl/oracle-free:slim-faststart
    
    echo "[OK] Oracle container created and started"
fi

echo ""
echo "[INFO] Waiting for Oracle database to be ready..."
echo "This may take 2-3 minutes on first startup..."

# Wait for database to be ready
while true; do
    if docker logs oracle19c 2>&1 | grep -q "DATABASE IS READY TO USE" || docker logs oracle19c 2>&1 | grep -q "Database ready to use" || docker logs oracle19c 2>&1 | grep -q "Database is ready to use"; then
        echo "[OK] Oracle database is ready!"
        break
    fi
    
    echo "[INFO] Still waiting for database to be ready..."
    sleep 10
done

echo ""
echo "[INFO] Testing database connection..."

# Test connection
if docker exec oracle19c sqlplus -s system/oracle@//localhost:1521/XE <<< "SELECT 1 FROM DUAL;" &> /dev/null; then
    echo "[OK] Database connection test successful"
else
    echo "[ERROR] Database connection test failed"
    echo "Please wait a bit longer and try again"
    exit 1
fi

echo ""
echo "Oracle Database Information:"
echo "Host: localhost"
echo "Port: 1521"
echo "Service: FREEPDB1"
echo "Username: system"
echo "Password: oracle"
echo "Database: Oracle Database Free (gvenzl)"

echo ""
echo "Next steps:"
echo "1. Run the Great Expectations notebook:"
echo "   jupyter notebook notebooks/great_expectations_oracle_demo.ipynb"
echo "2. Execute the cells to test data validation"
echo ""
echo "To stop Oracle later:"
echo "   docker stop oracle19c"
echo ""
echo "To restart Oracle:"
echo "   docker start oracle19c"
echo ""
echo "To remove Oracle container:"
echo "   docker stop oracle19c && docker rm oracle19c"
