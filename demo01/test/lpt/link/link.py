from datetime import datetime

from common import *
from demo01.test.util.DbUtil import DbManage

live_broadcast_columns = ['采集日期', '直播间ID', '直播间名称', '1号链接', '日期', '消耗(元)', '采集人']
video_columns = ['采集日期', '商品ID', '商品名称', '日期', '消耗(元)', '采集人']

#直播视频链接推广费
def run(dbManager):
    path = datetime.now().strftime('%Y%m%d')
    #日期获取文件夹目录
    dir_path = op.join(base_dir,path)
    print(dir_path)
    #获取文件夹下的所有文件目录集合
    filePathArray = getAllFilePath(dir_path)
    #遍历集合处理表格数据
    df_video = pd.DataFrame(columns=video_columns)
    df_live_broadcast = pd.DataFrame(columns=live_broadcast_columns)

    for next in filePathArray:
        df_new = readData(next)
        if df_new['fileType'] == '视频':

            df_video = pd.concat([df_video,df_new['df']],axis=0,ignore_index=True)
        elif df_new['fileType'] == '直播':

            df_live_broadcast = pd.concat([df_live_broadcast, df_new['df']], axis=0, ignore_index=True)
        print(df_live_broadcast)

if __name__ == '__main__':
    lM = DbManage()
    run(lM)

