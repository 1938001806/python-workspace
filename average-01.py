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