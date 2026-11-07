import requests
from plotly.graph_objects import Bar, Layout
from plotly import offline

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'

headers = {'Accept':'application/vnd.github.v3+json'}

print("正在向 Github 请求数据...")
r = requests.get(url, headers=headers)

print(f"状态码:{r.status_code}")

response_dict = r.json()

print(f"Github 上总共有{response_dict['total_count']} 个 python 项目。")

repo_dicts = response_dict['items']

repo_names, repo_stars = [], []

for repo_dict in repo_dicts:
    repo_names.append(repo_dict['name'])
    repo_stars.append(repo_dict['stargazers_count'])

for i in range(len(repo_names)):
    print(f"项目：{repo_names[i]} | 星标：{repo_stars[i]}")

repo_links = []
repo_names.reverse()
repo_stars.reverse()
repo_links.reverse()

for repo_dict in repo_dicts:
    repo_links.append(repo_dict['html_url'])

data = [Bar(x=repo_names, 
            y=repo_stars,
            hovertext=repo_links,
            marker={'color': 'rgb(60, 100, 150)'}
)]

my_layout = Layout(
    title='GitHub 上最热门的python项目',
    xaxis={'title':'项目名称'},
    yaxis={'title':'星标数(Stars)'}
)





fig = {'data':data, 'layout':my_layout}
offline.plot(fig, filename='python_repos.html')
print("✅ 图表已生成，快去浏览器查看 python_repos.html 吧！")