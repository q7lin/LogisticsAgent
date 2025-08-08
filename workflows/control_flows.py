from itertools import count

from workflows.config_workflows import *

class control_flow:
    def __init__(self, name:str, business:str, user_id:str, query:str, count:str):
        self.name = name                #设备或药品名称
        self.business = business        #第一个业务的名称
        self.user_id = user_id          #用户唯一标识
        self.query = query              #用户输入的自然语言
        self.count = count              #操作对象的数量

    def logic_judgement(self):
        """
        1.业务层整体的执行逻辑，入口
        2.主Agent根据输入判断业务数量和逻辑并传入到该类中
        3.通过业务个数来决定执行哪个业务
        """

        if self.business == "查询设备库存状态":
            messages = register_device_inbound(user_id=self.user_id, query=self.query, name=self.name)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用register_device_inbound函数")
            return messages


        if self.business == "查询设备状态":
            messages = process_device_outbound(user_id=self.user_id, query=self.query, name=self.name)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用process_device_outbound函数")
            return messages


        if self.business == "查询设备库存":
            messages = inventory_check_devices(user_id=self.user_id, name=self.name)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用inventory_check_devices函数")
            return messages


        if self.business == "查询操作日志":
            messages = trace_abnormal_operations(query=self.query, user_id=self.user_id)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用trace_abnormal_operations函数")
            return messages

        if self.business == "查询药品库存状态":
            messages = manage_medicine_inbound(user_id=self.user_id, query=self.query, name=self.name, count=self.count)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用manage_medicine_inbound函数")
            return messages


        if self.business == "查询药品状态":
            messages = handle_medicine_outbound(user_id=self.user_id, query=self.query, name=self.name, count=self.count)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用handle_medicine_outbound函数")
            return messages


        if self.business == "查询药品库存":
            messages = monitor_medicine_inventory(user_id=self.user_id, name=self.name)
            print("调用的结果为：", messages)
            print("结果的类型为：", type(messages))
            print("调用monitor_medicine_inventory函数")
            return messages