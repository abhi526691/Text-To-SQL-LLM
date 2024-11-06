import os
from .base_tts import View
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class GenerateQuery:

    def generate_sql_query_with_gemini(self, nlp_input, schema_context):

        # Prepare the schema context for the prompt
        prompt = View().prompt(nlp_input, schema_context)
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            # Extract and return the generated SQL query from the response
            sql_query = response.text
            return sql_query

        except Exception as e:
            View().error(f"An error occurred while generating SQL query: {e}")
            return ""
