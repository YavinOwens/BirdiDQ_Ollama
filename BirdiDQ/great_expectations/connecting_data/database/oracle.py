import great_expectations as ge
from ruamel import yaml
import ruamel
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint
from dotenv import load_dotenv
import os 
import oracledb
from sqlalchemy import create_engine
import pandas as pd
import sys
from pathlib import Path

# Import code display enhancer
sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers.code_display_enhancer import enhance_expectation_with_code 

load_dotenv('/Users/yavin/python_projects/ollama_jupyter/.env')

# Get your Oracle connection string from the environment variable
ORACLE_CONNECTION_STRING = os.environ.get('ORACLE_CONNECTION_STRING')

def read_oracle_tables(table_name):
    """
    Read Oracle table in pandas dataframe
    """
    try:
        # Parse the connection string for direct oracledb connection
        conn_str = ORACLE_CONNECTION_STRING.replace('oracle+oracledb://', '')
        
        # Extract components
        if '@' in conn_str:
            auth_part, host_part = conn_str.split('@', 1)
            if ':' in auth_part:
                user, password = auth_part.split(':', 1)
            else:
                user = auth_part
                password = ''
            
            if ':' in host_part:
                host_port, service_part = host_part.split(':', 1)
                if '/' in service_part:
                    port, service_part = service_part.split('/', 1)
                    if 'service_name=' in service_part:
                        service_name = service_part.split('service_name=')[1]
                    else:
                        service_name = 'FREEPDB1'
                else:
                    port = '1521'
                    service_name = 'FREEPDB1'
            else:
                host_port = host_part
                port = '1521'
                service_name = 'FREEPDB1'
        else:
            # Fallback to default values
            user = 'system'
            password = 'oracle'
            host_port = 'localhost'
            port = '1521'
            service_name = 'FREEPDB1'
        
        # Create oracledb connection string
        dsn = f"{host_port}:{port}/{service_name}"
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        
        # Use pandas read_sql with direct connection
        df = pd.read_sql_query(f'select * from {table_name}', con=conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error reading Oracle table {table_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def get_oracle_tables():
    """
    List all tables from an Oracle database using a connection string
    """
    try:
        # Parse the SQLAlchemy connection string for oracledb
        # Format: oracle+oracledb://user:password@host:port/?service_name=SERVICE
        conn_str = ORACLE_CONNECTION_STRING.replace('oracle+oracledb://', '')
        
        # Extract components
        if '@' in conn_str:
            auth_part, host_part = conn_str.split('@', 1)
            if ':' in auth_part:
                user, password = auth_part.split(':', 1)
            else:
                user = auth_part
                password = ''
            
            if ':' in host_part:
                host_port, service_part = host_part.split(':', 1)
                if '/' in service_part:
                    port, service_part = service_part.split('/', 1)
                    if 'service_name=' in service_part:
                        service_name = service_part.split('service_name=')[1]
                    else:
                        service_name = 'FREEPDB1'
                else:
                    port = '1521'
                    service_name = 'FREEPDB1'
            else:
                host_port = host_part
                port = '1521'
                service_name = 'FREEPDB1'
        else:
            # Fallback to default values
            user = 'system'
            password = 'oracle'
            host_port = 'localhost'
            port = '1521'
            service_name = 'FREEPDB1'
        
        # Create oracledb connection string
        dsn = f"{host_port}:{port}/{service_name}"
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = conn.cursor()

        # Query to get all user tables
        query = """
        SELECT table_name 
        FROM user_tables 
        WHERE table_name NOT LIKE 'BIN$%'
        ORDER BY table_name
        """
        cursor.execute(query)

        tables = cursor.fetchall()
        tables = [t[0] for t in tables]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"Error connecting to Oracle: {e}")
        return []

def oracle_data_owners():
    """
    Map each Oracle table with its data owner
    """
    tables = get_oracle_tables()
    return {datasource: 'oracle@birdidq.com' for datasource in tables}

class OracleDatasource():
    """
    Run Data Quality checks on Oracle database
    """
    def __init__(self, database, asset_name):
        """ 
        Init class attributes
        """
        self.database = database
        self.asset_name = asset_name
        self.table_name = asset_name  # Add table_name attribute
        self.expectation_suite_name = f"{asset_name}_expectation_suite"
        self.checkpoint_name = f"{asset_name}_checkpoint"
        self.context = ge.get_context()
        self._columns_cache = None  # Cache for column names
    
    def get_columns(self):
        """Get list of column names from the table"""
        if self._columns_cache is None:
            try:
                # Read just 1 row to get column names
                df = read_oracle_tables(self.table_name)
                self._columns_cache = list(df.columns)
            except Exception as e:
                print(f"Error getting columns: {e}")
                self._columns_cache = []
        return self._columns_cache

    def add_or_update_datasource(self):
        """
        Create pandas datasource using Fluent API (like the working notebooks)
        """
        datasource_name = f"oracle_pandas_{self.table_name}"
        
        try:
            # Try to get existing datasource
            self.data_source = self.context.get_datasource(datasource_name)
            print(f"Using existing datasource: {datasource_name}")
        except:
            # Create new datasource using Fluent API
            self.data_source = self.context.sources.add_pandas(datasource_name)
            print(f"Created new datasource: {datasource_name}")
        
        # Create or get data asset
        try:
            self.data_asset = self.data_source.get_asset(self.table_name)
            print(f"Using existing asset: {self.table_name}")
        except:
            self.data_asset = self.data_source.add_dataframe_asset(name=self.table_name)
            print(f"Created new asset: {self.table_name}")
        
        return self.data_source, self.data_asset

    def add_or_update_ge_suite(self):
        """
        create expectation suite if not exist and update it if there is already a suite
        """
        self.context.add_or_update_expectation_suite(
                     expectation_suite_name=self.expectation_suite_name)

    def get_validator(self):
        """
        Retrieve a validator object for a fine grain adjustment on the expectation suite.
        """
        self.add_or_update_datasource()
        batch_request = self.configure_datasource()
        self.add_or_update_ge_suite()
        validator = self.context.get_validator(batch_request=batch_request,
                                               expectation_suite_name=self.expectation_suite_name,
                                        )
        return validator, batch_request

    def setup_pandas_datasource(self):
        """
        Set up a pandas datasource for Oracle data using the modern Fluent API
        """
        try:
            # Check if pandas datasource already exists
            try:
                pandas_source = self.context.get_datasource("pandas_oracle_datasource")
            except:
                # Create pandas datasource using Fluent API (the correct way)
                pandas_source = self.context.sources.add_pandas("pandas_oracle_datasource")
            
            # Check if data asset exists
            try:
                data_asset = pandas_source.get_asset(self.table_name)
            except:
                # Create dataframe asset
                data_asset = pandas_source.add_dataframe_asset(name=self.table_name)
            
            return pandas_source, data_asset
        except Exception as e:
            print(f"Error setting up pandas datasource: {e}")
            raise

    def get_validator(self):
        """
        Get validator using Fluent API (like the working notebooks)
        """
        # Create datasource and asset using Fluent API
        data_source, data_asset = self.add_or_update_datasource()
        
        # Read data from Oracle as DataFrame
        df = read_oracle_tables(self.table_name)
        
        # Build batch request using Fluent API
        batch_request = data_asset.build_batch_request(dataframe=df)
        
        # Get or create expectation suite
        try:
            self.context.delete_expectation_suite(self.expectation_suite_name)
        except:
            pass
        
        self.context.add_or_update_expectation_suite(
            expectation_suite_name=self.expectation_suite_name
        )
        
        # Get validator using Fluent API
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=self.expectation_suite_name
        )
        
        print(f"✅ Validator created successfully using Fluent API")
        
        return validator, batch_request
    
    def run_expectation(self, expectation):
        """
        Run your data quality checks here - robustly handles multiple expectation formats
        """
        try:
            validator, batch_request = self.get_validator()
            
            # Import necessary GX expectations
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
                    enhanced_line, meta_dict = enhance_expectation_with_code(line, execution_engine="Oracle (Pandas)", return_meta=True)
                    
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
                    # Don't try workarounds, let GX handle it naturally
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
                    "This is likely because the PandasExecutionEngine with runtime data "
                    "doesn't support complex expectations like 'expect_column_values_to_be_unique'. "
                    "\n\nTry simpler expectations like:\n"
                    "- 'column_name should not be null'\n"
                    "- 'column_name values should be between X and Y'\n"
                    "\nOr use Data Assistants in the 'Data Assistants' tab for automatic profiling."
                )
                raise Exception(error_msg)
            
        except Exception as e:
            print(f"Error running expectation on Oracle data: {e}")
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

    def run_data_assistant(self, assistant_type="onboarding"):
        """
        Run Great Expectations Data Assistant for automatic profiling
        
        Params:
            assistant_type (str): Type of data assistant ('onboarding' or 'missingness')
        
        Returns:
            Validation results from the data assistant
        """
        try:
            # Read data from Oracle
            df = read_oracle_tables(self.table_name)
            
            if df.empty:
                raise Exception(f"No data found in table {self.table_name}")
            
            # Set up pandas datasource
            self.setup_pandas_datasource()
            
            # Create a runtime batch request using pandas
            from great_expectations.core.batch import RuntimeBatchRequest
            
            batch_request = RuntimeBatchRequest(
                datasource_name="pandas_datasource",
                data_connector_name="runtime_data_connector",
                data_asset_name=self.table_name,
                runtime_parameters={"batch_data": df},
                batch_identifiers={"default_identifier_name": "default_identifier"},
            )
            
            # Create suite name for data assistant
            assistant_suite_name = f"{self.table_name}_{assistant_type}_suite"
            
            # Check if suite already exists and delete it to allow re-running
            try:
                existing_suite = self.context.get_expectation_suite(assistant_suite_name)
                print(f"Deleting existing suite: {assistant_suite_name}")
                self.context.delete_expectation_suite(assistant_suite_name)
            except:
                print(f"No existing suite to delete: {assistant_suite_name}")
            
            # Get a validator for the data assistant
            validator = self.context.get_validator(
                batch_request=batch_request,
                create_expectation_suite_with_name=assistant_suite_name
            )
            
            # Run the data assistant using the context API (modern GX 0.18+ approach)
            print(f"Running {assistant_type} Data Assistant...")
            if assistant_type.lower() == "onboarding":
                result = self.context.assistants.onboarding.run(validator=validator)
            elif assistant_type.lower() == "missingness":
                result = self.context.assistants.missingness.run(validator=validator)
            else:
                raise ValueError(f"Unknown assistant type: {assistant_type}. Use 'onboarding' or 'missingness'")
            
            # Get the expectation suite from the result using the correct API
            # IMPORTANT: Data Assistant appends "_final" to the suite name automatically
            generated_suite = result.get_expectation_suite(expectation_suite_name=f"{assistant_suite_name}_final")
            
            # Enhance Data Assistant expectations with code display metadata
            from helpers.code_display_enhancer import enhance_expectation_with_code
            for expectation in generated_suite.expectations:
                # Convert expectation to Python code format
                exp_type = expectation.expectation_type
                kwargs_str = ', '.join([f'{k}={repr(v)}' for k, v in expectation.kwargs.items()])
                expectation_line = f"validator.{exp_type}({kwargs_str})"
                
                # Generate metadata (use Pandas for Oracle)
                _, meta_dict = enhance_expectation_with_code(
                    expectation_line, 
                    execution_engine="Oracle (Pandas) - Generated by Data Assistant",
                    return_meta=True
                )
                
                # Add notes to existing meta (preserve profiler_details)
                if meta_dict:
                    if not hasattr(expectation, 'meta') or expectation.meta is None:
                        expectation.meta = {}
                    expectation.meta['notes'] = meta_dict['notes']
            
            # Save the expectation suite generated by the assistant
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
