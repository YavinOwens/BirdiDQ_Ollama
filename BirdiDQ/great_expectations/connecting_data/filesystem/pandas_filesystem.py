import great_expectations as ge
import datetime
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint
from ruamel import yaml
import ruamel
import pandas as pd
import os

class PandasFilesystemDatasource():
    """
    Run Data Quality checks on Local Filesystem data
    """
    def __init__(self, datasource_name, dataframe, filename=None):
        """ 
        Init class attributes
        
        Args:
            datasource_name (str): The name identifier for the datasource (e.g., "Customers")
            dataframe (pd.DataFrame): The pandas DataFrame containing the data
            filename (str, optional): The actual CSV filename (e.g., "customers.csv")
        """
        self.datasource_name = datasource_name
        self.filename = filename or f"{datasource_name}.csv"
        self.expectation_suite_name = f"{datasource_name}_expectation_suite"
        self.checkpoint_name = f"{datasource_name}_checkpoint"
        self.dataframe = dataframe
        self.partition_date = datetime.datetime.now()
        self.context = ge.get_context()
    
    @property
    def table_name(self):
        """
        Return the datasource name for compatibility with app.py code that expects table_name
        Note: For filesystem data, this is really a file identifier, not a database table
        """
        return self.datasource_name
    
    @property
    def file_name(self):
        """Return the actual CSV filename"""
        return self.filename

    def add_or_update_datasource(self):
        """
        Create data source using Fluent API (consistent with Oracle/PostgreSQL)
        """
        try:
            # Use unique datasource name for this file
            datasource_name = f"pandas_filesystem_{self.datasource_name}"
            
            # Check if pandas datasource already exists
            try:
                self.data_source = self.context.get_datasource(datasource_name)
                print(f"Using existing datasource: {datasource_name}")
            except:
                # Create pandas datasource using Fluent API (same as Oracle)
                self.data_source = self.context.sources.add_pandas(datasource_name)
                print(f"Created new datasource: {datasource_name}")
            
            # Check if data asset exists
            try:
                self.data_asset = self.data_source.get_asset(self.datasource_name)
                print(f"Using existing asset: {self.datasource_name}")
            except:
                # Create dataframe asset (same as Oracle)
                self.data_asset = self.data_source.add_dataframe_asset(name=self.datasource_name)
                print(f"Created new asset: {self.datasource_name}")
                
            return self.data_source, self.data_asset
            
        except Exception as e:
            print(f"Error in add_or_update_datasource: {e}")
            raise

    def get_batch_request(self):
        """
        Create a batch request for DataFrame using Fluent API (same as Oracle)
        """
        # Build batch request with the DataFrame
        return self.data_asset.build_batch_request(dataframe=self.dataframe)
    
    def get_validator(self):
        """
        Retrieve a validator object using Fluent API (consistent with Oracle/PostgreSQL)
        """
        # Set up datasource and asset (Pandas-based with DataFrame)
        self.add_or_update_datasource()
        
        # Create batch request with DataFrame
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
        
        print(f"✅ Validator created successfully using Pandas Fluent API")
        return validator, batch_request
    
    def run_expectation(self, expectation):
        """
        Run your data quality checks here - robustly handles multiple expectation formats (same as Oracle)
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
            
            # Set up clean execution environment (same as Oracle)
            execution_env = {"validator": validator}
            
            results = []
            for idx, line in enumerate(expectation_lines, 1):
                if not line or line.startswith('#'):
                    print(f"Line {idx}: Skipping (empty or comment)")
                    continue
                
                print(f"\nLine {idx}: Attempting to execute:")
                print(f"  '{line}'")
                
                try:
                    # Execute expectation directly (same as Oracle)
                    # The line already contains "validator.expect_..." so we execute it as-is
                    exec(f"result = {line}", execution_env)
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
            
            # Run checkpoint
            self.run_ge_checkpoint(batch_request)
            
            return results[0] if results else None
            
        except Exception as e:
            print(f"Error in run_expectation: {e}")
            raise
    
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
        Run GE checkpoint
        """
        self.add_or_update_ge_checkpoint()

        self.context.run_checkpoint(
                checkpoint_name = self.checkpoint_name,
                validations=[
                            {
                             "batch_request": batch_request,
                            "expectation_suite_name": self.expectation_suite_name,
                            }
                            ],
                )

    def run_data_assistant(self, assistant_type="onboarding"):
        """
        Run Great Expectations Data Assistant for automatic profiling
        
        Params:
            assistant_type (str): Type of data assistant ('onboarding' or 'missingness')
        """
        try:
            # Set up datasource
            self.add_or_update_datasource()
            
            # Create batch request
            batch_request = self.configure_datasource()
            
            # Create suite name
            assistant_suite_name = f"{self.datasource_name}_{assistant_type}_suite"
            
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
                
                # Generate metadata (use Pandas for filesystem)
                _, meta_dict = enhance_expectation_with_code(
                    expectation_line, 
                    execution_engine="Pandas (Filesystem) - Generated by Data Assistant",
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
            
            print(f"✓ Data Assistant '{assistant_type}' completed successfully")
            print(f"✓ Data Docs updated with new expectations")
            
            return {
                "success": True,
                "suite_name": f"{assistant_suite_name}_final",
                "expectations_count": len(generated_suite.expectations),
                "checkpoint_name": checkpoint_name
            }
            
        except Exception as e:
            print(f"Error running Data Assistant: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def get_mapping(folder_path):
    """
    Map each local file to the correspondind data owner (DO)
    """
    mapping_dict = {}
    data_owners = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            name_without_extension = os.path.splitext(file_name)[0]
            name_with_uppercase = name_without_extension.capitalize()
            mapping_dict[name_with_uppercase] = file_name
            data_owners[name_with_uppercase] = "dioula01@gmail.com" #default DO for all files. To be modified
    return mapping_dict, data_owners


# Function to get mapping and data owners
def local_dataowners(local_filesystem_path):
    mapping, data_owners = get_mapping(local_filesystem_path)
    return mapping, data_owners

# Function to read local filesytem .csv file in a datafrale
def read_local_filesystem_tb(local_filesystem_path, data_source, mapping):
    data = pd.read_csv(f"{local_filesystem_path}{mapping.get(data_source, None)}")
    return data