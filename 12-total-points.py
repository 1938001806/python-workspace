import pandas as pd

df = pd.read_csv("scores.csv")

df["总分"] = df[["语文","数学","英语"]].sum(axis=1)

df = df.sort_values(by="总分",ascending=False)


print("")
print(df[["姓名","总分"]].head(3))