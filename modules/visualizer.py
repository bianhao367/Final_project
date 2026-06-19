import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
from typing import Dict, List, Any, Optional
import json

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class Visualizer:
    """数据可视化模块"""

    def __init__(self, output_dir: str = 'static/charts'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_bar_chart(self, data: pd.DataFrame, x: str, y: str,
                         title: str, xlabel: str = '', ylabel: str = '') -> str:
        """创建柱状图"""
        fig, ax = plt.subplots(figsize=(10, 6))

        # 如果数据太多，只显示前15个
        if len(data) > 15:
            data = data.head(15)

        bars = ax.bar(range(len(data)), data[y].values, color=plt.cm.Set3(np.linspace(0, 1, len(data))))

        ax.set_xlabel(xlabel or x, fontsize=12)
        ax.set_ylabel(ylabel or y, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data[x].values, rotation=45, ha='right')

        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        # 保存图表
        filename = f'bar_chart_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def create_line_chart(self, data: pd.DataFrame, x: str, y: List[str],
                          title: str, xlabel: str = '', ylabel: str = '') -> str:
        """创建折线图"""
        fig, ax = plt.subplots(figsize=(12, 6))

        for col in y:
            ax.plot(data[x].values, data[col].values, marker='o', linewidth=2, label=col)

        ax.set_xlabel(xlabel or x, fontsize=12)
        ax.set_ylabel(ylabel or '数值', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = f'line_chart_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def create_pie_chart(self, data: pd.DataFrame, names: str, values: str,
                         title: str) -> str:
        """创建饼图"""
        fig, ax = plt.subplots(figsize=(10, 8))

        # 如果数据太多，只显示前8个
        if len(data) > 8:
            top_data = data.head(8)
            other_sum = data[values].iloc[8:].sum()
            other_row = pd.DataFrame({names: ['其他'], values: [other_sum]})
            data = pd.concat([top_data, other_row], ignore_index=True)

        colors = plt.cm.Set3(np.linspace(0, 1, len(data)))
        wedges, texts, autotexts = ax.pie(data[values].values, labels=data[names].values,
                                          autopct='%1.1f%%', colors=colors, startangle=90)

        ax.set_title(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        filename = f'pie_chart_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def create_plotly_bar(self, data: pd.DataFrame, x: str, y: str,
                          title: str) -> str:
        """使用Plotly创建交互式柱状图"""
        fig = px.bar(data, x=x, y=y, title=title,
                     color=y, color_continuous_scale='Viridis')

        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            font=dict(size=12)
        )

        filename = f'plotly_bar_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.html'
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)

        return filepath

    def create_plotly_line(self, data: pd.DataFrame, x: str, y: List[str],
                           title: str) -> str:
        """使用Plotly创建交互式折线图"""
        fig = go.Figure()

        for col in y:
            fig.add_trace(go.Scatter(x=data[x], y=data[col], mode='lines+markers', name=col))

        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title='数值',
            font=dict(size=12)
        )

        filename = f'plotly_line_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.html'
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)

        return filepath

    def create_plotly_pie(self, data: pd.DataFrame, names: str, values: str,
                          title: str) -> str:
        """使用Plotly创建交互式饼图"""
        fig = px.pie(data, names=names, values=values, title=title)

        fig.update_layout(font=dict(size=12))

        filename = f'plotly_pie_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.html'
        filepath = os.path.join(self.output_dir, filename)
        fig.write_html(filepath)

        return filepath

    def create_heatmap(self, data: pd.DataFrame, title: str) -> str:
        """创建热力图"""
        fig, ax = plt.subplots(figsize=(10, 8))

        im = ax.imshow(data.values, cmap='YlOrRd', aspect='auto')

        ax.set_xticks(range(len(data.columns)))
        ax.set_yticks(range(len(data.index)))
        ax.set_xticklabels(data.columns, rotation=45, ha='right')
        ax.set_yticklabels(data.index)

        # 添加数值标签
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                text = ax.text(j, i, f'{data.values[i, j]:,.0f}',
                               ha="center", va="center", color="black", fontsize=9)

        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.colorbar(im)

        plt.tight_layout()

        filename = f'heatmap_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.png'
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def get_chart_list(self) -> List[str]:
        """获取已生成的图表列表"""
        charts = []
        for file in os.listdir(self.output_dir):
            if file.endswith(('.png', '.html')):
                charts.append(os.path.join(self.output_dir, file))
        return charts