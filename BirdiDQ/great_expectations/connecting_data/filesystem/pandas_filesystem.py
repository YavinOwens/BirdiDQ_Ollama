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
    def __init__(self, datasource_name, dataframe):
        """ 
        Init class attributes
        """
        self.datasource_name = datasource_name
        self.expectation_suite_name = f"{datasource_name}_expectation_suite"
        self.checkpoint_name = f"{datasource_name}_checkpoint"
        self.dataframe = dataframe
        self.partition_date = datetime.datetime.now()
        self.context = ge.get_context()

    def add_or_update_datasource(self):
        """
        Create data source if it does not exist or updating existing one
        """
        datasource_yaml = rf"""
        name: {self.datasource_name}
        class_name: Datasource
        execution_engine:
            class_name: PandasExecutionEngine
        data_connectors:
            runtime_connector:
                class_name: RuntimeDataConnector
                batch_identifiers:
                    - run_id
        """
        self.context.test_yaml_config(datasource_yaml)
        self.context.add_datasource(**yaml.load(datasource_yaml, Loader=ruamel.yaml.Loader))

    def configure_datasource(self):
        """
        Add a RuntimeDataConnector hat uses an in-memory DataFrame to a Datasource configuration
        """
        batch_request = RuntimeBatchRequest(
            datasource_name= self.datasource_name,
            data_connector_name= "runtime_connector",
            data_asset_name=f"{self.datasource_name}_{self.partition_date.strftime('%Y%m%d')}",
            batch_identifiers={
                "run_id": f'''
                {self.datasource_name}_partition_date={self.partition_date.strftime('%Y%m%d')}
                ''',
            },
            runtime_parameters={"batch_data": self.dataframe}
        )
        return batch_request
    
    def add_or_update_ge_suite(self):
        """
        create expectation suite if not exist and update it if there is already a suite
        """
        self.context.add_or_update_expectation_suite(
                     expectation_suite_name = self.expectation_suite_name)

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
    
    def run_expectation(self, expectation):
        """
        Run your dataquality checks here
        """
        validator, batch_request = self.get_validator()
        def my_function(expectation, validator):
            local_vars = {"validator": validator}
            exec(f"expectation_result = validator.{expectation}", globals(), local_vars)
            return local_vars.get("expectation_result")
        
        expectation_result = my_function(expectation, validator)
        exec(f"expectation_result = validator.{expectation}")

        validator.save_expectation_suite(discard_failed_expectations=False)
        self.run_ge_checkpoint(batch_request)
        #self.context.build_data_docs()
        return expectation_result
    
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