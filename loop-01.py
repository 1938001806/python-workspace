# while True :
#     score = int(input("请输入成绩"))
#     if score > 100 or score <0:   #应该是大于100 和小于0 错误写法score < 100 or score < 0
#         print("❌ 成绩输入不合法，请重新输入！\n")
#         continue  # continue 的意思是：停止当前循环，马上回到 while 开头重新开始
#     if score >= 60:
#         print(f"你的成绩是 {score} 分，合格！")
#     else:
#         print(f"你的成绩是 {score} 分，不合格！")
#     break

while True:
    text = input("请输入成绩（输入 q 退出）：").strip()
    if text.lower() == "q":
        break
    if not text.isdigit():
        print("请输入数字")
        continue
    score = int(text)
    if score < 0 or score > 100:
        print("成绩必须在 0~100 之间")
        continue
    print(f"{score}分，" + ("合格" if score >= 60 else "不合格")) 