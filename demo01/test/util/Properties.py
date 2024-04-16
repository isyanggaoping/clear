#读取配置文件的类
import re


class Properties:
    def __init__(self, file_name):
        self.file_name = file_name

    #实例方法 ,在类里面定义的成为实例方法，类外面定义的是函数
    def get_properties(self):
        try:
            pro_file = open(self.file_name, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    lines = re.sub(r'(\S+)(\s*)=(\S+)(\s*)', r'\1=\3', line.replace('\n', '')).split("=")
                    properties[lines[0]] = lines[1]
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties


