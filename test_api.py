import requests
import json

BASE_URL = 'http://localhost:5000'

def test_data_summary():
    """测试数据摘要API"""
    print("测试数据摘要API...")
    response = requests.get(f'{BASE_URL}/api/data/summary')
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"总记录数: {data['summary']['总记录数']}")
    print(f"总销售额: {data['statistics']['总销售额']:.2f}")
    print()

def test_category_analysis():
    """测试类别分析API"""
    print("测试类别分析API...")
    response = requests.get(f'{BASE_URL}/api/data/category')
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    print()

def test_query_suggestions():
    """测试查询建议API"""
    print("测试查询建议API...")
    response = requests.get(f'{BASE_URL}/api/query/suggestions')
    data = response.json()
    print(f"状态码: {response.status_code}")
    print(f"建议数量: {len(data['suggestions'])}")
    print()

def test_bar_chart():
    """测试柱状图API"""
    print("测试柱状图API...")
    payload = {
        "x": "产品类别",
        "y": "销售总额",
        "title": "各产品类别销售额"
    }
    response = requests.post(f'{BASE_URL}/api/visualization/bar',
                           json=payload,
                           headers={'Content-Type': 'application/json'})
    data = response.json()
    print(f"状态码: {response.status_code}")
    if 'error' in data:
        print(f"错误: {data['error']}")
    else:
        print(f"图表路径: {data['filepath']}")
    print()

if __name__ == '__main__':
    print("=" * 50)
    print("API测试")
    print("=" * 50)

    try:
        test_data_summary()
        test_category_analysis()
        test_query_suggestions()
        test_bar_chart()
        print("所有API测试完成！")
    except Exception as e:
        print(f"测试失败: {str(e)}")