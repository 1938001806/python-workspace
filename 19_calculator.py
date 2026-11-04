import json
import os


file_name = "history_calcilator.json"
history = []

def load_data():
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError,OSError):
        return []
    
def save_history():
    with open(file_name,"w",encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
def show_history():
    if len(history) == 0:
        print("暂无历史记录")
    else:
        for item in history:
            print(item)

def addition():
    print("--- 欢迎使用加法 ---")
    try:
        num1 = float(input("请输入第一个数字：").strip()) # 用 float 可以支持小数
        num2 = float(input("请输入第二个数字：").strip())
        result = num1 + num2

        record = f"{num1}+{num2}={result:.2f}"
        history.append(record)
        save_history()

        print(f"✅ 结果：{num1}+{num2}={result:.2f}")
    except ValueError:
        print("❌ 输入的不是有效数字！")
def subtraction():
    print("--- 欢迎使用减法 ---")
    try:
        num1 = float(input("请输入第一个数字：").strip())
        num2 = float(input("请输入第二个数字：").strip())
        result = num1 - num2

        record = f"{num1}-{num2}={result:.2f}"
        history.append(record)
        save_history()

        print(f"✅ 结果：{num1}-{num2}={result:.2f}")
    except ValueError:
        print("❌ 输入的不是有效数字！")

def multiplication():
    print("--- 欢迎使用乘法 ---")
    try:
        num1 = float(input("请输入第一个数字：").strip())
        num2 = float(input("请输入第二个数字：").strip())
        result = num1 * num2

        record = f"{num1}*{num2}={result:.2f}"
        history.append(record)
        save_history()

        print(f"✅ 结果：{num1}*{num2}={result:.2f}")
    except ValueError:
        print("❌ 输入的不是有效数字！")

def divisionmethed():
    print("--- 欢迎使用除法 ---")
    try:
        num1 = float(input("请输入第一个数字：").strip())
        num2 = float(input("请输入第二个数字：").strip())
        result = num1 / num2

        record = f"{num1}/{num2}={result:.2f}"
        history.append(record)
        save_history()

        print(f"✅ 结果：{num1}/{num2}={result:.2f}")
    except ValueError:
        print("❌ 输入的不是有效数字！")
    except ZeroDivisionError:
        print("❌ 数学老师警告：除数不能为 0！")


def main():
    global history
    history = load_data()
    print("欢迎使用简易计算器")
    while True:
        print("1.加法")
        print("2.减法")
        print("3.乘法")
        print("4.除法")
        print("5.退出简易计算器")
        print("6.查看历史记录")

        choice = input("请选择：").strip()

        if choice == "1":
            addition()
        elif choice == "2":
            subtraction()
        elif choice == "3":
            multiplication()
        elif choice == "4":
            divisionmethed()
        elif choice == "5":
            print("退出计算器，再见！")
            break
        elif choice == "6":
            show_history()
        else:
            print("❌ 无效的选择，请重新输入！")

if __name__ == "__main__":
    main()