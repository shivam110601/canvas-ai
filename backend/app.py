from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import base64
from dotenv import load_dotenv
import json
import asyncio
import platform
import logging
from pydantic import BaseModel
from agentic_assitance import extract_questions, agentic_solution, solution_with_explanation
# import nest_asyncio
#
# nest_asyncio.apply()

# Initialize FastAPI app
app = FastAPI()

load_dotenv()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Pydantic model for input validation
class ImageRequest(BaseModel):
    image: str  # Base64 encoded image


def solution_generation_system(image):
    try:
        questions = extract_questions(image)
        solutions = agentic_solution(questions)
        final_response = solution_with_explanation(solutions)
        logger.debug(f"Raw Gemini response: {final_response}")
        return final_response
    except Exception as e:
        logger.error(f"Error in process_image_with_gemini: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing image with Gemini")


@app.post('/generate')
def generate(request: ImageRequest):
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image.split(',')[1])
        image = Image.open(BytesIO(image_data))
        # image = Image.open('op.png')
        image.save('op.png')

        # Generate content using the Gemini model
        response = solution_generation_system(image)

        # Parse the JSON response
        try:
            solutions = json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Raw response: {response}")
            raise HTTPException(status_code=500, detail="Failed to parse Gemini response")

        return {
            'solutions': solutions,
        }

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
