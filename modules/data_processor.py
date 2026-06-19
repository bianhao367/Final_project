import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import sqlite3
from io import StringIO


class DataProcessor:
    """数据预处理与分析模块"""

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.db_connection = None

    def load_data(self) -> pd.DataFrame:
        """加载Excel数据文件"""
        try:
            self.df = pd.read_excel(self.data_path, engine='openpyxl')
            # 转换日期列
            if '日期' in self.df.columns:
                self.df['日期'] = pd.to_datetime(self.df['日期'])
            return self.df
        except Exception as e:
            raise Exception(f"数据加载失败: {str(e)}")

    def get_data_summary(self) -> Dict[str, Any]:
        """获取数据摘要信息"""
        if self.df is None:
            self.load_data()

        # 转换数据类型为字符串
        dtypes = {col: str(dtype) for col, dtype in self.df.dtypes.items()}

        summary = {
            "总记录数": len(self.df),
            "列数": len(self.df.columns),
            "列名": list(self.df.columns),
            "数据类型": dtypes,
            "缺失值": self.df.isnull().sum().to_dict(),
            "数值列统计": self.df.describe().to_dict()
        }
        return summary

    def get_basic_statistics(self) -> Dict[str, Any]:
        """获取基础统计信息"""
        if self.df is None:
            self.load_data()

        stats = {
            "总销售额": float(self.df['销售总额'].sum()),
            "平均订单金额": float(self.df['销售总额'].mean()),
            "最大订单金额": float(self.df['销售总额'].max()),
            "最小订单金额": float(self.df['销售总额'].min()),
            "总利润": float(self.df['利润'].sum()),
            "平均利润率": float((self.df['利润'] / self.df['销售总额']).mean()),
            "订单数量": len(self.df),
            "客户数量": self.df['客户ID'].nunique()
        }
        return stats

    def get_category_analysis(self) -> Dict[str, Any]:
        """按产品类别分析"""
        if self.df is None:
            self.load_data()

        category_stats = self.df.groupby('产品类别').agg({
            '销售总额': ['sum', 'mean', 'count'],
            '利润': 'sum',
            '销售数量': 'sum'
        }).round(2)

        # 转换为简单的字典结构
        result = {}
        for category in category_stats.index:
            result[category] = {
                '销售总额': float(category_stats.loc[category, ('销售总额', 'sum')]),
                '平均销售额': float(category_stats.loc[category, ('销售总额', 'mean')]),
                '订单数量': int(category_stats.loc[category, ('销售总额', 'count')]),
                '利润': float(category_stats.loc[category, '利润']),
                '销售数量': int(category_stats.loc[category, '销售数量'])
            }

        return result

    def get_region_analysis(self) -> Dict[str, Any]:
        """按地区分析"""
        if self.df is None:
            self.load_data()

        region_stats = self.df.groupby('地区').agg({
            '销售总额': ['sum', 'mean', 'count'],
            '利润': 'sum'
        }).round(2)

        # 转换为简单的字典结构
        result = {}
        for region in region_stats.index:
            result[region] = {
                '销售总额': float(region_stats.loc[region, ('销售总额', 'sum')]),
                '平均销售额': float(region_stats.loc[region, ('销售总额', 'mean')]),
                '订单数量': int(region_stats.loc[region, ('销售总额', 'count')]),
                '利润': float(region_stats.loc[region, '利润'])
            }

        return result

    def get_time_series_data(self, freq: str = 'M') -> pd.DataFrame:
        """获取时间序列数据"""
        if self.df is None:
            self.load_data()

        # 设置日期为索引
        df_time = self.df.set_index('日期')

        # 按频率重采样
        time_series = df_time.resample(freq).agg({
            '销售总额': 'sum',
            '利润': 'sum',
            '订单ID': 'count'
        }).rename(columns={'订单ID': '订单数量'})

        return time_series

    def init_sqlite_db(self):
        """初始化SQLite数据库"""
        if self.df is None:
            self.load_data()

        self.db_connection = sqlite3.connect(':memory:')
        self.df.to_sql('sales', self.db_connection, index=False, if_exists='replace')

    def execute_sql_query(self, query: str) -> pd.DataFrame:
        """执行SQL查询"""
        if self.db_connection is None:
            self.init_sqlite_db()

        try:
            result = pd.read_sql_query(query, self.db_connection)
            return result
        except Exception as e:
            raise Exception(f"SQL查询执行失败: {str(e)}")

    def search_data(self, keyword: str) -> pd.DataFrame:
        """搜索数据"""
        if self.df is None:
            self.load_data()

        # 在所有文本列中搜索
        mask = pd.Series([False] * len(self.df))
        for col in self.df.select_dtypes(include=['object']).columns:
            mask |= self.df[col].astype(str).str.contains(keyword, case=False, na=False)

        return self.df[mask]

    def get_top_products(self, n: int = 10) -> pd.DataFrame:
        """获取销售额最高的产品"""
        if self.df is None:
            self.load_data()

        top_products = self.df.groupby('产品名称').agg({
            '销售总额': 'sum',
            '销售数量': 'sum',
            '利润': 'sum'
        }).sort_values('销售总额', ascending=False).head(n)

        return top_products

    def get_monthly_trend(self) -> pd.DataFrame:
        """获取月度趋势"""
        if self.df is None:
            self.load_data()

        self.df['月份'] = self.df['日期'].dt.to_period('M')
        monthly_trend = self.df.groupby('月份').agg({
            '销售总额': 'sum',
            '利润': 'sum',
            '订单ID': 'count'
        }).rename(columns={'订单ID': '订单数量'})

        return monthly_trend