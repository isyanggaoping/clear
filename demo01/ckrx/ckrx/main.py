import datetime
import pandas as pd


#对于一个df来说，无论你选取哪几列，对应行的索引都是一样的，比如第一回抽取 前两列是张三的上下班时间 索引是 1号,2号,3号 再抽取第三列，第四列，索引也是索引是 1号,2号,3号
#竖向合并的时候，索引不会乱，能得到所需的每天没人的上下班时间

ywjs_col = ['日期','姓名','仓库编码','仓库名称','上班时间','下班时间','金额']

def run(sqlengin):
    #文件目录：读取文件 处理完文件目录
    read_yw_dir = '/demo01\\ckrx\\new_file\\origin_file\\oldfile\\'
    read_sd_dir = '/demo01\\ckrx\\new_file\\origin_file\\sd\\'
    write_dir = '/demo01\\ckrx\\new_file\\new_file\\'

    #时间
    date = datetime.datetime.now().strftime('%Y%m%d')
    datestart = '2023-10-03'
    dateend = '2023-10-10'

    #文件
    read_yw_file = read_yw_dir + '2024-01-18' + '义乌仓库调岗、预包、计时人员明细.xlsx'
    #读取文件

    try:
        df_yw_js = pd.read_excel(read_yw_file,sheet_name=0)
    except Exception as e:
        raise e

    #清洗文件
    df_yw_js_sxb_tmp = df_yw_js.iloc[:,5:]
    df_yw_js_sxb_tmp = df_yw_js_sxb_tmp.dropna(how = 'all')
    df_yw_js_sxb = df_yw_js_sxb_tmp.T
    df_yw_js_sxb['日期'] = df_yw_js_sxb.index
    df_yw_js_sxb['日期'] = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + pd.to_timedelta(df_yw_js_sxb['日期'], unit='D')
    # 保留时间范围内的数据
    df_yw_js_sxb = df_yw_js_sxb[(df_yw_js_sxb['日期'].dt.strftime('%Y-%m-%d') >= datestart) & (
                df_yw_js_sxb['日期'].dt.strftime('%Y-%m-%d') <= dateend)]
    df_yw_js_sxb.drop('日期',axis = 1,inplace = True)

    #列向循环抽取上下班时间及时长 相同行的竖向拼接完索引也一样，保证时间不错乱
    df_yw_js_sxb_new = pd.DataFrame()
    for i in range(df_yw_js_sxb.columns.size + 1):
        if i %3 == 0 and i != 0:
            df_yw_js_sxb_tmp = df_yw_js_sxb.iloc[:,i-3:i]
            df_tmp = pd.DataFrame(df_yw_js_sxb_tmp)
            #拼接列名要一样，要不然不竖向拼接
            df_tmp.columns = ['上班时间','下班时间','时长']
            df_yw_js_sxb_new = pd.concat([df_yw_js_sxb_new,df_tmp],axis=0)
    #处理名称列
    df_yw_js_name = pd.DataFrame()
    df_yw_js_name[['姓名','岗位']] = df_yw_js[['姓名','岗位']]
    df_yw_js_name.dropna(how= 'all',inplace=True)
    df_yw_js_fuzhi = pd.DataFrame()
    for i in range(len(df_yw_js_name)):
        #此处结果是series 单向的
        tmp = df_yw_js_name.iloc[i]
        tmp1 = pd.DataFrame([tmp] *((pd.to_datetime(dateend) - pd.to_datetime(datestart)).days + 1))
        df_yw_js_fuzhi = pd.concat([df_yw_js_fuzhi,tmp1])

    #重置索引，准备左右合并处理的上班时间和姓名  横向合并两个df时必须重置索引，因为横向是按索引合并的
    #关联两个df和上述道理一样，关联条件就相当于两个df的索引，比如按上边的，就可以把关联条件置为索引列，然后直接横向拼接两个df效果一样
    #df1.join(df2)是基于索引的合并，df2必须是df1的子集，索引要匹配，df2的索引df1都要有才行

    df_yw_js_czsy = df_yw_js_fuzhi.reset_index(drop=True)
    df_yw_js_sxb_new = df_yw_js_sxb_new.reset_index()
    df_yw_js_sxb_new.rename(columns={'index':'日期'},inplace=True)
    df_yw_js_sxb_new['日期'] = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + pd.to_timedelta(df_yw_js_sxb_new['日期'], unit='D')
    df_final = pd.concat([df_yw_js_sxb_new,df_yw_js_czsy],axis = 1)

    df_final['仓库编码'] = '123456'
    df_final['仓库名称'] = 'ygp'

    #时长，金额
    df_final=df_final[df_final['上班时间'] != '休']

    df_final['上班时间'] = df_final['上班时间'].astype(str).str[-8:]
    df_final['下班时间'] = df_final['下班时间'].astype(str).str[-8:]

    df_final['时长'] = (pd.to_datetime(df_final['日期'].astype(str) +' '+ df_final['下班时间'].astype(str)) \
                     - pd.to_datetime(df_final['日期'].astype(str) +' '+df_final['上班时间'].astype(str))).dt.total_seconds()/3600

    df_final['金额'] = df_final['时长']*17

    df_final.drop(columns='岗位',inplace=True)

    print(df_final)

    # 写入文件
    df_final.to_csv(write_dir + '\\' + 'warehouse_timing_details' +
                          '_' + date + '.csv',
                          encoding="utf-8",
                          index=False)

    #转换编码



    #写入数据库

if __name__ == '__main__':
    run(object)
