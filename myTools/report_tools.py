from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
from langchain.agents import tool


@tool
def generate_chart(data:List[Dict]):
    """当用户想要分析数据并且得到图示时调用这个工具"""
    df = pd.DataFrame(data)

    result = df.groupby("物品")["入库数量"].sum().reset_index()
    save_path = "static/物品入库统计.xlsx"

    result.to_excel(save_path, index=False)

    return f'/static/物品入库统计.xlsx'

@tool
def generate_table(data:List[Dict]):
    """当用户想要分析数据并且得到表格时调用这个工具"""
    df = pd.DataFrame(data)

    df["日期"] = pd.to_datetime(df["日期"])
    df = df.groupby("日期")["入库数量"].sum()

    plt.figure(figsize(8, 4))
    df.plot(kind='line', marker='o')
    plt.title("每日入库量")
    plt.xlabel("日期")
    plt.ylabel("数量")
    plt.grid(True)

    path = "/static/入库走势图.png"
    plt.tight_layout()
    plt.savefig(path)

    return f"/static/入库走势图.png"