"""简易通讯录：06_function_contacts.py 与 07_file_test.py 的整合版。

规则：业务函数只接收参数、返回结果，不碰 input()；
所有屏幕交互都集中在 main() 里，方便单独测试。
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "contacts_data.json")


def load_data(path):
    """读取通讯录；文件不存在、损坏或格式不对时返回空字典。"""
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("通讯录文件损坏或无法读取，已按空通讯录启动。")
        return {}

    if not isinstance(data, dict):
        print("通讯录文件格式不正确，已按空通讯录启动。")
        return {}

    return data


def save_data(path, contacts):
    """把通讯录写入文件，成功返回 True。"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(contacts, f, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"保存失败：{error}")
        return False

    return True


def add_contact(contacts, name, phone):
    """新增联系人，返回 (是否成功, 提示信息)。"""
    if not name:
        return False, "姓名不能为空"
    if not phone:
        return False, "电话不能为空"
    if name in contacts:
        return False, f"你添加的{name}已经存在了"

    contacts[name] = phone
    return True, f"已保存：{name}，电话：{phone}"


def format_contacts(contacts):
    """返回带编号的名单，例如 "1.张三  电话：13800000000"。"""
    lines = []
    for index, (name, phone) in enumerate(contacts.items(), start=1):
        lines.append(f"{index}.{name}  电话：{phone}")
    return lines


def delete_contact(contacts, number):
    """按从 1 开始的编号删除，返回 (是否成功, 提示信息)。"""
    names = list(contacts.keys())
    if not 1 <= number <= len(names):
        return False, "输入的编号超出范围了"

    target_name = names[number - 1]
    del contacts[target_name]
    return True, f"已成功删除：{target_name}"


def ask(text):
    """读一行输入并去掉首尾空格。"""
    return input(text).strip()


def main():
    contacts = load_data(FILE_NAME)
    print("欢迎使用简易通讯录！")

    while True:
        print("\n--- 菜单 ---")
        print("1.添加联系人")
        print("2.查看所有联系人")
        print("3.删除现有联系人")
        print("4.退出")

        choice = ask("请选择操作（1/2/3/4）：")

        if choice == "1":
            name = ask("请输入联系人姓名：")
            if not name:
                print("姓名不能为空")
                continue
            phone = ask("请输入联系人电话：")
            ok, message = add_contact(contacts, name, phone)
            print(message)
            if ok:
                save_data(FILE_NAME, contacts)

        elif choice == "2":
            lines = format_contacts(contacts)
            if not lines:
                print("通讯录还是空的哦！")
                continue
            print("--- 联系人列表 ---")
            for line in lines:
                print(line)

        elif choice == "3":
            lines = format_contacts(contacts)
            if not lines:
                print("通讯录还是空的哦！")
                continue
            print("--- 请选择要删除的联系人编号 ---")
            for line in lines:
                print(line)

            text = ask("请输入要删除的编号：")
            if not text.isdigit():
                print("请输入有效的数字！")
                continue

            ok, message = delete_contact(contacts, int(text))
            print(message)
            if ok:
                save_data(FILE_NAME, contacts)

        elif choice == "4":
            print("退出程序。再见！")
            break

        else:
            print("无效的选择！")


if __name__ == "__main__":
    main()
