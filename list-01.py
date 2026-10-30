scores = [85, 92, 78, 60, 99]
names = ["张三", "李四", "王五"]
print(scores[1])
scores.append(100)
print(len(scores))

#1. 建一个空列表，用来装名字
classnames = []

for i in range(3):  #i是循环自动产生的 不需要定义
    new_name = input("请输入第个同学姓名：").strip()
    if new_name:
        classnames.append(new_name)


print("\n全班同学名单如下：")
for name in classnames:
    print(f"同学：{name}")

print(f"全班一共录入了{len(classnames)}位同学。")