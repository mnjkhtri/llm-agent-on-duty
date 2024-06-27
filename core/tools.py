from langchain.tools import tool
from langchain_openai import OpenAI
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