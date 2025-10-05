import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import random
import webbrowser
import os
from models.gpt_model import naturallanguagetoexpectation
from models.ollama_model import get_expectations, load_ollama_client, test_ollama_connection
from helpers.utils import * 
from connecting_data.database.postgresql import *
from connecting_data.database.oracle import *
from connecting_data.filesystem.pandas_filesystem import *
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.no_default_selectbox import selectbox

local_filesystem_path = 'great_expectations/data/'
session_state = st.session_state

#data_owner_button_key = "data_owner_button_1"

st.set_page_config(
    page_title="BirdiDQ",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)  
st.title("❄️ BirdiDQ")
st.markdown('<h1 style="font-size: 24px; font-weight: bold; margin-bottom: 0;">Welcome to your DQ App</h1>', unsafe_allow_html=True)

with open("great_expectations/ui/side.md", "r", encoding="utf-8") as sidebar_file:
    sidebar_content = sidebar_file.read()

# Display the DDL for the selected table
st.sidebar.markdown(sidebar_content, unsafe_allow_html=True)

def display_data_preview(data, key_suffix=""):
    """
    Display data for quick data exploration
    Params:
        data (DataFrame) : Selected table on which to run DQ checks
        key_suffix (str) : Suffix to make keys unique
    """
    try:
        # Add a unique key to avoid conflicts
        unique_key = f"data_preview_{key_suffix}_{hash(str(data.shape))}"
        
        # Show basic data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(data))
        with col2:
            st.metric("Total Columns", len(data.columns));
        with col3:
            st.metric("Memory Usage", f"{data.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Show the data
        st.dataframe(data, width="stretch", use_container_width=True)
        
    except Exception as e:
        st.error(f"Unable to preview data: {str(e)}")
        # Fallback to basic dataframe display
        st.dataframe(data.head(10), width="stretch", use_container_width=True)


def perform_data_quality_checks(DQ_APP, key):
    """
    Function to perform data quality checks
    Params:
        DQ_APP (object) : Instanciated class for data quality checks
                          (Data sources : PostgreSQL, Filesystem, etc.)
    """
    st.subheader("Perform Data Quality Checks")
    
    checks_input = st.text_area("Describe the checks you want to perform", key=key.format(name='check_input'),
                                placeholder="For instance:  'Check that none of the values in the address column match the pattern for an address starting with a digit'. \n Provide the accurate column name as in the example.")

    if checks_input:
        submit_button = st.button("Submit", key=key.format(name='submit'))
        if submit_button:
            try:
                with st.spinner('🤖 Connecting to Ollama...'):
                    # Test Ollama connection first
                    connection_test = test_ollama_connection()
                    if connection_test['status'] == 'error':
                        st.error(f"Ollama connection failed: {connection_test['error']}")
                        st.info("Please check your .env file and ensure OLLAMA_API_KEY is set correctly.")
                        return
                    
                    st.success(f"✓ Connected to Ollama (Model: {connection_test['model']})")
                    
                    # Load Ollama client
                    client = load_ollama_client()
                    
                with st.spinner('🧠 Generating expectations from your description...'):
                    # Get available columns from the datasource
                    available_columns = None
                    try:
                        # Try to get columns from the datasource
                        if hasattr(DQ_APP, 'get_columns'):
                            available_columns = DQ_APP.get_columns()
                        elif hasattr(DQ_APP, 'df') and DQ_APP.df is not None:
                            available_columns = list(DQ_APP.df.columns)
                    except:
                        pass
                    
                    # Generate expectations using Ollama with column information
                    nltoge = get_expectations(checks_input, client, available_columns=available_columns)
                    
                    if not nltoge or len(nltoge.strip()) == 0:
                        st.error("❌ Ollama returned an empty response")
                        st.info("Try rephrasing your query or check your Ollama configuration")
                        return
                    
                    st.write("**Generated expectation code:**")
                    st.code(nltoge, language='python')
                    
                with st.spinner('⚡ Running expectations on your data...'):
                    # Run the expectation
                    expectation_result = DQ_APP.run_expectation(nltoge)
                    
                    st.success('✅ Your test has successfully been run!')
                    
                    # Show summary
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Test Status", "Passed ✓" if expectation_result.success else "Failed ✗")
                    with col2:
                        # Get expectation count from context
                        try:
                            suite = DQ_APP.context.get_expectation_suite(DQ_APP.expectation_suite_name)
                            st.metric("Total Expectations", len(suite.expectations))
                        except:
                            st.metric("Total Expectations", "N/A")
                    
                    with st.expander("📊 Show Detailed Results"):
                        st.subheader("Data Quality Result")
                        display_test_result(expectation_result.to_json_dict())
                    
                    st.info("💡 Click 'Open Data Docs' below to see all validation results in a beautiful report!")
                    
            except Exception as e:
                st.error(f"❌ Unable to successfully run the query: {str(e)}")
                st.info("This may occur if you have not configured Ollama correctly or misspelled the column name.")
                
                # Show more detailed error info in expander
                with st.expander("🔍 Show Error Details"):
                    st.code(str(e))
                    st.write("**Troubleshooting tips:**")
                    st.write("1. Verify column names match your data exactly")
                    st.write("2. Check that your Ollama API key is valid")
                    st.write("3. Ensure the table has data to validate")

def open_data_docs(DQ_APP, key):
    """
    Open expectation data docs (great expection html output)
    Params:
        DQ_APP (object) : Instanciated class for data quality checks
                          (Data sources : PostgreSQL, Filesystem, etc.)
    """

    open_docs_button = st.button("Open Data Docs", key=key.format(name='data_docs'))
    if open_docs_button:
        try:
            # Try to get the dynamic URL first (if validations have been run)
            data_docs_url = DQ_APP.context.get_docs_sites_urls()[0]['site_url']
            st.write(data_docs_url)
            webbrowser.open_new_tab(data_docs_url)
        except:
            # Fallback to the correct GX path relative to the context
            docs_path = "gx/uncommitted/data_docs/local_site/index.html"
            if os.path.exists(docs_path):
                file_url = f"file://{os.path.abspath(docs_path)}"
                st.write(f"Opening: {docs_path}")
                webbrowser.open_new_tab(file_url)
            else:
                st.warning("⚠️ No data docs found. Please run a validation first to generate data documentation.")
                st.info("💡 Tip: Upload a CSV file or connect to a database and run validations to generate data docs.")
                st.info(f"🔍 Looking for data docs at: {os.path.abspath(docs_path)}")



def contact_data_owner(session_state, data_owners, data_source, key):
    """
    Function to contact data owner
    Params:
        session_state : Current session state
        data_owners (dict) : Contains data sources (tables) as dict keys and the data owner email for each data source
        data_source (str) : Selected data source by user on which they want to run data quality checks
    """
    try:
        if session_state['page'] == 'home':
            data_owner_button = st.button("Contact Data Owner", key=key.format(name='do'))
            if data_owner_button:
                session_state['page'] = 'contact_form'

        if session_state['page'] == 'contact_form':
            st.header("Contact Form")
            sender_email = "birdidq@gmail.com"
            recipient_email = st.text_input("Recipient Email", value=data_owners[data_source])
            subject = st.text_input("Subject", key=key.format(name='subject'))
            message = st.text_area("Message", key=key.format(name='message'))
            attachement = "uncommitted/data_docs/local_site/index.html"
                
            if st.button("Send Email", key=key.format(name='email')):
                send_email_with_attachment(sender_email, recipient_email, subject, message, attachement)
                session_state['page'] = 'email_sent'

        if session_state['page'] == 'email_sent':
            session_state['page'] = 'home'
    except:
        st.warning('Unable to send email. Verify the email setup.', icon="⚠️")

def run_data_assistant(DQ_APP, key):
    """
    Run Great Expectations Data Assistant for automatic profiling
    Params:
        DQ_APP (object): Instantiated class for data quality checks
    """
    st.subheader("🤖 Automated Data Profiling")
    st.write("Use Data Assistants to automatically generate expectations based on your data.")
    
    assistant_type = st.selectbox(
        "Select Data Assistant Type:",
        ["Onboarding Assistant", "Missingness Assistant"],
        key=key.format(name='assistant_type')
    )
    
    run_assistant_button = st.button("Run Data Assistant", key=key.format(name='run_assistant'))
    
    if run_assistant_button:
        with st.spinner(f'🤖 Running {assistant_type}...'):
            try:
                # Determine assistant type
                if "Onboarding" in assistant_type:
                    assistant_key = "onboarding"
                else:
                    assistant_key = "missingness"
                
                # Run the data assistant
                result = DQ_APP.run_data_assistant(assistant_type=assistant_key)
                
                st.success(f'✅ {assistant_type} completed successfully!')
                
                # Display results summary
                # Handle both dict result (filesystem) and object result (database)
                if isinstance(result, dict):
                    # Filesystem connector returns a dict
                    suite_name = result.get("suite_name", f"{DQ_APP.table_name}_{assistant_key}_suite_final")
                    expectations_count = result.get("expectations_count", 0)
                    checkpoint_name = result.get("checkpoint_name", "")
                    
                    # Get the suite from context
                    suite = DQ_APP.context.get_expectation_suite(suite_name)
                else:
                    # Database connector returns an object with get_expectation_suite method
                    suite_name = f"{DQ_APP.table_name}_{assistant_key}_suite_final"
                    suite = result.get_expectation_suite(expectation_suite_name=suite_name)
                    expectations_count = len(suite.expectations)
                    checkpoint_name = f"{suite_name}_checkpoint"
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Suite Name", suite.expectation_suite_name.replace('_', ' ').title())
                with col2:
                    st.metric("Expectations Generated", expectations_count)
                with col3:
                    st.metric("Status", "✓ Validated")
                
                # Display detailed expectations
                with st.expander("📋 Show All Generated Expectations", expanded=True):
                    st.subheader(f"Expectations from {assistant_type}")
                    
                    # Group expectations by type
                    expectation_types = {}
                    for expectation in suite.expectations:
                        exp_type = expectation.expectation_type.replace('expect_', '').replace('_', ' ').title()
                        if exp_type not in expectation_types:
                            expectation_types[exp_type] = []
                        expectation_types[exp_type].append(expectation)
                    
                    # Display grouped expectations
                    for exp_type, expectations in expectation_types.items():
                        st.write(f"**{exp_type}** ({len(expectations)} expectations)")
                        for expectation in expectations:
                            # Extract column name if present
                            column = expectation.kwargs.get('column', 'N/A')
                            
                            # Extract mostly parameter if present (shows actual null/non-null percentage)
                            mostly = expectation.kwargs.get('mostly', None)
                            if mostly is not None:
                                mostly_pct = mostly * 100
                                st.write(f"  • Column: `{column}` - {expectation.expectation_type} (≥{mostly_pct:.0f}% threshold)")
                            else:
                                st.write(f"  • Column: `{column}` - {expectation.expectation_type}")
                
                st.info("💡 Data Docs have been updated with validation results. Click 'Open Data Docs' in the first tab to view the interactive report!")
                
            except Exception as e:
                st.error(f"❌ Unable to run Data Assistant: {str(e)}")
                st.info("This may occur if the data assistant encounters an issue. Please try again or use manual expectations.")
                
                with st.expander("🔍 Show Error Details"):
                    st.code(str(e))
                    st.write("**Common issues:**")
                    st.write("1. Insufficient data in the table")
                    st.write("2. Data type incompatibilities")
                    st.write("3. Missing or null columns")

def next_steps(DQ_APP, data_owners, data_source, key):
    """
    Actions to take after running data quality checks
    View expectation data docs
    Contact Data Owner by email with data docs as attachment
    """
    st.subheader("What's next ?")
    t1,t2,t3 = st.tabs(['Expectation Data Docs','Data Assistants','Get in touch with Data Owner']) 
    with t1:
        open_data_docs(DQ_APP, key)
    with t2:
        run_data_assistant(DQ_APP, key)
    with t3:           
        contact_data_owner(session_state, data_owners, data_source, key)


def main():
    # Set the app title
    DQ_APP = None  
    data_owners = None
    data_source = None

    if 'page' not in session_state:
        session_state['page'] = 'home'

    # Select the data connection
    t1,t2,t3 = st.tabs(['Local File System','PostgreSQL','Oracle']) 

    with t1:
        st.subheader("📁 Upload CSV File")
        
        # File upload functionality
        uploaded_file = st.file_uploader(
            "Choose a CSV file", 
            type="csv",
            help="Upload a CSV file to run data quality checks on it"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File uploaded successfully! ({uploaded_file.name})")
                
                # Show basic info about the file
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                
                # Store the uploaded data in session state
                session_state['uploaded_df'] = df
                session_state['uploaded_file_name'] = uploaded_file.name
                session_state['data_source'] = uploaded_file.name.split('.')[0]  # Use filename without extension
                
                # Show data preview
                st.subheader("📊 Data Preview")
                display_data_preview(df, "upload")
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        # Separator
        st.markdown("---")
        st.subheader("📂 Or select from existing files")
        
        # Existing file functionality
        try:
            mapping, data_owners = local_dataowners(local_filesystem_path)
            tables = list(mapping.keys())
            
            if tables:
                data_source = selectbox("Select table name", tables)
            else:
                st.info("No CSV files found in the data directory. Upload a file above or add files to the data folder.")
                data_source = None
        except FileNotFoundError:
            st.warning("Data directory not found. Please upload a file above or ensure the data directory exists.")
            tables = []
            data_source = None

        if data_source or 'uploaded_df' in session_state:
            key = "filesystem_{name}"
            
            # Use uploaded data if available, otherwise load from filesystem
            if 'uploaded_df' in session_state:
                data = session_state['uploaded_df']
                st.subheader("📊 Preview of uploaded data:")
                st.info(f"✅ Using uploaded file: {session_state['uploaded_file_name']}")
                actual_filename = session_state['uploaded_file_name']
                current_data_source = session_state['data_source']
            else:
                st.subheader("📊 Preview of local data:")
                data = read_local_filesystem_tb(local_filesystem_path, data_source, mapping)
                # Get the actual CSV filename from mapping
                actual_filename = mapping.get(data_source, f"{data_source}.csv")
                current_data_source = data_source
            
            display_data_preview(data, current_data_source)
            DQ_APP = PandasFilesystemDatasource(current_data_source, data, filename=actual_filename)
            perform_data_quality_checks(DQ_APP, key)
            next_steps(DQ_APP, data_owners, current_data_source, key)

    with t2:
        try:
            data_owners = postgresql_data_owners()
            tables = get_pg_tables()
            data_source = selectbox("Select PostgreSQL table", tables)
            if data_source:
                key = "postgresql_{name}"
                # Display a preview of the data
                st.subheader("Preview of the data:")
                data = read_pg_tables(data_source)
                display_data_preview(data, f"pg_{data_source}")
        
                DQ_APP = PostgreSQLDatasource('gx_example_db', data_source)
                perform_data_quality_checks(DQ_APP, key)
                next_steps(DQ_APP, data_owners, data_source, key)
        except Exception as e:
            st.error(f'Unable to connect to PostgreSQL: {str(e)}', icon="❌")
            st.info('Please verify that you have added your connection string in .env file and that the database is accessible.', icon="ℹ️")

    with t3:
        try:
            data_owners = oracle_data_owners()
            tables = get_oracle_tables()
            data_source = selectbox("Select Oracle table", tables)
            if data_source:
                key = "oracle_{name}"
                # Display a preview of the data
                st.subheader("Preview of the data:")
                data = read_oracle_tables(data_source)
                display_data_preview(data, f"ora_{data_source}")
        
                DQ_APP = OracleDatasource('oracle_db', data_source)
                perform_data_quality_checks(DQ_APP, key)
                next_steps(DQ_APP, data_owners, data_source, key)
        except Exception as e:
            st.warning(f'Unable to connect to Oracle: {str(e)}. Please verify that you have added your connection string in .env file and that Oracle is running.', icon="⚠️")
            st.info("Make sure your Oracle Docker container is running and accessible.")

 
local_css("great_expectations/ui/front.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
remote_css('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap')
# Run the app
if __name__ == "__main__":
    main()
