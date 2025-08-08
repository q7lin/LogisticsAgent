from agents.my_report_agent import report_agent
from agents.my_db_agent import db_agent
from datetime import datetime, date, timedelta

def monitor_medicine_inventory(user_id:str, name:str):
    """
    药品库存监控:查询药品库存->筛选低于阈值的药品->插入操作记录->表格
    """
    """业务升级：对年月也要进行处理加减"""

    # 对使用的变量进行初始化
    msg = None

    # 对user_id进行处理
    db_agent_user_id = user_id + "db_agent"
    report_agent_user_id = user_id + "report_agent"

    # 实例化副agent
    my_db = db_agent(db_agent_user_id)
    my_report = report_agent(report_agent_user_id)

    # 业务逻辑
    select_result = my_db.run("在medicines数据库的medicine表中查询"+name+"这个药品的库存和到期日期")

    target_date = datetime.strptime(select_result["data"]["data"], "%Y-%m-%d").date() #将查询的日期进行转换
    current_date = date.today() #获取当前日期
    delta_days = (current_date - target_date).days

    if delta_days < 30 or select_result["data"]["count"] < 50:
        if delta_days < 30:
            msg = "药品过期的数量过多，请尽快补货"
        else:
            msg = "药品库存过少，请尽快补货"

    if select_result is not None:
        my_db.run("将刚刚进行的sql操作的中文插入logs数据库的log表中")


    data = select_result
    table_result = my_report.run("生成一个表格，并将这些数据放入表格中，表格名字叫：" + name + "药品需要补货", data)

    return {msg, table_result}