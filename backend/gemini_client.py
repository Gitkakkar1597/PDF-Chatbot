import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')
if API_KEY is None:
    raise ValueError("API_KEY not found in environment variables")

genai.configure(api_key=API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_response(self, context, query):
        # Ensure the prompt explicitly restricts the response to the context
        prompt = (
            "You are an assistant trained to answer questions in short based on the following context. "
            "Please provide answers only using the information from the provided context and be concise, "
            "to the point, and structured in the domain of knowledge of the given data.\n\n"
            f"Context: {context}\n\n"
            f"Query: {query}"
        )

        # Debug: Print context and query
        print(f"Prompt: {prompt[:500]}...")  # Print first 500 chars of prompt

        # Use the Gemini model to generate a response based on the context and query
        response = self.model.generate_content(prompt)
        
        # Debug: Print response
        print(f"Response: {response.text}")

        return response.text
