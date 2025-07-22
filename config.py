import os

YUANFENJU_API_KEY = "Jo9ygM2IEHdThGEqqTLdmqdO4"

os.environ['OPENAI_API_KEY'] = "sk-bCI5yo6f9TadMj4RRQXBLSGIfqJBuIb2J1BxPHfEUEcmiv9z"
os.environ['OPENAI_API_PROXY'] = "https://sg.uiuiapi.com/v1"
os.environ["SERPAPI_API_KEY"] = "068b64425c91c585949dea83790462e3f1477a4e4a969b14525fe10d2157c775"
os.environ["ELEVEN_API_KEY"] = "sk_a376bdd617c72aff2ee320a9c911fda7d31ef5dd863d5c4a"

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_PROXY")
serpapi_key = os.getenv("SERPAPI_API_KEY")
elevenlabs_key = os.getenv("ELEVEN_API_KEY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base=api_base,
    temperature=0,
    model="gpt-3.5-turbo"
)