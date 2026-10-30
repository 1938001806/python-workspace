import random

#题目：
#查询list里面的数字
#查询玩家输入了几次
#当数字之和为5时 统计玩家电脑平局次数 输出谁赢
#玩家输入5次就判定错误

print("===== 数字猜拳大作战（和到 5 就分胜负）=====")
print("你和电脑各输入一个 1~4 的数字，谁的数字大谁赢。")
print("当你们两人数字之和正好是 5 时，这一局算平局！")
print("注意：玩家总共只能输入 5 次，到第 5 次就判定错误，游戏结束。\n")

# 1. 建一个空列表，用来装玩家每次输入的数字
nums = []

stats = {
    "玩家赢": 0,
    "电脑赢": 0,
    "平局": 0
}

MAX_TIMES = 5

while True:
    # 玩家输入次数 = 列表的长度
    if len(nums) >= MAX_TIMES:
        print("\n=========== 游戏结束 ==========")
        print(f"你一共输入了 {len(nums)} 次数字，已经达到 {MAX_TIMES} 次，判定错误！")
        print(f"你输入过的数字：{nums}")
        print(f"数字之和：{sum(nums)}")
        print(f"战绩：你赢了 {stats['玩家赢']} 次，电脑赢了 {stats['电脑赢']} 次，平局 {stats['平局']} 次。")

        if stats["玩家赢"] > stats["电脑赢"]:
            print("🏆 最终胜者：你！")
        elif stats["玩家赢"] < stats["电脑赢"]:
            print("💻 最终胜者：电脑！")
        else:
            print("🤝 势均力敌，最终是平局！")
        break

    print(f"--- 第 {len(nums) + 1} 次输入（还剩 {MAX_TIMES - len(nums)} 次机会）---")
    choice = input("请输入一个 1~4 的数字：")

    if choice not in ["1", "2", "3", "4"]:
        print("❌ 输入有误，只能输入 1~4 的数字，请重新输入！\n")
        continue

    user_num = int(choice)
    # 2. 把玩家输入的数字存进列表，方便查询
    nums.append(user_num)

    computer_num = random.randint(1, 4)

    print(f"你输入的数字是：{user_num}")
    print(f"电脑输入的数字是：{computer_num}")

    # 3. 数字之和为 5 时算平局，否则数字大的赢
    if user_num + computer_num == 5:
        print("结果：数字之和是 5，平局！")
        stats["平局"] += 1
    elif user_num > computer_num:
        print("结果：你赢了！🎉")
        stats["玩家赢"] += 1
    elif user_num < computer_num:
        print("结果：电脑赢了！")
        stats["电脑赢"] += 1
    else:
        print("数字相同，平局")
        stats["平局"] += 1

    print(f"目前你已输入 {len(nums)} 次，历史数字：{nums}\n")