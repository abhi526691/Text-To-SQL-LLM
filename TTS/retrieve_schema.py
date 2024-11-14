import tempfile

from .base_tts import View
from .db_management import Database


class schemaRetrieve(View):

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = ""
        self.extension = ""

    def db_to_schema(self):
        if self.db_file is not None:
            # Save file temporarily and retrieve file path
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(self.db_file.getvalue())
                file_path = temp_file.name

            try:
                if self.db_file.name.endswith('.sql'):
                    self.extension = "sql"
                    self.conn = Database().sql_handling(self.db_file)
                else:
                    self.extension = "db"
                    self.conn = Database().db_handling(file_path)

                # Fetch tables from the database
                tables = Database().fetch_table_details(self.conn)
                schema = Database().define_schema(tables, self.conn)

                # Display table names
                View().header("Available Tables")
                preprocessed_table = View().process_text(tables)
                for table in preprocessed_table:
                    with View().expander(table):
                        Database().return_first_5_row(table, self.conn)

                return schema

            except Exception as e:
                View().error(f"An error occurred: {e}")
                return ""

    def transform_schema(self, schema):
        transformed_schema = {}
        for table, columns in schema.items():
            transformed_schema[table] = {
                column["name"]: column["type"] for column in columns}

        return transformed_schema


    def display_schema_diagram(self, schema):

        # Define the number of columns to display the schema side by side
        cols = View().columns(3)  # You can change this number depending on how many columns you want

        # For each column, display the table schema
        col_index = 0
        for table_name, columns in schema.items():
            with cols[col_index]:
                View().subheader(f"Table: {table_name}")
                for column_name, column_type in columns.items():
                    View().write(f"{column_name}: {column_type}")
            
            # Move to the next column after each table
            col_index += 1
            if col_index >= len(cols):
                col_index = 0  # Reset to the first column if there are more tables than columns
        
