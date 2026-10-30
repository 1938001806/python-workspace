count = 0  # 计数器，记录试了几次

while count < 5:  # 只要少于5次，就继续循环
    name = input("请输入你的名字（提示：姓谷）：")
    
    if name == "谷明真":
        print("欢迎回家！游戏结束。")
        break  # 对了就直接结束
    else:
        count += 1  # 错了一次，计数器加1
        print(f"不认识你！你还有 {5 - count} 次机会。\n")

# 如果5次都错了，循环自然结束，会执行下面这行
if count == 5:
    print("尝试次数太多，账号已锁定！")

while True:
   name = input("请输入你的名字（提示：姓谷）：").strip()

   if name == "谷明真":
      print("欢迎回家！游戏结束")
      break
   else:
      print("不认识你，请重新输入！\n")

   