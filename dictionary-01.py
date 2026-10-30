contacts = {}

print("欢迎使用简易通讯录！")

while True:
    print("\n--- 菜单 ---")
    print("1.添加联系人")
    print("2.查看所有联系人")
    print("3.退出")


    choice = input("请选择操作（输入1/2/3）：")

    if choice == "1":
        name = input("请输入联系人姓名：")

        if name in contacts:
            print(f"你添加的{name}已经存在！")
        else:
            phone = input("请输入联系人电话：")
            contacts[name] = phone
            print(f"✅已保存：{name}的电话时{phone}")




    elif choice == "2":
        if len(contacts) == 0:
            print("通讯录还是空的哦！")
        else:
            print("--- 联系人列表 ---")
            for name , phone in contacts.items():
                print(f"姓名：{name},电话：{phone}")

    elif choice == "3":
        print("退出程序，再见！")
        break

    else:
        print("❌ 无效的选择，请重新输入")