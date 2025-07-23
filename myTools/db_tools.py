from langchain.agents import tool

from config import *

#增
@tool
def create(name:str, quantity:int):
    return None

#删
@tool
def delete(name:str, quantity:int):
    return None

#改
@tool
def update(name:str, quantity:int):
    return None

#查
@tool
def read(name:str):
    #返回字典，如果字典为空，则说明是新增的；否则就是添加。根据字典的空来判断，不然后续需要单独查询某一个物品信息返回来的是布尔值不好
    return None