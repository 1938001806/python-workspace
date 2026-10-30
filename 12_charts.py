import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("scores.csv")


subjects = ["语文","数学","英语"]
average_scores = [df["语文"].mean(),df["数学"].mean(),df["英语"].mean()]

subjects = ["语文","数学","英语"]
average_scores = [df["语文"].mean(),df["数学"].mean(),df["英语"].mean()]

plt.figure(figsize=(8,5))
plt.bar(subjects,average_scores,color=['skyblue','orange','lightgreen'])

plt.title("各科平均分对比图",fontsize=16)
plt.xlabel("科目",fontsize=12)
plt.xlabel("平均分",fontsize=12)

for i, v  in enumerate(average_scores):
    plt.text(i,v + 1,f"{v:1f}",ha='center',fontsize=12)


plt.show()

plt.figure(figsize=(8,5))
plt.plot(df["姓名"],df["数学"],marker='o',color='red',linestyle='--')

plt.title("学生数学成绩折线图",fontsize=16)
plt.xlabel("姓名")
plt.xlabel("分数")

plt.grid(True)
plt.show()