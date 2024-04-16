import os
import traceback

import pandas as pd
import os.path as op
from sqlalchemy import create_engine
from demo01.test.util.Properties import Properties
import re

def readWrite():
    # 获取表格数据路径
    dir_path = op.join(op.dirname(op.dirname(op.abspath(__file__))), "../../../..", "new_file\\")
    file_path = re.sub(r'../..\\', '', dir_path)
    file_path += os.listdir(file_path)[0]
    # print(file_path)

    # 读取表格数据
    dff = pd.read_excel(io=file_path, sheet_name=0, header=0, names=['dt', 'a', 'b'], usecols=[0, 1, 2])
    dff = dff.loc[dff['b'] != '汇总']
    dff['dt'] = 1
    dff = dff[['dt', 'a']]
    print(dff)

    # 获取配置文件路径
    config_path = op.join(op.dirname(op.abspath(__file__)), '../../../..', 'config\\config.properties')
    config_path = re.sub(r'../..\\', '', config_path)
    print(config_path)

    # 创建读取配置文件类对象
    prop = Properties(config_path).get_properties()

    ##提取配置文件的配置信息赋给各变量
    hostname, port, database, username, password = prop['HOSTNAME'], prop['PORT'], prop['DATABASE'], prop[
        'USERNAME'], prop['PASSWORD']
    db_uri = 'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}?charset=utf8' \
        .format(username=username, pwd=password, host=hostname, port=port, db=database)
    # 创建数据库引擎
    engine = create_engine(db_uri, echo=False, pool_pre_ping=True, pool_recycle=1800)

    # 创建数据库连接对象
    conn = engine.connect()

    # 从数据库读数据
    df = pd.read_sql('''select * from demo01''', conn)
    df['id'] = df['id'] + 1
    print(df)

    # 写入时字段名需对应，否则报错
    df.rename(columns={'dt': 'id', 'a': 'name'}, inplace=True)

    # 往数据库写入数据
    df.to_sql('demo01', conn, if_exists='append', index=False)

    try:
        # 查询插入前的表总行数
        with conn:
            num_before = conn.execute('''SELECT COUNT(*) FROM demo01''').fetchone()[0]

        with conn:
            ##使用pandas的to_sql方法将DataFrame中的数据写入到数据库中
            df.to_sql('demo01', conn, if_exists='append', index=False)
            ##f''字符串格式化方法 允许字符串中嵌入表达式 如{name}
            num_after = conn.execute('''SELECT COUNT(*) FROM demo01''').fetchone()[0]
            num_inserted = num_after - num_before
        print(f"test表插入数据{num_inserted}条")
    except Exception as e:
        print("出错异常信息：", e)
        print(traceback.format_exc())
        raise e


    # 从数据库读数据
    dfRead = pd.read_sql('''select * from demo01''', conn)
    print(dfRead)

    # 返回的是值，不是dataframe
    # dt = conn.execute('''select * from demo01''').fetchall()
    # print(dt)

if __name__ == '__main__':
    readWrite()



