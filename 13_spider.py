import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("正在发送请求...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ 网页获取成功！开始解析...\n")
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("span", class_="text")

    for i, quote in enumerate(quotes):
        print(f"第{i+1}句名言；{quote.text}")

else:
    print(f"❌ 请求失败，状态码：{requests.status_code}")