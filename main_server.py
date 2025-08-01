import ast
import re

import uvicorn
from fastapi import FastAPI
from main_Agent import LogisticsAgent

app = FastAPI(redirect_slashes=False)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query:str, user_id:str):
    uid = user_id

    my_agent = LogisticsAgent(uid)

    result = my_agent.run(query)

    text = result["output"]

    """
    text = result["output"]

    # 用正则匹配花括号包围的json部分
    pattern = r"(\[.*\])"  # 贪婪匹配，匹配第一个和最后一个花括号之间所有内容
    match = re.search(pattern, text, re.S)  # re.S 让.匹配换行符
    data = None

    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print("JSON解析失败:", e)
    else:
        print("没有找到有效的JSON数据")
        """

    pattern = r"(\[.*?\])"  # 非贪婪匹配，防止跨多段匹配错误
    match = re.search(pattern, text, re.S)
    list_str = None

    if match:
        list_str = match.group(1)


    lst = ast.literal_eval(list_str)
    print("提取并转换后的数据：", lst)
    print("转换后的数据类型为：", type(lst))

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

