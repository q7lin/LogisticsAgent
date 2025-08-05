import re
import ast
from typing import Any


def transfer(text:Any):

    pattern = r"(\[.*?\])"  # 非贪婪匹配，防止跨多段匹配错误
    match = re.search(pattern, text, re.S)
    list_str = None

    if match:
        list_str = match.group(1)

    lst = ast.literal_eval(list_str)
    print("提取并转换后的数据：", lst)
    print("转换后的数据类型为：", type(lst))

    return lst