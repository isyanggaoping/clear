import datetime
import os
import os.path as op
# 导入库下边是一个一个的类，包含对应的属性和方法
import pandas as pd

if __name__ == '__main__':

    #处理时间
    #这相当于new了个对象调用方法
    now = datetime.datetime.now()
    dateend = now.strftime('%Y-%m-%d')
    #这个相当于直接类名调用静态方法
    # today = datetime.datetime.strftime(now,'%Y%m%d')
    datestart = (now - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    datefile = dateend

    #处理路径
    filepath = op.dirname(op.abspath(__file__))
    absoldpath = '\\origin_file\\oldfile\\'
    absnewpath = '\\origin_file\\newfile\\'
    olddir = filepath + absoldpath
    newdir = filepath + absnewpath
    for f in os.listdir(olddir):
        if '计时' in f:
            oldfile = olddir + f
    newfile = newdir + f'\\{datefile}-计时明细'

    #获取表格 因为上边存在判断，oldfile可能不存在
    jsdf = pd.read_excel(oldfile,sheet_name='义乌仓库计时人员出勤明细')
    #处理表格数据
    #只拿取日期及上下班部分数据
    jsdfi = jsdf.iloc[:,5:]
    jsdfi.dropna(how = 'all',inplace = True)
    jsdft = jsdfi.T
    jsdft['date'] = jsdft.index
    jsdft['date'] = jsdft['date'].apply(lambda x: (datetime.timedelta(days=x) + datetime.datetime.strptime('1899-12-30','%Y-%m-%d')).strftime('%Y-%m-%d'))
    #取要求时间范围内的数据
    jsdft = jsdft[(jsdft['date'] >= datestart) & (jsdft['date'] < dateend)]
    #删除弄的日期列，准备遍历将每个人的上下班、时长三列竖向拼接
    jsdft.drop(columns = 'date', inplace = True)
    #循环遍历列拼接上下班及时长
    concatdf = pd.DataFrame() #准备空df,盛放拼接后的df
    for col in range(jsdft.columns.size + 1):
        if (col %3 == 0) & (col != 0):
            tmp = jsdft.iloc[:,col - 3:col]
            tmp1 = pd.DataFrame(tmp)
            tmp1.columns = ['上班时间','下班时间','时长']
            concatdf = pd.concat([concatdf,tmp1])

    #上边从表格里拿出来，转置，拼接，未动顺序和原来表格里的顺序一致，把名字拿出来可直接左右拼接
    jsdfname = jsdf['姓名']
    jsdfname.dropna(how = 'all',inplace = True)
    listname = jsdfname.to_list()
    listname = (item for item in listname for _ in range(7))  #将名字扩展七份
    jsdfnamem = pd.DataFrame(listname)
    jsdfnamem.columns = ['name']

    #重置两部分索引，准备左右合并，合并需要左右两部分索引一致
    jsdfnamem.reset_index(inplace=True)
    jsdfnamem.drop(columns='index',inplace=True)
    concatdf.reset_index(inplace=True)
    concatdf.rename(columns={'index':'date'},inplace=True)

    #将天数日期转化为日期格式日期
    concatdf['date'] = concatdf['date'].apply(lambda x: datetime.timedelta(x) + datetime.datetime.strptime('1899-12-30','%Y-%m-%d'))

    #拼接左右两个df
    merdf = pd.concat([jsdfnamem,concatdf],axis=1)

    #merdf.to_csv(newfile+'.csv',encoding='utf-8',index=False)

    #drop的参数是索隐列或者索引列表，不是布尔
    merdf.drop(index=merdf[merdf['上班时间'] == '请假'].index.tolist(),
                  inplace=True)
    merdf.drop(index=merdf[merdf['上班时间'] == '休'].index.tolist(),
                  inplace=True)
    merdf.drop(index=merdf[merdf['上班时间'] == '离职'].index.tolist(),
                  inplace=True)
    merdf.drop(index=merdf[merdf['上班时间'] == '辞职'].index.tolist(),
                  inplace=True)

    #增加仓库编码，名称两列
    merdf['warehousecode'] = '12345'
    merdf['warehousename'] = '54321'


    #算金额和时长  datetime.timedelta(此处传参为单个时间数据)  pd.to_timedelta(此处传参为时间数据列)
    merdf['时长'] = (pd.to_timedelta(merdf['下班时间'].astype(str))
                   - pd.to_timedelta(merdf['上班时间'].astype(str))).dt.total_seconds()/3600
    #print(pd.to_datetime(merdf['下班时间'].astype(str)) - pd.to_datetime(merdf['下班时间'].astype(str)))


    merdf['金额'] = merdf['时长']*17



    #调整字段顺序
    print(merdf)








