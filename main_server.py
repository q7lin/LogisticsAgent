import uvicorn
from fastapi import FastAPI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from main_Agent import LogisticsAgent
from utils.config import *
from utils.transfer_Type import transfer
from workflows.control_flows import control_flow

app = FastAPI(redirect_slashes=False)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query:str, user_id:str):

    #从主agent获取信息，流程的入口
    my_agent = LogisticsAgent(user_id)
    result = my_agent.run(query)

    #将主agent的数据进行处理，方便副agent的使用
    text = result["output"]
    lst = transfer(text)

    #调用业务层完成实际业务
    control = control_flow(lst[-1], lst[0], user_id, query)
    final_result = control.logic_judgement()
    print("操作结果为：", final_result)
    
    return final_result


@app.post("/add_urls")
def add_urls(url:str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=50,
    )
    documents = documents.split_documents(docs)

    #引入向量数据库
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=api_base,
        ),
        path = "E:/LogisticsAgent/local-qdrant",
        collection_name="local_documents",
    )
    print("向量数据库创建完成")
    return {"ok": "添加成功！"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

