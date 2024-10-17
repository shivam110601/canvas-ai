def parse_wolfram_res_prompt(res):
    # prompt = f"""
    #     Analyze the provided API response. Focus on extracting the solution of the
    #     question from the 'Result' section and identify the URL for any related plot.
    #     Output only the solution and the if any plot is available then output the plot_url.
    #     Provide concise output in JSON format like:
    #     'solution': str, 'plot_url': str
    #
    #     API response: {res}
    #     """
    prompt = f"""
           Analyze the provided API response. Focus on extracting the solution from the
           response available in 'plaintext' section and try to identify the URL for any plot related to it.
           Output only the solutions and the if any plot is available then output the plot_url. 
           Provide concise output in JSON format like:
           'solution': str, 'plot_url': str

           API response: {res}
           """
    return prompt


def extract_question():
    prompt = """
    You are a senior university professor, with over two decades of experience
    reviewing handwritten notes. You began your teaching career in schools and
    through dedication, rose to the pinnacle of academia. You excel in identifying
    and correcting handwritten questions across a variety of subjects including
    general knowledge, arithmetic, algebra, and calculus.

    Your task:
    1. Analyze the provided image of handwritten content.
    2. Identify and extract each distinct question.
    3. Correct any spelling, grammar, or mathematical errors.
    4. Output the corrected questions in a concise format.

    Guidelines:
    - Focus only on questions, ignore irrelevant text.
    - Ensure mathematical symbols are precise.
    - Use clear, compact phrasing for each question.
    - Separate each question by a new line.
    """
    return prompt


def find_solution(question):
    prompt = f"""
    You are an intelligent assistant with access to three powerful tools:
    `non_math_tool`, `basic_math_tool`, and `advanced_math_tool`.
    Your task is to analyze each question in the list provided and provide accurate answer.

    Steps:
    1. Classify the Question:
       - Determine whether the question is mathematical or non-mathematical.
       - If the question is non-mathematical (general knowledge, science, etc.), use the `non_math_tool`.
       - If the question involves basic arithmetic operations (addition, subtraction, multiplication, division, 
          root, power) on two numbers only, use the `basic_math_tool`.
       - If the question requires solving arithmetic operations on more than two numbers or advanced mathematical 
          problems (integrals, derivatives or solving equations), use the `advanced_math_tool`.

    2. For Non-Mathematical Questions:
       - Call `non_math_tool(question: str)` with the question string.
       - Example: `non_math_tool("What is the percentage Iron in earth crust?")`

    3. For Basic Math Questions:
       - Extract the two numbers and the operation from the question.
       - Call `basic_math_tool(operation: str, num1: float, num2: float)`, where `operation` is one of ['add', 
          'subtract', 'multiply', 'divide', 'root', 'power'].
       - Example: For question '³√133629 = ?', `basic_math_tool('root', 133629, 3)`
                  For question '5³ = ?', `basic_math_tool('power', 5, 3)`

    4. For Advanced Math Questions:
       - Identify the type of operation (e.g., solve, integrate, derivative).
       - Call `advanced_math_tool(operation: str, expressions: List[str])` with the appropriate operation and 
          expression list.
       - Example: `advanced_math_tool('solve', ['4x² + 36x + 9 = 0'])`, 

    Questions: {question}

    """
    return prompt


def provide_explanation(solutions):
    # prompt = f"""
    # You are a highly experienced senior university professor with over two decades of expertise in reviewing handwritten
    # notes and guiding students through complex concepts. Having started your career in schools and risen to the pinnacle
    # of academia, you are well-versed in identifying where students need additional explanations.
    #
    # You will be given a list of questions, each with its corresponding solution. Your task is to provide a short
    # and concise explanation on how solution is derived. Only provide explanation when the content of solution is not
    # enough to explain itself, at any other time don't output explanation.
    #
    # Output Format:
    # - The output should be in JSON format.
    # - Each entry should include the following parameters:
    #   - question: str
    #   - explanation: A detailed breakdown of how the solution was reached.
    #   - solution: The solution that was already provided.
    #
    # Output in the form of List[Json], for multiple questions.
    #
    # Questions with Solutions:
    # {solutions}
    # """
    prompt = f"""
        You will be given a list of questions, each with its corresponding solution. Your task is to them and identify
        questions where the content of solution is not sufficient to explain itself, there you have to provide a short
         and concise explanation. In any other case don't provide explanation.

        Output Format:
        - The output should be in JSON format having following parameters:
          - question: str (necessary)
          - explanation: str (optional)
          - solution: str (necessary)

        Output in the form of List[Json], for multiple questions.

        Questions with Solutions:
        {solutions}
        """

    return prompt
