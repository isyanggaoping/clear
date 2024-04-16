import pandas as pd



if __name__ == '__main__':
    df1 = pd.DataFrame({'name':['zz','ll','ww'],'age':[11,22,33]})
    df2 = pd.DataFrame({'name': ['zz', 'll', 'ww'],'age':[11,22,33],'happy':['ym', 'tq', 'yx'],'blue':['aa','bb',None]})
    df3 = pd.DataFrame({'name': ['qq', 'rr', 'tt'], 'age': [44, 55, 66]})

    mergeDfInner = pd.merge(df1,df2,on= 'name').reset_index(drop=True)
    mergeDfInner = mergeDfInner[['name','age_x','happy']]
    mergeDfInner.rename(columns={'age_x' : 'age'},inplace=True)
    #print(mergeDfInner)

    mergeDfMore = pd.merge(df1,df2,left_on=['name','age'],right_on=['name','age']).reset_index(drop=True)
    #print(mergeDfMore)

    concatDf = pd.concat([df1,df3],ignore_index=True)
    #print(concatDf)

    # 可用来判断列是否包含空值，也可筛选出想或者不想保留的行数据
    filterDf = concatDf[~concatDf['name'].isin(['zz', 'll', 'ww'])]
    resultDf = concatDf.loc[concatDf[['name','age']].isin(['qq',66]).any(axis = 1)].reset_index(drop=True)
    print(resultDf)




