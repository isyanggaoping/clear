import os
import numpy as np
import pandas as pd
import chardet

if __name__ == '__main__':
    #获取文件
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\file\\'
    file_path += os.listdir(file_path)[0]
    print(file_path)

    # 创建列表或元祖
    arr1 = np.array([1,2,3,4],dtype= float)
    print(arr1)
    # 二维数组，要求长度一样，就是列数一样
    arr1 = np.array([[1,2,3],[4,5,6]],dtype=float)
    print(arr1)
    # 二维数组可以使用二维索引
    a = arr1[:,0:1]
    # #转为int列表，数组不可以整体转换类型，需要循环数组内的元素，一个一个改变
    #arr2 = [int(x) for x in arr1]
    # print(arr2)
    arr2 = [int(z) for item in arr1 for z in item] #二维数组也可以，不过要嵌套循环
    print(arr2)

    # 读取文件
    # csv
    path = 'D:\\lpt\\test\\demo03\\aa.csv'
    openfile = open(path,'rb')
    filehead = openfile.read(1024)
    chardet = chardet.detect(filehead)  #获取编码格式
    encoding = chardet['encoding']

    #读取csv时不确定编码，就先打开文件检测编码 然后传到参数里
    df = pd.read_csv(filepath_or_buffer=path,encoding = encoding,header=0,index_col=None)
    print(df)