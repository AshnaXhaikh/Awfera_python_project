# app/services/gemini_handler.py
import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY

# Configure the Gemini API
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5-flash as it's a strong, fast model

def generate_answer_from_text(context: str, query: str) -> str:
    """
    Generates an answer using Gemini based on provided text and a query.

    Args:
        context: The text extracted from the PDF.
        query: The user's question.

    Returns:
        The generated answer from the Gemini model.
    """
    if not context:
        return "Could not extract text from the PDF. Please ensure the PDF contains selectable text."

    prompt = f"""
    Based on the following document text, please provide a clear and concise answer to the user's question.
    If the answer cannot be found within the text, state that the information is not available in the document.

    **Document Text:**
    ---
    {context}
    ---

    **User's Question:**
    {query}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the Gemini API: {e}"