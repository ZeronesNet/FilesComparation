'''
编写者:ZeroNet
最新编写日期:2024/3/29
模块功能说明
通过实例化对象可以完成
1.指定路径下所有文件的绝对路径获取
2.单文件的哈希值计算
3.配置文件的生成
'''
from hashlib import new
from os import walk

class Hash_get(object):

    def __init__(self, HashMethod,File_Path,Read_Size,Length=None):

        self.HashMethod = HashMethod # 用于指定哈希加密方法
        self.Length = Length         # 用于指定shake族下的字符串长度
        self.File_Path = File_Path   # 用于指定所读取的文件夹路径
        self.Read_Size = Read_Size   # 用于指定一次读取的数据块大小

    def __call__(self,File_Path):
        # 实现多进程时的对象调用
        Hash_Value = self.get_hash(File_Path=File_Path)
        return(Hash_Value)

    def get_path(self):
        '''
        遍历self.File_Path下的所有文件
        储存在 File_List 中
        '''
        
        File_List = []

        for file_1 in walk(self.File_Path):

            Father_Path = file_1[0]
            Son_Path = file_1[len(file_1) - 1]

            for file_2 in Son_Path:

                file = Father_Path + "\\" + file_2
                File_List.append(file)

        if len(File_List) == 0:
            raise IndexError # 判断列表是否为空,是则为Main.py抛出IndexError
        else:
            return(File_List)

    def get_hash(self,File_Path):
        '''
        以二进制方式读取File_Path
        并进行哈希值加密
        返回单文件的哈希值
        '''
        with open(File_Path,"rb") as f1:

            text = b""

            while True:

                f2 = f1.read(self.Read_Size)
                if f2 == b"":
                    break
                else:
                    text = text + f2
        
            text = str(text)
            text = text.encode("utf-8")
            HashValue = new(self.HashMethod)
            HashValue.update(text)

            if self.Length == None:
                Result = HashValue.hexdigest()
                return(Result)
            else:
                Result = HashValue.hexdigest(self.Length)
                return(Result)
    
    def file_IO(self,Path_OR_Dict):
        '''
        本意是想将文件读写使用一个函数操控
        后经考虑保留以减少main中的代码量
        '''

        with open(self.File_Path + "\HashValue.txt","w") as F1:

            F1.write("HashValue\n")
            F1.write(self.HashMethod + "\n")
            for File,HashValue in Path_OR_Dict.items():

                F1.write(File)
                F1.write("\n")
                F1.write(HashValue)
                F1.write("\n")

if __name__ == '__main__':
    pass
