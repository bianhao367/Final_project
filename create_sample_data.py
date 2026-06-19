import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置随机种子以确保可重复性
np.random.seed(42)

# 生成500条销售数据
n_records = 500

# 产品类别
categories = ['电子产品', '服装', '食品', '家居用品', '运动器材']
products = {
    '电子产品': ['智能手机', '笔记本电脑', '平板电脑', '耳机', '智能手表'],
    '服装': ['T恤', '牛仔裤', '外套', '运动鞋', '帽子'],
    '食品': ['零食', '饮料', '调味品', '冷冻食品', '生鲜'],
    '家居用品': ['床上用品', '厨房用具', '清洁用品', '装饰品', '收纳盒'],
    '运动器材': ['瑜伽垫', '哑铃', '跑步机', '运动水壶', '健身手套']
}

# 地区
regions = ['华东', '华南', '华北', '华中', '西南', '西北', '东北']

# 销售渠道
channels = ['线上', '线下', '批发']

# 生成数据
data = []
start_date = datetime(2024, 1, 1)

for i in range(n_records):
    # 随机选择类别和产品
    category = np.random.choice(categories)
    product = np.random.choice(products[category])

    # 生成日期（2024年全年）
    days_offset = np.random.randint(0, 365)
    date = start_date + timedelta(days=days_offset)

    # 生成销售数量（1-50件）
    quantity = np.random.randint(1, 51)

    # 根据产品类别设置价格范围
    if category == '电子产品':
        unit_price = np.random.uniform(100, 8000)
    elif category == '服装':
        unit_price = np.random.uniform(50, 1000)
    elif category == '食品':
        unit_price = np.random.uniform(5, 200)
    elif category == '家居用品':
        unit_price = np.random.uniform(20, 500)
    else:  # 运动器材
        unit_price = np.random.uniform(30, 2000)

    unit_price = round(unit_price, 2)
    total_amount = round(quantity * unit_price, 2)

    # 随机选择地区和渠道
    region = np.random.choice(regions)
    channel = np.random.choice(channels, p=[0.5, 0.35, 0.15])  # 线上占比50%

    # 生成客户ID
    customer_id = f'C{np.random.randint(1000, 9999)}'

    # 生成利润率（10%-40%）
    profit_margin = np.random.uniform(0.1, 0.4)
    profit = round(total_amount * profit_margin, 2)

    data.append({
        '订单ID': f'ORD{10000 + i}',
        '日期': date.strftime('%Y-%m-%d'),
        '产品类别': category,
        '产品名称': product,
        '销售数量': quantity,
        '单价': unit_price,
        '销售总额': total_amount,
        '利润': profit,
        '地区': region,
        '销售渠道': channel,
        '客户ID': customer_id
    })

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel文件
output_path = 'D:/python_code/transformer/sales_analyzer/data/sales.xlsx'
df.to_excel(output_path, index=False, engine='openpyxl')

print(f'已生成 {n_records} 条销售数据，保存至: {output_path}')
print(f'数据概览:')
print(df.head())
print(f'\n数据统计:')
print(df.describe())