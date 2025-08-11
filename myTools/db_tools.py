from distutils.util import execute

from langchain.agents import tool, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate

from utils.config import *


def extract_dosage(query, dosage_mapping=None):
    """
    从药品名称字符串中提取剂型关键词（如"胶囊"、"片剂"等）
    参数:
        query (str): 输入的药品名称字符串（如"阿莫西林胶囊"）
        dosage_mapping (list, optional): 剂型关键词映射表，默认包含常见剂型

    返回:
        str: 提取到的剂型关键词，若未匹配到则返回None
    """
    # 默认剂型关键词映射表（按长度从长到短排序，避免短词优先匹配）
    default_mapping = [
        "注射液", "混悬剂", "口服液", "气雾剂", "灌肠剂", "口崩片",
        "胶囊", "片剂", "颗粒", "散剂", "丸剂", "糖浆", "软膏",
        "乳膏", "贴剂", "滴剂", "膏剂", "丹剂", "酒剂", "露剂",
        "设备", "装备", "仪器", "仪", "日志",
    ]

    # 预处理：去除字符串中的空格和特殊符号
    processed_query = query.replace(" ", "").strip()

    # 按关键词长度从长到短排序，确保长关键词优先匹配
    sorted_mapping = sorted(default_mapping, key=lambda x: len(x), reverse=True)

    matches = []
    for dosage in sorted_mapping:
        if processed_query.endswith(dosage) or dosage in processed_query:
            matches.append(dosage)
    return matches if matches else None

def get_db_urls(query: str):

    result = extract_dosage(query)
    print("从用户输入获取到的关键词为：", result)

    if result == "日志" or (isinstance(result, list) and "日志" in result):
        return "mysql+pymysql://root:123456@localhost:3306/logs"

    elif result in ["设备", "装备", "仪器", "仪"] or (
    isinstance(result, list) and any(x in ["设备", "装备", "仪器", "仪"] for x in result)):
        return "mysql+pymysql://root:123456@localhost:3306/equipments"

    else:
        return "mysql+pymysql://root:123456@localhost:3306/medicines"


def get_sql_agents(query:str):
    url = get_db_urls(query)
    print("使用的数据库为:", url)
    db = SQLDatabase.from_uri(url)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )

    result = agent.invoke({"input":query})

    return result

#增加操作
@tool
def insert(query:str):
    """只有在插入物品时，才会使用这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成INSERT增加语句并执行**，
    禁止生成和执行DELETE，SELECT，UPDATE语句，否则你将受到惩罚。
    需求：{query}
    """

    prompt = PromptTemplate.from_template(template)
    prompt_value = prompt.format(query=query)
    result = get_sql_agents(prompt_value)

    print(result)

    return True

#删除操作
@tool
def delete(query:str):
    """只有在删除物品信息或者删除物品时才会用到这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成DELETE删除语句并执行**，
    禁止生成和执行INSERT，SELECT，UPDATE语句，否则你将受到惩罚。
    需求：{query}
    """

    prompt = PromptTemplate.from_template(template)
    prompt_value = prompt.format(query=query)
    result = get_sql_agents(prompt_value)

    print(result)

    return True

#修改操作，修改操作是在数据库上直接进行修改，因此不需要返回值，只需要知道是否修改成功
@tool
def update(query:str):
    """只有在修改或者更新物品信息时才会用到这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成UPDATE修改语句并执行**，
    禁止生成和执行DELETE，INSERT，SELECT语句，否则你将受到惩罚。
    需求：{query}
    """

    prompt = PromptTemplate.from_template(template)
    prompt_value = prompt.format(query=query)
    result = get_sql_agents(prompt_value)

    print(result)

    return True

#查询操作
@tool
def select(query:str):
    """只有在查询物品信息时才会用到这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成SELECT查询语句并执行**，
    禁止生成和执行DELETE，INSERT，UPDATE语句，否则你将受到惩罚。
    需求：{query}
    """

    prompt = PromptTemplate.from_template(template)
    prompt_value = prompt.format(query=query)
    data_info = get_sql_agents(prompt_value)

    print("查询到的数据信息为：", data_info)
    print("查询到的数据类型为：", type(data_info))

    return data_info