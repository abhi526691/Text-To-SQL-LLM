import tempfile
import os
import uuid
from database import FileFormat
from frontend import View
import google.generativeai as genai

from chromadb import Client
from chromadb.config import Settings
from chromadb.types import Collection

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


View().title("Text(NLP) to SQL LLM")


class FileUploader:
    def __init__(self):
        # Initialize ChromaDB client and create a collection
        self.client = Client()
        self.initialize_collection()
        self.conn = ""

    def initialize_collection(self):
        # Attempt to delete the existing collection
        try:
            self.client.delete_collection(name="schema_collection")
        except Exception as e:
            print("Collection not found or unable to delete:", e)

        # Create a new collection that will have the correct dimensionality
        self.collection = self.client.get_or_create_collection(
            name="schema_collection")

    def process_file(self):
        # Step 1: Upload SQLite or SQL file
        uploaded_file = View().file_uploader(
            "Upload file", type=["sqlite", "db", "sql"])

        if uploaded_file is not None:

            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                file_path = temp_file.name

            try:
                if uploaded_file.name.endswith('.sql'):
                    self.conn = FileFormat().extensionSql(uploaded_file)
                else:
                    self.conn = FileFormat().extensionDb(file_path)

                # Fetch tables from the database
                tables = FileFormat().fetchTable(self.conn)

                schema = FileFormat().define_schema(tables, self.conn)

                return schema

                # # Display table names
                # View().header("Available Tables")
                # if tables:
                #     View().write("Tables in the uploaded SQL file:")
                #     for table_name in tables:
                #         View().write(f"- {table_name[0]}")

                #         # Optional: Display first 5 rows from each table
                #         data = FileFormat().return_first_5_row(table_name, self.conn)
                #         View().write(data)
                # else:
                #     View().warning("No tables found in the SQL script.")

            except Exception as e:
                View().error(f"An error occurred: {e}")

            finally:
                # Ensure the database connection is closed
                if 'conn' in locals():
                    self.conn.close()
                if os.path.exists(file_path):
                    os.remove(file_path)  # Cleanup temporary file

    # def get_sql_from_text(self, question, schema):
    #     schema_context = "\n".join([f"Table: {item['metadata']['table']}, Column: {
    #                                item['metadata']['column']} ({item['metadata']['type']})" for item in schema])
    #     prompt = f"""
    #     Schema Information:
    #     {schema_context}

    #     Generate an SQL query based on this schema for the user query: "{question}"
    #     """
    #     model = genai.GenerativeModel('gemini-pro')
    #     response = model.generate.content([prompt, question])
    #     return response.text
    def encoding_schema(self, schema):
        for table, columns in schema.items():
            for column in columns:
                metadata = {
                    "table": table,
                    "column": column["name"],
                    "type": column["type"]
                }
                # Generate a unique ID for each entry
                doc_id = str(uuid.uuid4())

                # Generate embedding for the column name
                column_embedding_response = genai.embed_content(
                    model="models/text-embedding-004", content=column["name"]
                )
                column_embedding = column_embedding_response['embedding']

                # Add to ChromaDB collection with the embedding
                self.collection.add(
                    ids=[doc_id],
                    documents=[column["name"]],
                    metadatas=[metadata],
                    embeddings=[column_embedding]  # Add the embedding
                )

    def retrieve_schema_elements_with_gemini(self, query, top_k=3):
        # Generate embeddings for the query using Gemini
        response = genai.embed_content(
            model="models/text-embedding-004", content=query)
        # Ensure this returns a single embedding
        query_embedding = response['embedding']

        # Perform a similarity search in the vector database
        results = self.collection.query(query_embedding, n_results=top_k)
        return results  # Returns relevant schema elements for the query

    def generate_sql_query_with_gemini(self, nlp_input, schema_elements):
        # Inspect the structure of schema_elements
        # Debugging line to inspect contents
        print("Schema Elements:", schema_elements)

        # if not schema_elements or not isinstance(schema_elements, list):
        #     View().warning("No schema elements provided for generating SQL query.")
        #     return ""

        # Prepare the schema context for the prompt
        try:
            schema_context = "\n".join([
                f"Table: {item['metadata']['table']}, Column: {
                    item['metadata']['column']} ({item['metadata']['type']})"
                for item in schema_elements
                # Ensure item is a dict with 'metadata'
                if isinstance(item, dict) and 'metadata' in item
            ])
        except Exception as e:
            View().error(
                f"An error occurred while processing schema elements: {e}")
            return ""

        prompt = f"""
        Schema Information:
        {schema_context}

        Generate an SQL query based on this schema for the user query: "{nlp_input}"
        """

        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            # Extract and return the generated SQL query from the response
            sql_query = response.text  # Assuming 'result' contains the generated text
            return sql_query

        except Exception as e:
            View().error(f"An error occurred while generating SQL query: {e}")
            return ""

    def execute_sql_query(self, query):
        FileFormat.execute_query(query, self.conn)


# Main Flow
file_uploader = FileUploader()
schema = file_uploader.process_file()
if schema:
    encoded_schema = file_uploader.encoding_schema(schema)

    # Step 3: SQL Query Input
    View().header("SQL Query Tester")
    query = View().text_area("Write your SQL query here:")

    if View().button("Create SQL Query"):
        schema_elements = file_uploader.retrieve_schema_elements_with_gemini(
            query)
        sql_query = file_uploader.generate_sql_query_with_gemini(
            query, schema_elements)

        if sql_query:
            View().write(sql_query)
            # Error need to be worked upon
            file_uploader.execute_sql_query(sql_query)
