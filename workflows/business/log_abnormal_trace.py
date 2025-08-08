from agents.my_report_agent import report_agent
from agents.my_db_agent import db_agent

def trace_abnormal_operations(query:str, user_id:str):
    """
    异常操作追踪:查询失败操作->表格汇总
    """
    # 对需要使用的变量进行初始化
    msg = None
    table_result = None

    # 对user_id进行处理
    db_agent_user_id = user_id + "db_agent"
    report_agent_user_id = user_id + "report_agent"

    # 实例化副agent
    my_db = db_agent(db_agent_user_id)
    my_report = report_agent(report_agent_user_id)

    # 业务逻辑
    select_result = my_db.run(query)

    if select_result is not None:
        data = select_result
        table_result = my_report.run("生成一个表格，将数据放在表格中", data)

    return {msg, table_result}