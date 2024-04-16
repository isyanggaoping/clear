import os.path as op
import os
import re
from datetime import datetime

import pandas as pd
#link的属性与方法

#属性
base_dir = op.dirname(op.dirname(op.dirname(op.dirname(op.abspath(__file__)))))
base_dir += '\\new_file\\'

#方法 先判断属于文件还是文件夹，文件就追加输出，如果是文件夹就切割后循环判断切割后的结果是文件还是文件夹
def getAllFilePath(dir_path):
    #将所有路径放到一个集合里
    filePathArray = []
    #递归遍历目录下的文件和文件夹装入集合
    if op.isfile(dir_path):
        filePathArray.append(dir_path)
        return filePathArray
    elif op.isdir(dir_path):
        listDir = os.listdir(dir_path)
        for next in listDir:
            filePathArray += getAllFilePath(op.join(dir_path,next))
    else:
        print(f'{base_dir}路径有问题，请检查！')
    return filePathArray

def transData(dt):
    if type(dt) is str:
        if len(dt) == 10 and re.match(re.compile(r'^d{4}-d{2}-d(2)'),dt):
            dt_new = dt
        elif len(dt) == 18 and re.match(re.compile(r'^d{4}-d{2}-d{2} 00:00:00'),dt):
            dt_ = pd.to_datetime(dt)
            year_ = str(dt_.year)
            month_ = "0" + str(dt_.month) if dt_.month < 10 else str(dt_.month)
            day_ = "0" + str(dt_.day) if dt_.day < 10 else str(dt_.day)
            dt_new = year_ + "-" + month_ + "-" + day_
        else:
            dt_new = dt
    elif type(dt) is datetime:
        dt_new = datetime.strftime(dt,'%Y%m%d')
    else:
        print('日期格式错误')
    return dt_new

def readData(next):
        df = pd.read_excel(next,sheet_name=0,header=0,names=None,index_col=None,usecols=None,dtype=None)
        cols = df.columns.values
        if '商品ID' in cols:
            channl = '商品ID'
            fileType = '视频'
        elif '直播间ID' in cols:
            channl = '直播间ID'
            fileType = '直播'
        else:
            print(f'{next}文件错误')
        if channl == '直播间ID':
            df_new = df[[ '直播间ID', '直播间名称', '1号链接', '日期', '消耗(元)']]
        elif channl == '商品ID':
            df_new = df[[ '商品ID', '商品名称', '日期', '消耗(元)']]
        #日期列有汇总行去掉
        # df_new['日期'] = df_new['日期'].loc[df_new['日期'] != '汇总'] 把汇总改成nal但是不会删除那一行
        df_new = df_new.loc[df_new['日期'] != '汇总']
        #对日期进行编辑 修改成需要的格式
        df_new[['日期']] = df_new[['日期']].apply(lambda x:transData(x['日期']),axis = 1)
        #插入采集日期和采集人 从文件目录获取
        #获取日期
        listPath = next.split('\\')
        caiDt = listPath[listPath.index('new_file') + 2]
        if re.match(re.compile(r'^\d{8}$'),caiDt):
            df_new.insert(loc = 0, column = "采集日期",value =  datetime.strptime(caiDt,'%Y%m%d').strftime('%Y-%m-%d'))
        else:
            caiDt_ = datetime.now().strftime('%Y-%m-%d')
            df_new.insert(loc = 0, column = "采集日期",value =  caiDt_)
        #获取采集人
        caiRen = re.search(re.compile(r'(?<=自营-).+?(?=\\)'),next).group(0)
        df_new.insert(loc = 5 if channl == '商品ID' else 6, column = '采集人',value = caiRen)
        return {'fileType':fileType,'df':df_new}
