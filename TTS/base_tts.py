import streamlit as st
import re


class View:
    def __init__(self):
        self.apply_dark_theme()

    def apply_dark_theme(self):
        # Apply custom CSS to create a full black theme
        st.markdown("""
            <style>
            /* Text area specifically (for larger editor size) */
            .stTextArea textarea {
                height: 300px !important;  /* Larger editor size */
                font-size: 16px !important; /* Larger font size */
            }
            </style>
        """, unsafe_allow_html=True)

    # Existing methods in View class...
    def process_text(self, data):
        pattern = r"'(.*?)'"
        return [re.search(pattern, str(item)).group(1) for item in data if re.search(pattern, str(item))]

    def extract_sql_query(self, sql):
        sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
        sql = re.sub(r"--.*", "", sql)
        sql = re.sub(r"\s+", " ", sql).strip()
        sql = sql.replace("sql", "")
        sql = sql.replace("`", "")
        return sql

    def tabs(self, tab_list):
        return st.tabs(tab_list)

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
        return st.dataframe(data=data, hide_index=True)

    def select_box(self, data):
        return st.selectbox("Select a table to display:", data)

    def expander(self, text):
        return st.expander(text)

    def subheader(self, text):
        return st.subheader(text)

    def columns(self, col):
        return st.columns(col)

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
