import json
import os

FILE_NAME = "contacts_data.json"
# 读取数据 程序启动时执行
def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError,OSError):
        print("通讯录文件损坏或无法读取，已按空通讯录启动。")
        return {}
    if not isinstance(data, dict):          # 防止文件里是 [] 或 "abc"
        print("通讯录文件格式不正确，已按空通讯录启动。")
        return {} #格式校验
    return data

def save_data():
    with open(FILE_NAME,"w",encoding="utf-8") as f:
        json.dump(contacts,f,ensure_ascii=False,indent=4) #indent=4 排版
    return {}

contacts = load_data()

def add_contacts():
    name = input("请输入联系人姓名：").strip()
    if name in contacts:
        print(f"⚠️ 你添加的{name}已经存在了！")

    else:
        phone = input("请输入联系人电话：").strip()
        contacts[name] = phone
        save_data()
        print(f"✅已保存：{name}，电话：{phone}")

def show_contacts():
    if not contacts:
        print("通讯录还是空的哦！")
    else:
        print("--- 联系人列表 ---")
        for name,phone in contacts.items():
            print(f"姓名：{name}，电话{phone}")

def delete_contacts():
    if not contacts:
        print("通讯录还是空的哦！")
    else:
        names = list(contacts.keys())
        print("---请选择要删除的联系人编号 ---")
        for i in range(len(names)):
            print(f"{i+1}.{names[i]}")

        choice = input("请输入要删除的编号：").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <=choice <= len(names):
                target_name = names[choice - 1]
                del contacts[target_name]
                save_data()
                print(f"✅已成功删除：{target_name}")
            else:
                print("❌输入的编号超出范围了")
        else:
            print("❌请输入有效的数字！")

def main():
    print("欢迎使用简易通讯录！")
    while True:
        print("\n--- 菜单 ---")
        print("1.添加联系人")
        print("2.查看所有联系人")
        print("3.删除现有联系人")
        print("4.退出")

        choice = input("请选择操作（1/2/3/4）：").strip()

        if choice == "1":
            add_contacts()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            delete_contacts()
        elif choice == "4":
            print("退出程序。再见")
            break
        else:
            print("无效操作")

if __name__ == "__main__":
    main()