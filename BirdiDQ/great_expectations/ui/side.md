# About 🔍

BirdiDQ is an intuitive and user-friendly data quality application that allows you to run data quality checks on top of python great expectation open source library using natural language queries. Type in your requests, and BirdiDQ will generate the appropriate GE method, run the quality control and return the results along with data docs you need.

## Features

- **Data Exploration**: Quickly and interactively explore your data (apply filters, comparison, etc.)
- **Natural Language Processing**: Understands your text queries and converts them into GE methods.
- **Instant Results**: Run data quality checks on selected datasource.
- **Automate Email Alert**: Alert Data Owners when you find inconsistencies in the data
- **AI-Powered Data Assistants**: Automatic data profiling and expectation generation using LLM and GX Data Assistants
- **Multi-Database Support**: Works with Oracle, PostgreSQL, and more

## Tech Stack

This app is an LLM-powered app built using:

- **[Streamlit](https://streamlit.io/)**
- **[Great Expectations](https://greatexpectations.io/)**: Open-source data validation framework
- **[Ollama](https://ollama.com/)**: Local and cloud LLM inference
  - **Model**: [gpt-oss:20b](https://ollama.com/models)** - 20 billion parameter open-source model
  - Deployed via Ollama Cloud for high-performance inference
- **[Oracle Database 19c](https://www.oracle.com/database/)**: Enterprise database support
- **[PostgreSQL](https://www.postgresql.org/)**: Open-source relational database

## Queries example

Here are some example queries you can try with BirdiDQ:

- Ensure that at least 80% of the values in the country column are not null.
- Check that none of the values in the address column match the pattern for an address starting with a digit.
