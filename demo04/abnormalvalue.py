import pandas as pd
import numpy as np

# 假设这是我们的数据集
data = {
    'height': [165, 170, 175, 180, 9999, 172, 168]
}

df = pd.DataFrame(data)

#设置异常阈值
threshold = 260


#判断数据是否超过这个阈值，超过给true
df['flag'] = df['height'] > threshold


df.drop(df[df['flag'] == True].index,inplace=True)

meandf = df['height'].mean()

df['mean'] = meandf

print(df)