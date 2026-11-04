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

    #爬虫
    #想要爬取的网站
    #查看网页的结构，寻找自己想要得到的信息
    #伪造访问的权限，模拟真人
    #爬取网页结构内 如标题 title等
    #将数据保存下来 先造一个列表，然后将爬取的信息逐一输入到列表中 再分析列表找到自己想要的内容 将想要的内容save到文件中 注意格式

    