import pandas as pd
import os
if __name__ == '__main__':
    print(os.path.abspath(__file__))
    orig_path = 'D:\\lpt\\test\\demand\\old_file\\out.xlsx'
    sheetdf = pd.read_excel(orig_path,sheet_name=None,header=None)

    dfs = {}

    #这样读取没有表头
    for sheetname,df in sheetdf.items():
        if sheetname in ['售后问题总表','退货跟进','微信免单打款']:
            #print(df.columns)
            #处理
            for i in range(len(df.columns)):
                if df.iloc[0,i] != df.iloc[1,i]:
                    df.iloc[0,i] = df.iloc[0,i] + '_' + df.iloc[1,i]
                    df.columns = df.iloc[0].tolist()
            df = df.iloc[2:]
            dfs[sheetname] = df
        dfs[sheetname] = df

    with pd.ExcelWriter('D:\\lpt\\test\\demand\\new_file\\out1.xlsx',engine='xlsxwriter') as writer:
        for sheetname,df in dfs.items():
            df.to_excel(writer,sheet_name=sheetname,index=False)