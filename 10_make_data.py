import csv


data = [["姓名","班级","语文","数学","英语"],
        ["张三","一班",85,92,78],
        ["李四","一班",76,88,90],
        ["王五","二班",95,79,85],
        ["赵六","二班",60,65,70],
        ["孙七","三班",88,95,92],
        ["周八","一班",45,55,50]
]


with open("scores.csv","w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("✅ 假数据 scores.csv 生成成功！")