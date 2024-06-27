# Agents and Tasks:
from core.agents import Agent, Task

# Tools:
from core.tools import random_joke_from_openai, translator_from_openai

tools = {
    "random_joke_from_openai": random_joke_from_openai,
    "translator_from_openai": translator_from_openai
}

agent = Agent("joke teller in French", "to tell funny jokes for everyone to laugh in French language")
task = Task(
    "Create a joke and translate it into French", 
    "A very funny joke in French",
    agent, 
    tools
)
print(task.execute())