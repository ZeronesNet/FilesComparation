import Hash_Get
from multiprocessing import Pool,freeze_support

def main(Choice):

    match Choice:

        case "help":

            print("create 创建哈希文件")
            print("compare 通过读取哈希文件进行对比")
            print("exit 退出程序")
            print("\nMethod可选的方法:")
            print("md5 sha1 sha224 sha256 sha384 sha512 sha3_224")
            print("sha3_256 sha3_384 sha3_512")
            print("shake_128 shake_256 会输出指定长度两倍的哈希值")
            print("\n\033[32m[Success]\033[0m 操作完成")
            Exit = input("回车以返回上级菜单")

        case "create":

            Target_Path = input("请输入目标文件夹:")
            HashMethod = input("请键入加密方法:")
            
            # 返回正确的 File_List
            try:

                Class_Hash_Get = Hash_Get.Hash_get(HashMethod=HashMethod,
                                                   File_Path=Target_Path,
                                                   Read_Size=2048)
                
                File_List = Class_Hash_Get.get_path()

                # 取首个地址计算哈希值判断是否需要Length参数
                First_Path_List = File_List[0]
                First_Path_Value = Class_Hash_Get.get_hash(First_Path_List)

                # 回收垃圾变量
                del First_Path_List
                del First_Path_Value
    
            #　产生TypeError报错,表明缺少Length参数
            except TypeError:

                Str_Length = int(input("请键入期望的哈希值长度(x2):"))

                del Class_Hash_Get
                Class_Hash_Get =Hash_Get.Hash_get(HashMethod=HashMethod,
                                                  File_Path=Target_Path,
                                                  Read_Size=2048,
                                                  Length=Str_Length)  # 销毁并生成一个新的Class_Hash_Get对象,传递参数Length
                
                File_List = Class_Hash_Get.get_path()
                
                pool = Pool(10)

                Apply_Async_Dict = {} # 储存路径与其哈希对象的字典

                # 直接在for中使用get方法会导致阻塞
                for i in File_List:
                    result = pool.apply_async(Class_Hash_Get,args=(i,))
                    Apply_Async_Dict[i] = result
                pool.close()
                pool.join()

                Path_Value_Dict ={}

                for Path,Value in Apply_Async_Dict.items():
                    Path_Value_Dict[Path] = Value.get()
                
                # 取得正确的字典
                Class_Hash_Get.file_IO(Path_Value_Dict)
                print("\n\033[32m[Success]\033[0m 写入成功")
                print("哈希文件已生成")
                print("\n\033[32m[Success]\033[0m 操作完成")
                Exit = input("回车以返回上级菜单")

            # 当目标路径输入错误时,返回以下报错信息
            except IndexError:

                print("\n\033[31m[Error]\033[0m 非法路径")
                print("指定不存在的文件路径或无权限访问")
                Exit = input("回车以返回上级菜单")

            # 当加密方法输入错误时,返回以下报错信息
            except ValueError:

                print("\n\033[31m[Error]\033[0m 非法加密")
                print("指定不存在的加密方式,请输入help获取帮助")
                Exit = input("回车以返回上级菜单")
            
            # 当取得正常的File_List 列表
            else:

                pool = Pool(10)

                Apply_Async_Dict = {} # 储存路径与其哈希对象的字典

                # 直接在for中使用get方法会导致阻塞
                for i in File_List:
                    result = pool.apply_async(Class_Hash_Get,args=(i,))
                    Apply_Async_Dict[i] = result
                pool.close()
                pool.join()

                Path_Value_Dict ={}

                for Path,Value in Apply_Async_Dict.items():
                    Path_Value_Dict[Path] = Value.get()
                
                # 取得正确的字典
                Class_Hash_Get.file_IO(Path_Value_Dict,"w")
                print("\n\033[32m[Success]\033[0m 写入成功")
                print("哈希文件已生成")
                print("\n\033[32m[Success]\033[0m 操作完成")
                Exit = input("回车以返回上级菜单")
        
        case "compare":

            INI_File = input("请键入配置文件的路径:")
            Target_Path = input("请输入目标文件夹路径:")
            Read_Path_Value = {}

            try:
                with open(INI_File,"r") as F2:
                    F3 = F2.readlines()

                    num = 0
                    for i in range(0,len(F3) // 2):

                        Read_Path_Value[F3[num]] = F3[num + 1]
                        num = num + 2
                    
                # 读取加密方法并储存在Read_Hash_Method        
                Read_Hash_Method = Read_Path_Value["HashValue\n"]
                Read_Hash_Method = Read_Hash_Method[:-1]
                del Read_Path_Value["HashValue\n"]

                # 读取首个文件的哈希值计算长度,方便后续shake族的使用
                Value_Length = (len(F3[3]) - 1) // 2

                # 根据加密方法不同实例化不同的Class_Hash_Get对象
                if Read_Hash_Method == "shake_128" or Read_Hash_Method == "shake_256":
                    Class_Hash_Get =Hash_Get.Hash_get(HashMethod=Read_Hash_Method,
                                                      File_Path=Target_Path,
                                                      Read_Size=2048,
                                                      Length=Value_Length)
                else:
                    Class_Hash_Get =Hash_Get.Hash_get(HashMethod=Read_Hash_Method,
                                                      File_Path=Target_Path,
                                                      Read_Size=2048)
                File_List = Class_Hash_Get.get_path() # 取得正常的文件路径列表

            except FileNotFoundError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("配置文件不存在或无权限读取")
                Exit = input("回车以返回上级菜单")

            except TypeError:
                print("\n\033[31m[Error]\033[0m 非法路径")
                print("路径不存在或无权限访问,请以管理员身份重试")
                Exit = input("回车以返回上级菜单")

            else:

                pool = Pool(10)

                Apply_Async_Dict = {} # 储存路径与其哈希对象的字典

                # 直接在for中使用get方法会导致阻塞
                for i in File_List:
                    result = pool.apply_async(Class_Hash_Get,args=(i,))
                    Apply_Async_Dict[i] = result
                pool.close()
                pool.join()

                Path_Value_Dict ={}

                for Path,Value in Apply_Async_Dict.items():
                    Path_Value_Dict[Path] = Value.get()
                
                # 取得正确的字典 Read_Path_Value Path_Value_Dict
                
                PrintResult = []

                for Key1,Value1 in Read_Path_Value.items():

                    for Key2,Value2 in Path_Value_Dict.items():

                        if Value1 == Value2 + "\n":

                            PrintResult.append(Key1)
                            PrintResult.append(Key2)
                            del Path_Value_Dict[Key2]
                            break
                            # (100) => (690)
                            # 哈希值发生了碰撞
                # 记录两个字典中值相等的键值
                
                num = 0

                for i in range(0,len(PrintResult) // 2):

                    Read_Path_Value.pop(PrintResult[num])
                    num = num + 2
                # 删去两个字典中相同的部分

                
                print("\n\033[32m[Success]\033[0m 对比完成")
                print("对比结果:")
                print("共计对比\033[32m{}\033[0m个文件".format(len(PrintResult)//2 + len(Read_Path_Value) + len(Path_Value_Dict)))
                print("共有\033[32m{}\033[0m个文件通过哈希校验".format(len(PrintResult) // 2))
                Exit = input()
                print("未通过哈希校验的文件如下\n")

                print("HashValue.txt所读取的文件:")
                if len(Read_Path_Value) == 0:
                    print("无\n")
                else:
                    for a in Read_Path_Value.keys():
                        print(a)
                Exit = input()
                print("目标文件夹路径所读取的文件:")
                if len(Path_Value_Dict) == 0:
                    print("无\n")
                else:
                    for b in Path_Value_Dict.keys():
                        print(b + "\n")
                Exit = input("回车以返回上级菜单")

        
        case _:
            print("\n\033[31m[Error]\033[0m 非法指令")
            print("指定不存在的操作指令,请输入help获取帮助")
            Exit = input("回车以返回上级菜单")

if __name__ == '__main__':

    freeze_support()
    while True:

        print("\033c",end="")
        Choice = input("请键入操作指令:")
        if Choice == "exit":
            break
        else:
            main(Choice)