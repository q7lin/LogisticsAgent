from config import *
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationTokenBufferMemory

class report_agent:
    def __init__(self, user_id):
        self.llm = llm
        self.MEMORY_KEY = "chat_history",
        self.template = """
        用户输入为：
        {input}
        """

        tools = []

        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.memory = self.get_memory(user_id=user_id)

        memory = ConversationTokenBufferMemory(
            llm=self.llm,
            memory_key=self.MEMORY_KEY,
            human_prefix="",
            ai_prefi="",
            output_key="output",
            return_messages=True,
            max_token_limit=1000,
            chat_memory=self.memory,
        )

        report_agent = create_openai_tools_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.report_agent_executor = AgentExecutor(
            agent=report_agent,
            memory=memory,
            tools=tools,
            max_iteration=3,
            verbose=True,
        )

    def get_memory(self, user_id):
        return None

    def run(self, query: str):
        result = self.report_agent_executor.invoke({"input": query})

        return result