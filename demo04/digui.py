def digui(aa):
    for i in range(len(aa)):
        if isinstance(aa[i], int):
            print(aa[i])
        else:
            digui(aa[i])   # 此处不能再放循环，再放循环的话，嵌套的列表就会被打印多次

if __name__ == '__main__':
    list_in = [1, [2, [5,7,8], 6], 3, 4]
    digui(list_in)

