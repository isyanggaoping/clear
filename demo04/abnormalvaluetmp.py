import pandas as pd
import numpy as np

# 假设这是我们的数据集
data = {
    'height': [165, 170, 175, 180, 9999, 172, 168]
}

df = pd.DataFrame(data)

# 显示原始数据集
print("原始数据集:")
print(df)

# 定义异常值的阈值
THRESHOLD = 300

# 识别异常值  返回的结果是ture或false
df['is_abnormal'] = df['height'] > THRESHOLD

# 显示包含异常值标记的数据集
print("标记异常值的数据集:")
print(df)

# 处理异常值：删除含有异常值的行
df_cleaned = df[~df['is_abnormal']]

# 或者，处理异常值：将异常值替换为均值或中位数
mean_height = df['height'].mean()
median_height = df['height'].median()

# 使用均值替换异常值
#df['height'].replace(9999, mean_height, inplace=True)

df['height'].apply(lambda x: mean_height if x > THRESHOLD else x)

# 或者使用中位数替换异常值
# df['height'].replace(9999, median_height, inplace=True)

# 显示清洗后的数据集
print("清洗后的数据集:")
print(df_cleaned)