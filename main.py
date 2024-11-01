import tempfile
import os
from database import FileFormat
from frontend import View

View().title("Text(NLP) to SQL LLM")

# Step 1: Upload SQLite or SQL file
uploaded_file = View().file_uploader(
    "Upload file", type=["sqlite", "db", "sql"])

if uploaded_file is not None:

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        file_path = temp_file.name

    try:

        # Check the file type
        if uploaded_file.name.endswith('.sql'):
            conn = FileFormat().extensionSql(uploaded_file)
        else:
            conn = FileFormat().extensionDb(file_path)

        # Fetch tables from the database
        tables = FileFormat().fetchTable(conn)

        # Display table names
        View().header("Available Tables")
        if tables:
            View().write("Tables in the uploaded SQL file:")
            for table_name in tables:
                View().write(f"- {table_name[0]}")

                # Optional: Display first 5 rows from each table
                data = FileFormat().return_first_5_row(table_name, conn)
                View().write(data)
        else:
            View().warning("No tables found in the SQL script.")

        # Step 3: SQL Query Input
        View().header("SQL Query Tester")
        query = View().text_area("Write your SQL query here:")

        if View().button("Execute Query"):
            FileFormat().execute_query(query, conn)

    except Exception as e:
        View().error(f"An error occurred: {e}")

    finally:
        # Ensure the database connection is closed
        if 'conn' in locals():
            conn.close()
        if os.path.exists(file_path):
            os.remove(file_path)  # Cleanup temporary file
