import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    BASE_URL = os.getenv('BASE_URL')
    MODEL = os.getenv('model', 'ep-20260312161409-csvf6')

    # 数据路径
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sales.xlsx')
    CHARTS_PATH = os.path.join(os.path.dirname(__file__), 'static', 'charts')