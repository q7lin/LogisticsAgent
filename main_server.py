import uvicorn
from fastapi import FastAPI

app = FastAPI(redirect_slashes=False)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query:str):
    return query

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

