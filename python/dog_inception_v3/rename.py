import os

INPUT_DATA="./images"
def renameMy():
    folder = "D:\github\\usualProject\python\dog_inception_v3\images"

    for i in os.listdir(folder):
        new_name = i.split('-');
        full = ''
        for j in range(1, len(new_name)):
            full = full + new_name[j]
        print(full)
        os.rename(folder + "\\" + i, folder + "\\" + full)

def getNameList():
    result = {}

    # 获取当前目录下所有的子目录
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]
    # print(sub_dirs)
    # 得到的第一个目录是当前目录，不予考虑
    is_root_dir = True
    for sub_dir in sub_dirs:
        # print(sub_dir)
        if is_root_dir:
            is_root_dir = False
            continue
        dir_name = os.path.basename(sub_dir)
        label_name = dir_name.lower()
        result[label_name] = {
            'dir': dir_name,
        }
    print(list(result.keys())[0])



if __name__=="__main__":
    test()