from langchain.tools import tool
from langchain_openai import OpenAI, ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

@tool
def sum(a: int, b: int) -> str:
    """A calculator that can add variables a and b, i.e., calculate a + b."""
    return f"The result of {a} + {b} is {str(a+b)}"

@tool
def multiply(a: int, b: int) -> str:
    """A calculator that can perform multiplication of variables a and b, i.e., calculate a * b."""
    return f"The result of {a} * {b} is {str(a*b)}"

@tool
def random_joke_from_openai(topic: str) -> str:
    """A comedian who can perform good jokes in English."""
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=1.1)
    return (llm | StrOutputParser()).invoke(f"Tell me a random funny joke on {topic} in English")

@tool
def translator_from_openai(text: str, lang: str) -> str:
    """A translator that translates a given text into the specified language."""
    prompt = f"Translate the following text into {lang}: '{text}'"
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.3)
    return (llm | StrOutputParser()).invoke(prompt)

@tool
def programmer_from_openai(question: str) -> str:
    """
    A programmer who writes accurate Python functions to solve general competitive programming problems.
    """
    prompt = f"""
                Write a Python function to solve the following competitive programming problem. No need to write comments. Question: {question}. \
            """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    return (llm | StrOutputParser()).invoke(prompt)

# WARNING!!! This code runner allows all global environments
@tool
def code_runner(code: str, input_dict: dict) -> str:
    """
    Executes a Python function named 'main' defined in the provided 'code' string using the arguments specified in 'input_dict'. Must provide 'input_dict' argument.
    
    The 'code' string must contain a definition for a function named 'main', which will be invoked with the arguments passed in 'input_dict'. 
    This function is intended for dynamically executing user-defined Python functions where the function's interface (i.e., name and parameters) 
    are known and consistent.

    Args:
    - code (str): A string containing valid Python code that must define a function named 'main'. 
                  This function should accept parameters as specified in 'input_dict'.
    - input_dict (dict): A dictionary where keys are the parameter names expected by the 'main' function, 
                         and values are the corresponding arguments to be passed to the function.
    """

    local_env = {}
    global_env = globals()

    try:
        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code, global_env, local_env)
        if 'main' in local_env: return str(local_env['main'](**input_dict))
        else: raise Exception("No function named 'main' found in the provided code.")
    except Exception as e:
        return f"An error occurred: {str(e)}"
