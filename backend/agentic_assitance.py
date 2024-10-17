import logging
from prompts import extract_question, find_solution, provide_explanation
from llm import basic_model, chat_model, json_op_model
from tools import non_math_tool, basic_math_tool, advanced_math_tool
# import nest_asyncio
#
# nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Log an informational message to indicate the start of the program
logging.info('Agentic assistance started')


def extract_questions(image):
    try:
        logging.info('Extracting questions from image')  # Log before starting processing
        model = basic_model()
        prompt = extract_question()
        response = model.generate_content([image, prompt])

        # Log the response from the model (for debugging purposes)
        logging.debug(f'Extracted questions response: {response.text}')

        # ques_list = response.text.split("\n")
        # ques_str = ", ".join(ques_list)

        return response.text

    except Exception as e:
        # Log the error with stack trace for better debugging
        logging.error(f"Error extracting questions: {str(e)}", exc_info=True)
        raise  # Re-raise the exception after logging it


def agentic_solution(questions):
    try:
        logging.info('Generating solution for questions')  # Log before processing questions
        prompt = find_solution(questions)
        chat = chat_model([non_math_tool, basic_math_tool, advanced_math_tool], True)
        response = chat.send_message(prompt)

        # Log the solution for debugging purposes
        logging.debug(f'Solution generated: {response}')

        return response.text

    except Exception as e:
        # Log the error with stack trace
        logging.error(f"Error generating solution: {str(e)}", exc_info=True)
        raise  # Re-raise the exception after logging it


def solution_with_explanation(solutions):
    try:
        logging.info('Generating explanation for questions')  # Log before processing questions
        model = json_op_model()
        prompt = provide_explanation(solutions)
        response = model.generate_content(prompt)

        # Log the response for debugging purposes
        logging.debug(f'Solution generated: {response.text}')

        return response.text
    except Exception as e:
        logging.error(f"Error generating solution:{str(e)}", exc_info=True)
        raise
