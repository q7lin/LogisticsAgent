from agents.my_db_agent import db_agent

def process_device_outbound(query:str, user_id:str, name:str, num:str):
    """
    设备出库操作:查询设备状态->修改库存数量->插入出库记录
    """
    my_db = db_agent(user_id)

    #查询设备状态
    result_flag = my_db.run("查询"+name+"字段是否存在")
    result = False

    #修改库存数量
    if result_flag:
        result = my_db.run(query)
        msg = "修改成功"
    else:
        msg = "修改失败"

    if result:
        my_db.run("将刚刚的操作记录到logs数据库中")

    return msg