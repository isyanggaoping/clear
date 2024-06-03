import datetime

# datetime.datetime.now() 库.类.方法（） 返回的是datetime类对象实例  return cls.fromtimestamp(t)
# datetime.date.today() 库.类.方法（）  返回值是date类对象实例

# 假设您已经建立了数据库连接（db_conn）
if __name__ == '__main__':

    start_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
    print(start_date)
    print(end_date)

    print(datetime.date.today())
    print(datetime.datetime.now().date())
    print(datetime.timedelta(days=1))

    # datetime与date之间可以加减
    print((datetime.datetime.now() +
           (datetime.datetime.now().date() - datetime.datetime.strptime('2022-04-18','%Y-%m-%d').date())).date())