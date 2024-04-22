import os


def get_all_filepath(filedir, filelist):
    for item in os.listdir(filedir):
        files_path = os.path.join(filedir, item)

        if os.path.isfile(files_path):
            filelist.append(files_path)
        else:
            get_all_filepath(files_path, filelist)
    return filelist

if __name__ == '__main__':

    file_dir = 'D:\\lpt\\test\\demo04\\file'
    files = []

    all_files = get_all_filepath(file_dir, files)

    for i in all_files:
        print(i)