from agents.my_db_agent import db_agent

def handle_medicine_outbound(query:str, user_id:str, name:str, count:str):
    """
    药品出库管理:查询药品库存->修改库存数量->插入出库日志
    """
    # 对需要使用的变量进行初始化
    update_result = False

    # 对user_id进行处理
    db_agent_user_id = user_id + "db_agent"
    my_db = db_agent(db_agent_user_id)

    # 查询设备状态
    select_result = my_db.run("在medicines数据库的medicine表中查询" + name + "字段是否存在")

    # 修改库存数量
    if select_result is not None:
        my_db.run("将"+name+"这个药品的数量减少"+count+"个。")
        msg = "修改成功"
    else:
        msg = "修改失败"

    return {
        "sql_result" : msg,
        "report_result" : None
    }