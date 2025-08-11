import re

from agents.my_db_agent import db_agent
from agents.my_report_agent import report_agent


def register_device_inbound(query:str, user_id:str, name:str, count:str):
    """
    设备入库登记:查询设备库存状态->插入设备数据->查询校验->写入入库日志->表格导出
    """
    # 对需要使用的变量进行初始化
    img_result = False
    rear_count = 0
    front_count = 0

    # 对user_id进行处理，对记忆进行隔离
    db_agent_user_id = user_id + "db_agent"
    report_agent_user_id = user_id + "report_agent"

    # 对副agent进行实例化
    my_db = db_agent(db_agent_user_id)
    my_report = report_agent(report_agent_user_id)

    # 查询校验，看设备是否存在，查询返回的结果是数据
    select_result = my_db.run("查询equipments数据库的equips表中" + name + "这个设备的最新一条库存记录")

    text = select_result["output"]

    # 查询到的数据不为空，证明设备存在，直接完成插入即可；否则需要创建字段在插入
    if "库存数量" in text or "件" in text or "日期" in text:
        my_db.run("调用update工具，将" + name + "这个设备的数量再添加" + count + "个并且不需要再添加一次。")
        update_result = my_db.run("查询equipments数据库的equips表中" + name + "最新一条库存记录")
    else:
        my_db.run(query)
        update_result = my_db.run("查询equipments数据库的equips表中" + name + "这个设备的最新一条库存记录")

    # 判断数据库的入库数量
    front = select_result["output"]
    rear = update_result["output"]
    match1 = re.search(r"数量[:：]\s*(\d+)", rear)
    match2 = re.search(r"数量[:：]\s*(\d+)", front)
    if match1 and match2:
        rear_count = int(match1.group(1))
        front_count = int(match2.group(1))

    if rear_count > front_count:
        equipments_count = rear_count - front_count
    else:
        equipments_count = front_count - rear_count

    # 完成第四步操作
    if equipments_count > 0:
        my_db.run("将本次所有sql操作的中文名称插入logs数据库的log表中")
        table_result = my_db.run("查询equipments数据库的equips表中的所有数据")
        data = table_result["output"]
        img_result = my_report.run("将此数据进行分析并生成图示", data)

    return {
        "sql_result" : update_result,
        "report_result" : img_result
    }