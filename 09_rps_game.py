import random

print("===== 欢迎来到石头剪刀布大作战 =====")

stats = {
    "玩家赢":0,
    "电脑赢":0,
    "平局":0
}

round_count = 0
MAX_ROUNDS = 5


while True:
    if round_count >= MAX_ROUNDS:
        print("\n===========游戏结束==========")
        print(f"总比分：你赢了{stats['玩家赢']}次，电脑赢了{stats['电脑赢']}次，平局{stats['平局']}次。")


        if stats["玩家赢"] > stats["电脑赢"]:
            print("🏆 最终胜者：你！太厉害了！")
        elif stats["玩家赢"] < stats["电脑赢"]:
            print("💻 最终胜者：电脑！下次加油！")
        else:
            print("🤝 势均力敌，最终是平局！")
        break
    print(f"\n---第{round_count + 1}局，请出拳 ---")
    print("0.石头")
    print("1.剪刀")
    print("2.布")
    print("3.不玩了，退出")

    choice = input("请输入数字（0/1/2/3）：").strip()

    if choice == "3":
        print("退出游戏，最终战绩：")
        print(f"你赢了{stats['玩家赢']}次，电脑赢了{stats['电脑赢']}次，平局{stats['平局']}次。")
        break
    if choice not in ["0","1","2"]:
        print("❌输入有误，请重新输入！")
        continue

    user_choice = int(choice)

    computer_choice = random.randint(0,2)


    names = ["石头","剪刀","布"]
    user_name = names[user_choice]
    computer_name = names[computer_choice]


    print(f"\n你出的是：{user_name}")
    print(f"电脑出的是：{computer_name}")

    if user_choice == computer_choice:
        print("结果：平局！")
        stats["平局"] += 1
    elif (user_choice == 0 and computer_choice == 1) or \
         (user_choice == 1 and computer_choice == 2) or \
         (user_choice == 2 and computer_choice ==0):
        print("结果：你赢了！🎉")
        stats["玩家赢"] +=1
    else:
        print("结果：电脑赢了！")
        stats["电脑赢"] += 1
    round_count += 1


#查询list里面的数字 
#查询玩家输入了几次
#当数字之和为5时 统计玩家电脑平局次数 输出谁赢
#玩家输入5次就判定错误