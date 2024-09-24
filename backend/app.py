from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import json
import os
import logging
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, sympify
from sympy.plotting import plot

app = Flask(__name__)

load_dotenv()

CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Ensure you have set this environment variable
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config={"response_mime_type": "application/json"})


def process_image_with_gemini(image):
    prompt = 'You are an expert Physics and math tutor. Your job to recognize ' \
             'questions in image and provide their answers. There may be single ' \
             'or multiple questions in the image and the questions maybe numbered ' \
             'or not numbered. The output should be in JSON format having ' \
             'parameters "question", "explanation", "solution" and "equations". ' \
             'Recognize the question then provide explanation, solution. ' \
             'Only provide equations of polynomials, equations in 2 variables and ' \
             'equations of lines present in mathematics questions that can be ' \
             'plotted in graph, for any other condition output an empty list. If ' \
             'there exists multiple questions then separate them based on schema. ' \
             'Using this JSON schema: ' \
             ' Solutions = {"question": str, "explanation": str, "solution": str, "equations": list[str]} ' \
             'Return list[Solutions]. if you don\'t find any question just return no questions asked in same format.'

    try:
        response = model.generate_content([prompt, image])
        app.logger.debug(f"Raw Gemini response: {response.text}")
        return response.text
    except Exception as e:
        app.logger.error(f"Error in process_image_with_gemini: {str(e)}")
        raise


@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get the image data from the request
        image_data = request.json['image']

        # Convert base64 image to PIL Image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data))
        image.save("op.png")

        # Generate content using the Gemini model
        response = process_image_with_gemini(image)  #list of dictionary

        # Parse the JSON response
        try:
            solutions = json.loads(response)
        except json.JSONDecodeError as e:
            app.logger.error(f"Failed to parse JSON: {e}")
            app.logger.error(f"Raw response: {response}")
            return jsonify({'error': 'Failed to parse Gemini response', 'raw_response': response}), 500

        # Extract equations for plotting
        equations = []
        for solution in solutions:
            equations.extend(solution.get('equations', []))

        return jsonify({
            'solutions': solutions,
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
