import pandas as pd

def rep(x):
    if isinstance(x,str):
        x = float(x.replace(',',''))
        return x
    return x

if __name__ == '__main__':
    # 字符串替换
    str1 = 'aaa,bbb'
    float = 1
    #数字类型的数据不能用astyle方法转换类型，但可以用传参的方式转换
    #print(str1 + str(float))

    data = {
        'a': [123, 111, 234, '1ss234.55']
    }
    df = pd.DataFrame(data)
    #读取的列为混合型数据，可以判断后分别处理
    #df['a'] = df['a'].apply(lambda x: float(x.replace(',','')) if isinstance(x,str) else x)
    #df['a'] = df['a'].replace(',', '', regex=True)

    df['a'] = df['a'].replace('ss', '')
    str1 = str1.replace(',','')


    print(df)



