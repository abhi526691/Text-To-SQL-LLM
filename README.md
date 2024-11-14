# Text-to-SQL Gemini Project

This project is a Text-to-SQL application that leverages Google’s Gemini LLM to transform natural language input into SQL queries. The application reads a database schema, processes user inputs, and generates SQL queries to retrieve data based on those inputs. It is built with Python and Streamlit, making it suitable for both database management and natural language processing tasks.



https://github.com/user-attachments/assets/89f436d0-9d92-4b44-bda4-16cbcabc74dc


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Example Usage](#example-usage)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Dynamic Database Connection**: Connects to both SQL script files and SQLite databases, dynamically retrieving table schemas.
- **Text-to-SQL Query Generation**: Generates SQL queries using Gemini LLM based on user-inputted natural language queries.
- **Schema Visualization**: Displays database schema in a user-friendly layout with tables, columns, and data types.
- **Customizable UI**: Streamlit-based interface with dark theme support for enhanced user experience.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abhi526691/ATS-Resume-
   cd Text-To-SQL-LLM
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables by creating a `.env` file and adding your Google Gemini API key:<br>
   Get Your API KEY from [Gemini](https://ai.google.dev/gemini-api/docs/api-key)

   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

---

## Usage

1. Run the application with the following command:

   ```bash
   streamlit run main.py
   ```

2. Upload a database file (.sql or .db) using the UI file uploader.
3. Enter a natural language query describing the data you wish to retrieve from the database.
4. View the generated SQL query and its results.

---

## Modules

### `main.py`

Contains the primary application code, initializing the database schema, generating SQL queries, and displaying the schema diagram.

### `TTS/base_tts.py`

Defines the `View` class, which provides methods for rendering UI elements in Streamlit, processing user input, and applying custom styles.

### `TTS/db_management.py`

Handles database management, including loading SQL files or SQLite databases, executing SQL queries, and retrieving schema information.

### `TTS/retrieve_schema.py`

Responsible for retrieving and transforming the schema, including visual representation in Streamlit.

### `TTS/text_to_sql_gemini.py`

Contains the logic for generating SQL queries from natural language input using the Google Gemini model.

---

## Example Usage

1. Launch the application and upload a `.db` or `.sql` file.
2. Enter a query, such as:

   - "Show me all user details with active status."
   - "Retrieve the top 5 orders sorted by date."

3. The system will use the Gemini LLM to generate the SQL query based on the database schema and execute it, displaying the results.

---

## Acknowledgements

- [Google Gemini LLM](https://cloud.google.com/): Used for text-to-SQL query generation.
- [Streamlit](https://streamlit.io/): Provides the web interface for the application.

## Contributor

<p align="center">

|                                                                                                                                                                                                                   <a href="https://github.com/abhi526691"><img src="https://avatars.githubusercontent.com/abhi526691" width="150px" height="150px" /></a>                                                                                                                                                                                                                    |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                                                                                                                                                                                                             **[Abhishek Pandey](https://github.com/abhi526691)**                                                                                                                                                                                                                                                              |
| <a href="https://github.com/abhi526691"><img src="https://cdn.iconscout.com/icon/free/png-256/github-108-438008.png" width="32px" height="32px"></a> <a href="https://www.instagram.com/_abhishek__pandey___/"><img src="https://cdn.iconscout.com/icon/free/png-512/free-instagram-216-721958.png" width="32px" height="32px"></a> <a href="https://www.linkedin.com/in/abhishek-pandey-1515aa171/"><img src="https://i.ibb.co/Kx2GSrT/linkedin.png" width="32px" height="32px"></a><a href="https://www.facebook.com/abhishek10548"><img src="https://cdn.iconscout.com/icon/free/png-512/free-facebook-263-721950.png" width="32px" height="32px"></a> |

This project demonstrates a powerful integration of LLMs with SQL databases, making it easy to retrieve data without needing in-depth knowledge of SQL syntax.
