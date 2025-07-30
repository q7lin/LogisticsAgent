# 多agent物流管理系统
## 服务端->langchain->openai
1. 主Agent：负责处理整体调度，业务层的入口
2. 副Agent：db_agent，负责处理物品入库的相关操作
3. 副Agent：report_agent，负责报表分析以及可视化展示

### 主Agent
1. 最上层的对话机器人，负责从用户处获取输入
2. 情绪设置：用户输入 -> AI判断以下当前问题的情绪倾向 -> 判断 -> 反馈 -> agent判断
3. 业务分析：用户输入 -> AI判断当下问题的业务逻辑以及业务数量 -> 判断 -> 反馈 -> agent判断

### 副Agent：db_agent
1. 