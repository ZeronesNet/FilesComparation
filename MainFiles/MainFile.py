from multiprocessing import Process,Manager
from Get_Files import Get_AllFiles
import hashlib
from os import system
# Get_AllFiles 函数会返回一个包含目标目录以及子目录路径的列表
#1048576
HashMd5 = hashlib.md5()
# 父进程与子进程共享的两个字典

def BigFiles(List,Dict):

    for file in List:

        with open(file,"rb") as f1:

            text = b""
            f2 = f1.read(2048)

            if f2 == b"":
                break
            else:
                text = text + f2
        # 输出text为完整的文本信息
        text = str(text)
        text = text.encode("utf-8")
        HashMd5.update(text)
        result = HashMd5.hexdigest()
        Dict[file] = result

def SmallFiles(List,Dict):

    for file in List:

        with open(file,"rb") as f1:

            text = b""
            f2 = f1.read()

            if f2 == b"":
                break
            else:
                text = text + f2
        # 输出text为完整的文本信息
        text = str(text)
        text = text.encode("utf-8")
        HashMd5.update(text)
        result = HashMd5.hexdigest()
        Dict[file] = result

if __name__ == '__main__':

    while True:

        system("cls")
        system("color a")
        print("****************************")
        print("****  文件对比工具v0.1  ****")
        print("****************************")
        print("*******操作      指令*******")
        print("****************************")
        print("****生成配置文件  create****")
        print("****************************")
        print("****进行对比操作  compare***")
        print("****************************")
        print("****退出对比工具  exit******")        
        print("****************************")        
        print("\n")
        print("\n")
        print("\n")

        Choice = input("请输入操作:")
        
        if Choice == "exit":
            break

        elif Choice == "create":


            BigResult_list = Manager().dict()
            SmallResult_List = Manager().dict()
            TarPath = input("请输入文件夹路径")
            BigSize_Files,SmallSize_Files = Get_AllFiles(TarPath)

            p1 = Process(target=BigFiles,name="big",args=(BigSize_Files,BigResult_list,))
            p2 = Process(target=SmallFiles,name="small",args=(SmallSize_Files,SmallResult_List))

            p1.start()
            p2.start()
            p1.join()
            p2.join()
            SmallResult_List.update(BigResult_list)
        # 至此取得两个字典分别储存大文件和小文件以及他们的哈希值
            with open(TarPath + "py.txt","w") as F1:

                for File,HashValue in SmallResult_List.items():

                    F1.write(File)
                    F1.write("\n")
                    F1.write(HashValue)
                    F1.write("\n")

        # 功能1开发完毕，现在可以生成指定的哈希值文件
            print("down")
            ExitEnter = input("操作完成，键入回车以返回一级菜单")

        elif Choice == "compare":

            HashMap = {}
            FileINI = input("请键入配置文件的路径:")

            with open(FileINI,"r") as F2:

                F3 = F2.readlines()

                num = 0
                for i in range(0,len(F3) // 2):

                    HashMap[F3[num]] = F3[num + 1]
                    num = num + 2
            # =========================
            # 读取配置文件获取哈希值
            BigResult_list = Manager().dict()
            SmallResult_List = Manager().dict()
            TarPath = input("请输入文件夹路径")
            BigSize_Files,SmallSize_Files = Get_AllFiles(TarPath)

            p1 = Process(target=BigFiles,name="big",args=(BigSize_Files,BigResult_list,))
            p2 = Process(target=SmallFiles,name="small",args=(SmallSize_Files,SmallResult_List))

            p1.start()
            p2.start()
            p1.join()
            p2.join()
            SmallResult_List.update(BigResult_list)
            # =========================
            # 读取文件获取哈希值
            PrintResult = []

            for Key1,Value1 in HashMap.items():

                for Key2,Value2 in SmallResult_List.items():

                    if Value1 == Value2 + "\n":

                        PrintResult.append(Key1)
                        PrintResult.append(Key2)
            
            num = 0
            for i in range(0,len(PrintResult) // 2):

                HashMap.pop(PrintResult[num])
                SmallResult_List.pop(PrintResult[num+1])
                num = num + 2
            # 删去两个字典中相同的部分
                
            print("对比结果：")
            print("共计对比{}个文件".format(len(PrintResult) + len(HashMap) + len(SmallResult_List)))
            print("共有{}个文件通过哈希校验".format(len(PrintResult) // 2))
            print("未通过哈希校验的文件如下")
            print("配置文件")
            for a in HashMap.keys():
                print(a[0:-1])
            print("读取文件")
            for b in SmallResult_List.keys():
                print(b)
                    
            ExitEnter = input("操作完成，键入回车以返回一级菜单")
        else:
            ExitEnter = input("未知指令，键入回车以返回一级菜单")            