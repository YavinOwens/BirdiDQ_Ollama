# Docker Setup for Ollama Jupyter - Data Validation & AI Integration

This Docker Compose configuration provides a complete development environment for the Ollama Jupyter project, including Oracle and PostgreSQL databases for Great Expectations data validation workflows.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available for containers
- Ports 1521 (Oracle) and 5432 (PostgreSQL) available

## Quick Start

### 1. Start All Services
```bash
docker-compose up -d
```

### 2. Wait for Services to be Ready
```bash
# Check Oracle status
docker-compose logs oracle19c

# Check PostgreSQL status  
docker-compose logs postgres
```

### 3. Verify Connections
```bash
# Test Oracle connection
docker exec oracle19c sqlplus -s system/oracle@//localhost:1521/XE <<< "SELECT 1 FROM DUAL;"

# Test PostgreSQL connection
docker exec postgres_gx psql -U try_gx -d gx_example_db -c "SELECT 1;"
```

## Database Connections

### Oracle Database
- **Host**: localhost
- **Port**: 1521
- **Service**: FREEPDB1
- **Username**: system
- **Password**: oracle
- **Connection String**: `oracle+cx_oracle://system:oracle@localhost:1521/FREEPDB1`

### PostgreSQL Database
- **Host**: localhost
- **Port**: 5432
- **Database**: gx_example_db
- **Username**: try_gx
- **Password**: try_gx
- **Connection String**: `postgresql+psycopg2://try_gx:try_gx@localhost:5432/gx_example_db`

## Available Data

### PostgreSQL Tables
- `nyc_taxi_data` - Sample NYC taxi trip data
- `housing_data` - Real estate data for validation testing
- `supermarket_sales` - Retail sales data

### Oracle Tables
- Use the existing Oracle setup scripts to create additional tables as needed

## Management Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs oracle19c
docker-compose logs postgres
```

### Restart Services
```bash
docker-compose restart
```

### Remove Everything (including data)
```bash
docker-compose down -v
```

## Development Workflow

1. **Start the databases**: `docker-compose up -d`
2. **Run Jupyter notebooks**: `jupyter notebook notebooks/great_expectations/`
3. **Test connections**: Use the connection strings above in your notebooks
4. **Stop when done**: `docker-compose down`

## Troubleshooting

### Oracle Issues
- **Slow startup**: Oracle takes 2-3 minutes to fully initialize
- **Connection refused**: Wait for health check to pass
- **Memory issues**: Ensure Docker has at least 4GB RAM allocated

### PostgreSQL Issues
- **Permission denied**: Check if port 5432 is already in use
- **Data not loading**: Check init script execution in logs

### Port Conflicts
If ports are already in use, modify the `docker-compose.yml` file:
```yaml
ports:
  - "1522:1521"  # Change Oracle port
  - "5433:5432"  # Change PostgreSQL port
```

## Data Persistence

- **Oracle data**: Stored in `oracle_data` volume
- **PostgreSQL data**: Stored in `postgres_data` volume
- **Backups**: Oracle backups stored in `oracle_backup` volume

Data persists between container restarts. Use `docker-compose down -v` to remove all data.

## Security Notes

- Default passwords are used for development only
- Change passwords in production environments
- Consider using Docker secrets for sensitive data

## Integration with Great Expectations

The databases are pre-configured to work with the Great Expectations notebooks:

1. **Oracle**: Use for enterprise data validation workflows
2. **PostgreSQL**: Use for standard data validation and PySpark workflows
3. **Sample data**: Ready-to-use datasets for testing expectations

## Next Steps

1. Run the Great Expectations notebooks:
   - `great_expectations_batch.ipynb` - PostgreSQL workflow
   - `great_expectations_spark.ipynb` - PySpark workflow
   - `demo.ipynb` - General demonstration

2. Explore the Data Assistants and validation workflows

3. Customize the setup for your specific data sources
