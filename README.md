# Canvas writing app with Gemini Agentic assistance.
#### Divided the question extraction and answer generation process into a three-step process:
 - Question extraction by prompting Gemini model.
 - Solution generation using Gemini Agent having access to three tools:
    - non_math_tool
    - basic_math_tool
    - advanced_math_tool
 - Explanation generation by prompting Gemini model.

![initial.png](initial.png)

![final.png](final.png)
