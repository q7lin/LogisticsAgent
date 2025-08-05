from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationTokenBufferMemory
from myTools.report_tools import *
from utils.config import *

class report_agent:
    def __init__(self, user_id):
        self.llm = llm
        self.user_id = user_id
        self.MEMORY_KEY = "chat_history"
        self.template = """你是报表信息助手，你主要负责所有数据的总结和可视化，你的名字叫小星
        以下是你的个人设定：
        1.你比较严格，你会对用户发出的指令进行严格判断，指令不清晰、模糊时，你都会让用户重新下指令。
        2.你对待工作比较认真，一点数据处理上的错误都不会犯，你做出来的报表质量都很高。
        3.当用户给你指令进行操作时，你在完成操作的过程中，有时会加上你之前处理数据的案例。
        4.你从不说自己是人工智能或者ai，而是称呼自己为小星。
        以下是你的口头禅：
        1.开始工作咯，美好的一天开始啦。
        2.好多数据信息要处理啊，看本天才怎么又快又好的完成。
        3.太厉害了，这么完美的数据处理工作也只有我能完成了。
        以下是你的工作流程：
        1.当初始和用户对话时，你会先询问用户的工作任务。
        2.在明确用户需求之后，你会从用户输入那里拿到数据data，以此来进行数据分析。
        3.当用户想要图形数据总结时，你会调用绘图数据总结工具。
        4.当用户想要表格数据总结时，你会调用制表数据总结工具。
        5.你会保存每一次的聊天记录，以便后续对话使用。
        用户输入为：
        {input}
        
        需要用到的数据为：
        {data}
        """

        tools = [generate_chart, generate_table]

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.template
                ),
                (
                    "user",
                    "{input}\n{data}"
                )
            ]
        )

        self.memory = self.get_memory()

        memory = ConversationTokenBufferMemory(
            llm=self.llm,
            memory_key=self.MEMORY_KEY,
            human_prefix="用户",
            ai_prefi="小星",
            output_key="output",
            return_messages=True,
            max_token_limit=1000,
            chat_memory=self.memory,
        )

        my_report_agent = create_openai_tools_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.report_agent_executor = AgentExecutor(
            agent=my_report_agent,
            memory=memory,
            tools=tools,
            max_iteration=3,
            verbose=True,
        )

    def get_memory(self):
        """
            1.报表处理的记忆模块，可以查询对哪些数据进行了总结
            2.现在有一个问题，报表的数据来源从哪里获得？是也弄一个查询工具，还是从db_agent的查询返回信息来获得数据，这样要怎么获取，不会耦合程度太高了吗
        """

        chat_message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0", session_id=self.user_id + "_agent_b",
        )

        #对memory进行处理，防止超出窗口限制
        store_message = chat_message_history.messages

        # 实现总结链，完成语义压缩和滑动窗口功能
        if len(store_message) > 10:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        self.template+"\n 这是一段你和用户的对话记录，对其进行总结摘要，\
                                    摘要使用第一人称“我”，并且提取其中的关键信息，如：操作指令等。\
                                    以如下格式返回：\n \
                                    总结摘要 | 用户关键指令 \n 例如：用户章三给予我任务\
                                    指令，我回复后并调用相关工具完成任务，然后他告辞离开\
                                    | 章三，苹果入库五箱"
                    ),
                    (
                        "user","{input}"
                    )
                ]
            )

            chain = prompt | self.llm
            summary = chain.invoke({"input":store_message})
            print(summary)

            #将超出窗口的记忆
            chat_message_history.clear()

            #将清除的记忆总结精炼后添加进来
            chat_message_history.add_message(summary)

        return chat_message_history

    def run(self, query: str, data: dict):

        result = self.report_agent_executor.invoke({"input": query, "data":data})

        return result