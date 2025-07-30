from workflows.business.device_inbound import register_device_inbound


class control_flow:
    def __init__(self, flag):
        self.flag = flag

    def logic_judgement(self):
        """
        1.业务层整体的执行逻辑，入口
        2.主Agent根据输入判断业务数量和逻辑并传入到该类中
        3.通过业务个数来决定执行哪个业务
        """

        if self.flag == 1:
            is_true = register_device_inbound()
            if is_true:
                return "操作成功"
            else:
                return "操作失败"


        pass
