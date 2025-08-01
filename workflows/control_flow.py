from workflows.business.device_inbound import register_device_inbound
from workflows.business.device_outbound import process_device_outbound


class control_flow:
    def __init__(self, count, name, business, user_id, query:str):
        self.count = count              #业务数量
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


        if self.count == 4 & self.business == "插入设备数据":
            messages = register_device_inbound(user_id=self.user_id, query=self.query)
            if messages:
                return messages
            else:
                return {"操作失败"}

        if self.count == 3 & self.business == "查询设备状态":
            messages = process_device_outbound(user_id=self.user_id, query=self.query, name=self.name)

            return messages

