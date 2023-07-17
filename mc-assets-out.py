import os
import shutil
import sys
import json


VERSION = "1.0"


def main():
    print("="*10, "Assets Out", "="*10)
    print(f"Minecraft资源提取器(Version{VERSION})")
    print("By the-cat1")
    print("Github:https://github.com/the-cat1/mc-assets-out")
    print()
    
    if not os.path.isdir("./assets"):
        print("请把“.minecraft/assets”文件夹放在此文件旁边！")
        return -1

    print("查找indexes...")
    indexes = []
    for file in os.listdir("./assets/indexes"):
        if os.path.splitext(file)[1] == ".json":
            indexes.append(file)
    
    print("Minecraft assets indexes:")
    for index in indexes:
        print(f"    {index}")
    
    indexFile = input("请选择index文件(输入clean以删除输出目录)：")
    if indexFile == "clean":
        """删除输出目录"""
        try:
            shutil.rmtree("./out")
        except FileNotFoundError:
            print("还没有“out”文件夹！")
        else:
            print("已删除输出目录。")
        finally:
            return 0
    elif indexFile not in indexes:
        print("请选择正确的文件！")
        return -1
    indexVersion = os.path.splitext(indexFile)[0]
    

    indexObjects:dict = None
    try:
        with open(f"./assets/indexes/{indexFile}") as file:
            print("读取index文件...")
            indexObjects = json.load(file)["objects"]
    except json.decoder.JSONDecodeError:
        print("index JSON文件解析错误！")
        return -1
    except KeyError:
        print("index JSON文件格式错误！")
        return -1

    
    fail = 0
    success = 0

    for file in indexObjects.keys():
        try:
            os.makedirs(f"./out/{indexVersion}/{os.path.dirname(file)}")
        except OSError:
            pass

        try:
            hashValue = indexObjects[file]["hash"]
            shutil.copy(f"./assets/objects/{hashValue[:2]}/{hashValue}",
                        f"./out/{indexVersion}/{file}")
        except FileNotFoundError as e:
            print(f"[失败] {file}")
            print(f"    找不到文件({e})")
            fail += 1
        except KeyError as e:
            print(f"[失败] {file}")
            print(f"    index JSON文件格式错误！({e})")
            fail += 1
        except Exception as e:
            print(f"[失败] {file}")
            print(f"    未知错误({e})")
            fail += 1
        else:
            print(f"[成功] {file}")
            success += 1
    
    print()
    print("-"*32)
    print(f"完成，已输出到目录：out/{indexVersion}。")
    print(f"共计：{fail+success}文件，{success}成功，{fail}失败。")


if __name__ == "__main__":
    sys.exit(main())
