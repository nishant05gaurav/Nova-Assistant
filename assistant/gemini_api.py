"""Contains all the API credentials"""

# Importing necessary libraries
import google.generativeai as genai
from assistant.speech import speak

# Getting credentials of APIs used
API_KEY = "AIzaSyAEbv6V43-Pnx0OKrrm87hiys9eoUfVDmRqQ0ZYI"

# Initializing GenAI with API key  
genai.configure(api_key=API_KEY)

# Initializing model - gemini-pro
# model = genai.GenerativeModel("gemini-pro") --> Not useable anymore
# backup model: model = "models/gemini-2.5-flash-lite"
model = genai.GenerativeModel("models/gemini-2.5-flash")



# Gemini Integration 
def ask_gemini(prompt):
    """
    Sends a text prompt to the Gemini API, retrieves the generated response, 
    and audibly speaks the answer.

    This function interacts with the Gemini model to generate a response based 
    on the provided prompt. The response text is both returned and spoken aloud 
    using the `speak` function. If an error occurs during the API request, it 
    prints the error message, speaks an apology, and returns None.

    Args:
        prompt (str): The input text or question to be sent to the Gemini API.

    Returns:
        str or None: The generated response text from Gemini, or None if an 
        error occurred.
    """
    try:
        response = model.generate_content(
                f"""
                Answer briefly and clearly in 2–3 sentences.
                Avoid extra details.
                Question: {prompt}
                """
        )

        answer = response.text
        speak(answer)   
        return answer
    except Exception as e:
        print(f"[Gemini Error] {e}")
        speak("Sorry, I couldn't process that request.")
        return None