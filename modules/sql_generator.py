import pandas as pd
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from .llm_service import LLMService


class SQLGenerator:
    """自然语言转SQL查询模块"""

    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.llm_service = LLMService()
        self.table_schema = self._get_table_schema()

    def _get_table_schema(self) -> str:
        """获取表结构信息"""
        if self.data_processor.df is None:
            self.data_processor.load_data()

        schema = "表名: sales\n列信息:\n"
        for col in self.data_processor.df.columns:
            dtype = str(self.data_processor.df[col].dtype)
            schema += f"- {col} ({dtype})\n"

        return schema

    def natural_language_to_sql(self, query: str) -> str:
        """将自然语言查询转换为SQL"""
        try:
            sql_query = self.llm_service.generate_sql_query(query, self.table_schema)
            return sql_query
        except Exception as e:
            raise Exception(f"SQL生成失败: {str(e)}")

    def execute_query(self, natural_language_query: str) -> Tuple[pd.DataFrame, str]:
        """执行自然语言查询并返回结果"""
        # 生成SQL
        sql_query = self.natural_language_to_sql(natural_language_query)

        try:
            # 执行查询
            result = self.data_processor.execute_sql_query(sql_query)
            return result, sql_query
        except Exception as e:
            raise Exception(f"查询执行失败: {str(e)}")

    def validate_sql(self, sql_query: str) -> bool:
        """验证SQL查询的安全性"""
        # 禁止危险操作
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
        sql_upper = sql_query.upper()

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False

        return True

    def get_query_suggestions(self) -> List[str]:
        """获取查询建议"""
        suggestions = [
            "查询所有电子产品的销售总额",
            "按地区统计销售额排名",
            "查找销售额最高的前10个订单",
            "统计每个月的订单数量",
            "计算各产品类别的平均利润率",
            "查询华东地区的销售数据",
            "找出销售额超过10000的订单",
            "按销售渠道统计订单数量",
            "查询2024年第一季度的销售数据",
            "统计各地区的利润总额"
        ]
        return suggestions