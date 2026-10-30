contacts = {}

def add_contacts():
    name = input("请输入联系人姓名：").strip()
    if name in contacts:
        print(f"⚠️ 你添加的{name}已经存在了！")
    else:
        phone = input("请输入联系人电话：").strip()
        contacts[name] = phone
        print(f"✅已保存：{name}，电话：{phone}")

def show_contacts():
    if not contacts:
        print("通讯录还是空的哦！")
    else:
        print("--- 联系人列表 ---")
        for name , phone in contacts.items():
            print(f"姓名：{name}，电话：{phone}")

def delete_contacts():
    if not contacts:
        print("通讯录还是空的哦！")
        return
         
    names = list(contacts.keys())
    print("---请选择要删除的联系人编号：---")
        
    for index, name in enumerate(names, start=1):
        print(f"{index}.{name}")

    choice = input("请输入要删除的编号：").strip()

    if not choice.isdigit():
        print("请输入有效数字！")
        return
    
    number = int(choice)
    if not 1<= number <= len(names):
        print("输入的编号超出范围了！")
        return
    target_name = names[number - 1]
    del contacts[target_name]
    print(f"✅已成功删除:{target_name}")


def main():
    print("欢迎使用简易通讯录！")
    while True:
        print("\n--- 菜单 ---")
        print("1.添加联系人")
        print("2.查看所有联系人")
        print("3.删除现有联系人")
        print("4.退出")

        choice = input("请选择操作(输入1/2/3/4):")

        if choice == "1":
            add_contacts()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            delete_contacts()
        elif choice == "4":
            print("退出程序。再见！")
            break
        else:
            print("❌无效的选择！")

if __name__ == "__main__":
    main()
#先列出所有联系人并打上编号
#然后选择编号进行删除