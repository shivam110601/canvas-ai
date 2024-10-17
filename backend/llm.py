import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


def json_op_model():
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config={"response_mime_type": "application/json"})
    return model


def chat_model(tools: list = None, fn_call: bool = False):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=tools)
    chat = model.start_chat(enable_automatic_function_calling=fn_call)
    return chat


def basic_model():
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    return model
