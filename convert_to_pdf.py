from fpdf import FPDF
import os


class ChinesePDF(FPDF):
    """支持中文的PDF类"""

    def __init__(self):
        super().__init__()
        # 添加中文字体
        font_path = 'C:/Windows/Fonts/simhei.ttf'
        if os.path.exists(font_path):
            self.add_font('SimHei', '', font_path)
            self.add_font('SimHei', 'B', font_path)
            self.set_font('SimHei', '', 12)
        else:
            print("警告：未找到中文字体，将使用默认字体")

    def header(self):
        self.set_font('SimHei', 'B', 10)
        self.cell(0, 10, '智能销售数据分析系统 - 技术报告', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('SimHei', '', 8)
        self.cell(0, 10, f'第 {self.page_no()} 页', align='C')

    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('SimHei', 'B', 16)
            self.ln(10)
        elif level == 2:
            self.set_font('SimHei', 'B', 14)
            self.ln(5)
        else:
            self.set_font('SimHei', 'B', 12)
            self.ln(3)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(2)

    def body_text(self, text):
        self.set_font('SimHei', '', 11)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def bullet_point(self, text):
        self.set_font('SimHei', '', 11)
        self.cell(10, 7, '- ')
        self.multi_cell(0, 7, text)
        self.ln(1)

    def table_row(self, cells, is_header=False):
        if is_header:
            self.set_font('SimHei', 'B', 10)
            self.set_fill_color(200, 200, 200)
        else:
            self.set_font('SimHei', '', 10)

        col_width = 180 / len(cells)
        for cell in cells:
            self.cell(col_width, 8, str(cell), border=1, align='C', fill=is_header)
        self.ln()


def generate_pdf():
    """生成PDF技术报告"""
    pdf = ChinesePDF()
    pdf.add_page()

    # 封面
    pdf.set_font('SimHei', 'B', 24)
    pdf.ln(40)
    pdf.cell(0, 15, '智能销售数据分析系统', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.set_font('SimHei', '', 16)
    pdf.cell(0, 10, '技术报告', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(30)
    pdf.set_font('SimHei', '', 12)
    pdf.cell(0, 8, '基于大语言模型的智能问答与数据可视化平台', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(20)
    pdf.cell(0, 8, '小组成员：程曦', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    pdf.cell(0, 8, '日期：2026年6月', new_x="LMARGIN", new_y="NEXT", align='C')

    # 第1章：项目概述
    pdf.add_page()
    pdf.chapter_title('1. 项目概述', 1)

    pdf.chapter_title('1.1 项目背景', 2)
    pdf.body_text('随着大数据时代的到来，企业对数据分析的需求日益增长。传统的数据分析方式需要专业的技术人员编写复杂的SQL查询和代码，对普通用户不够友好。本项目旨在开发一个基于大语言模型的智能数据分析系统，让用户能够通过自然语言与数据进行交互，降低数据分析的门槛。')

    pdf.chapter_title('1.2 项目目标', 2)
    pdf.bullet_point('实现一个完整的智能销售数据分析系统')
    pdf.bullet_point('提供自然语言问答、数据可视化、SQL查询等功能')
    pdf.bullet_point('使用大语言模型实现智能交互')
    pdf.bullet_point('构建用户友好的Web界面')

    pdf.chapter_title('1.3 技术选型', 2)
    pdf.table_row(['技术', '选型', '理由'], True)
    pdf.table_row(['后端框架', 'Flask', '轻量级、易于扩展'])
    pdf.table_row(['前端', 'Vue.js 3', '组件化、响应式'])
    pdf.table_row(['数据库', 'SQLite', '轻量级、无需配置'])
    pdf.table_row(['LLM', 'OpenAI API', '功能强大、兼容性好'])
    pdf.table_row(['可视化', 'Matplotlib+Plotly', '静态+交互式图表'])
    pdf.table_row(['数据处理', 'Pandas', '功能丰富、性能优秀'])

    # 第2章：系统架构
    pdf.add_page()
    pdf.chapter_title('2. 系统架构', 1)

    pdf.chapter_title('2.1 整体架构', 2)
    pdf.body_text('系统采用前后端分离架构，前端使用Vue.js 3框架，后端使用Python Flask框架。前后端通过RESTful API进行通信，后端负责数据处理、LLM调用和图表生成，前端负责用户界面展示和交互。')

    pdf.chapter_title('2.2 模块说明', 2)

    pdf.chapter_title('2.2.1 数据预处理模块', 3)
    pdf.body_text('功能：加载Excel数据文件、数据清洗和格式化、基础统计分析、SQL查询执行。关键方法包括load_data()、get_data_summary()、get_basic_statistics()、execute_sql_query()等。')

    pdf.chapter_title('2.2.2 LLM服务模块', 3)
    pdf.body_text('功能：集成OpenAI API、智能问答、自然语言理解、对话历史管理。关键方法包括chat()、generate_sql_query()、analyze_data_question()、clear_history()等。')

    pdf.chapter_title('2.2.3 可视化模块', 3)
    pdf.body_text('功能：生成柱状图、折线图、饼图，支持Matplotlib和Plotly，图表保存和管理。关键方法包括create_bar_chart()、create_line_chart()、create_pie_chart()等。')

    pdf.chapter_title('2.2.4 SQL生成器模块', 3)
    pdf.body_text('功能：自然语言转SQL、SQL查询执行、查询建议生成。关键方法包括natural_language_to_sql()、execute_query()、get_query_suggestions()等。')

    # 第3章：核心功能实现
    pdf.add_page()
    pdf.chapter_title('3. 核心功能实现', 1)

    pdf.chapter_title('3.1 智能问答', 2)
    pdf.body_text('实现原理：')
    pdf.bullet_point('用户输入自然语言问题')
    pdf.bullet_point('系统构建包含数据上下文的提示词')
    pdf.bullet_point('调用LLM API获取回答')
    pdf.bullet_point('返回结果并更新对话历史')

    pdf.chapter_title('3.2 数据可视化', 2)
    pdf.body_text('支持三种图表类型：柱状图展示类别对比、折线图展示趋势变化、饼图展示占比分布。前端发送图表类型和参数，后端准备数据并生成图表，保存图表文件并返回路径。')

    pdf.chapter_title('3.3 自然语言查询', 2)
    pdf.body_text('用户输入自然语言查询，LLM将查询转换为SQL语句，执行SQL查询并返回结果。例如输入"查询所有电子产品的销售总额"，系统生成SQL：SELECT SUM(销售总额) FROM sales WHERE 产品类别 = "电子产品"。')

    pdf.chapter_title('3.4 数据概览', 2)
    pdf.body_text('展示关键指标：总销售额、订单数量、总利润、平均订单金额。数据从后端API获取，实时更新显示。')

    # 第4章：数据说明
    pdf.add_page()
    pdf.chapter_title('4. 数据说明', 1)

    pdf.chapter_title('4.1 数据来源', 2)
    pdf.body_text('系统使用sales.xlsx作为示例数据，包含500条销售记录。')

    pdf.chapter_title('4.2 数据字段', 2)
    pdf.table_row(['字段名', '数据类型', '说明'], True)
    pdf.table_row(['订单ID', '字符串', '唯一标识'])
    pdf.table_row(['日期', '日期', '订单日期'])
    pdf.table_row(['产品类别', '字符串', '电子产品/服装等'])
    pdf.table_row(['产品名称', '字符串', '具体产品名称'])
    pdf.table_row(['销售数量', '整数', '购买数量'])
    pdf.table_row(['单价', '浮点数', '产品单价'])
    pdf.table_row(['销售总额', '浮点数', '数量乘单价'])
    pdf.table_row(['利润', '浮点数', '销售利润'])
    pdf.table_row(['地区', '字符串', '销售地区'])
    pdf.table_row(['销售渠道', '字符串', '线上/线下/批发'])
    pdf.table_row(['客户ID', '字符串', '客户标识'])

    pdf.chapter_title('4.3 数据统计', 2)
    pdf.bullet_point('总记录数：500条')
    pdf.bullet_point('时间范围：2024年全年')
    pdf.bullet_point('产品类别：5类')
    pdf.bullet_point('地区：7个')

    # 第5章：系统测试
    pdf.add_page()
    pdf.chapter_title('5. 系统测试', 1)

    pdf.chapter_title('5.1 测试环境', 2)
    pdf.bullet_point('操作系统：Windows 11')
    pdf.bullet_point('Python版本：3.11.9')
    pdf.bullet_point('浏览器：Chrome')

    pdf.chapter_title('5.2 测试结果', 2)
    pdf.table_row(['测试项', '结果', '说明'], True)
    pdf.table_row(['数据加载', '通过', '成功加载500条记录'])
    pdf.table_row(['LLM服务', '通过', '成功初始化并响应'])
    pdf.table_row(['可视化', '通过', '成功生成图表'])
    pdf.table_row(['SQL生成', '通过', '成功执行查询'])
    pdf.table_row(['Web服务', '通过', '成功启动并访问'])

    pdf.chapter_title('5.3 性能测试', 2)
    pdf.bullet_point('数据加载时间：< 1秒')
    pdf.bullet_point('图表生成时间：< 2秒')
    pdf.bullet_point('LLM响应时间：2-5秒（取决于网络）')

    # 第6章：创新点
    pdf.add_page()
    pdf.chapter_title('6. 创新点与不足', 1)

    pdf.chapter_title('6.1 创新点', 2)
    pdf.bullet_point('自然语言交互：用户无需学习SQL或编程，通过自然语言即可查询数据')
    pdf.bullet_point('智能问答：基于大语言模型的问答系统，能够理解复杂问题并给出专业回答')
    pdf.bullet_point('多维度可视化：支持多种图表类型，满足不同分析需求')
    pdf.bullet_point('实时查询：自然语言实时转换为SQL，即时返回查询结果')

    pdf.chapter_title('6.2 不足与改进', 2)
    pdf.body_text('当前不足：')
    pdf.bullet_point('LLM响应速度受网络影响')
    pdf.bullet_point('图表类型有限')
    pdf.bullet_point('缺少数据导出功能')
    pdf.bullet_point('缺少用户认证')

    pdf.body_text('改进方向：')
    pdf.bullet_point('添加更多图表类型')
    pdf.bullet_point('实现数据导出功能')
    pdf.bullet_point('优化LLM响应速度')
    pdf.bullet_point('添加用户认证和权限管理')

    # 第7章：总结
    pdf.add_page()
    pdf.chapter_title('7. 总结', 1)
    pdf.body_text('本项目成功实现了一个基于大语言模型的智能销售数据分析系统，具有以下特点：')
    pdf.bullet_point('功能完整：涵盖数据加载、分析、可视化、查询等完整流程')
    pdf.bullet_point('技术先进：集成大语言模型，实现智能交互')
    pdf.bullet_point('用户友好：提供直观的Web界面，降低使用门槛')
    pdf.bullet_point('扩展性强：模块化设计，便于功能扩展')
    pdf.body_text('系统达到了预期目标，为数据分析提供了一种新的交互方式。')

    # 保存PDF
    output_path = 'D:/python_code/transformer/sales_analyzer/技术报告.pdf'
    pdf.output(output_path)
    print(f"PDF已生成：{output_path}")
    return output_path


if __name__ == '__main__':
    generate_pdf()