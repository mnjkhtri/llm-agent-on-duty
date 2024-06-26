from rich.pretty import pprint

# Langchain Imports:
from typing import Callable
from langchain.schema import AgentFinish
from langchain_core.runnables.base import RunnableSequence
from langchain_core.runnables.utils import Output
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

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
    def __init__(self, description: str, agent: Agent, tools: dict[str: Callable]):
        self.description = description
        self.agent = agent
        self.tools = tools

    def execute(self):
        llm_with_tools = self.agent.llm.bind_tools(list(self.tools.values()))
        prompt = f"""
        You are a {self.agent.role}. Your goal is to {self.agent.goal}. Perform the given task. Task: {self.description}
        """
        llm_chain: RunnableSequence = llm_with_tools | OpenAIToolsAgentOutputParser()
        res: Output = llm_chain.invoke(prompt)

        if self.agent.verbose:
            pprint(res)
            print("-------------------")

        if isinstance(res, AgentFinish): return res.return_values['output']
        else: return self.tools[res[0].tool].run(res[0].tool_input)