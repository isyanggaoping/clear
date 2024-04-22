import time

# 文件监控服务
from watchdog.observers import Observer
from watchdog.events import *
import time
import os
import logging
import datetime
import pymysql
from warnings import filterwarnings
filterwarnings("ignore",category=pymysql.Warning)   # 忽略数据库警告
# os.path.basename() 返回路径的最后一部分路径名  如D:\\lpt\\test,结果就是test

class FileEventHandler(FileSystemEventHandler):
    # 构造函数
    def __init__(self):
        # 调用父类的构造方法，使父类初始化方法得以执行（这个过程可能会设置一些状态或属性），
        FileSystemEventHandler.__init__(self)

    # 重写事件移动监控方法
    # 监控文件夹下文件或目录移动情况的方法  envent就是移动的文件或目录  src_path源路径 dest_path目标路径
    # 如果移动的是文件就在日志中生成：**文件移动，**从源路径中切出
    # move方法不生效，从一个文件夹中迁出的话就会默认是删除，往一个文件夹迁入的话就会认为是创建
    def on_moved(self, event):
        print('move')
        if event.is_directory:
            # {}字符串中的占位符，也可以写成f'{参数名}'
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("new_file moved from {0} to {1}".format(event.src_path, event.dest_path))
            # 路径的split函数是把文件的绝对路径拆成两部分形成元祖，元祖索引0就是文件目录 索引1就是文件
            logger.info("new_file moved:{0}".format(os.path.split(event.src_path)[1]))

    # 删除文件或目录  删除方法并没有判断事件路径是文件还是文件夹的能力 所以不能这样写event.is_directory
    def on_deleted(self, event):
        path = event.src_path
        if '.' not in path:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("new_file deleted:{0}".format(event.src_path))
            logger.info("new_file deleted:{0}".format(os.path.split(event.src_path)[1]))


    # 重写创建或导入事件方法，并在此方法中读取创建或导入的事件，并将其写入到数据库中
    def on_created(self, event):
        if event.is_directory:
            # 打印创建的文件夹
            print("directory created:{0}".format(event.src_path))
        # 就是 event.is_file
        else:
            file_name = os.path.split(event.src_path)[1]    # 切割事件源路径，就是创建的文件的绝对路径
            f_name = os.path.splitext(file_name)[0]     # 获取文件名不包含扩展名
            suffix_name = os.path.splitext(event.src_path)[1]  # 获取文件的扩展名
            file_, file_format = file_name.split('.')  # 把文件名按点切割 文件名和扩展名分别各前面变量
            # file_date = file_.split('_')[-1] #文件日期在文件名的_最后一部分
            file = 'D:\\lpt\\test\\demo01\\filehandler\\file\\' + file_name
            if file_format not in ('csv', 'CSV', 'txt', 'TXT'):  # or len(file_date) != 8:
                print('文件名错误，已删除！')
                os.remove(file)   # 文件命名不规范，打印错误信息，并删除文件 此处为文件的绝对路径
            else:
                # 文件名没问题打印文件创建信息
                print("new_file created:{0}".format(event.src_path))

                if f_name == 'ygp_info':
                    try:
                        # pymysql 创建连接，连接创建游标  sqlalchemy 创建连接引擎，连接引擎创建连接
                        db = pymysql.connect(host='localhost', user='root', passwd='ygp159753', db='dbl',
                                             port=3306, charset="utf8", local_infile=1)
                        db.autocommit(True)
                        cursor = db.cursor()
                        sql = "load data local infile 'new_file\\\\" + f_name + suffix_name + "\' into table dbl.ygp_info CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' IGNORE 1 ROWS" \
                                                                                               "(name,age,high,weight,phone,wechat,qq);"
                        start_time = datetime.datetime.now()
                        print('运行开始时间：' + format(start_time))
                        # 执行SQL语句
                        cursor.execute(sql)
                        print(sql)
                        end_time = datetime.datetime.now()
                        print('运行结束时间：' + format(end_time))
                        print('运行时长：{:.3f}s'.format((end_time - start_time).total_seconds()))
                        print('已插入：', cursor.rowcount, '条数据')
                        print('执行成功！')
                        cursor.close()
                        db.close()
                    except pymysql.Error as e:
                        print('异常出错：' + str(e))
                    logger.info("new_file created:{0}".format(os.path.split(event.src_path)[1]))


if __name__ == "__main__":
    #print(os.path.abspath(__file__))
    # 创建日志记录器 logging模块的getLogger方法
    logger = logging.getLogger(__name__)
    # logging模块中，handler（处理器）是负责将日志记录（log record）发送到指定的目的地的对象。
    logger.handlers.clear()
    # 设置日志打印级别
    logger.setLevel(logging.INFO)
    # 设置日志保存位置
    handler_info = logging.FileHandler('D:/lpt/test/demo01/filehandler/log/logs.log')
    # 设置保存日志的级别
    handler_info.setLevel(logging.INFO)
    # 设置日志打印格式 时间戳 + 日志信息
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    # 把日志格式赋给打印日志对象
    handler_info.setFormatter(formatter)
    # 把打印日志对象赋给日志记录器
    logger.addHandler(handler_info)

    # 创建类对象，并调用监控服务并启动
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, 'D:\\lpt\\demo01\\filehandler\\new_file', True)
    observer.start()

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()