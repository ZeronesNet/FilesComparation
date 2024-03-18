from multiprocessing import Process,Manager,freeze_support
import hashlib
from Get_Files import Get_AllFiles

def main(Choice):

    match Choice:

        case "help":

            print("create 创建哈希文件")
            print("compare 通过读取哈希文件进行对比")
            print("exit 退出程序")
            print("\nMethod可选的方法:")
            print("md5 sha1 sha224 sha256 sha384 sha512 sha3_224")
            print("sha3_256 sha3_384 sha3_512")
            print("\n\033[32m[Success]\033[0m 操作完成")
            Exit = input("回车以返回上级菜单")
            # shake_128 shake_256 需要在hexdigest()规定长度 暂不支持

        case "create":

            HashMethod = input("Method:")
            MethodList = ["md5","sha1","sha224","sha256","sha384","sha512","sha3_224","sha3_256","sha3_384","sha3_512"]
            # 根据HashMethod的值确定不同的加密方法
            if HashMethod in MethodList:

                LargeRes_dict = Manager().dict()
                SmallRes_dict = Manager().dict()

                TarPath = input("请输入目标文件夹路径:")
                Large_Path,Small_Path = Get_AllFiles(TarPath)
                # 维护 LargeRes_list SmallRes_List 两个可被其他进程操控的字典
                # 通过 Get_AllFiles 取得不同大小的文件路径并存储在Large_Path Small_Path中

                p1 = Process(target=Large_Size,name="Large",args=(Large_Path,LargeRes_dict,HashMethod,))
                p2 = Process(target=Small_Size,name="Small",args=(Small_Path,SmallRes_dict,HashMethod,))

                p1.start()
                p2.start()
                p1.join()
                p2.join()
                LargeRes_dict.update(SmallRes_dict)
                # 统一两个字典的信息

                if len(LargeRes_dict) != 0:
                    with open(TarPath + "\\HashValue.txt","w") as F1:

                        F1.write("HashValue\n")
                        F1.write(HashMethod + "\n")
                        for File,HashValue in LargeRes_dict.items():

                            F1.write(File)
                            F1.write("\n")
                            F1.write(HashValue)
                            F1.write("\n")
                    print("\n\033[32m[Success]\033[0m 写入成功")
                    print("哈希文件已生成")
                    print("\n\033[32m[Success]\033[0m 操作完成")
                    Exit = input("回车以返回上级菜单")

                else:
                    print("\n\033[31m[Error]\033[0m 非法路径")
                    print("路径不存在或无权限访问,请以管理员身份重试")
                    Exit = input("回车以返回上级菜单")
                       
            else:
                print("\n\033[31m[Error]\033[0m 非法加密")
                print("指定不存在的加密方式,请输入help获取帮助")
                Exit = input("回车以返回上级菜单")

        case "compare":# HashMap的第一个键值为文件的加密方式

            HashMap = {}
            FileINI = input("请键入配置文件的路径:")

            try:
                with open(FileINI,"r") as F2:

                    F3 = F2.readlines()

                    num = 0
                    for i in range(0,len(F3) // 2):

                        HashMap[F3[num]] = F3[num + 1]
                        num = num + 2
                # 读取配置文件获取储存的文件路径以及哈希值,存储在HashMap
                Hash_Value_Read = HashMap["HashValue\n"]
                del HashMap["HashValue\n"]
                # 读取配置文件中的加密方式并赋值给Hash_Value_Read[:-2]
 
                LargeRes_dict = Manager().dict()
                SmallRes_dict = Manager().dict()

                TarPath = input("请输入目标文件夹路径:")
                Large_Path,Small_Path = Get_AllFiles(TarPath)
                # 维护 LargeRes_list SmallRes_List 两个可被其他进程操控的字典
                # 通过 Get_AllFiles 取得不同大小的文件路径并存储在Large_Path Small_Path中

                p1 = Process(target=Large_Size,name="Large",args=(Large_Path,LargeRes_dict,Hash_Value_Read[:-1],))
                p2 = Process(target=Small_Size,name="Small",args=(Small_Path,SmallRes_dict,Hash_Value_Read[:-1],))

                p1.start()
                p2.start()
                p1.join()
                p2.join()
                LargeRes_dict.update(SmallRes_dict)
                # 读取文件获取哈希值

                PrintResult = []

                for Key1,Value1 in HashMap.items():

                    for Key2,Value2 in LargeRes_dict.items():

                        if Value1 == Value2 + "\n":

                            PrintResult.append(Key1)
                            PrintResult.append(Key2)
                # 记录两个字典中值相等的键值
                            
                num = 0
                for i in range(0,len(PrintResult) // 2):

                    HashMap.pop(PrintResult[num])
                    LargeRes_dict.pop(PrintResult[num+1])
                    num = num + 2
                # 删去两个字典中相同的部分
                
                print("\n\033[32m[Success]\033[0m 对比完成")
                print("对比结果:")
                print("共计对比\033[32m{}\033[0m个文件".format(len(PrintResult)//2 + len(HashMap) + len(LargeRes_dict)))
                print("共有\033[32m{}\033[0m个文件通过哈希校验".format(len(PrintResult) // 2))
                print("未通过哈希校验的文件如下\n")

                print("配置文件")
                if len(HashMap) == 0:
                    print("无\n")
                else:
                    for a in HashMap.keys():
                        print(a)
                        
                print("读取文件")
                if len(LargeRes_dict) == 0:
                    print("无\n")
                else:
                    for b in LargeRes_dict.keys():
                        print(b + "\n")
                Exit = input("回车以返回上级菜单")

            except FileNotFoundError:
                print("\n\033[31m[Error]\033[0m 非法输入")
                print("配置文件不存在或无权限读取")
                Exit = input("回车以返回上级菜单")
            except TypeError as e:
                print("\n\033[31m[Error]\033[0m 非法路径")
                print("路径不存在或无权限访问,请以管理员身份重试")
                Exit = input("回车以返回上级菜单")
                raise e

            
        case _:
            print("\n\033[31m[Error]\033[0m 非法指令")
            Exit = input("回车以返回上级菜单")

def Large_Size(Large_Path,LargeRes_dict,HashMethod):

    for file in Large_Path:

        with open(file,"rb") as f1:

            text = b""
            f2 = f1.read(2048)

            if f2 == b"":
                break
            else:
                text = text + f2
        # 输出text为文件完整的二进制信息
        text = str(text)
        text = text.encode("utf-8")
        Hash = hashlib.new(HashMethod)
        Hash.update(text)
        result = Hash.hexdigest()
        LargeRes_dict[file] = result

    # 将文件路径以及其对应的哈希值维护到 LargeRes_dict 字典中
        
def Small_Size(Small_Path,SmallRes_dict,HashMethod):

    for file in Small_Path:

        with open(file,"rb") as f1:

            text = b""
            f2 = f1.read(2048)

            if f2 == b"":
                break
            else:
                text = text + f2
        # 输出text为文件完整的二进制信息
        text = str(text)
        text = text.encode("utf-8")
        Hash = hashlib.new(HashMethod)
        Hash.update(text)
        result = Hash.hexdigest()
        SmallRes_dict[file] = result
    # 将文件路径以及其对应的哈希值维护到 SmallRes_dict 字典中

if __name__ == '__main__':

    freeze_support()
    while True:

        print("\033c",end="")
        Chioice = input("请键入操作指令:")
        if Chioice == "exit":
            break
        else:
            main(Chioice)