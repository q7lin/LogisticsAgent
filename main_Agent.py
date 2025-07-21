from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os

os.environ['OPENAI_API_KEY'] = "sk-bCI5yo6f9TadMj4RRQXBLSGIfqJBuIb2J1BxPHfEUEcmiv9z"
os.environ['OPENAI_API_PROXY'] = "https://sg.uiuiapi.com/v1"

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_PROXY")

llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0,
    model="gpt-3.5-turbo"
)

class LogisticsAgent:
    def __init__(self):
        self.llm = llm
        self.MEMORY_KEY = "chat_history"
        self.template = """你是一个物流仓管管理系统的智能助手，你的名字叫，
        以下是你的个人设定：
        {who_you_are}
        """
        self.emotion="default"
        self.MOODS = {

        }

        tools = []

        self.memory = ""

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.template.format(who_you_are=self.MOODS[self.emotion]["roleSet"]),
                ),
                MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                (
                    "user",
                    "input",
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            max_iterations=3,
            verbose=True,
        )