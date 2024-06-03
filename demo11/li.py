import  pandas as pd

if __name__ == '__main__':

    my_list = [[1, 'hello', 3.14, True]] # 列表套列表就是一行数据  # [1, 'hello', 3.14, True] 不套的话就是series，是一列数据
    cols = ['id','name','bili','yun']
    df = pd.DataFrame(my_list,columns=cols)
    print(df)

    # 创建多个Series对象
    ID = pd.Series([1, 2, 3], name='ID')
    Name = pd.Series(['Alice', 'Bob', 'Charlie'], name='Name')
    Age = pd.Series([25, 30, 35], name='Age')

    # 使用字典形式的Series对象创建DataFrame
    df_from_dicts_of_series = pd.DataFrame({'ID': ID, 'Name': Name, 'Age': Age})

    print(df_from_dicts_of_series)

