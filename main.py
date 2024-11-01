import streamlit as st
import sqlite3
import pandas as pd
import tempfile
import os

st.title("SQLite File Viewer & Query Tester")

# Step 1: Upload SQLite or SQL file
uploaded_file = st.file_uploader(
    "Upload SQLite (.sqlite/.db) file or SQL (.sql) file", type=["sqlite", "db", "sql"])
    
if uploaded_file is not None:
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    try:
        # Check the file type
        if uploaded_file.name.endswith('.sql'):
            # If it's a SQL file, create a new SQLite database to execute the SQL commands
            db_conn = sqlite3.connect(temp_file_path.replace('.sql', '.db'))
            with open(temp_file_path, 'r') as sql_file:
                sql_script = sql_file.read()
                if sql_script.strip():  # Check if script is not empty
                    try:
                        # Execute the SQL script
                        db_conn.executescript(sql_script)
                        st.success("SQL script executed successfully.")
                    except sqlite3.Error as sql_error:
                        st.error(f"Error executing SQL script: {sql_error}")
                else:
                    st.warning(
                        "The SQL file is empty. Please provide valid SQL statements.")
            # Use the new database connection
            conn = db_conn
        else:
            # Connect to SQLite database file
            conn = sqlite3.connect(temp_file_path)

        # Step 2: Display table names
        st.header("Available Tables")
        tables = pd.read_sql(
            "SELECT name FROM sqlite_master WHERE type='table';", conn)
        st.write(tables)

        # Step 3: SQL Query Input
        st.header("SQL Query Tester")
        query = st.text_area("Write your SQL query here:")

        if st.button("Execute Query"):
            try:
                # Step 4: Execute and display the query result
                result = pd.read_sql(query, conn)
                st.write(result)
            except Exception as e:
                st.error(f"Error executing query: {e}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        # Ensure the database connection is closed
        if 'conn' in locals():
            conn.close()
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Cleanup temporary file
