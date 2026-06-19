import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_processor import DataProcessor
from modules.llm_service import LLMService
from modules.visualizer import Visualizer
from modules.sql_generator import SQLGenerator

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = 'data'
app.config['CHARTS_FOLDER'] = 'static/charts'

# 初始化模块
data_processor = None
llm_service = None
visualizer = None
sql_generator = None


def initialize_modules():
    """初始化所有模块"""
    global data_processor, llm_service, visualizer, sql_generator

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'sales.xlsx')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"数据文件不存在: {data_path}")

    data_processor = DataProcessor(data_path)
    data_processor.load_data()

    llm_service = LLMService()
    visualizer = Visualizer()
    sql_generator = SQLGenerator(data_processor)


@app.route('/')
def index():
    """主页 - 提供Vue.js前端"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    return send_from_directory(frontend_dir, 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """智能问答接口"""
    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return jsonify({'error': '请输入消息'}), 400

        # 获取数据上下文
        data_summary = data_processor.get_data_summary()
        context = f"数据概览：共{data_summary['总记录数']}条记录，{data_summary['列数']}列"

        # 调用LLM
        response = llm_service.chat(message, context)

        return jsonify({
            'response': response,
            'history': llm_service.get_history()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """获取数据摘要"""
    try:
        summary = data_processor.get_data_summary()
        stats = data_processor.get_basic_statistics()

        return jsonify({
            'summary': summary,
            'statistics': stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/category', methods=['GET'])
def get_category_analysis():
    """获取类别分析"""
    try:
        category_data = data_processor.get_category_analysis()
        return jsonify(category_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/region', methods=['GET'])
def get_region_analysis():
    """获取地区分析"""
    try:
        region_data = data_processor.get_region_analysis()
        return jsonify(region_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/top-products', methods=['GET'])
def get_top_products():
    """获取热门产品"""
    try:
        n = request.args.get('n', 10, type=int)
        top_products = data_processor.get_top_products(n)
        return jsonify(top_products.to_dict())

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/query', methods=['POST'])
def execute_query():
    """执行自然语言查询"""
    try:
        data = request.get_json()
        query = data.get('query', '')

        if not query:
            return jsonify({'error': '请输入查询'}), 400

        # 执行查询
        result, sql_query = sql_generator.execute_query(query)

        return jsonify({
            'sql': sql_query,
            'result': result.to_dict(orient='records'),
            'columns': list(result.columns)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/query/suggestions', methods=['GET'])
def get_query_suggestions():
    """获取查询建议"""
    try:
        suggestions = sql_generator.get_query_suggestions()
        return jsonify({'suggestions': suggestions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/bar', methods=['POST'])
def create_bar_chart():
    """创建柱状图"""
    try:
        data = request.get_json()
        x = data.get('x', '产品类别')
        y = data.get('y', '销售总额')
        title = data.get('title', '柱状图')

        # 准备数据
        if x == '产品类别':
            chart_data = data_processor.df.groupby('产品类别')[y].sum().reset_index()
        elif x == '地区':
            chart_data = data_processor.df.groupby('地区')[y].sum().reset_index()
        elif x == '销售渠道':
            chart_data = data_processor.df.groupby('销售渠道')[y].sum().reset_index()
        else:
            chart_data = data_processor.df.groupby(x)[y].sum().reset_index()

        # 创建图表
        filepath = visualizer.create_bar_chart(chart_data, x, y, title)

        return jsonify({
            'filepath': filepath,
            'data': chart_data.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/line', methods=['POST'])
def create_line_chart():
    """创建折线图"""
    try:
        data = request.get_json()
        title = data.get('title', '趋势图')

        # 获取时间序列数据
        time_series = data_processor.get_time_series_data('M')
        time_series = time_series.reset_index()
        time_series['日期'] = time_series['日期'].astype(str)

        # 创建图表
        filepath = visualizer.create_line_chart(time_series, '日期', ['销售总额', '利润'], title)

        return jsonify({
            'filepath': filepath,
            'data': time_series.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/pie', methods=['POST'])
def create_pie_chart():
    """创建饼图"""
    try:
        data = request.get_json()
        names = data.get('names', '产品类别')
        values = data.get('values', '销售总额')
        title = data.get('title', '饼图')

        # 准备数据
        chart_data = data_processor.df.groupby(names)[values].sum().reset_index()

        # 创建图表
        filepath = visualizer.create_pie_chart(chart_data, names, values, title)

        return jsonify({
            'filepath': filepath,
            'data': chart_data.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """清除对话历史"""
    try:
        llm_service.clear_history()
        return jsonify({'message': '对话历史已清除'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/charts/<filename>')
def serve_chart(filename):
    """提供图表文件"""
    return send_from_directory(app.config['CHARTS_FOLDER'], filename)


@app.route('/css/<path:filename>')
def serve_css(filename):
    """提供CSS文件"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'css')
    return send_from_directory(frontend_dir, filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    """提供JS文件"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'js')
    return send_from_directory(frontend_dir, filename)


if __name__ == '__main__':
    try:
        initialize_modules()
        print("系统初始化完成！")
        print("访问地址: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"启动失败: {str(e)}")
        sys.exit(1)