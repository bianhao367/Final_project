import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMService:
    """大语言模型服务模块"""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('BASE_URL')
        self.model = os.getenv('model', 'ep-20260312161409-csvf6')

        if not self.api_key or not self.base_url:
            raise ValueError("请在.env文件中配置OPENAI_API_KEY和BASE_URL")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []

        # 系统提示词
        self.system_prompt = """你是一个智能数据分析助手，专门帮助用户分析销售数据。

你的能力包括：
1. 回答关于销售数据的问题
2. 解释数据趋势和模式
3. 提供数据洞察和建议
4. 帮助用户理解统计指标

当用户询问数据相关问题时，请基于提供的数据上下文给出准确、有帮助的回答。
如果需要执行SQL查询来获取数据，请说明你的分析思路。

请用中文回复，保持专业且易于理解。"""

    def _build_messages(self, user_message: str, data_context: Optional[str] = None) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = [{"role": "system", "content": self.system_prompt}]

        # 添加数据上下文
        if data_context:
            messages.append({
                "role": "system",
                "content": f"当前数据上下文：\n{data_context}"
            })

        # 添加历史对话
        messages.extend(self.conversation_history[-10:])  # 保留最近10轮对话

        # 添加用户消息
        messages.append({"role": "user", "content": user_message})

        return messages

    def chat(self, user_message: str, data_context: Optional[str] = None) -> str:
        """与LLM进行对话"""
        try:
            messages = self._build_messages(user_message, data_context)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )

            assistant_message = response.choices[0].message.content

            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            return f"抱歉，处理您的请求时出现错误: {str(e)}"

    def analyze_data_question(self, question: str, data_summary: str) -> str:
        """分析数据相关问题"""
        prompt = f"""基于以下数据摘要信息，回答用户的问题：

数据摘要：
{data_summary}

用户问题：{question}

请提供详细的分析和解答。"""

        return self.chat(prompt)

    def generate_sql_query(self, natural_language_query: str, table_schema: str) -> str:
        """将自然语言转换为SQL查询"""
        prompt = f"""请将以下自然语言查询转换为SQL语句。

表结构：
{table_schema}

自然语言查询：{natural_language_query}

请只返回SQL语句，不需要其他解释。"""

        response = self.chat(prompt)
        # 提取SQL语句
        sql_query = response.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        return sql_query.strip()

    def explain_visualization(self, chart_type: str, data_description: str) -> str:
        """解释可视化图表"""
        prompt = f"""请解释以下可视化图表的含义和洞察：

图表类型：{chart_type}
数据描述：{data_description}

请用简洁易懂的语言解释图表展示的主要信息和趋势。"""

        return self.chat(prompt)

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history