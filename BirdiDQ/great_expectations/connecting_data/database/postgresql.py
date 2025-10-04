import great_expectations as ge
from ruamel import yaml
import ruamel
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint
from dotenv import load_dotenv, find_dotenv
import os 
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import sys
from pathlib import Path

# Import code display enhancer
sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers.code_display_enhancer import enhance_expectation_with_code 

from pathlib import Path

# Load environment variables from main project directory
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

# Get your postgresql connection string from the environment variable
POSTGRES_CONNECTION_STRING = os.environ.get('POSTGRES_CONNECTION_STRING')

def read_pg_tables(table_name):
    """
    Read postgresql table in pandas dataframe
    """
    # Use psycopg2 connection directly (same approach as get_pg_tables)
    # to avoid 'Engine' object has no attribute 'cursor' error
    conn_str = POSTGRES_CONNECTION_STRING.replace('postgresql+psycopg2://', 'postgresql://')
    conn = psycopg2.connect(conn_str)
    
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df

def get_pg_tables():
    """
    List all tables from a PostgreSQL database using a connection string
    """
    try:
        if not POSTGRES_CONNECTION_STRING:
            raise ValueError("POSTGRES_CONNECTION_STRING is not set in environment variables")
        
        # Convert SQLAlchemy connection string to psycopg2 format
        conn_str = POSTGRES_CONNECTION_STRING.replace('postgresql+psycopg2://', 'postgresql://')
        
        # Use psycopg2 directly to avoid Engine object issues
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()

        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        cursor.execute(query)

        tables = cursor.fetchall()
        tables = [t[0] for t in tables]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"Error in get_pg_tables: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise

def postgresql_data_owners():
    """
    Map each postgresql with its data owner
    """
    try:
        tables = get_pg_tables()
        return {datasource : 'postgreso@birdidq.com' for datasource in tables}
    except Exception as e:
        print(f"Error in postgresql_data_owners: {type(e).__name__}: {e}")
        raise

class PostgreSQLDatasource():
    """
    Run Data Quality checks on PostgreSQL data database using Fluent API
    """
    def __init__(self, database, asset_name):
        """ 
        Init class attributes
        """
        self.database = database
        self.asset_name = asset_name
        self.table_name = asset_name  # Use asset_name as table_name
        self.expectation_suite_name = f"{asset_name}_expectation_suite"
        self.checkpoint_name = f"{asset_name}_checkpoint"
        self.context = ge.get_context()
        self.datasource_name = f"postgres_sql_{asset_name}"

    def add_or_update_datasource(self):
        """
        Create PostgreSQL datasource using Fluent API with SQL execution engine
        """
        try:
            # Check if datasource already exists
            existing_datasources = self.context.list_datasources()
            datasource_exists = any(ds['name'] == self.datasource_name for ds in existing_datasources)
            
            if datasource_exists:
                print(f"Using existing datasource: {self.datasource_name}")
                self.datasource = self.context.get_datasource(self.datasource_name)
            else:
                print(f"Creating new PostgreSQL datasource: {self.datasource_name}")
                # Use SQL datasource with Fluent API (native PostgreSQL support)
                self.datasource = self.context.sources.add_postgres(
                    self.datasource_name,
                    connection_string=POSTGRES_CONNECTION_STRING
                )
                
            # Check if asset already exists
            try:
                self.data_asset = self.datasource.get_asset(self.asset_name)
                print(f"Using existing asset: {self.asset_name}")
            except:
                print(f"Creating new asset: {self.asset_name}")
                # Add table asset (uses SQL directly, no DataFrame needed)
                self.data_asset = self.datasource.add_table_asset(
                    name=self.asset_name,
                    table_name=self.table_name
                )
                
        except Exception as e:
            print(f"Error in add_or_update_datasource: {e}")
            raise

    def get_batch_request(self):
        """
        Create a batch request for SQL table (no DataFrame needed)
        """
        return self.data_asset.build_batch_request()

    def get_validator(self):
        """
        Retrieve a validator object using Fluent API with SQL execution engine
        """
        # Set up datasource and asset (SQL-based, no DataFrame loading)
        self.add_or_update_datasource()
        
        # Create batch request (queries SQL directly)
        batch_request = self.get_batch_request()
        
        # Create/get expectation suite
        try:
            self.context.add_or_update_expectation_suite(
                expectation_suite_name=self.expectation_suite_name
            )
        except:
            pass
        
        # Get validator
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=self.expectation_suite_name,
        )
        
        print(f"✅ Validator created successfully using SQL Fluent API")
        return validator, batch_request

    def run_expectation(self, expectation):
        """
        Run your data quality checks here - robustly handles multiple expectation formats
        Uses clean execution environment like working test script
        """
        try:
            validator, batch_request = self.get_validator()
            
            print(f"\n{'='*60}")
            print(f"EXPECTATION INPUT (raw):")
            print(f"{expectation}")
            print(f"{'='*60}\n")
            
            # Process the expectation code - it may contain multiple lines
            expectation_lines = [line.strip() for line in expectation.split('\n') if line.strip()]
            print(f"Parsed into {len(expectation_lines)} lines")
            
            # Set up clean execution environment (like in test script)
            execution_env = {"validator": validator}
            
            results = []
            for idx, line in enumerate(expectation_lines, 1):
                if not line or line.startswith('#'):
                    print(f"Line {idx}: Skipping (empty or comment)")
                    continue
                
                print(f"\nLine {idx}: Attempting to execute:")
                print(f"  '{line}'")
                
                try:
                    # Enhance expectation with code display metadata for Data Docs
                    # This returns the expectation line with meta parameter added
                    enhanced_line, meta_dict = enhance_expectation_with_code(line, execution_engine="PostgreSQL (SQL)", return_meta=True)
                    
                    # Add meta dict to execution environment so it's available when exec runs
                    if meta_dict:
                        execution_env['_expectation_meta'] = meta_dict
                        # Replace the meta placeholder with the actual dict from environment
                        enhanced_line = enhanced_line.replace('meta={...}', 'meta=_expectation_meta')
                    
                    # Execute enhanced expectation
                    # Let GX handle validation naturally (like in working test script)
                    exec(f"result = {enhanced_line}", execution_env)
                    result = execution_env.get("result")
                    
                    if result:
                        results.append(result)
                        print(f"  ✓ SUCCESS: Expectation executed and added to suite")
                        if hasattr(result, 'success'):
                            print(f"    Validation result: {result.success}")
                    else:
                        print(f"  ✗ FAILED: No result returned")
                    
                except Exception as e:
                    print(f"  ✗ FAILED during execution: {line}")
                    print(f"    Error type: {type(e).__name__}")
                    print(f"    Error message: {str(e)[:200]}")
                    
                    # For metric errors, just skip - the expectation wasn't added
                    print(f"    Skipping this expectation - it cannot be validated with current engine")
                    continue
            
            print(f"\n{'='*60}")
            print(f"EXECUTION SUMMARY:")
            print(f"  Lines processed: {len(expectation_lines)}")
            print(f"  Successful: {len(results)}")
            print(f"  Failed: {len(expectation_lines) - len(results)}")
            print(f"{'='*60}\n")
            
            # Save the expectation suite with all expectations
            validator.save_expectation_suite(discard_failed_expectations=False)
            
            # Verify expectations were saved
            saved_suite = self.context.get_expectation_suite(self.expectation_suite_name)
            print(f"Suite '{self.expectation_suite_name}' now has {len(saved_suite.expectations)} expectations")
            
            # Run checkpoint to validate and generate docs
            self.run_ge_checkpoint(batch_request)
            
            # Return the last result or raise informative error
            if results:
                return results[-1]
            else:
                # Provide helpful error message about why expectations failed
                error_msg = (
                    "No expectations were successfully executed. "
                    "This may be due to using complex expectations that require metrics not available. "
                    "\n\nTry simpler expectations like:\n"
                    "- 'column_name should not be null'\n"
                    "- 'column_name values should be between X and Y'\n"
                    "\nOr use Data Assistants in the 'Data Assistants' tab for automatic profiling."
                )
                raise Exception(error_msg)
            
        except Exception as e:
            print(f"Error running expectation on PostgreSQL data: {e}")
            raise Exception(f"Unable to run expectation: {e}")
    
    def add_or_update_ge_checkpoint(self):
        """
        Create new GE checkpoint or update an existing one
        """
        checkpoint_config = {
                    "name": self.checkpoint_name,
                    "class_name": "SimpleCheckpoint",
                    "run_name_template": "%Y%m%d-%H%M%S",
                }
        self.context.test_yaml_config(yaml.dump(checkpoint_config))
        self.context.add_or_update_checkpoint(**checkpoint_config)

    def run_ge_checkpoint(self, batch_request):
        """
        Run GE checkpoint to validate expectations and generate Data Docs with results
        """
        try:
            # Create/update checkpoint configuration
            self.add_or_update_ge_checkpoint()
            
            # Run checkpoint with validation - this will actually execute expectations
            print(f"Running checkpoint '{self.checkpoint_name}' to validate expectations...")
            checkpoint_result = self.context.run_checkpoint(
                checkpoint_name=self.checkpoint_name,
                validations=[
                    {
                        "batch_request": batch_request,
                        "expectation_suite_name": self.expectation_suite_name,
                    }
                ],
            )
            
            print(f"✓ Checkpoint executed: {checkpoint_result.success}")
            print(f"✓ Validation results saved to Data Docs")
            
            # Build data docs to show results
            self.context.build_data_docs()
            
            return checkpoint_result
            
        except Exception as e:
            print(f"Warning: Checkpoint execution failed: {e}")
            # If checkpoint fails, still build docs with just expectations (no validation results)
            self.context.build_data_docs()
            
            # Return a mock checkpoint result
            return type('obj', (object,), {
                'success': False,
                'run_results': {}
            })()
    
    def get_columns(self):
        """
        Get column names from the PostgreSQL table
        """
        try:
            df = read_pg_tables(self.table_name)
            return list(df.columns)
        except Exception as e:
            print(f"Error getting columns: {e}")
            return []
    
    def run_data_assistant(self, assistant_type='onboarding'):
        """
        Run Great Expectations Data Assistant for automatic profiling
        """
        try:
            # Set up datasource (SQL-based, no DataFrame loading)
            self.add_or_update_datasource()
            
            # Create batch request (queries SQL directly)
            batch_request = self.get_batch_request()
            
            # Create suite name
            assistant_suite_name = f"{self.table_name}_{assistant_type}_suite"
            
            # Delete existing suite if it exists
            try:
                self.context.delete_expectation_suite(assistant_suite_name)
                self.context.delete_expectation_suite(f"{assistant_suite_name}_final")
                print(f"Deleting existing suite: {assistant_suite_name}")
            except:
                pass
            
            # Create validator with new suite
            validator = self.context.get_validator(
                batch_request=batch_request,
                create_expectation_suite_with_name=assistant_suite_name
            )
            
            # Run appropriate data assistant
            print(f"Running {assistant_type} Data Assistant...")
            if assistant_type == 'onboarding':
                result = self.context.assistants.onboarding.run(validator=validator)
            elif assistant_type == 'missingness':
                result = self.context.assistants.missingness.run(validator=validator)
            else:
                raise ValueError(f"Unknown assistant type: {assistant_type}")
            
            # Get and save the expectation suite
            generated_suite = result.get_expectation_suite(expectation_suite_name=f"{assistant_suite_name}_final")
            
            # Enhance Data Assistant expectations with code display metadata
            from helpers.code_display_enhancer import enhance_expectation_with_code
            for expectation in generated_suite.expectations:
                # Convert expectation to Python code format
                exp_type = expectation.expectation_type
                kwargs_str = ', '.join([f'{k}={repr(v)}' for k, v in expectation.kwargs.items()])
                expectation_line = f"validator.{exp_type}({kwargs_str})"
                
                # Generate metadata (use SQL for PostgreSQL)
                _, meta_dict = enhance_expectation_with_code(
                    expectation_line, 
                    execution_engine="PostgreSQL (SQL) - Generated by Data Assistant",
                    return_meta=True
                )
                
                # Add notes to existing meta (preserve profiler_details)
                if meta_dict:
                    if not hasattr(expectation, 'meta') or expectation.meta is None:
                        expectation.meta = {}
                    expectation.meta['notes'] = meta_dict['notes']
            
            self.context.save_expectation_suite(generated_suite)
            
            print(f"Data Assistant generated {len(generated_suite.expectations)} expectations (enhanced with code display)")
            
            # Create and run checkpoint for the data assistant suite
            checkpoint_name = f"{assistant_suite_name}_checkpoint"
            checkpoint_config = {
                "name": checkpoint_name,
                "class_name": "SimpleCheckpoint",
                "run_name_template": "%Y%m%d-%H%M%S",
            }
            
            try:
                self.context.add_or_update_checkpoint(**checkpoint_config)
                
                # Run the checkpoint to validate with the new expectations
                # IMPORTANT: Use the _final suffix that Data Assistant added
                checkpoint_result = self.context.run_checkpoint(
                    checkpoint_name=checkpoint_name,
                    validations=[
                        {
                            "batch_request": batch_request,
                            "expectation_suite_name": f"{assistant_suite_name}_final",
                        }
                    ],
                )
                
                print(f"✓ Checkpoint '{checkpoint_name}' executed successfully")
                print(f"✓ Validation results saved to Data Docs")
                
            except Exception as e:
                print(f"Warning: Could not run checkpoint: {e}")
                # If checkpoint fails, still build docs
            
            # Build data docs to show results
            self.context.build_data_docs()
            
            return result
            
        except Exception as e:
            print(f"Error running data assistant: {e}")
            raise Exception(f"Unable to run data assistant: {e}")


