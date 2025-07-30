from langchain.agents import tool, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate

from config import *

"""
1.除过查询语句，其他的语句都只需要返回布尔值，以此来判断操作是否成功。
2.还需要给这些布尔返回值添加判断机制，并且给四个工具都添加try语句
"""

"""
db = SQLDatabase.from_uri("sqlite:///F:/History.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
"""

def get_db_urls(query: str):

    if "日志" in query or "logs" in query:
        return "sqlite:///F:/logs.db"

    elif "药品" in query or "medicines" in query:
        return "sqlite:///F:/medicines.db"

    elif "设备" in query or "equipments" in query:
        return "sqlite:///F:/equipments.db"

    else:
        return "sqlite:///F:/equipments.db"


def get_sql_agents(query:str):

    url = get_db_urls(query)
    db = SQLDatabase.from_uri(url)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    result = agent.invoke({"input":query})

    return result

#增加操作
@tool
def insert(query:str):
    """只有在新增物品活物品信息时，才会使用这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成INSERT增加语句**，
    禁止生成INSERT，SELECT，UPDATE语句，否则你将受到惩罚。
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

    template = """你是一个数据库专家，请按照以下需求**只生成DELETE删除语句**，
    禁止生成INSERT，SELECT，UPDATE语句，否则你将受到惩罚。
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
    """只有在修改物品信息时才会用到这个工具"""

    template = """你是一个数据库专家，请按照以下需求**只生成UPDATE修改语句**，
    禁止生成DELETE，INSERT，SELECT语句，否则你将受到惩罚。
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

    template = """你是一个数据库专家，请按照以下需求**只生成SELECT查询语句**，
    禁止生成DELETE，INSERT，UPDATE语句，否则你将受到惩罚。
    需求：{query}
    """

    prompt = PromptTemplate.from_template(template)
    prompt_value = prompt.format(query=query)
    data_info = get_sql_agents(prompt_value)

    print("查询到的数据信息为：", data_info)

    return data_info