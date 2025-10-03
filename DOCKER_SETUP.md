# Docker Setup for Ollama Jupyter - Data Validation & AI Integration

This Docker Compose configuration provides Oracle database for the Ollama Jupyter project. PostgreSQL is available online from the Great Expectations workshop.

## Prerequisites

- Docker and Docker Compose installed
- At least 2GB RAM available for Oracle container
- Port 1521 (Oracle) available
- Internet connection for PostgreSQL access

## Quick Start

### 1. Start Oracle Service
```bash
docker-compose up -d
```

### 2. Wait for Oracle to be Ready
```bash
# Check Oracle status
docker-compose logs oracle19c
```

### 3. Verify Oracle Connection
```bash
# Test Oracle connection
docker exec oracle19c sqlplus -s system/oracle@//localhost:1521/XE <<< "SELECT 1 FROM DUAL;"
```

## Database Connections

### Oracle Database (Local Docker)
- **Host**: localhost
- **Port**: 1521
- **Service**: FREEPDB1
- **Username**: system
- **Password**: oracle
- **Connection String**: `oracle+cx_oracle://system:oracle@localhost:1521/FREEPDB1`

### PostgreSQL Database (Online - Great Expectations Workshop)
- **Host**: postgres.workshops.greatexpectations.io
- **Port**: 5432
- **Database**: gx_example_db
- **Username**: try_gx
- **Password**: try_gx
- **Connection String**: `postgresql+psycopg2://try_gx:try_gx@postgres.workshops.greatexpectations.io/gx_example_db`

## Available Data

### PostgreSQL Tables (Online)
- `nyc_taxi_data` - Sample NYC taxi trip data
- Additional tables available from Great Expectations workshop

### Oracle Tables (Local)
- Use the existing Oracle setup scripts to create additional tables as needed

## Management Commands

### Start Oracle Service
```bash
docker-compose up -d
```

### Stop Oracle Service
```bash
docker-compose down
```

### View Logs
```bash
# Oracle logs
docker-compose logs oracle19c
```

### Restart Oracle Service
```bash
docker-compose restart
```

### Remove Everything (including data)
```bash
docker-compose down -v
```

## Development Workflow

1. **Start Oracle**: `docker-compose up -d`
2. **Run Jupyter notebooks**: `jupyter notebook notebooks/great_expectations/`
3. **Test connections**: Use the connection strings above in your notebooks
4. **Stop when done**: `docker-compose down`

## Troubleshooting

### Oracle Issues
- **Slow startup**: Oracle takes 2-3 minutes to fully initialize
- **Connection refused**: Wait for health check to pass
- **Memory issues**: Ensure Docker has at least 2GB RAM allocated

### PostgreSQL Issues
- **Connection issues**: Ensure internet connectivity to Great Expectations workshop server
- **Authentication failed**: Verify credentials are correct

### Port Conflicts
If port 1521 is already in use, modify the `docker-compose.yml` file:
```yaml
ports:
  - "1522:1521"  # Change Oracle port
```

## Data Persistence

- **Oracle data**: Stored in `oracle_data` volume
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
