import pandas as pd
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', passwd='ygp159753', db='dbl',
                         port=3306, charset="utf8", local_infile=1)

    try:
        cursor = conn.cursor()

        cursor.execute('select count(*) from ygp_info')
        a = cursor.fetchone()[0]
        cursor.execute('delete from ygp_info where name = "wyy"')
        cursor.execute('select count(*) from ygp_info')
        b = cursor.fetchone()[0]
        c = a - b
        print(f'删除 {c} 条数据')

        # mysql是支持事务的数据库，需手动提交事务，否则会回滚
        conn.commit()
    #套用try except 可以手动出错回滚
    except Exception as e:
        print(e)
        if conn is not None:
            conn.rollback()

    cursor.execute('select * from ygp_info')

    rows = cursor.fetchall()

    col = [i[0] for i in cursor.description] #列名列表
    data = [list(row) for row in rows] #数据列表

    #列表套列表，列表套元祖，字典这两种可以创建Dataframe
    #[[zz,11],[ls,22]] 列名单独一个列表[列名1,列名2]
    #[(zz,11),(ls,22)] 列名单独一个列表[列名1,列名2]
    #{列名1：[zz,ls],列名2：[11,22]}
    df = pd.DataFrame(data,columns=col)
    print(df)

    cursor.close()
    conn.close()