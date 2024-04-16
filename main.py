
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    live_broadcast_columns = ['采集日期', '直播间ID', '直播间名称', '1号链接', '日期', '消耗(元)', '采集人']
    live_broadcast_cols_rename = {'采集日期': 'put_dt'
        , '直播间ID': 'live_broadcast_id'
        , '直播间名称': 'live_broadcast_name'
        , '1号链接': 'first_link'
        , '日期': 'dt'
        , '消耗(元)': 'amount'
        , '采集人': 'gatherer'}
    print(live_broadcast_columns[0])
    print(live_broadcast_cols_rename['采集日期'])

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
