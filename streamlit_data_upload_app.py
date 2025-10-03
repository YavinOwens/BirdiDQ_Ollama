#!/usr/bin/env python3
"""
Streamlit Data Upload Application for BirdiDQ
Allows users to upload data files and run Great Expectations validation workflows
using the Pandas execution engine.
"""

import streamlit as st
import pandas as pd
import great_expectations as gx
from pathlib import Path
import tempfile
import json
import io
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="BirdiDQ Data Upload & Validation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_gx_context():
    """Initialize Great Expectations context"""
    try:
        context = gx.get_context()
        return context, None
    except Exception as e:
        return None, str(e)

def create_temp_file(uploaded_file):
    """Create temporary file from uploaded file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def detect_file_format(filename):
    """Detect file format based on extension"""
    ext = Path(filename).suffix.lower()
    if ext == '.csv':
        return 'csv'
    elif ext in ['.xlsx', '.xls']:
        return 'excel'
    elif ext == '.json':
        return 'jon'
    elif ext == '.parquet':
        return 'parquet'
    else:
        return 'csv'  # Default to CSV

def load_data_from_file(uploaded_file):
    """Load data from uploaded file"""
    try:
        file_format = detect_file_format(uploaded_file.name)
        
        if file_format == 'csv':
            df = pd.read_csv(io.StringIO(uploaded_file.read().decode('utf-8')))
        elif file_format == 'excel':
            df = pd.read_excel(uploaded_file)
        elif file_format == 'json':
            df = pd.read_json(uploaded_file)
        elif file_format == 'parquet':
            df = pd.read_parquet(uploaded_file)
        else:
            df = pd.read_csv(io.StringIO(uploaded_file.read().decode('utf-8')))
        
        return df, None
    except Exception as e:
        return None, str(e)

def create_pandas_dataframe_asset(context, df, asset_name):
    """Create pandas DataFrame asset in Great Expectations"""
    try:
        # Create temporary datasource
        datasource_name = f"uploaded_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            datasource = context.get_datasource(datasource_name)
        except:
            datasource = context.sources.add_pandas("uploaded_data")
        
        # Create DataFrame asset
        asset = datasource.add_dataframe_asset(name=asset_name, dataframe=df)
        asset_name_final = f"uploaded_data_{asset_name}"
        
        return asset, asset_name_final, None
    except Exception as e:
        return None, None, str(e)

def run_data_assistants(context, asset, asset_name):
    """Run Great Expectations Data Assistants"""
    try:
        # Build batch request
        batch_request = asset.build_batch_request()
        
        # Create validator
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=f"{asset_name}_suite"
        )
        
        # Run Missingness Data Assistant
        missingness_result = context.assistants.missingness.run(validator=validator)
        missingness_suite = missingness_result.get_expectation_suite(
            expectation_suite_name=f"{asset_name}_missingness_final"
        )
        context.save_expectation_suite(missingness_suite)
        
        # Run Onboarding Data Assistant
        onboarding_result = context.assistants.onboarding.run(validator=validator)
        onboarding_suite = onboarding_result.get_expectation_suite(
            expectation_suite_name=f"{asset_name}_onboarding_final"
        )
        context.save_expectation_suite(onboarding_suite)
        
        return missingness_suite, onboarding_suite, None
    except Exception as e:
        return None, None, str(e)

def create_and_run_checkpoint(context, asset_name, missingness_suite, onboarding_suite):
    """Create and run validation checkpoints"""
    try:
        results = {}
        
        # Create checkpoint for Missingness
        missingness_checkpoint = context.add_or_update_checkpoint(
            name=f"{asset_name}_missingness_cp",
            config_version=1.0,
            class_name='Checkpoint',
            run_name_template=f'%Y%m%d-%H%M%S-{asset_name}-missingness',
            expectation_suite_name=f"{asset_name}_missingness_final",
            batch_request={
                'datasource_name': 'uploaded_data',
                'data_asset_name': asset_name
            },
            action_list=[
                {
                    'name': 'store_validation_result',
                    'action': {'class_name': 'StoreValidationResultAction'}
                }
            ]
        )
        
        # Create checkpoint for Onboarding
        onboarding_checkpoint = context.add_or_update_checkpoint(
            name=f"{asset_name}_onboarding_cp",
            config_version=1.0,
            class_name='Checkpoint',
            run_name_template=f'%Y%m%d-%H%M%S-{asset_name}-onboarding',
            expectation_suite_name=f"{asset_name}_onboarding_final",
            batch_request={
                'datasource_name': 'uploaded_data',
                'data_asset_name': asset_name
            },
            action_list=[
                {
                    'name': 'store_validation_result',
                    'action': {'class_name': 'StoreValidationResultAction'}
                }
            ]
        )
        
        # Run checkpoints
        missingness_result = context.run_checkpoint(checkpoint_name=f"{asset_name}_missingness_cp")
        onboarding_result = context.run_checkpoint(checkpoint_name=f"{asset_name}_onboarding_cp")
        
        results['missingness'] = missingness_result
        results['onboarding'] = onboarding_result
        
        return results, None
    except Exception as e:
        return None, str(e)

def display_data_overview(df):
    """Display data overview"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        null_count = df.isnull().sum().sum()
        st.metric("Missing Values", f"{null_count:,}")
    
    # Display basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(df.describe(), width='content')

def display_validation_results(results):
    """Display validation results"""
    st.subheader("📋 Validation Results")
    
    for result_type, result in results.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{result_type.title()} Data Assistant Results**")
        
        with col2:
            if result.success:
                st.success("✅ PASSED")
            else:
                st.error("❌ FAILED")
        
        # Display statistics
        stats = result.statistics
        if 'evaluated_expectations' in stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Expectations", stats['evaluated_expectations'])
            
            with col2:
                st.metric("Successful", stats.get('successful_expectations', 0))
            
            with col3:
                st.metric("Unsuccessful", stats.get('unsuccessful_expectations', 0))

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 BirdiDQ Data Upload & Validation</h1>', unsafe_allow_html=True)
    st.markdown("Upload your data files and run automated data quality validation using Great Expectations with Pandas execution engine.")
    
    # Sidebar
    st.sidebar.header("🔧 Configuration")
    
    # Initialize Great Expectations
    if 'gx_context' not in st.session_state:
        gx_context, error = initialize_gx_context()
        if gx_context:
            st.session_state.gx_context = gx_context
            st.sidebar.success("✅ Great Expectations initialized")
        else:
            st.sidebar.error(f"❌ GX Error: {error}")
            st.stop()
    
    # File upload
    st.markdown('<h2 class="section-header">📁 Upload Data File</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a data file",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
        help="Supported formats: CSV, Excel, JSON, Parquet"
    )
    
    if uploaded_file is not None:
        # Load data
        with st.spinner("Loading data..."):
            df, error = load_data_from_file(uploaded_file)
        
        if df is not None:
            st.success(f"✅ Successfully loaded {uploaded_file.name}")
            
            # Data overview
            st.markdown('<h2 class="section-header">📈 Data Overview</h2>', unsafe_allow_html=True)
            display_data_overview(df)
            
            # Data preview
            st.markdown('<h2 class="section-header">👀 Data Preview</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**First 5 rows:**")
                st.dataframe(df.head(), use_container_width=True)
            
            with col2:
                st.write("**Last 5 rows:**")
                st.dataframe(df.tail(), use_container_width=True)
            
            # Data info
            st.markdown('<h2 class="section-header">ℹ️ Data Information</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Data Types:**")
                dtype_df = pd.DataFrame({
                    'Column': df.columns,
                    'Data Type': [str(dtype) for dtype in df.dtypes],
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum()
                })
                st.dataframe(dtype_df, use_container_width=True)
            
            with col2:
                st.write("**Missing Values Heatmap:**")
                if not df.isnull().sum().sum() == 0:
                    fig = px.imshow(df.isnull().T, aspect='auto', color_continuous_scale='Reds')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No missing values found!")
            
            # Validation button
            st.markdown('<h2 class=\"section-header\">🔍 Data Validation</h2>', unsafe_allow_html=True)
            
            if st.button("🚀 Run Data Quality Validation", type="primary", use_container_width=True):
                with st.spinner("Running Great Expectations validation..."):
                    try:
                        # Create asset
                        asset_name = f"uploaded_{uploaded_file.name.split('.')[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        asset, full_asset_name, error = create_pandas_dataframe_asset(
                            st.session_state.gx_context, df, asset_name
                        )
                        
                        if asset is None:
                            st.error(f"❌ Error creating asset: {error}")
                            st.stop()
                        
                        # Run Data Assistants
                        missingness_suite, onboarding_suite, error = run_data_assistants(
                            st.session_state.gx_context, asset, asset_name
                        )
                        
                        if error:
                            st.error(f"❌ Error running data assistants: {error}")
                            st.stop()
                        
                        # Run checkpoints
                        results, error = create_and_run_checkpoint(
                            st.session_state.gx_context, asset_name, missingness_suite, onboarding_suite
                        )
                        
                        if error:
                            st.error(f"❌ Error running validation: {error}")
                            st.stop()
                        
                        # Display results
                        display_validation_results(results)
                        
                        # Summary
                        st.markdown('<h2 class="section-header">📊 Validation Summary</h2>', unsafe_allow_html=True)
                        
                        total_expectations = len(missingness_suite.expectations) + len(onboarding_suite.expectations)
                        successful_validations = sum(1 for result in results.values() if result.success)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Missingness Expectations", len(missingness_suite.expectations))
                        with col2:
                            st.metric("Onboarding Expectations", len(onboarding_suite.expectations))
                        with col3:
                            st.metric("Total Expectations", total_expectations)
                        
                        with col3:
                            st.metric("Successful Validations", f"{successful_validations}/2")
                        
                        # Download results
                        st.markdown('<h2 class="section-header">💾 Download Results</h2>', unsafe_allow_html=True)
                        
                        # Create summary JSON
                        summary = {
                            "validation_timestamp": datetime.now().isoformat(),
                            "file_name": uploaded_file.name,
                            "data_shape": f"{df.shape[0]} rows, {df.shape[1]} columns",
                            "expectation_suites": {
                                "missingness": {
                                    "expectations_count": len(missingness_suite.expectations),
                                    "status": "PASSED" if results['missingness'].success else "FAILED"
                                },
                                "onboarding": {
                                    "expectations_count": len(onboarding_suite.expectations),
                                    "status": "PASSED" if results['onboarding'].success else "FAILED"
                                }
                            },
                            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
                            "missing_values": df.isnull().sum().to_dict()
                        }
                        
                        json_str = json.dumps(summary, indent=2)
                        st.download_button(
                            label="📥 Download Validation Summary (JSON)",
                            data=json_str,
                            file_name=f"validation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                        # Download data
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Processed Data (CSV)",
                            data=csv,
                            file_name=f"processed_{uploaded_file.name}",
                            mime="text/csv"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Unexpected error during validation: {str(e)}")
            
            else:
                st.info("👆 Click the button above to run data quality validation")
        
        else:
            st.error(f"❌ Error loading data: {error}")
    
    else:
        st.info("👆 Please upload a data file to get started")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🐦 Built with BirdiDQ & Great Expectations | Powered by Pandas Execution Engine</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
