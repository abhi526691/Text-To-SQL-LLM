import streamlit as st


class View:
    def __init__(self):
        pass

    def title(self, message):
        return st.title(message)

    def file_uploader(self, message, type=[]):
        return st.file_uploader(message, type=type)

    def button(self, message):
        return st.button(message)

    def text_area(self, label, message):
        return st.text_area(label=label, value=message)

    def write(self, message):
        return st.write(message)

    def header(self, message):
        return st.header(message)

    def success(self, message):
        return st.success(message)

    def warning(self, message):
        return st.warning(message)

    def error(self, message):
        return st.error(message)

    def table(self, data):
        # Display the DataFrame as a table without row index
        return st.dataframe(data=data, hide_index=True)

    def prompt(self, nlp_input, schema_context):
        return f"""
        Schema Information:
        {schema_context}
        For each table, the schema is defined as follows:
            Table: <table_name>
                <column_name>: <column_type>

        Example:
            Table: user_details
                user_id: INTEGER
                username: VARCHAR(255)
                first_name: VARCHAR(50)
                last_name: VARCHAR(50)
                gender: VARCHAR(10)
                password: VARCHAR(50)
                status: TINYINT

        and there can be multiple tables and schema in the same db

        Generate an SQL query based on this schema for the user query: "{nlp_input}"
        """
