import uvicorn
from fastapi import FastAPI
from agents.my_db_agent import *

app = FastAPI(redirect_slashes=False)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query:str, user_id:str):
    uid = user_id

    mydb = db_agent(uid)

    result = mydb.run(query)

    return result

@app.post("/add_urls")
def add_urls(url:str):
    return url

@app.post("add_pdfs")
def add_pdfs():
    return {"response":"pdf added"}

@app.post("/add_texts")
def add_texts():
    return {"response":"text added"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

