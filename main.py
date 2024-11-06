
from TTS.base_tts import View
from TTS.retrieve_schema import schemaRetrieve
from TTS.text_to_sql_gemini import GenerateQuery
from TTS.db_management import Database


def main():
    View().title("Text(NLP) to SQL LLM")
    db_file = View().file_uploader(
        "Upload file", type=["sqlite", "db", "sql"])
    schema_retrieve = schemaRetrieve(db_file=db_file)
    schema = schema_retrieve.db_to_schema()
    if schema:
        schema_context = schema_retrieve.transform_schema(schema=schema)
        View().header("SQL Query Tester")
        nlp_input = View().text_area("Write your SQL query here:", "")

        if View().button("SQL Query Tester"):
            sql_query = GenerateQuery().generate_sql_query_with_gemini(
                nlp_input, schema_context)
            View().write(sql_query)

            sql_query = sql_query.replace('`', '')
            sql_query = sql_query.replace('sql', '')

            if schema_retrieve.extension == 'sql':
                Database().execute_sql_query(sql_query, schema_retrieve.conn)
            else:
                Database().execute_db_query(sql_query, schema_retrieve.conn)


main()


# # Main Flow
# file_uploader = FileUploader()
# schema = file_uploader.process_file()
# if schema:
#     encoded_schema = file_uploader.transform_schema(schema)

#     # Step 3: SQL Query Input
#     View().header("SQL Query Tester")
#     query = View().text_area("Write your SQL query here:", "")

#     if View().button("Create SQL Query"):
#         # schema_elements = file_uploader.retrieve_schema_elements_with_gemini(
#         #     query)
#         sql_query = file_uploader.generate_sql_query_with_gemini(
#             query, encoded_schema)

#         if sql_query:
#             View().title("Interactive SQL Query Editor")
#             View().write(sql_query)
#             # data = View().text_area(label="Edit SQL Query", message=sql_query)
#             if View().button("Run SQL Query"):
#                 # Error need to be worked upon
#                 file_uploader.execute_sql_query(sql_query)


# class FileUploader:

#     def __init__(self):
#         # Initialize ChromaDB client and create a collection
#         self.client = Client()
#         self.initialize_collection()
#         self.conn = ""

#     def initialize_collection(self):
#         # Attempt to delete the existing collection
#         try:
#             self.client.delete_collection(name="schema_collection")
#         except Exception as e:
#             print("Collection not found or unable to delete:", e)

#         # Create a new collection that will have the correct dimensionality
#         self.collection = self.client.get_or_create_collection(
#             name="schema_collection")

#     def process_file(self):
#         # Step 1: Upload SQLite or SQL file
#         uploaded_file = View().file_uploader(
#             "Upload file", type=["sqlite", "db", "sql"])

#         if uploaded_file is not None:

#             # Save file temporarily
#             with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#                 temp_file.write(uploaded_file.getvalue())
#                 file_path = temp_file.name

#             try:
#                 if uploaded_file.name.endswith('.sql'):
#                     self.conn = FileFormat().extensionSql(uploaded_file)
#                 else:
#                     self.conn = FileFormat().extensionDb(file_path)

#                 # Fetch tables from the database
#                 tables = FileFormat().fetchTable(self.conn)

#                 schema = FileFormat().define_schema(tables, self.conn)

#                 # Display table names
#                 View().header("Available Tables")
#                 if tables:
#                     View().write("Tables in the uploaded SQL file:")
#                     for table_name in tables:
#                         View().write(f"- {table_name[0]}")

#                         # Optional: Display first 5 rows from each table
#                         data = FileFormat().return_first_5_row(table_name, self.conn)
#                         View().write(data)
#                 else:
#                     View().warning("No tables found in the SQL script.")

#                 return schema

#             except Exception as e:
#                 View().error(f"An error occurred: {e}")

#             # finally:
#             #     # Ensure the database connection is closed
#             #     if 'conn' in locals():
#             #         self.conn.close()
#             #     if os.path.exists(file_path):
#             #         os.remove(file_path)  # Cleanup temporary file

#     def transform_schema(self, schema):
#         transformed_schema = {}
#         for table, columns in schema.items():
#             transformed_schema[table] = {
#                 column["name"]: column["type"] for column in columns}

#         return transformed_schema

#     def generate_sql_query_with_gemini(self, nlp_input, schema_context):

#         # Prepare the schema context for the prompt

#         prompt = f"""
#         Schema Information:
#         {schema_context}
#         For each table, the schema is defined as follows:
#             Table: <table_name>
#                 <column_name>: <column_type>

#         Example:
#             Table: user_details
#                 user_id: INTEGER
#                 username: VARCHAR(255)
#                 first_name: VARCHAR(50)
#                 last_name: VARCHAR(50)
#                 gender: VARCHAR(10)
#                 password: VARCHAR(50)
#                 status: TINYINT

#         and there can be multiple tables and schema in the same db

#         Generate an SQL query based on this schema for the user query: "{nlp_input}"
#         """

#         try:
#             model = genai.GenerativeModel('gemini-pro')
#             response = model.generate_content(prompt)

#             # Extract and return the generated SQL query from the response
#             sql_query = response.text  # Assuming 'result' contains the generated text
#             return sql_query

#         except Exception as e:
#             View().error(f"An error occurred while generating SQL query: {e}")
#             return ""

#     def execute_sql_query(self, query):
#         FileFormat.execute_query(query, self.conn)
