from agents.my_db_agent import db_agent
from agents.my_report_agent import report_agent

def inventory_check_devices(user_id:str, name:str):
    """
    设备库存盘点:查询设备库存->写入操作日志->表格导出
    """
    # 对需要使用的变量进行初始化
    table_result = None
    msg = None

    # 对user_id进行处理
    db_agent_user_id = user_id + "db_agent"
    report_agent_user_id = user_id + "report_agent"

    # 对副agent进行实例化
    my_db = db_agent(db_agent_user_id)
    my_report = report_agent(report_agent_user_id)

    # 业务逻辑
    select_result = my_db.run("在equipments数据库的equips表中查询"+name+"这个设备当前的所有记录")

    insert_result = None #对需要使用的变量进行初始化

    if select_result:
        insert_result = my_db.run("将刚刚的sql操作的中文写入logs数据库的log表中")

    if insert_result:
        data = select_result["output"]
        table_result = my_report.run("将数据做成表格", data)

    return {msg, table_result}
