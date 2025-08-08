import os

YUANFENJU_API_KEY = "Jo9ygM2IEHdThGEqqTLdmqdO4"

os.environ['OPENAI_API_KEY'] = "sk-bCI5yo6f9TadMj4RRQXBLSGIfqJBuIb2J1BxPHfEUEcmiv9z"
os.environ['OPENAI_API_PROXY'] = "https://sg.uiuiapi.com/v1"

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_PROXY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0,
    model="gpt-3.5-turbo"
)

from langchain_community.chat_message_histories import RedisChatMessageHistory