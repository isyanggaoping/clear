import requests
import pandas as pd
import schedule
import time
import sys
from datetime import datetime

# API接口地址
API_URL = 'http://jsonplaceholder.typicode.com/posts'


# 数据清洗函数
def clean_data():
    try:
        # 获取数据，使用url去连接api，按api定义的规则获取对应的数据
        # 使用 requests，你可以发送 GET、POST、PUT、DELETE 等各种 HTTP 请求，
        # 并且它会自动处理 URL 编码、cookies、重定向、SSL 等一系列繁琐的事情。
        response = requests.get(API_URL)
        # 确保请求成功
        # 判断http响应是不是200；如果不是抛出异常
        response.raise_for_status()

        # 将response的内容解析为JSON
        data = response.json()
        print("Fetched data:", data)  # 打印获取的数据，以供检查

        # jsonplaceholder.typicode.com 的数据结构是直接返回一个帖子列表
        # 我们可以直接将其转换为 DataFrame
        df = pd.DataFrame(data)

        # 数据清洗逻辑（根据实际数据结构进行相应的清洗操作）
        # 例如：去除缺失值
        df = df.dropna()

        # 如果列表中包含你想要处理的字段，可以进行相应的替换或转换
        # 例如，将空字符串替换为 pd.NA（注意：这里的 'title' 是示例字段）
        df['title'].replace('', pd.NA, inplace=True)

        # 有些字段可能需要转换数据类型或格式化
        # 例如，如果 'date' 字段存在，并且需要转换为日期格式
        # df['date'] = pd.to_datetime(df['date'])

        # 保存清洗后的数据到CSV
        output_filename = f'cleaned_data_{datetime.now().strftime("%Y%m%d")}.xlsx'
        df.to_excel(output_filename, index=False)

        print(f'Data cleaned and saved to {output_filename}')

    except Exception as e:
        print(f'An error occurred: {e}')

# 调度函数
def schedule_daily_job():
    schedule.every().day.at("08:00").do(clean_data)

# 运行调度器
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 调度函数和运行调度器的代码保持不变...

if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == 'now':
        # 如果提供了 'now' 参数，则立即执行数据清洗
        clean_data()
    else:
        # 启动定时任务
        schedule_daily_job()
        # 运行调度器
        run_scheduler()

