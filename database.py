import sqlite3

import pandas as pd
from frontend import View


class FileFormat(View):
    def __init__(self):
        pass

    def extensionSql(self, file_path):
        # Create an in-memory SQLite database
        conn = sqlite3.connect(':memory:')
        sql_script = file_path.read().decode("utf-8")

        if sql_script.strip():  # Check if script is not empty
            try:
                # Execute the SQL script
                conn.executescript(sql_script)
                self.success("SQL script executed successfully.")

            except sqlite3.Error as sql_error:
                self.error(f"Error executing SQL script: {sql_error}")
        else:
            self.warning(
                "The SQL file is empty. Please provide valid SQL statements.")

        return conn

    def extensionDb(self, file_path):
        return sqlite3.connect(file_path)
    
    def fetchTable(self, conn):
        # Retrieve and display table names
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")

        tables = cursor.fetchall()
        return tables
    
    def return_first_5_row(self, table_name, conn):
        return pd.read_sql_query(
                    f"SELECT * FROM {table_name[0]} LIMIT 5;", conn)
    
    def execute_query(self, query, conn=""):
        try:
            # Step 4: Execute and display the query result
            result = pd.read_sql(query, conn)
            self.write(result)
        except Exception as e:
            self.error(f"Error executing query: {e}")
