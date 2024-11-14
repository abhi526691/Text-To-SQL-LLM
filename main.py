from TTS.base_tts import View
from TTS.retrieve_schema import schemaRetrieve
from TTS.text_to_sql_gemini import GenerateQuery
from TTS.db_management import Database


def main():
    view = View()  # Initialize the view with the dark theme
    view.title("Text(NLP) to SQL LLM")
    Home, QueryEditor = view.tabs(["Home", "Query Editor"])

    with Home:
        db_file = view.file_uploader(
            "Upload file", type=["sqlite", "db", "sql"])
        Tables, Schema = view.tabs(["Tables List", "Schema Diagram"])

        with Tables:
            if db_file:
                schema_retrieve = schemaRetrieve(db_file=db_file)
                schema = schema_retrieve.db_to_schema()
                if schema:
                    schema_context = schema_retrieve.transform_schema(
                        schema=schema)
            else:
                view.subheader("Please Upload the SQL file to view the tables")

        with Schema:
            try:
                schema_retrieve.display_schema_diagram(schema_context)
            except Exception as e:
                view.subheader(
                    "Please Upload the SQL file to view the schema diagram")

    with QueryEditor:
        view.header("SQL Query Tester")
        nlp_input = view.text_area("Write your NLP Input here:", "")

        if view.button("SQL Query Tester"):
            if schema_context:
                sql_query = GenerateQuery().generate_sql_query_with_gemini(nlp_input, schema_context)
                view.write(sql_query)

                sql_query = view.extract_sql_query(sql_query)
                print("SQL QUERY", sql_query)

                if schema_retrieve.extension == 'sql':
                    Database().execute_sql_query(sql_query, schema_retrieve.conn)
                else:
                    Database().execute_db_query(sql_query, schema_retrieve.conn)
            else:
                view.error("Please Upload the Database file")


main()
