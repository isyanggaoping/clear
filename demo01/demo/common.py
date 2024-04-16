import os.path as op
import os
import re
from datetime import datetime

import pandas as pd
#link的属性与方法

#属性
base_dir = op.dirname(op.dirname(op.dirname(op.dirname(op.abspath(__file__)))))
base_dir += '\\new_file\\'


#递归遍历目录下的所有目录和文件，将结果放到集合中，供后续遍历一个一个文件清洗
#
def get_all_file(filedir):
    all_file_list = []
    if op.isfile(filedir):
        all_file_list.append(next)
        return all_file_list
    else:
        list = os.listdir(filedir)
        for  list_next in list:
            all_file_list += get_all_file(list_next)
    return all_file_list
