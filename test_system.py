import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_data_processor():
    """测试数据预处理模块"""
    print("测试数据预处理模块...")
    from modules.data_processor import DataProcessor

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'sales.xlsx')
    processor = DataProcessor(data_path)

    # 测试数据加载
    df = processor.load_data()
    print(f"[OK] 数据加载成功，共 {len(df)} 条记录")

    # 测试数据摘要
    summary = processor.get_data_summary()
    print(f"[OK] 数据摘要获取成功，共 {summary['总记录数']} 条记录")

    # 测试基础统计
    stats = processor.get_basic_statistics()
    print(f"[OK] 基础统计获取成功，总销售额: {stats['总销售额']:.2f}")

    # 测试类别分析
    category_data = processor.get_category_analysis()
    print("[OK] 类别分析获取成功")

    # 测试SQL查询
    processor.init_sqlite_db()
    result = processor.execute_sql_query("SELECT * FROM sales LIMIT 5")
    print(f"[OK] SQL查询执行成功，返回 {len(result)} 条记录")

    return True


def test_llm_service():
    """测试LLM服务模块"""
    print("\n测试LLM服务模块...")
    from modules.llm_service import LLMService

    try:
        llm = LLMService()
        print("[OK] LLM服务初始化成功")

        # 测试对话（不实际调用API）
        print("[OK] LLM服务模块测试通过")
        return True
    except Exception as e:
        print(f"[FAIL] LLM服务测试失败: {str(e)}")
        return False


def test_visualizer():
    """测试可视化模块"""
    print("\n测试可视化模块...")
    from modules.visualizer import Visualizer
    import pandas as pd

    visualizer = Visualizer()

    # 创建测试数据
    test_data = pd.DataFrame({
        '类别': ['A', 'B', 'C', 'D'],
        '值': [100, 200, 150, 300]
    })

    # 测试柱状图
    try:
        filepath = visualizer.create_bar_chart(test_data, '类别', '值', '测试柱状图')
        print(f"[OK] 柱状图生成成功: {filepath}")
    except Exception as e:
        print(f"[FAIL] 柱状图生成失败: {str(e)}")
        return False

    return True


def test_sql_generator():
    """测试SQL生成器模块"""
    print("\n测试SQL生成器模块...")
    from modules.data_processor import DataProcessor
    from modules.sql_generator import SQLGenerator

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'sales.xlsx')
    processor = DataProcessor(data_path)
    processor.load_data()

    try:
        generator = SQLGenerator(processor)
        print("[OK] SQL生成器初始化成功")

        # 测试查询建议
        suggestions = generator.get_query_suggestions()
        print(f"[OK] 查询建议获取成功，共 {len(suggestions)} 个建议")

        return True
    except Exception as e:
        print(f"[FAIL] SQL生成器测试失败: {str(e)}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("智能销售数据分析系统 - 系统测试")
    print("=" * 50)

    results = []
    results.append(("数据预处理模块", test_data_processor()))
    results.append(("LLM服务模块", test_llm_service()))
    results.append(("可视化模块", test_visualizer()))
    results.append(("SQL生成器模块", test_sql_generator()))

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)

    all_passed = True
    for name, result in results:
        status = "[OK] 通过" if result else "[FAIL] 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("所有测试通过！系统可以正常运行。")
    else:
        print("部分测试失败，请检查相关模块。")
    print("=" * 50)