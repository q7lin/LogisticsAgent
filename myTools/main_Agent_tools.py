from langchain.agents import tool
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from utils.config import *


@tool
def get_info_from_local(query:str):
    """只有用户想要知道设备信息和功能以及药品的信息和功能时才会使用这个工具"""
    client = Qdrant(
        QdrantClient(path="E:/LogisticsAgent/local-qdrant"),
        "local-documents",
        OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=api_base,
        ),
    )
    retriever = client.as_retriever(
        search_type="mmr"
    )

    result = retriever.get_relevant_documents(query)
    return result