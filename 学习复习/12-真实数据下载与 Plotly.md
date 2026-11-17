# 12 · 真实数据下载与 Plotly

> 类别定位：把「别人给的数据」（CSV 文件、JSON 文件、GitHub API）读进程序，再画成图。
> 覆盖《Python 编程从入门到实践》第 16~17 章。四个脚本都实跑过；Plotly 部分因本机默认解释器缺 pandas，用临时依赖目录取证（见文末）。

## 本类文件

| 文件 | 行数 | 数据来源 | 输出 |
| --- | --- | --- | --- |
| [sitka_weather.py](../sitka_weather.py) | 32 | `sitka_weather_07-2014.csv` | 最高/最低温折线 + 填充带 |
| [17_eq_worldmap.py](../17_eq_worldmap.py) | 21 | `eq_data.json` | 控制台打印震级/经度/纬度 |
| [17_eq_plotly.py](../17_eq_plotly.py) | 34 | `eq_data.json` | Plotly 世界地图散点 |
| [18_pighub_api.py](../18_pighub_api.py) | 55 | GitHub Search API | 星标排行柱状图 HTML |

---

## 一、sitka_weather.py —— CSV + datetime + 填充带

### 数据长什么样

`sitka_weather_07-2014.csv` 表头 23 列，前 4 列是：

```text
AKDT,Max TemperatureF,Mean TemperatureF,Min TemperatureF,...
2014-07-01,64,53,50,...
2014-07-02,56,51,48,...
```

本次文件共 12 行数据（7 月 1~12 日）。

### 读取与解析

[sitka_weather.py:5-18](../sitka_weather.py#L5-L18)：

```python
filename = r'E:\python源码\python工作区\lreaning\sitka_weather_07-2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    highs, lows, dates = [], [], []
    for row in reader:
        current_date = datetime.strptime(row[0], "%Y-%m-%d")
        dates.append(current_date)

        high = int(row[1])
        highs.append(high)
        low = int(row[3])
        lows.append(low)
```

三个要点：

1. **`next(reader)` 先吃掉表头**，否则第一行日期 `AKDT` 会在 `strptime` 处报错。
2. **`datetime.strptime(row[0], "%Y-%m-%d")`** 把字符串转成日期对象；matplotlib 的 x 轴才能按时间比例排布，而不是当普通字符串。
3. **`row[1]` 是最高温，`row[3]` 是最低温**（索引 2 是平均温，跳过了）。这是「魔数索引」，后面会讲怎么改。

### 实际结果

```text
天数: 12 | 日期范围: 2014-07-01 -> 2014-07-12
highs: [64, 56, 61, 64, 68, 68, 66, 64, 69, 73, 66, 64]
lows:  [50, 48, 50, 52, 52, 54, 53, 52, 54, 56, 54, 54]
最高: 73 | 最低: 48
```

手工核对：7 月 10 日最高 73°F 是全月最高；7 月 2 日最低 48°F 是全月最低。

### 画图

[sitka_weather.py:20-31](../sitka_weather.py#L20-L31)：

```python
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red', alpha=0.6)
plt.plot(dates, lows, c='blue', alpha=0.6)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
plt.title("Daily High and low Temperatures, july 2014", fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature(f)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()
```

- `fill_between(dates, highs, lows)` 把最高/最低之间的区域填色，这是温度图的常用表达。
- `fig.autofmt_xdate()` 自动旋转日期标签，否则 12 个日期会挤在一起。
- `dpi=128` 让图更清晰。

### 六个问题

| # | 问题 | 位置 | 后果 / 改法 |
| --- | --- | --- | --- |
| 1 | **绝对路径写死** | [:5](../sitka_weather.py#L5) | 换电脑/换目录立刻 `FileNotFoundError`；用 `Path(__file__).with_name(...)` |
| 2 | **列索引是魔数** | [:15](../sitka_weather.py#L15)、[:17](../sitka_weather.py#L17) | 数据源换列顺序就静默读错；用 `header_row.index("Max TemperatureF")` |
| 3 | **空值会让 `int()` 崩** | [:15](../sitka_weather.py#L15) | 天气 CSV 常有空单元格；先判空或 `csv.DictReader` |
| 4 | **`open` 没写 `encoding`** | [:6](../sitka_weather.py#L6) | 本文件是 ASCII 才没出事；含中文/符号时用 `encoding="utf-8"` |
| 5 | **`plt.xlabel('')` 空标签** | [:25](../sitka_weather.py#L25) | 删掉或写「日期」 |
| 6 | **没有 `savefig`** | [:31](../sitka_weather.py#L31) | 无窗口/批处理时看不到图 |

`header_row` 现在完全没被使用（[:8](../sitka_weather.py#L8)）。它最有价值的用法就是换成列名索引：

```python
date_col = header_row.index("AKDT")
high_col = header_row.index("Max TemperatureF")
low_col = header_row.index("Min TemperatureF")
```

这样列顺序变化时不会静默读错。

### 修正版骨架

```python
import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

CSV_PATH = Path(__file__).with_name("sitka_weather_07-2014.csv")

with CSV_PATH.open(encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    date_i = header.index("AKDT")
    high_i = header.index("Max TemperatureF")
    low_i = header.index("Min TemperatureF")

    dates, highs, lows = [], [], []
    for row in reader:
        if not row[high_i] or not row[low_i]:      # 跳过空值
            continue
        dates.append(datetime.strptime(row[date_i], "%Y-%m-%d"))
        highs.append(int(row[high_i]))
        lows.append(int(row[low_i]))
```

---

## 二、17_eq_worldmap.py —— 嵌套 JSON 的取值练习

### 数据结构

`eq_data.json` 是 GeoJSON 的简化版：

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "properties": {"mag": 6.5, "place": "Southern Alaska", "title": "M 6.5 - Southern Alaska"},
      "geometry": {"type": "Point", "coordinates": [-149.5, 60.2]}
    }
  ]
}
```

本文件只有 4 条 `features`（样例数据），不是真实全量地震数据。

### 取值

[17_eq_worldmap.py:7-17](../17_eq_worldmap.py#L7-L17)：

```python
all_eq_dicts = all_eq_data['features']

for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]
```

**GeoJSON 的坐标顺序是 `[经度, 纬度]`**，即 `coordinates[0]` 是 lon、`[1]` 是 lat。写反了图会画到海里，而且不报错。

### 实际输出

```text
提取到的震级 [6.5, 4.2, 7.1, 3.0]
提取到的经度 [-149.5, 142.3, 120.4, -115.8]
提取到的维度 [60.2, 38.1, -8.5, 35.2]
```

### 两个问题

1. **「维度」应为「纬度」**（[:21](../17_eq_worldmap.py#L21)）。「维度」是另一个词，属于文案错。
2. **绝对路径写死**（[:2](../17_eq_worldmap.py#L2)），同 sitka_weather。

### 健壮性提醒

真实 USGS 数据里 `mag` 可能为 `null`。直接 `mags.append(mag)` 不报错，但后面画图/排序会崩。读外部 JSON 时至少要：

```python
mag = eq_dict['properties'].get('mag')
if mag is None:
    continue
```

---

## 三、17_eq_plotly.py —— 用 Plotly 画世界地图

### 代码结构

[17_eq_plotly.py:11-32](../17_eq_plotly.py#L11-L32)：

```python
mags, lons, lats, eq_titles = [], [], [], []
for eq_dict in all_eq_dicts:
    ...
    eq_titles.append(eq_dict['properties']['title'])

fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=mags,
    color=mags,
    hover_name=eq_titles,
    color_continuous_scale='Viridis',
    title='Global Earthquakes',
    projection='natural earth'
)
fig.show()
```

参数含义：

| 参数 | 作用 |
| --- | --- |
| `lat` / `lon` | 点的纬度/经度 |
| `size=mags` | 震级越大，气泡越大 |
| `color=mags` | 颜色也映射震级（Viridis 色带） |
| `hover_name=eq_titles` | 鼠标悬停时显示 `M 6.5 - ...` 标题 |
| `projection='natural earth'` | 自然地球投影，比默认投影更像常见世界地图 |

### 实际生成的图对象

```text
trace type: scattergeo
points: 4 | lat: [60.2, 38.1, -8.5, 35.2]
marker.size:  [6.5, 4.2, 7.1, 3.0]
marker.color: [6.5, 4.2, 7.1, 3.0]
projection: natural earth | title: Global Earthquakes
```

### 关键依赖：`plotly.express` 需要 pandas

`px.scatter_geo` 传的是**列表**而不是 DataFrame 时，Plotly 内部会先构造 DataFrame。本机一个只有 plotly、没有 pandas 的解释器实测直接失败：

```text
NotImplementedError: Pandas installation is required if no dataframe is provided.
```

所以 `pip install plotly` 不够，`plotly.express` 还要 `pandas`。这是「依赖的依赖」问题，装包后要**实际跑一次**才知道缺什么。

### `fig.show()` 在无界面环境下的行为

`fig.show()` 默认调浏览器渲染。脚本/服务器/无头环境里要么没反应，要么报「无法打开浏览器」。批处理时改成：

```python
fig.write_html("earthquakes.html")
```

想同时保留交互性，用 `include_plotlyjs="cdn"` 可把 HTML 从 ~4.8MB 降到几十 KB（代价是打开时需联网）。

### 其他可改进点

- `size=mags` 直接用震级当像素半径，7.1 的点会比 3.0 大很多；可以用 `size_max` 限制上限。
- 绝对路径写死（[:4](../17_eq_plotly.py#L4)）。
- `fig.show()` 前没有 `if __name__ == "__main__"`，一 import 就弹浏览器。

---

## 四、18_pighub_api.py —— GitHub API + 离线柱状图

### 请求与解析

[18_pighub_api.py:5-18](../18_pighub_api.py#L5-L18)：

```python
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)
response_dict = r.json()
repo_dicts = response_dict['items']
```

### 实际运行（本次联网）

```text
正在向 Github 请求数据...
状态码:200
Github 上总共有35770007 个 python 项目。
项目：public-apis | 星标：496816
项目：free-programming-books | 星标：401166
...
项目：pytorch | 星标：105227
✅ 图表已生成，快去浏览器查看 python_repos.html 吧！
```

生成了 `python_repos.html`，约 **4.8 MB**（内嵌完整 plotly.js）。

### 问题 1：`hovertext` 与柱子错位（真 bug）

[18_pighub_api.py:29-35](../18_pighub_api.py#L29-L35)：

```python
repo_links = []
repo_names.reverse()
repo_stars.reverse()
repo_links.reverse()

for repo_dict in repo_dicts:
    repo_links.append(repo_dict['html_url'])
```

`repo_names` 和 `repo_stars` 被反转了，但 `repo_links` 是先反转一个**空列表**（什么也没发生），再按**原始顺序**追加链接。结果：

- 柱子的 x/y 是「星标从低到高」
- `hovertext` 的链接仍是「从高到低」

鼠标悬停在最低星标的柱子上，弹出的却是**最高星标仓库**的链接。图看起来完全正常，只有点开链接才发现错——典型的静默 bug。

正确做法是**三个字段一起排**：

```python
repos = [
    (d['name'], d['stargazers_count'], d['html_url'])
    for d in repo_dicts
]
repos.sort(key=lambda item: item[1])      # 星标升序
names = [r[0] for r in repos]
stars = [r[1] for r in repos]
links = [r[2] for r in repos]
```

### 问题 2：没有 `timeout`，也没判状态码

[18_pighub_api.py:10](../18_pighub_api.py#L10)：

```python
r = requests.get(url, headers=headers)
```

- 无超时：网络挂起会永久卡住。
- `r.json()` 在 403/429 时仍可能解析出一个**错误字典**（含 `message`），随后 `response_dict['total_count']` 直接 `KeyError`。
- GitHub 未认证的 Search API 有速率限制（约每分钟 10 次），连续跑几次就可能被限流。

改法：

```python
r = requests.get(url, headers=headers, timeout=10)
r.raise_for_status()
response_dict = r.json()
if 'items' not in response_dict:
    print("接口返回异常:", response_dict.get('message'))
    raise SystemExit(1)
```

### 问题 3：`Accept` 头是旧版本

`application/vnd.github.v3+json` 仍可用，但 GitHub 现在推荐：

```python
headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
```

### 问题 4：`offline.plot` 会弹浏览器 + HTML 很大

[18_pighub_api.py:54](../18_pighub_api.py#L54)：

```python
offline.plot(fig, filename='python_repos.html')
```

- 默认 `auto_open=True`，会弹浏览器。批处理要 `auto_open=False`。
- 默认内嵌完整 plotly.js，4.8 MB。加 `include_plotlyjs="cdn"` 可大幅减小。

### 问题 5：文件名拼写

`pighub` 应为 `github`。不影响运行，但搜索/引用时不方便。

### 修正版片段

```python
import requests
from plotly import offline
from plotly.graph_objects import Bar, Layout

URL = "https://api.github.com/search/repositories"
PARAMS = {"q": "language:python", "sort": "stars"}
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

r = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=10)
r.raise_for_status()
items = r.json()["items"]

repos = sorted(
    ((d["name"], d["stargazers_count"], d["html_url"]) for d in items),
    key=lambda item: item[1],
)
names = [x[0] for x in repos]
stars = [x[1] for x in repos]
links = [x[2] for x in repos]

fig = {
    "data": [Bar(x=names, y=stars, hovertext=links,
                 marker={"color": "rgb(60, 100, 150)"})],
    "layout": Layout(
        title="GitHub 上最热门的 Python 项目",
        xaxis={"title": "项目名称"},
        yaxis={"title": "星标数 (Stars)"},
    ),
}
offline.plot(fig, filename="python_repos.html", auto_open=False,
             include_plotlyjs="cdn")
```

---

## 五、四条真实数据的读取路线

| 数据形态 | 工具 | 关键点 |
| --- | --- | --- |
| CSV 文件 | `csv.reader` / `csv.DictReader` | `newline=""`、表头、空值 |
| 嵌套 JSON | `json.load` + 逐层取键 | 坐标顺序 `[lon, lat]`、`null` 值 |
| 在线 API（JSON） | `requests.get(..., timeout=)` | 状态码、速率限制、`timeout` |
| 交给 Plotly | `px.*` / `go.*` + `write_html` | express 需要 pandas、`auto_open=False` |

---

## 六、易错清单

| # | 现场 | 类型 | 对策 |
| --- | --- | --- | --- |
| 1 | 绝对路径 `E:\...` | 换机即崩 | `Path(__file__).with_name(...)` |
| 2 | `row[1]` / `row[3]` 魔数 | 换列即静默读错 | `header.index("列名")` |
| 3 | 「维度」 | 文案错 | 「纬度」 |
| 4 | `coordinates[0]` 当纬度 | 静默画错位置 | GeoJSON 是 `[经度, 纬度]` |
| 5 | 三个列表分别 `reverse()` | 悬停链接错位 | 三个字段一起 `zip` + `sort` |
| 6 | 无 `timeout` / 不判状态码 | 卡死或 `KeyError` | `timeout=10` + `raise_for_status()` |
| 7 | `px` 缺 pandas | `NotImplementedError` | 同时安装 pandas |
| 8 | `offline.plot` 弹浏览器 | 批处理阻塞 | `auto_open=False` |
| 9 | 内嵌 plotly.js 4.8MB | 文件过大 | `include_plotlyjs="cdn"` |
| 10 | 顶层 `fig.show()` | import 即弹窗 | `if __name__ == "__main__"` |

---

## 七、练习

1. 把 `sitka_weather.py` 的绝对路径改成 `Path(__file__)`，并把三个列索引改成 `header.index(...)`。
2. 给 `17_eq_worldmap.py` 加 `mag is None` 过滤，并修正「维度」。
3. 把 `17_eq_plotly.py` 改成 `fig.write_html("earthquakes.html")`，再用浏览器打开确认可交互。
4. 修 `18_pighub_api.py` 的链接错位，悬停每个柱子确认链接与仓库名一致。
5. 给 GitHub 请求加 `timeout` 和 `raise_for_status()`，然后故意把 URL 改错，确认能打印出可读的错误。
6. 把 `include_plotlyjs` 改成 `"cdn"`，比较 HTML 文件大小。

---

## 八、取证环境说明

本机两套解释器的依赖并不齐：

```text
默认 python 3.15：pandas 3.1.0 / matplotlib 3.11.2 / requests 2.34.2 / bs4 4.15.0，无 plotly
py -3.12：plotly 7.1.0 / matplotlib / requests，无 pandas、无 bs4
```

因此：

- `sitka_weather.py`、`15_dice_visual.py`、`16_random_walk.py` 用默认 3.15（`MPLBACKEND=Agg` 无头运行）。
- `17_eq_plotly.py`、`18_pighub_api.py` 需要 plotly + pandas，本次把 plotly 装到**临时目录**，用 `PYTHONPATH` 指向它运行，未改动全局环境。

如果你在 VS Code 里运行报 `ModuleNotFoundError`，先确认右下角选的解释器，再按上面的清单补包。

---

## 参考

- matplotlib 基础与轴标签见 [04-数据分析与可视化.md](04-数据分析与可视化.md)。
- 类与 `self` 见 [06-面向对象入门.md](06-面向对象入门.md)。
- 网络请求的 `timeout`、状态码、UA 见 [05-网络爬虫.md](05-网络爬虫.md)。
- 骰子与随机游走的模拟见 [11-数据生成与模拟.md](11-数据生成与模拟.md)。
