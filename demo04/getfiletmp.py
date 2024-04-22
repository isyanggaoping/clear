import os


def get_all_files(root_dir, files):
    """
    递归遍历指定目录，返回所有文件的路径列表。

    :param root_dir: 遍历的根目录
    :return: 包含所有文件路径的列表
    """
    # files = []  # 用于存储文件路径的列表

    # 遍历根目录下的所有文件和子目录
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)

        # 如果是文件，则添加到列表中
        if os.path.isfile(path):
            files.append(path)
            # 如果是目录，则递归遍历该目录
        elif os.path.isdir(path):
            # 不是递归作用域的问题，是因为每次调用自己就要创建一个新的空的列表 files +=  如果把列表放到main里面，传参进来会怎样？
            get_all_files(path,files)

    return files


if __name__ == '__main__':
    # 使用当前目录作为根目录
    current_dir = os.getcwd() + '\\file'
    print(current_dir)

    # 如果在此处创建空列表而不是在方法中创建，在递归调用自己时就不会创建新的空列表，就不用files.expend了
    files_path = []  # 创建一个空列表存储文件路径

    # 获取所有文件的路径列表
    all_files = get_all_files(current_dir, files_path)

    # 打印文件列表
    for file_path in all_files:
        print(file_path)