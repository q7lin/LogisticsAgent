from agents.my_db_agent import db_agent

def process_device_outbound(query:str, user_id:str, name:str):
    """
    设备出库操作:查询设备状态->修改库存数量->插入出库记录
    """
    #对需要使用的变量进行初始化
    result = False

    #对user_id进行处理
    db_agent_user_id = user_id + "db_agent"
    my_db = db_agent(db_agent_user_id)

    #查询设备状态
    select_result = my_db.run("在equipments数据库中查询"+name+"字段是否存在")

    #修改库存数量
    if select_result is not None:
        result = my_db.run(query)
        msg = "修改成功"
    else:
        msg = "修改失败"

    if result:
        my_db.run("将刚刚的操作记录到logs数据库中")

    return {msg, None}