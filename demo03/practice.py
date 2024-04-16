import numpy as np
import pandas as pd
import chardet

if __name__ == '__main__':
    # 创建列表或元祖
    #arr1 = np.array([1,2,3,4],dtype= float)
    # print(arr1)
    #二维数组，要求长度一样，就是列数一样
    #arr1 = np.array([[1,2,3],[4,5,6]],dtype=float)
    #print(arr1)
    #二维数组可以使用二维索引
    #a = arr1[:,0:1]
    # #转为int列表，数组不可以整体转换类型，需要循环数组内的元素，一个一个改变
    # arr2 = [int(x) for x in arr1]
    # print(arr2)
    #arr2 = [int(z) for item in arr1 for z in item] #二维数组也可以，不过要嵌套循环
    #print(arr2)

    # #转为字符串列表  用float和int输出的效果不一样
    # arr3 = [str(x) for x in arr2]
    # print(arr3)
    #转化为str,什么样就是什么样，浮点型就会带小数，int就不会有小说

    #要想使用二维数组的二维索引的方法，就必须保证二维索引里面的列表长度一致，就是列相同
    # arr4 = np.array([[1,2,3],[3,4,5]])
    # print(arr4[0][1]) #如果二维列表里面的列表长度不一致的话就只能使用这种索引方式才行
    # print(arr4[:,0:3]) #此处二维索引为左闭右开
    #
    arr5 = np.array([4,2,3,6])
    print(np.sort(arr5))  # np.sort(arr5) 返回的是一个新的数组  arr5.sort()直接作用在arr5数组上，没有返回值，直接打印这个相当于打印none
    print(arr5) #此处打印返回的还是原数组，因为上边虽然排序了，但是返回的是新的数组
    print(arr5.sort())
    #一个是numpy库的方法 把数组传参进去，返回的是一个新的数组
    #下边一个是数组的方法，调用的话直接作用到原数组上,是没有返回值的，直接打印结果为None

    # #要这样用，才能打印出结果，排完序后作用到arr5上再打印
    # arr5.sort()
    # print(arr5)


    #series 列表形式创建
    # series1 = pd.Series([1,2,3])
    # print(series1)
    # #可以手动设定索引
    # series2 = pd.Series([2,3,4],index=['a','b','c'],dtype=float,name='myseries')
    # print(series2)

    #直接给series赋值，是没有索引和名称的，给的是数字默认索引
    series1 = pd.Series([1,2,3])
    print(series1)

    #字典形式创建{索引：值}
    # series3 = pd.Series({'q':10,'w':12,'e':30})
    # print(series3)
    #
    # value = series3['q']
    # print(list)
    #
    # list = series3.tolist()
    # print(list)
    #
    # index = series3.index
    # print(index)
    #
    # #dateframe dateframe的索引需要 在关联，拼接，分组求和，就是当行有变化的时候可以重制索引，重置索引会将原来的索引保存的index列中保存下拉

    # values = [['zz','12'],['xx','11']]
    # clo = ['name','age']
    # df1 = pd.DataFrame(data=values,columns=clo)
    # print(df1)
    #
    # valnam = {'name':['aa','ss'],'age':[14,15]}
    # df2 = pd.DataFrame(valnam)
    # print(df2.size)
    # print(df2.shape)
    # print(df2.ndim)

    #读取文件
    #csv
    # path = 'D:\\lpt\\test\\demo03\\aa.csv'
    # openfile = open(path,'rb')
    # filehead = openfile.read(1024)
    # chardet = chardet.detect(filehead)  #获取编码格式
    # encoding = chardet['encoding']
    #
    # #读取csv时不确定编码，就先打开文件检测编码 然后传到参数里
    # df = pd.read_csv(filepath_or_buffer=path,encoding = encoding,header=0,index_col=None)
    # print(df)

    # df.loc[] #左右都闭合
    # df.iloc[]#左闭右开

    #axis = 0 是跨行操作
    #axis = 1 是跨列操作

    #df[这里面接受布尔]
    #df.iloc[这里面接受的是索引值]

    #字符串函数
    #contains()包含
    #replace()替换
    #lower()转成小写
    #upper()转成大写
    #split()切割字符串返回列表
    #strip()删除前导和后置的空格
    #join()字符串拼接

    #可以使用map函数进行数据转换，对字段进行数据转换
    #如一列df['gender'].map({'0':男,'1':女})
    #将对应列的数据按枚举替换

    #读取csv文件需要传参编码，如果不清楚文件编码，可以使用chardet库中的detect方法去检测
    path = 'D:\\lpt\\test\\demo03\\aa.csv'
    openfile = open(path,'rb')# 以只读形式创建文件读取对象
    readfile = openfile.read(1024)# 读取文件 前1024个字节就包含了编码信息
    detectfile = chardet.detect(readfile)# 检测文件编码 转为字典格式，包含文件的各种信息
    encoding = detectfile['encoding']# 获取encoding键对应的值
    print(encoding)
    df_read = pd.read_csv(path,encoding = encoding,index_col=False)# 读取csv文件，需要上传文件的编码格式，如果已知格式，不需要进行上述检测，可以直接写死，不过复用性不高
    print(df_read)

    #读取excel文件 只需要确定对应参数就行，读对应sheet还是所有，要不要表里的表头，等等
    #pd.read_excel(sheet_name = 这里可以是None读整个工作表，或者是数字，对应索引sheet页，或者直接是sheet页名称
    # ，head = None会默认表里都是数据，没有表头，数字的话就是对应行为表头)

    #还可以加载工作簿load_workbook  这针对表格操作
    #还可以获取工作簿ExcelFile  这针对数据操作

    #处理json文件有对应的json库可以使用
    #json字符串：json.load(json_string)
    #json文件：json_date = open(path,'rb') json.load(json_file)

    #处理接口中过来的数据,使用requests库
    #url
    #response = requests.get(url)
    #data = response.json() 如果接口中过来的是json格式的数据

    #json获取后和字典使用方式一样，因为他俩格式一样
