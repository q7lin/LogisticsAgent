from agents.my_db_agent import db_agent
from agents.my_report_agent import report_agent

def register_device_inbound(query:str, user_id:str, name:str):
    """
    设备入库登记:查询设备库存状态->插入设备数据->查询校验->写入入库日志->表格导出
    如果没有该设备则需要创建
    """
    #对需要使用的变量进行初始化
    res_flag = False
    img_result = False

    #对user_id进行处理，对记忆进行隔离
    db_agent_user_id = user_id + "db_agent"
    report_agent_user_id = user_id + "report_agent"

    #对副agent进行实例化
    my_db = db_agent(db_agent_user_id)
    my_report = report_agent(report_agent_user_id)

    #查询校验，看设备是否存在，查询返回的结果是数据
    select_result = my_db.run("查询equipments数据库中是否有"+name+"这个设备")

    #查询到的数据不为空，证明设备存在，直接完成插入即可；否则需要创建字段在插入
    if select_result is not None:
        insert_result = my_db.run(query)
    else:
        my_db.run("按equipments数据库中其他字段的规格创建"+name+"字段")
        insert_result = my_db.run(query)

    if insert_result:
        res_flag = my_db.run("查询equipments数据库中的"+name+"字段")

    equipments_count = select_result["data"]["count"] - res_flag["data"]["count"]

    #完成第四步操作
    if equipments_count > 0:
        my_db.run("将本次数据库所有操作插入logs数据库中")


    if res_flag:
        data = my_db.run("查询入库前的该物品信息和入库物品信息并进行对比然后将整条数据返回")

        img_result = my_report.run("将此数据进行分析并生成图示", data)

    return {res_flag, img_result}