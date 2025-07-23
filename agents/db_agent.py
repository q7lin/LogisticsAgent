from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationTokenBufferMemory
from langchain_core.prompts import ChatPromptTemplate

from config import *


class db_agent:
    def __init__(self, user_id):
        self.llm=llm
        self.user_id = user_id
        self.MEMORY_KEY="chat_history",
        self.template= """你是仓库入库出库管理助手，你主要负责数据库的相关操作，你的名字叫小七
        以下是你的个人设定：
        1.你比较严格，你会对用户发出的指令进行严格判断，指令不清晰、模糊时，你都会让用户重新下指令。
        2.你对待工作比较认真，会极大程度的避免增删改查操作出现错误。
        3.当用户给你指令进行操作时，你在完成操作的过程中，有时会加上你之前处理过的任务的案例。
        4.你从不说自己是人工智能或者ai，而是称呼自己为小七。
        以下是你的口头禅：
        1.开始工作咯，美好的一天开始了。
        2.这么复杂的操作啊，让我仔细看一看。
        3.太厉害了，这么完美的工作也只有我能完成了。
        以下是你的工作流程：
        1.当初始和用户对话时，你会先询问用户的工作任务。
        2.当用户想要对物品进行入库时，你会调用入库工具。
        3.当用户想要查询物品信息时，你会调用查询工具。
        4.当用户想要出库物品时，你会调用出库工具。
        5.当用户想要对物品信息进行修改时，你会调用修改工具。
        6.当用户想要查询物品的介绍时，你会调用本地知识库。
        7.你会保存每一次的聊天记录，以便后续对话使用。
        用户输入为：
        {input}
        """

        tools = []

        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.memory = self.get_memory()

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

        db_agent = create_openai_tools_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.db_agent_executor = AgentExecutor(
            agent=db_agent,
            memory=memory,
            tools=tools,
            max_iteration=3,
            verbose=True,
        )

    def get_memory(self):
        """
            1.出入库管理的副agent记忆模块
            2.为了防止共享记忆而导致记忆混乱，从而造成无法准确理解上下文，对不同的agent进行处理
            3.id唯一标识一个用户，则对唯一的一个id后面添加独有的字符串，可以实现一个用户三个不同记忆池的功能
        """

        chat_message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0", session_id=self.user_id + "_agent_a",
        )
        print("历史记录为：", chat_message_history.messages)

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

            chain = prompt | llm
            summary = chain.invoke({"input":store_message})

            #将超出限制的记忆清除
            chat_message_history.clear()

            #将清除的记忆总结之后再添加进来，避免模型无法根据上下文回答问题
            chat_message_history.add_message(summary)
            print("总结精炼后的记忆：", chat_message_history.messages)

        return chat_message_history

    def run(self, query:str):

        result = self.db_agent_executor.invoke({"input":query})

        return result
