from agents.my_db_agent import db_agent
from agents.my_report_agent import report_agent

def register_device_inbound(query:str, user_id:str):
    """
    设备入库登记:插入设备数据->查询校验->写入入库日志->表格导出
    """

    #根据用户输入完成第一步操作
    my_db = db_agent(user_id)
    my_report = report_agent(user_id)
    result = my_db.run(query)

    #根据第一步操作完成第二步操作
    result_flag = False

    if type(result) != dict:
        result_flag = my_db.run(result)

    if result_flag:
        my_db.run("将前两条记录插入logs数据库")
        msg = "入库成功"
    else:
        msg =  "入库失败"

    #完成第四步操作
    result_report = None

    if result_flag:
        data = my_db.run("查询入库前的该物品信息和入库物品信息并进行对比然后将整条数据返回")

        result_report = my_report.run({"input": "将此数据进行分析并生成图示", "data": data})

    return {msg, result_report}