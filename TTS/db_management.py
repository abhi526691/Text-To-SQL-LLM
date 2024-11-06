import sqlite3
import pandas as pd
from .base_tts import View


class Database(View):

    def __init__(self):
        pass

    def sql_handling(self, file_path):

        # Create an in-memory SQLite database
        conn = sqlite3.connect(':memory:')
        sql_script = file_path.read().decode("utf-8")

        if sql_script.strip():

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

    def db_handling(self, file_path):
        return sqlite3.connect(file_path)

    def fetch_table_details(self, conn):
        # Retrieve and display table names
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return tables

    def return_first_5_row(self, table_name, conn):
        return pd.read_sql_query(
            f"SELECT * FROM {table_name[0]} LIMIT 5;", conn)

    def execute_db_query(self, query, conn):
        try:
            result = pd.read_sql(query, conn)
            self.write(result)
        except Exception as e:
            self.error(f"Error executing query: {e}")

    def execute_sql_query(self, query, conn):
        # try:
        cursor = conn.cursor()
        cursor.execute(f"{query}")
        data = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]
        print("column_names", column_names)
        df = pd.DataFrame(data, columns=column_names)
        View().table(df)

        # except Exception as e:
        #     self.error(f"Error executing query: {e}")

    def define_schema(self, tables, conn):
        schema = {}
        cursor = conn.cursor()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [
                {"name": col[1], "type": col[2]} for col in columns]
        return schema

    def display_table_data(self, tables, conn):
        View().header("Available Tables")
        if tables:
            View().write("Tables in the uploaded SQL file:")
            for table_name in tables:
                View().write(f"- {table_name[0]}")

                # Optional: Display first 5 rows from each table
                data = self.return_first_5_row(table_name, conn)
                View().write(data)
        else:
            View().warning("No tables found in the SQL script.")
