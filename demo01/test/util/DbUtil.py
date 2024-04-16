#数据库工具类
import os
import os.path as op
import re
from demo01.test.util.Properties import Properties
from sqlalchemy import create_engine
import traceback
import pandas as pd

class DbManage:

    #定义两个变量 一个存放本类对象，构成单例模式 另一个变量存放数据库连接引擎
    __LM = None
    __engine = None

    #定义构造方法，并在构造方法里面调用创建数据库连接引擎的方法
    def __init__(self):
        DbManage.__init_engine()

    #定义new方法，并在new方法里形成单例模式  有对象就用，没有就调用父类方法创建
    def __new__(cls, *args, **kwargs):
        print('创建新连接' + '>'*50)
        if cls.__LM is None:
            cls.__LM = object.__new__(cls)
        else:
            return cls.__LM
        return cls.__LM


    #创建数据库连接引擎
    @classmethod
    def __init_engine(cls):
        if cls.__engine is None:
            #读取配置文件
            configdir = op.join(op.dirname(op.dirname(op.abspath(__file__))),'..\\..', 'config\\')
            configfile = re.sub(r'\.\.\\\.\.\\', '', configdir)
            configfile += os.listdir(configfile)[0]

            prop = Properties(configfile).get_properties()

            hostname, port, database, username, password = prop['HOSTNAME'], prop['PORT'], prop['DATABASE'], prop[
                'USERNAME'], prop['PASSWORD']
            db_uri = 'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}?charset=utf8' \
                .format(username=username, pwd=password, host=hostname, port=port, db=database)
            # 创建数据库引擎
            cls.__engine = create_engine(db_uri, echo=False, pool_pre_ping=True, pool_recycle=1800)
            print(cls.__engine)

    #读数据库表数据
    @staticmethod
    def read_sql(sql):
        try:
            with DbManage.__engine.connect() as conn:
                read_df = pd.read_sql(sql,conn)
                return read_df
        except Exception as e:
            print("异常",e)
            print(traceback.format_exc())
            raise e

    #往数据库写数据
    @staticmethod
    def write_sql(df, name, col=None, mode="append"):
        try:
            # 查询插入前的表总行数
            with DbManage.__engine.connect() as conn:
                result = conn.execute(f'SELECT COUNT(*) FROM {name}')
                num_before = result.fetchone()[0]
            with DbManage.__engine.connect() as conn:
                ##使用pandas的to_sql方法将DataFrame中的数据写入到数据库中
                df.to_sql(name=name, con=conn,
                          if_exists=mode,
                          index=False,
                          dtype=col,
                          chunksize=5000)
                ##f''字符串格式化方法 允许字符串中嵌入表达式 如{name}
                result = conn.execute(f'SELECT COUNT(*) FROM {name}')
                num_after = result.fetchone()[0]
                num_inserted = num_after - num_before
            print(f"{name}表插入数据{num_inserted}条")
        except Exception as e:
            print("出错异常信息：", e)
            print(traceback.format_exc())
            raise e



if __name__ == '__main__':
    dbManage = DbManage()

    df = dbManage.read_sql('''select * from demo01''')
    print(df.head(10))

