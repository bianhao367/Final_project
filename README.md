# 智能销售数据分析系统

基于大语言模型的智能问答与数据可视化平台

**小组成员：程曦**

## 项目简介

本系统是一个基于大语言模型的智能销售数据分析平台，能够对销售数据进行多维度分析，提供智能问答、数据可视化、自然语言查询等功能。

## 功能特性

- **智能问答助手**：基于大语言模型的自然语言问答，回答数据相关问题
- **数据可视化**：支持柱状图、折线图、饼图等多种图表类型
- **自然语言查询**：将自然语言转换为SQL查询，自动执行并返回结果
- **数据概览**：展示总销售额、订单数量、利润等关键指标
- **对话历史管理**：支持对话历史记录和清除功能

## 技术栈

- **后端**：Python + Flask
- **前端**：Vue.js 3 + Axios
- **数据库**：SQLite（内存数据库）
- **LLM**：OpenAI API（火山引擎端点）
- **可视化**：Matplotlib + Plotly
- **数据处理**：Pandas + OpenPyXL

## 项目结构

```
sales_analyzer/
├── app.py                 # Flask后端主入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包
├── .env                   # API配置
├── data/                  # 数据目录
│   └── sales.xlsx         # 销售数据（500条）
├── frontend/              # Vue.js前端
│   ├── index.html         # 主页面
│   ├── css/               # 样式文件
│   │   └── style.css
│   └── js/                # JavaScript文件
│       ├── app.js         # Vue应用入口
│       └── components/    # Vue组件
│           ├── DataSummary.js
│           ├── ChatAssistant.js
│           ├── DataVisualization.js
│           └── NaturalQuery.js
├── static/                # 静态资源
│   └── charts/            # 生成的图表
├── modules/               # 核心模块
│   ├── data_processor.py  # 数据预处理
│   ├── llm_service.py     # LLM服务
│   ├── visualizer.py      # 可视化模块
│   └── sql_generator.py   # SQL生成器
└── utils/                 # 工具函数
```

## 安装与运行

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

```bash
cd sales_analyzer
pip install -r requirements.txt
```

### 3. 配置API

在项目根目录创建 `.env` 文件，配置以下内容：

```env
OPENAI_API_KEY=your_api_key
BASE_URL=your_base_url
model=your_model_id
```

### 4. 运行系统

```bash
python app.py
```

系统将在 http://localhost:5000 启动

## 使用说明

### 1. 数据概览

系统首页展示销售数据的关键指标：
- 总销售额
- 订单数量
- 总利润
- 平均订单金额

### 2. 智能问答

在聊天界面输入问题，系统将基于大语言模型给出回答：
- "各产品类别的销售额占比是多少？"
- "哪个地区的利润最高？"
- "分析一下销售趋势"

### 3. 数据可视化

选择图表类型生成可视化：
- **柱状图**：展示各类别销售额对比
- **折线图**：展示月度销售趋势
- **饼图**：展示销售额占比分布

### 4. 自然语言查询

输入自然语言查询，系统自动转换为SQL并执行：
- "查询所有电子产品的销售总额"
- "按地区统计销售额排名"
- "找出销售额超过10000的订单"

## API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/chat` | POST | 智能问答 |
| `/api/data/summary` | GET | 获取数据摘要 |
| `/api/data/category` | GET | 获取类别分析 |
| `/api/data/region` | GET | 获取地区分析 |
| `/api/data/top-products` | GET | 获取热门产品 |
| `/api/query` | POST | 执行自然语言查询 |
| `/api/query/suggestions` | GET | 获取查询建议 |
| `/api/visualization/bar` | POST | 创建柱状图 |
| `/api/visualization/line` | POST | 创建折线图 |
| `/api/visualization/pie` | POST | 创建饼图 |
| `/api/history/clear` | POST | 清除对话历史 |

## 数据说明

系统使用 `sales.xlsx` 作为示例数据，包含500条销售记录，字段包括：
- 订单ID、日期、产品类别、产品名称
- 销售数量、单价、销售总额、利润
- 地区、销售渠道、客户ID

## 测试

运行系统测试：

```bash
python test_system.py
```

## 常见问题

### 1. 数据加载失败

确保 `data/sales.xlsx` 文件存在且格式正确

### 2. LLM服务不可用

检查 `.env` 文件中的API配置是否正确

### 3. 图表生成失败

确保 `static/charts` 目录存在且有写入权限

## 开发说明

### 添加新的图表类型

在 `modules/visualizer.py` 中添加新的图表创建方法

### 扩展数据处理功能

在 `modules/data_processor.py` 中添加新的数据分析方法

### 自定义LLM提示词

修改 `modules/llm_service.py` 中的 `system_prompt`

## 许可证

本项目仅供学习和研究使用

## 联系方式

如有问题或建议，请联系项目维护者