from multiprocessing import Process,Manager,freeze_support
import HashProcess
import FileOpertion

def multProcess(target_path,hash_method,length="None"):
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



def main(choice):

    match choice:

        case "help":

            print("create 创建哈希文件")
            print("compare 通过读取哈希文件进行对比")
            print("exit 退出程序")
            print("\nMethod可选的方法:")
            print("md5 sha1 sha224 sha256 sha384 sha512 sha3_224")
            print("sha3_256 sha3_384 sha3_512")
            print("shake_128 shake_256\n")
            print("请尽量将exe文件放在单独的文件夹中")
            print("使用过程中会产生HashValue(x).txt和history.txt文件,请不要删除或移动")
            print("\n\033[32m[Success]\033[0m 操作完成")
            exit = input("回车以返回上级菜单")

        case "create":

            # 基础信息的初始化
            target_path = input("请输入目标文件夹路径:")
            hash_method = input("请键入加密方法:")


            # 实例化HashProcess对象
            # !!!与函数中重复,着手优化中
            Hash = HashProcess.Hash_Process(file_path=target_path,hash_method=hash_method)


            try:
                # 测试用,能够抛出不同的异常
                Hash.hash_test("test")

                shared_dict = multProcess(target_path,hash_method)

                FileOpertion.write_file(target_path,hash_method,shared_dict)

                print("\n\033[32m[Success]\033[0m 操作完成")
                exit = input("回车以返回上级菜单")
                
            except TypeError:
                
                length = int(input("请输入字符串长度:"))

                shared_dict = multProcess(target_path,hash_method,length)

                FileOpertion.write_file(target_path,hash_method,shared_dict,length)

                print("\n\033[32m[Success]\033[0m 操作完成")
                exit = input("回车以返回上级菜单")

            except ValueError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("指定了不存在的哈希加密方式,输入help以查看帮助")
                exit = input("回车以返回上级菜单")
            except IndexError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("指定了不存在的文件路径,输入help以查看帮助")
                exit = input("回车以返回上级菜单")
            except Exception:
                print("\n\033[31m[Error]\033[0m 未知错误")
                print("产生了未知的错误,请尝试重启应用")
                exit = input("回车以返回上级菜单")              

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
            choice_num = input("请输入数字")
            history_operation = choice_list[choice_num]

            # 从列表中读取相关信息
            target_path = history_operation[0].replace("\n","")
            hash_method = history_operation[1].replace("\n","")
            length = history_operation[2].replace("\n","")

            # 计算得到第一个字典
            target_hash_value = multProcess(target_path,hash_method,length=length)

            # 调用 FileOpertion.read_file() 获取另一个字典
            read_path = input("(path)>")
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

            print("配置文件")
            if len(target_hash_value) == 0:
                print("无\n")
            else:
                for a in target_hash_value.keys():
                    print(a)
                    
            print("读取文件")
            if len(read_hash_value) == 0:
                print("无\n")
            else:
                for b in read_hash_value.keys():
                    print(b)
            Exit = input("回车以返回上级菜单")

        case _:
            print("\n\033[31m[Error]\033[0m 非法指令")
            Exit = input("回车以返回上级菜单")



if __name__ == '__main__':#

    freeze_support()

    while True:

        print("\033c",end="")
        choice = input("请键入操作指令:")
        if choice == "exit":
            break
        else:
            main(choice)