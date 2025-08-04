from config_workflows import *

class control_flow:
    def __init__(self, name, business, user_id, query:str):
        self.name = name                #设备或药品名称
        self.business = business        #第一个业务的名称
        self.user_id = user_id          #用户唯一标识
        self.query = query              #用户输入的自然语言

    def logic_judgement(self):
        """
        1.业务层整体的执行逻辑，入口
        2.主Agent根据输入判断业务数量和逻辑并传入到该类中
        3.通过业务个数来决定执行哪个业务
        """

        if self.business == "查询设备库存状态":
            messages = register_device_inbound(user_id=self.user_id, query=self.query, name=self.name)
            return messages

        if self.business == "查询设备状态":
            messages = process_device_outbound(user_id=self.user_id, query=self.query, name=self.name)
            return messages

        if self.business == "查询设备库存":
            messages = inventory_check_devices(user_id=self.user_id, name=self.name)
            return messages

        if self.business == "查询操作日志":
            messages = trace_abnormal_operations(query=self.query, user_id=self.user_id)
            return messages

        if self.business == "查询药品库存状态":
            messages = manage_medicine_inbound(user_id=self.user_id, query=self.query, name=self.name)
            return messages

        if self.business == "查询药品状态":
            messages = handle_medicine_outbound(user_id=self.user_id, query=self.query, name=self.name)
            return messages

        if self.business == "查询药品库存":
            messages = monitor_medicine_inventory(user_id=self.user_id, name=self.name)
            return messages


