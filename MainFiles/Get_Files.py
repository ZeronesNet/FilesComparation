# 模块注释
# TargetPath 指定目标路径

import os
# Get_AllFiles 函数会返回一个包含目标目录以及子目录的文件的列表
def Get_AllFiles(TargetPath):

    BigSize_Files = []
    SmallSize_Files = []

    for a in os.walk(TargetPath):

        ListLength = len(a)
        FatherPath = a[0]
        SonFile = a[ListLength - 1]

        for b in SonFile:

            file = FatherPath + "\\" + b

            if os.path.getsize(file) <= 1000:
                SmallSize_Files.append(file)
            else:
                BigSize_Files.append(file)
    
    return(BigSize_Files,SmallSize_Files)

if __name__ == '__main__':
    print("此模块不可直接运行")