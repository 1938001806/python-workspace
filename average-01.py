#列表
#录入成绩
#计算平均值

scores = []

for i in range(5):
    s = int(input(f"请输入第{i}个成绩："))
    scores.append(s)

total = 0
for s in scores:
    total = total + s

average = total/len(scores)

print(f"所有成绩：{scores}")
print(f"总分是{total}，平均分是{average}")

#重构后的代码
scores = []
while len(scores) < 3:
    text = input(f"请输入第{len(scores) + 1}个成绩：").strip()
    try:
        s = int(text)
    except ValueError:
        print("必须时整数，重来")
        continue
    if not 0 <= s <= 100:
        print("成绩要在0~100之间")
        continue
    scores.append(s)

print(f"所有成绩：{scores}")
print(f"总分是{sum(scores)},平均分是{sum(scores) / len(scores)}")