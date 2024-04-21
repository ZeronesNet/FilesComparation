from os import walk,path
from hashlib import new

class Hash_Process(object):
    '''哈希加密'''

    def __init__(self,file_path,hash_method):

        self.file_path = file_path  # 指定的文件路径
        self.hash_method = hash_method  # 指定的哈希加密方法
   
    def get_path(self):
        '''
        函数功能:
        遍历self.File_Path下的所有文件并计算大小,分别储存在不同的列表

        传入:
        无 直接调用即可

        返回:
        file_list_1 -> 0-500MB
        file_list_2 -> 501-1GB
        file_list_3 -> 1-5GB
        file_list_4 -> 5-10GB
        file_list_5 -> >10GB
        '''
        
        file_list_1 = []
        file_list_2 = []
        file_list_3 = []
        file_list_4 = []
        file_list_5 = []
        
        print("\033[32m[Success]\033[0m 获取文件路径中")

        for file_1 in walk(self.file_path):

            father_path = file_1[0]  # 最上层文件夹的路径
            son_path = file_1[len(file_1) - 1]  # 相对文件路径的列表

            for file_2 in son_path:

                file = father_path + "\\" + file_2  # 取得文件的绝对路径
                File_Size = path.getsize(file)

                if File_Size <= 5E+05:
                    file_list_1.append(file)
                elif 5E+05 < File_Size <= 1E+06:
                    file_list_2.append(file)
                elif 1E+06 < File_Size <= 5E+07:
                    file_list_3.append(file)
                elif 5E+07 < File_Size <= 1E+08:
                    file_list_4.append(file)
                else:
                    file_list_5.append(file)
        
        all_file_list = file_list_1 + file_list_2 + file_list_3 + file_list_4 + file_list_5
        if all_file_list == []:
            raise ArithmeticError
        else:
            return(file_list_1,file_list_2,file_list_3,file_list_4,file_list_5)

    def get_hash(self,file_path,read_size,res_dict,length=None):
        '''
        函数功能:
        遍历file_path列表 读取单文件进行哈希值加密
        向进程共享字典中添加键值对 -> path:hashvalue

        传入:
        文件路径列表,单次读取块大小,进程共享字典,字符串长度(可选)

        返回:
        无
        '''
        hash_value = new(self.hash_method)

        for i in range(len(file_path) - 1,-1,-1):  # 逆序读取列表

            single_file_path = file_path[i]  # 取得当前列表的最后一项

            with open(single_file_path,"rb") as f1:

                text = ""

                while True:

                    f2 = f1.read(read_size)

                    # 检测文件是否读取完以及text的长度
                    if f2 == b"" and len(text) <= 512000: 
                        break

                    # text长度超过限制则计算text的哈希值并重新赋给text
                    elif f2 != b"" and len(text) > 512000: 
                        hash_value.update(text.encode("utf-8"))

                        if length==None:
                            Res_f2 = hash_value.hexdigest()
                            text = Res_f2
                        else:
                            Res_f2 = hash_value.hexdigest(length)
                            text = Res_f2

                    # 计算读取块的哈希值并累加到text中         
                    else:
                        hash_value.update(f2)

                        if length==None:
                            Res_f2 = hash_value.hexdigest()
                            text = text + Res_f2
                        else:
                            Res_f2 = hash_value.hexdigest(length)
                            text = text + Res_f2                            
                
                # 最后计算text的值
                hash_value.update(text.encode("utf-8"))

                if length == None:
                    Result = hash_value.hexdigest()
                    print("\033[32m[Success]\033[0m 计算完成\t" + single_file_path)
                    res_dict[single_file_path] = Result
                else:
                    Result = hash_value.hexdigest(length)
                    print("\033[32m[Success]\033[0m 计算完成\t" + single_file_path)
                    res_dict[single_file_path] = Result

            # 信息写入Res_Dict后执行以下代码
            # 从列表中删除所计算的文件路径以节省内存
            del file_path[i]

    def hash_test(self,test_str):
        '''
        函数功能:
        在try语句下调用,通过不对hexdigest()传入参数是否产生所悟
        判断是否需要传参数

        传入
        test_str - 测试用的字符串

        返回
        无
        '''

        hash_value = new(self.hash_method)  # 加密
        hash_value.update(test_str.encode("utf-8"))
        hash_value.hexdigest()
        
if __name__ == '__main__':
    pass