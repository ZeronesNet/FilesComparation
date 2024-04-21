from os import getcwd,walk,path
from time import strftime,localtime
from re import search

def list_searcher(start_element,end_element):
    '''
    函数功能:
    读取History.txt文件中指定的两个标签之间的内容

    传入:
    起始标签,结束标签

    返回:
    包含标签之间每行内容的列表
    '''

    absolute_path = getcwd()
    
    if not path.exists(absolute_path):
        raise FileNotFoundError
    if not path.exists(absolute_path + "\\History.txt"):
        raise FileNotFoundError
    
    return_list = []

    with open(absolute_path + "\\History.txt","r",encoding="utf-8") as f1:

        start_element_list = []
        end_element_list = []

        f2 = f1.readlines()

        num = 0
        for i in f2:
            if i == start_element:
                start_element_list.append(num)
            num = num + 1

        num = 0
        for j in f2:
            if j == end_element:
                end_element_list.append(num)
            num = num + 1
        
        num = 0
        for l in start_element_list:
            return_list = return_list + f2[start_element_list[num] : end_element_list[num]]
            num = num + 1
    return(return_list)

    


def write_file(target_path,hash_method,shared_dict,length="None"):
    '''
    函数功能:
    在当前工作路径下生成两种文件

    传入:
    target_path - 本次操作的目标路径
    hash_method - 本次操作的加密方法
    shared_dict - 保存文件路径以及其哈希值的字典
    length      - shake族加密方法的字符串长度,默认为"None"

    生成:
    HashValue(x).txt - 保存50000条文件路径以及哈希值
    History.txt      - 保存用户的操作,如时间 目标路径等
    ''' 

    absolute_path = getcwd()  # 获取脚本的绝对路径
    list_shared_dict = shared_dict.items()

    # 检查文件夹内是否已经存在HashValue.txt文件夹并求出最大值
    num_list = []
    for file_list in walk(absolute_path):
        for file in file_list[len(file_list) - 1]:
            res = search(r'HashValue\(\d+\).txt',file)
            if res != None:
                num_res = search(r"\d+",res.group())
                num_list.append(int(num_res.group()))

    # 通过检查num_list的最后一个值确定start_point的值
    if len(num_list) == 0:
        start_point = 0
    elif len(num_list) == 1 and num_list[0] == 0:
        start_point = 1
    else:
        start_point = max(num_list) + 1

    # 循环取五万个文件路径以及哈希值写入一个文件
    list_path = []  # 储存下文生成的txt文件的路径

    for i in range(start_point,(len(list_shared_dict)//50000) + 1 + start_point):

        part_shared_dict = list_shared_dict[(i-start_point)*50000:((i-start_point)*50000)+49999]
        path = absolute_path + "\\HashValue({}).txt".format(str(i))

        with open(path,"w",encoding="utf-8") as f1:

            for Key,Value in part_shared_dict:

                f1.write(Key)
                f1.write("\n")
                f1.write(Value)
                f1.write("\n")
        list_path.append(path)
    
    # 将操作写入History.txt文件
    with open(absolute_path + "\\History.txt","a",encoding="utf-8") as f2:

        f2.write("[Time]\n")  # 时间
        f2.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        f2.write("\n")

        f2.write("[Target_Path]\n")  # 目标路径
        f2.write(target_path)
        f2.write("\n")

        f2.write("[Hash_Method]\n")  # 加密方法
        f2.write(hash_method)
        f2.write("\n")

        f2.write("[Length]\n")  # 字符串长度 
        f2.write(str(length))
        f2.write("\n")

        f2.write("[Create_File_Path]\n")  # 生成的HashValue(x).txt文件
        for i in list_path:
            f2.write(i)
            f2.write("\n")
        
        f2.write("[end]\n")  # 分割符
        f2.write("\n")

def read_file(file_path):
    '''
    函数功能:
    获取指定路径下所有HashValue.txt文件的路径并读取其中的内容
    将所有内容加载到一个字典中

    传入:
    指定路径

    返回:
    包含 {"文件路径":哈希值,.....} 的字典
    '''

    if file_path == '0':
        absolute_path = getcwd()
        file_path = absolute_path # 将file_path的值更改为absolute_path

    # 获取file_path下所有的 HashValue(x).txt 文件路径并储存在HashValue_path中
    HashValue_path = []

    for file_list in walk(file_path):
        for file in file_list[len(file_list) - 1]:
            res = search(r'HashValue\(\d+\).txt',file)
            if res != None:
                path = file_list[0] + "\\" + res.group()
                HashValue_path.append(path)

    # 列表为空表示HashValue.txt文件不存在,抛出错误
    if HashValue_path == []:
        raise FileNotFoundError

    # 循环读取HashValue(x).txt的内容并将值加入hash_map
    hash_map = {}

    for file in HashValue_path:

        with open(file,"r",encoding="utf-8") as f1:

            f2 = f1.readlines()
            for i in range(0,len(f2),2):
                hash_map[f2[i].replace("\n","")] = f2[i+1].replace("\n","")
    
    return(hash_map)
    
    
    

if __name__ == '__main__':
    pass