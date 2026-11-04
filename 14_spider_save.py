import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://quotes.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chorme/120.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")

    all_data = []

    for i in range(len(quotes)):
        quote_text = quotes[i].text
        author_text = authors[i].text

        all_data.append([quote_text, author_text])

        print(f"已抓取第{i+1}条：{author_text} 说 {quote_text}")

    print("\n✅ 抓取完毕，开始保存到文件...")

    df = pd.DataFrame(all_data, columns=["名言内容", "作者"])
    df.to_csv("quotes_pandas.csv", index=False, encoding="utf-8-sig")

    print("🎉 保存成功！快去左侧文件栏双击打开 quotes.csv 看看吧！")
else:
    print("请求失败")