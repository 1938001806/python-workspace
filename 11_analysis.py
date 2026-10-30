import pandas as pd

df = pd.read_csv("scores.csv")

print("===== 原始数据长这样 =====")
print(df)
print("-"*30)

print("===== 语文及格的名单 =====")
passed_chinese = df[df["语文"] >= 60]
print(passed_chinese)
print("-"*30)

average_math = df["数学"].mean()
print(f"全班的数学平均分是：{average_math:.1f}分")
print("-"*30)

print("双科优秀名单")
double_good = df[(df["数学"] >80) &(df["英语"] >80)]
print(double_good)

print("==== 英语不及格的名单 ====")
bad_English_names = df[df["英语"] < 60]["姓名"]
print(bad_English_names)
print("-"*30)