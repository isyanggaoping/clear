import os

import pymysql
import datetime

from schedule import logger
from sqlalchemy import event

if __name__ == '__main__':

    f_name = None
    suffix_name = None
# if f_name[:-9] == 'txdp_tg_fee_day':
# 整个过程为连接数据库并对数据表进行插入删除操作的事务操作，不需要开始，只需要提交、回滚操作
# 格式为：try:commit except:rollback finally:close
try:
    db = pymysql.connect(host='1.11.111.111', user='caiji11', passwd='111111', db='1111',
                         port=3306, charset="utf8", local_infile=1)
    db.autocommit(True)
    cursor = db.cursor()
    sql = "load data local infile 'data_file\\\\" + f_name + suffix_name + "\' into table caiji.txdp_tg_fee_day CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' IGNORE 1 ROWS" \
                                                                           "(type_of_group,shop_no,shop_name, date, wxt_expenses, ztc_expenses, cjtj_expenses,ylmf_expenses, zz_expenses, taoke_expenses, other_expenses);"
    start_time = datetime.datetime.now()
    print('运行开始时间：' + format(start_time))
    # 执行SQL语句
    cursor.execute(sql)
    rowcount = cursor.rowcount
    print("\t插入语法：" + sql)
    # 查看重复条数,如果结果大于零，则执行删除
    consql = "select count(1) from (select   min(id) as id from caiji.txdp_tg_fee_day group by shop_name,date having count(1) > 1) t ;"
    ##获取重复条数
    cursor.execute(consql)
    con = cursor.fetchone()
    # 此处只会删除重复的数据一条，如果一条数据重复一次以上，就不行了，可以开窗排名只保留id最大的那条
    # 此处如果没有重复数据的话，con[0]为none 与零作比较应该会抛出类型异常错误
    if con[0] > 0:  # 此处获取上边查询结果的第一行的第一个元素，若大于0 执行删除
        # 查看重复数据
        resql = "select  min(id)  as id  ,shop_name,date from caiji.txdp_tg_fee_day group by shop_name,date having count(1) > 1;"
        print("\t查询重复：" + resql)
        # 执行resql
        cursor.execute(resql)
        # 获取查询结果
        datas = cursor.fetchall()  # 返回的datas是一个列表
        print("重复数据为：")
        for a in datas:  # a 是返回的列表中的每一行数据，其格式为元祖
            id = a[0]
            shop_name = a[1]
            date = a[2]
            print("\tid=%s\tshop_name=%s\tdate=%s" % \
                  (id, shop_name, date))

        delsql = "delete from caiji.txdp_tg_fee_day " \
                 "where id not in (select max(id) from " \
                 "(select id,shop_name,date," \
                 "row_number() over(partition by shop_name,date order by id desc) as rn  " \
                 "from caiji.txdp_tg_fee_day " \
                 ")as subquery " \
                 "where rn = 1);"
        print("\t删除语法：" + delsql)
        # 执行删除任务
        cursor.execute(delsql)
        # 执行增删改需要提交
        db.commit()
    end_time = datetime.datetime.now()
    print('运行结束时间：' + format(end_time))
    print('运行时长：{:.3f}s'.format((end_time - start_time).total_seconds()))
    print('已插入：', rowcount, '条数据')
    print('已删除：', con[0], '条数据')
    print('执行成功！')
except pymysql.Error as e:
    # 如果执行失败需要回滚
    db.rollback()
    print('异常出错：' + str(e))
finally:
    # 不管成功还是失败都要关闭游标以及数据库
    cursor.close()
    db.close()
logger.info("jgd created:{0}".format(os.path.split(event.src_path)[1]))