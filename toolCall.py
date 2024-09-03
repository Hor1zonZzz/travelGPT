from langchain_core.tools import tool
from duckduckgo_search import DDGS
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import pandas as pd

# 加载环境变量
load_dotenv()

ALI_MAP_API_KEY = os.getenv('ALI_MAP_API_KEY')


@tool
def duckduckgo(query: str) -> list:
    """
    Invoke DuckDuckGo's service to retrieve the latest information from the internet.
    
    Args:
        query: The query.

    Returns:
        search_results: The search results.
    """
    search_results = DDGS().text(keywords=query, region="wt-wt", safesearch="on", max_results=2)
    return search_results

# 天气查询工具
@tool
def get_weather(city):
    """
    调用高德API查询中国国内地区的天气数据

    参数:
    city: 城市或县区，比如北京市、杭州市、余杭区、西城区等。

    返回:
    dict: 包含天气数据的字典
    """
    df = pd.read_excel('AMap_adcode_citycode.xlsx')
    adcode = df[df['中文名'] == city]['adcode']
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': ALI_MAP_API_KEY,
        'city': adcode,  # adcode城市代码
    }

    try:
        # 发送HTTP GET请求
        response = requests.get(url, params=params)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应JSON数据
            data = response.json()
            return data
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    
@tool
def _get_datetime():
    """
    获取当前时间
    
    参数: None

    返回: str: 当前时间字符串
    """
    # now = datetime.now()
    # return now.strftime("%m/%d/%Y, %H:%M:%S")