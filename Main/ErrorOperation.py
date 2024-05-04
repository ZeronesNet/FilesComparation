from os import getcwd
from time import strftime,localtime


class ErrorRaise(Exception):

    def __init__(self,error_code,error_type):

        self.error_code = error_code  # 错误代码
        self.error_type = error_type  # 错误类型

    def error_save(self,message):
        
        absolute_path = getcwd()

        with open(absolute_path + "\\ErrorSave.txt","a",encoding="utf-8") as f1:
            
            f1.write("="*30)
            f1.write("\n")

            f1.write("[Time]\n")
            f1.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))
            f1.write("\n")

            f1.write("[Error_Code]\n")
            f1.write(self.error_code)
            f1.write("\n")

            f1.write("[Error_Type]\n")
            f1.write(self.error_type)
            f1.write("\n")

            f1.write("[Error_Message]\n")
            f1.write(message)
            f1.write("\n")

class NeedLengthError(ErrorRaise):  # 0
    pass

class PathExistError(ErrorRaise):

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"指定了不存在的文件路径")
    
class HashMethodError(ErrorRaise):  # 1

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"指定了错误的哈希加密方式")

class PathfileExistError(ErrorRaise):  # 2

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"文件夹路径不存在或文件夹内无文件")

class HistoryExistError(ErrorRaise):  # 3

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"History.txt文件缺失")

class HistoryNoneError(ErrorRaise):  # 4

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"未检索到任何操作历史")

class KeyExistError(ErrorRaise):  # 5

    def __init__(self, error_code, error_type):
        super().__init__(error_code, error_type)
        ErrorRaise.error_save(self,"键入不存在的数字")