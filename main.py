# Agents and Tasks:
from core.agents import Agent, Task

# Tools:
from core.tools import sum, multiply, random_joke_from_openai

tools = {
    "sum": sum,
    "multiply": multiply,
    "random_joke_from_openai": random_joke_from_openai
}

agent = Agent("joke teller", "to tell funny jokes for everyone to laught")
task = Task("Tell a joke where even a dead person would laugh", agent, tools)
print(task.execute())