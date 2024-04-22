import pandas as pd
import numpy as np

data = {
    'user_id': [1, 2, 2, 3, 4, 5, 5, 5],
    'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'David', 'Eve', np.nan, 'Frank'],
    'age': [25, 30, np.nan, 35, 40, 45, 50, 55],
    'email': ['alice@example.com', 'bob@example.com', 'bob@example.com', 'charlie@example.com',
               'david@example.com', 'eve@example.com', 'frank@example.com', 'frank@example.org'],
    'income': [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000]
}
df = pd.DataFrame(data)

print(df)

# 每个user_id保留一条，有多条的保留收入最多的一条
maxseries = df.groupby('name')['income'].transform('max')

df['maxincome'] = maxseries  # 此处为series,索引为name,值为income

df = df[df['maxincome'] == df['income']]

# 空值填充
# df['age'] = df['age'].apply(lambda x: 22 if pd.isna(x) else x)
# df['age'] = df['age'].fillna(22)

# 空值删除
df.dropna(subset=['name', 'age'], how='all', inplace=True)

# 主要列为空，报错并停止程序运行
have_null = df[['name', 'age', 'email']].isnull().any(axis=1)  # 任一列
if have_null.any():  # 任意行
    print('error_message: 主要字段为空')
    import sys
    sys.exit(1)




print(df)