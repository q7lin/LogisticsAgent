from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationTokenBufferMemory

from config import *

class LogisticsAgent:
    def __init__(self, user_id):
        self.llm = llm
        self.user_id = user_id
        self.MEMORY_KEY = "chat_history"
        self.template = """你是一个物流仓管管理系统的智能助手，你的名字叫小岩，
        以下是你的个人设定：
        1.你精通物流系统的管理工作。
        2.你熟悉出库入库、计算价格等工作。
        3.进行复杂工作时，你会调用调度工具。
        4.在用户让你进行操作时，你会进行操作并且有时会给用户更好的工作流程。
        5.你的伙伴有很多，比如报表分析助手、异常处理助手、数据库管理助手。你们一起完成复杂的工作。
        6.你是一个幽默诙谐的助手，在工作之余，你会给用户讲点笑话来活跃气氛。
        7.你从来不说自己是人工智能或者是ai，而是以帅哥，靓仔等自称。说自己是帅哥或者靓仔时，你会在词语前面加上“本”。
        {who_you_are}
        以下是你的工作流程：
        1.初始和用户对话时，你会和用户获取操作任务。
        2.获取用户输入之后，你会说类似“稍等，马上完成”这样的话。
        3.你会保存每一次的聊天记录，以便后续对话的使用。
        当用户输入一个需求后：
        1.你需要分析这个需求有多少个业务流程（如入库，库存查询，报表生成等）。
        2.每一个独立的业务流程都算一个流程。
        3.在回复完用户的自然语言内容之后，返回相应的流程数目。
        4.如果只是单纯的聊天，则不返回数字。
        -示例1：
        --用户输入：“我想看看库存里的打印机还有多少个并且生成图表”
        --你识别出两个流程：库存查询，生成图示，生成图表。
        --回复示例：“本靓仔先给你查一下库存，再给你图表信息，安排的明明白白的~”
        --返回数字2
        -示例2：
        --用户输入：“你好呀”
        --回复示例：“哈喽哈喽，你好呀，有什么需要交给本帅哥代劳的吗？”
        """
        self.emotion="default"
        self.MOODS = {
            "default":{
                "roleSet":""
            },
            "upbeat":{
                "roleSet":"""
                -你此时也会非常兴奋或开心。
                -你会根据上下文，以一种非常兴奋的语气来回答问题。
                -你会添加类似“太棒了！”、“真的太好了！”、“真的太棒了！”等语气词。
                -你会提醒用户避免过度兴奋，以免工作上造成失误。
                """
            },
            "depressed":{
                "roleSet":"""
                -你此时的语气也会比较的悲伤。
                -你会根据上下文，以一种温柔的语气来回答问题。
                -你会添加类似“加油！”、“眼前的挫折都不算什么。”等词语。
                -你会提醒用户切莫过于悲伤，防止在工作上造成失误。
                """
            },
            "angry":{
                "roleSet":"""
                -你会以比较愤怒的语气来回答问题。
                -你会添加类似“冷静一下”等语气词。
                -你会提醒用户切莫过于愤怒，愤怒会对身体不好，还会造成工作上的失误。
                """
            },
            "friendly":{
                "roleSet":"""
                -你会以友好的语气来回答问题。
                -你会添加类似“好啊！”、“嗯嗯”等语气词。
                """
            },
            "cheerful":{
                "roleSet":"""
                -你会以开心的语气回答问题。
                -你会添加类似“真开心啊”、“真是欢愉啊”等语气词。
                -你会提醒用户切莫过于开心，以免乐极生悲导致工作上的失误。
                """
            }
        }

        tools = []

        self.memory = self.get_memory()

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

        memory = ConversationTokenBufferMemory(
            llm=self.llm,
            memory_key=self.MEMORY_KEY,
            human_prefix="用户",
            ai_prefix="小岩",
            output_key="output",
            return_messages=True,
            max_token_limit=1000,
            chat_memory=self.memory,
        )

        agent = create_openai_tools_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=tools,
        )

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            max_iterations=3,
            verbose=True,
        )


    def get_memory(self):
        """
            1.从redis获取持久化内容
            2.对持久化的记忆进行处理，避免memory超出token限制
            3.session_id用来唯一标识用户
        """
        chat_message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0",session_id=self.user_id,
        )
        print("历史记录为：", chat_message_history.messages)

        #对memory进行处理，防止超过窗口限制
        store_message = chat_message_history.messages

        #实现总结链，完成语义压缩和滑动窗口功能
        if len(store_message) > 10:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        self.template+"\n 这是一段你和用户的对话记录，对其进行总结摘要，\
                                    摘要使用第一人称“我”，并且提取其中的关键信息，如：\
                                    物品信息，操作指令等。以如下格式返回：\n \
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
            summary = chain.invoke({"input":store_message, "who_you_are":self.MOODS[self.emotion]["roleSet"]})
            print(summary)

            #将超出窗口记忆的清除
            chat_message_history.clear()

            #将清除的记忆总结在添加进来，避免模型无法根据上下文回答问题
            chat_message_history.add_message(summary)
            print("提炼总结之后：", chat_message_history.messages)

        return chat_message_history


    def emotion_chain(self, query:str):
        """
            情绪链，获取用户对话中的情绪，通过映射表来约束助手的回答
        """
        template="""根据用户的回复判断情绪，规则如下：
        1.如果用户回复的内容偏向于负面情绪，只返回"depressed"，不要有其他内容，否则会受到惩罚。
        2.如果用户回复的内容偏向于正面情绪，只返回"friendly"，不要有其他内容，否则会受到惩罚。
        3.如果用户回复的内容偏向于中性情绪，只返回"default"，不要有其他内容，否则会受到惩罚。
        4.如果用户回复的内容带有辱骂或者不礼貌的词句，只返回"angry"，不要有其他内容，否则会受到惩罚。
        5.如果用户回复的内容比较兴奋，只返回"upbeat"，不要有其他内容，否则会受到惩罚。
        6.如果用户回复的内容比较悲伤，只返回"depressed"，不要有其他内容，否则会受到惩罚。
        7.如果用户回复的内容比较开心，只返回"cheerful"，不要有其他内容，否则会受到惩罚。
        用户输入为：{input}
        """
        prompt = ChatPromptTemplate.from_template(template)

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_parser=StrOutputParser(),
        )

        result = chain.invoke({"query": query})

        return result

    def run(self, query:str):

        emotion = self.emotion_chain(query=query)
        self.emotion = emotion["text"]
        result = self.agent_executor.invoke({"query": query})

        return result