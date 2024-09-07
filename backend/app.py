from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

CORS(app)  # Enable CORS for all routes

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Ensure you have set this environment variable
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def process_image_with_gemini(image):
    # Convert image to bytes
    # buffer = BytesIO()
    # image.save(buffer, format='PNG')
    # image_bytes = buffer.getvalue()
    #
    # # Prepare the request
    # image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    prompt = "You are an expert math tutor. " \
             "Your job to recognize math questions in image " \
             "and provide their answers. There may be single " \
             "or multiple questions in the image and the questions " \
             "may be numbered or not numbered. The output should " \
             "have the math question along with its answer."

    # print(prompt)

    # Call the Gemini model
    response = model.generate_content([
        prompt,
        image
    ])

    # Extract the response text
    # print(response)
    return response.text


@app.route('/process-image', methods=['POST'])
def process_image():
    data = request.json
    image_data = data['image']

    # Remove the Base64 header part
    image_data = image_data.split(",")[1]

    # Decode the image
    img = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGB")

    img.save('received_image.png')

    # Resize the image to fit the model's input size (optional, you can experiment with different sizes)
    # img = img.resize((384, 384))

    # Use the Gemini model to process the image
    generated_text = process_image_with_gemini(img)

    return jsonify({"message": generated_text})


if __name__ == '__main__':
    app.run(debug=True)
