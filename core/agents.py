from rich.pretty import pprint

# Langchain Imports:
from typing import Callable
from langchain.schema import AgentFinish
from langchain_core.runnables.base import RunnableSequence
from langchain_core.runnables.utils import Output
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_functions

class Agent:
    def __init__(self, role, goal, verbose=True):
        self.role = role
        self.goal = goal
        self.verbose = verbose
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        # Apparently text completion endpoint is different from chat completion. Only latter seems support tool calling.
        # llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_retries=3)

class Task:
    def __init__(self, description: str, outcome: str, agent: Agent, tools: dict[str: Callable]):
        self.description = description
        self.outcome = outcome
        self.agent = agent
        self.tools = tools

    def execute(self):
        """
        Tasks through chain of agents. Call this for general tasks.
        """
        history = []

        llm_with_tools = self.agent.llm.bind_functions(list(self.tools.values()))

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a {role}. Your goal is to {goal}. Use the provided tools appropriately to accomplish tasks."
                ),
                ("human", "Perform the given task. Task: {description}. The desired outcome is {outcome}. Use the necessary tools."),
                MessagesPlaceholder(variable_name="history")
            ]
        )

        llm_chain: RunnableSequence = prompt | llm_with_tools | OpenAIFunctionsAgentOutputParser()

        while True:
            fmt_openai_functions = format_to_openai_functions(history)
            res = llm_chain.invoke(
                {
                    "role": self.agent.role,
                    "goal": self.agent.goal,
                    "description": self.description,
                    "outcome": self.outcome,
                    "history": fmt_openai_functions,
                }
            )

            if self.agent.verbose:
                pprint(res)
                print("-------------------")

            if isinstance(res, AgentFinish): 
                return res.return_values['output']

            else: 
                tool_res = self.tools[res.tool].run(res.tool_input)
                history.append((res, tool_res))