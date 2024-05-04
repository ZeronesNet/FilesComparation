from multiprocessing import Process,Manager,freeze_support
import HashProcess
import FileOpertion
from ErrorOperation import *

def mult_process(target_path,hash_method,length="None"):
    '''
    函数功能:
    多进程计算target_path下所有文件的哈希值,并以键值对的形式储存在shared_dict中

    传入:
    文件路径,加密方法,字符串长度(可选)

    返回:
    包含 {文件路径:哈希值,.....}的字典
    '''

    # 建立一个可以在进程之间共享的字典
    manager = Manager()
    shared_dict = manager.dict()

    # 实例化HashProcess对象
    Hash = HashProcess.Hash_Process(file_path=target_path,hash_method=hash_method)

    List_1,List_2,List_3,List_4,List_5 = Hash.get_path()  # 取到包含不同大小文件的5个列表

    if hash_method == "shake_128" or hash_method == "shake_256":
        P1 = Process(target=Hash.get_hash,name="Process_1",args=(List_1,1024,shared_dict,int(length)))
        P2 = Process(target=Hash.get_hash,name="Process_2",args=(List_2,2048,shared_dict,int(length)))
        P3 = Process(target=Hash.get_hash,name="Process_3",args=(List_3,3072,shared_dict,int(length)))
        P4 = Process(target=Hash.get_hash,name="Process_4",args=(List_4,4096,shared_dict,int(length)))
        P5 = Process(target=Hash.get_hash,name="Process_5",args=(List_5,5120,shared_dict,int(length)))
    else:
        P1 = Process(target=Hash.get_hash,name="Process_1",args=(List_1,1024,shared_dict))
        P2 = Process(target=Hash.get_hash,name="Process_2",args=(List_2,2048,shared_dict))
        P3 = Process(target=Hash.get_hash,name="Process_3",args=(List_3,3072,shared_dict))   
        P4 = Process(target=Hash.get_hash,name="Process_4",args=(List_4,4096,shared_dict))
        P5 = Process(target=Hash.get_hash,name="Process_5",args=(List_5,5120,shared_dict))

    P1.start()
    P2.start()
    P3.start()
    P4.start()
    P5.start()

    P1.join()
    P2.join()
    P3.join()
    P4.join()
    P5.join()
    return(shared_dict)

def hash_test(hash_method):
    '''
    函数功能:通过对hash_method的判断抛出不同的错误

    传入
    hash_method - 指定的哈希加密方法

    返回
    无
    '''
    hash_list_1 = ["md5","sha1","sha224","sha256","sha384","sha512","sha3_224",
                 "sha3_224","sha3_256","sha3_384","sha3_512"]
    hash_list_2 = ["shake_128","shake_256"]

    if hash_method in hash_list_1:
        pass
    elif hash_method in hash_list_2:
        error = NeedLengthError("0","need length")
        raise error
    else:
        error = HashMethodError("1","Wrong Hash Method")
        raise error


def main(operation,target_path,hash_method,read_path,length):

    match operation:

        case "help":

            print("\n哈希加密方法:")
            print("md5,sha1,sha224,sha256,sha384,sha512")
            print("sha3_224,sha3_256,sha3_384,sha3_512")
            print("shake3_128,shake3_256\n")

            print("可供执行的命令有:\033[32mcreate compare\033[0m\n")
            print("create命令将计算文件的哈希值并将其与文件路径保存在HashValue.txt中")
            print("Example -> create -p [file path] -m [hash method] -l [str length]")
            print("1.create -p D:\Tools -m md5")
            print("2.create -p D:\Tools -m shake_128 -l 10")
            print("-l 允许用户在 -m 的参数为shake_128或shake_256时自定义字符串长度\n")

            print("compare命令将读取本地历史文件以及HashValue文件并比较哈希值")
            print("Example -> compare -r [file_path]")
            print("1.compare -r D:\Tools")
            print("2.compare -r 0")
            print("当-r的参数为0时,使用exe文件所在目录\n")
            Exit = input("回车以返回上级菜单")

        case "create":

            try:
                hash_test(hash_method)
                # 测试用,能够抛出不同的异常

                shared_dict = mult_process(target_path,hash_method)

                FileOpertion.write_file(target_path,hash_method,shared_dict)

                print("\n\033[32m[Success]\033[0m 操作完成")
                exit = input("回车以返回上级菜单")
                
            except NeedLengthError:

                shared_dict = mult_process(target_path,hash_method,length)

                FileOpertion.write_file(target_path,hash_method,shared_dict,length)

                print("\n\033[32m[Success]\033[0m 操作完成")
                exit = input("回车以返回上级菜单")

            except HashMethodError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("指定了不存在的哈希加密方式,输入help以查看帮助")
                exit = input("回车以返回上级菜单")

            except PathfileExistError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("指定了不存在的文件路径,输入help以查看帮助")
                exit = input("回车以返回上级菜单")
                
            except Exception:
                print("\n\033[31m[Error]\033[0m 未知错误")
                print("产生了未知的错误,请尝试重启应用")
                raise Exception         

        case "compare":

            choice_list = {}  # 储存后续 {数字:[文件路径 哈希加密 字符串长度],........}
            return_list = FileOpertion.list_searcher("[Target_Path]\n","[Create_File_Path]\n")

            # 计算得到{数字:[文件路径 哈希加密 字符串长度],........}
            for i in range(0,len(return_list),6):

                part_return_list = return_list[i:i+6]
                print_result = ""
                for j in part_return_list:
                    print_result = print_result + j.replace("\n","") + "\t"
                print(str(i//6) + " => " + print_result)
                part_return_list.remove('[Target_Path]\n')
                part_return_list.remove('[Hash_Method]\n')
                part_return_list.remove('[Length]\n')
                choice_list[str(i//6)] = part_return_list

            # 通过用户输入数字寻找指定列表
            choice_num = input("请输入数字->")
            history_operation = choice_list[choice_num]  # 应该没有人会瞎输吧?

            # 从列表中读取相关信息
            target_path = history_operation[0].replace("\n","")
            hash_method = history_operation[1].replace("\n","")
            length = history_operation[2].replace("\n","")

            # 计算得到第一个字典
            target_hash_value = mult_process(target_path,hash_method,length=length)

            # 调用 FileOpertion.read_file() 获取另一个字典
            read_hash_value = FileOpertion.read_file(read_path)

            # 记录两个字典中值相等的键值,并添加到PrintResult中            
            PrintResult = []

            for Key1,Value1 in target_hash_value.items():

                for Key2,Value2 in read_hash_value.items():

                    if Value1 == Value2:

                        PrintResult.append(Key1)
                        del read_hash_value[Key2]
                        break

            # 删去两个字典中相同的部分
            num = 0
            for i in range(0,len(PrintResult)):

                target_hash_value.pop(PrintResult[num])
                num = num + 1

            print("\n\033[32m[Success]\033[0m 对比完成")
            print("对比结果:")
            print("共计对比\033[32m{}\033[0m个文件".format(len(PrintResult)//2 + len(target_hash_value) + len(read_hash_value)))
            print("共有\033[32m{}\033[0m个文件通过哈希校验".format(len(PrintResult) // 2))
            print("未通过哈希校验的文件如下\n")

            print("回车查看配置文件")
            Exit = input()
            if len(target_hash_value) == 0:
                print("无\n")
            else:
                for a in target_hash_value.keys():
                    print(a)
                    
            print("回车读取文件")
            Exit = input()
            if len(read_hash_value) == 0:
                print("无\n")
            else:
                for b in read_hash_value.keys():
                    print(b)
            Exit = input("回车以返回上级菜单")

        case _:
            print("\n\033[31m[Error]\033[0m 非法指令")
            Exit = input("回车以返回上级菜单")



if __name__ == '__main__':

    freeze_support()

    while True:

        print("\033c",end="")
        user_input = input("FileComparation>:")
        splited_user_input = user_input.split(" ")

        # 提取 操作 路径 加密方法等信息
        operation = splited_user_input[0]
        target_path = ""
        hash_method = ""
        length = 6
        read_path = "0"

        num = 0
        for i in splited_user_input:
            
            if   splited_user_input[num] == "-p":
                target_path = splited_user_input[num + 1]
                
            elif splited_user_input[num] == "-m":
                hash_method = splited_user_input[num + 1]

            elif splited_user_input[num] == "-l":
                length = splited_user_input[num + 1]

            elif splited_user_input[num] == "-r":
                read_path = splited_user_input[num + 1]
            num = num + 1

        if operation == "exit":
            break
        else:
            main(operation=operation,target_path=target_path,hash_method=hash_method,read_path=read_path,length=length)