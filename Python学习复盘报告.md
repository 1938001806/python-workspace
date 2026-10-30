# Python 学习代码复盘报告

> 复盘对象：`E:\python源码\python工作区\lreaning`（14 个 `.py` + 1 个 `scores.csv` + 1 份已有的 `学习总结.txt`）
> 运行环境（实测）：Python 3.15.0、pandas 3.1.0、matplotlib 3.11.2、numpy 2.5.4
> 复盘方式：逐个文件通读 → 提取每个函数与每处语法点 → **实际运行脚本复现问题**。下文凡标注「实测」的，都有真实运行输出作证据，不是推测。

---

## 一、总体结论（先看这 6 条）

| # | 结论 | 证据 |
|---|---|---|
| 1 | 学习轨迹非常清晰：基础语法 → 数据结构 → 函数 → 文件持久化 → 小游戏 → pandas/matplotlib，是一条标准的爬坡路线 | 文件时间从 10-21 排到 10-30，编号 06→12 与难度同步 |
| 2 | **"函数"这一章只练了一半**：10 个自定义函数里，**0 个带参数、9 个没有返回值**，全部依赖模块级全局变量 | 见第三章统计 |
| 3 | **12 / 14 个文件是"平铺脚本"，没有函数**，只有 `06`、`07` 两个文件真正做了函数封装 | `list/loop/count/average/dictionary/09/10/11/12` 全是顶层语句 |
| 4 | 存在 **3 个 P0 级真 bug** 和 **3 个 P1 级问题**，其中 2 个会让程序直接崩溃 | 第二章逐条给出行号与实测输出 |
| 5 | 《学习总结.txt》诊断得很准，但**"总结 → 回改代码 → 跑一遍验证"的闭环只走了一半**：病历本里 7 条错误，至少 3 条在现在的代码里**依然存在** | 见第六章开头对照表 |
| 6 | 数据分析部分（pandas/matplotlib）语法基本正确，问题集中在"图表标签写错、格式符写错、索引没重置"这类细节 | 见 2.13 / 2.14 |

### 最有价值的一句话结论

> 你的**语法记忆没问题，问题在"工程习惯"**：不写参数/返回值、不写 `if __name__ == "__main__"`、不处理输入、不处理文件异常、总结完不回头改代码。
> 下一步不需要学新语法，需要把已有的 14 个文件**重写成 3 个带参数和返回值的程序**，并逐个跑通。

---

## 二、逐个文件精读

### 学习轨迹一览

| 文件 | 修改时间 | 主题 | 是否有函数 | 状态 |
|---|---|---|---|---|
| `list-01.py` | 10-21 20:25 | 列表 + 输入 | 无 | 有 1 个逻辑错误 |
| `loop-01.py` | 10-21 20:31 | while 循环 | 无 | **全文被注释，不可运行** |
| `count-01.py` | 10-21 20:31 | 计数器 + break | 无 | 可运行，有小瑕疵 |
| `check_age.py` | 10-21 20:31 | if/while 练习 | 无 | **全文被注释，不可运行** |
| `average-01.py` | 10-22 09:20 | 列表累加求平均 | 无 | 可运行，有 1 个显示错误 |
| `dictionary-01.py` | 10-22 09:54 | 字典 + 菜单循环 | 无 | 可运行，有 1 个错别字 |
| `06_function_contacts.py` | 10-22 11:04 | 函数版通讯录 | 4 个 | **P0：空通讯录删除时崩溃** |
| `07-file-test.py` | 10-23 14:13 | 函数 + JSON 持久化 | 6 个 | **P0/P1：删除菜单不显示姓名；空文件仍会崩** |
| `10_add_game.py` | 10-28 13:51 | 猜数字比大小 | 无 | 可运行，有 1 个规则漏洞 |
| `09_rps_game.py` | 10-30 09:34 | 石头剪刀布 | 无 | **P0：局数永远不累加，5 局结束功能失效** |
| `10_make_data.py` | 10-30 10:56 | csv 生成假数据 | 无 | 正确，`newline=""` 用对了 |
| `11_analysis.py` | 10-30 11:18 | pandas 筛选/均值 | 无 | 可运行，命名与链式索引待改 |
| `12-total-points.py` | 10-30 13:27 | 总分 + 排序 Top3 | 无 | 正确，索引未重置（显示 4/2/0） |
| `12_charts.py` | 10-30 13:35 | matplotlib 柱状图/折线图 | 无 | **P1：ylabel 写成 xlabel；`{v:1f}` 格式符写错** |
| `scores.csv` | 10-30 10:56 | 数据源 | — | 纯 UTF-8，无 BOM（实测前 3 字节为 `e5 a7 93`） |

---

### 2.1 `list-01.py` —— 列表与输入

**逐行解释**

```python
scores = [85,92,78,60,99]      # 第 1-5 行：上一节的演示代码残留，与本节主题无关
names = ["张三", "李四", "王五"]
print(scores[1])               # 索引访问，打印 92（下标从 0 开始）
scores.append(100)             # 追加到末尾
print(len(scores))             # 6

classnames =[]                 # 第 8 行：建空列表；PEP8 要求 = 两边各一个空格
for i in range(3):             # range(3) 产生 0,1,2
    new_name = input()         # 第 11 行：没有提示文字，用户看不到任何引导
    classnames.append(new_name)

for name in classnames:        # 直接遍历元素（比 range(len()) 更好）
    print(f"同学：{name}")

print(f"全班一共录入了{classnames}位同学。")   # 第 19 行：BUG
```

**实测输出**

```
92
6

全班同学名单如下：
同学：张三
同学：李四
同学：王五
全班一共录入了['张三', '李四', '王五']位同学。
```

**问题**

1. **[逻辑错误] 第 19 行**：`{classnames}` 把整个列表塞进了句子，应当是人数 `{len(classnames)}`。你上一行刚用过 `len()`，这里没用上——说明"变量存在"和"变量含义"还没完全对齐。
2. **[PEP8] 第 8 行** `classnames =[]` 缺空格；第 1 行 `[85,92,...]` 逗号后缺空格。
3. **[习惯] 第 10 行** `i` 没被使用，应为 `for _ in range(3):`。第 10 行注释写着 `#if要定义i`——**这个概念是错的**：`for i in range(3)` 里的 `i` 是循环自动产生的，不需要"定义"。
4. **[交互] 第 11 行** `input()` 空提示，运行起来是"黑屏等输入"，体验差且容易误以为卡死。
5. **[健壮性]** 姓名没做 `strip()` 和空值判断，直接回车会存进一个空字符串。

**改法**

```python
classnames = []
for _ in range(3):
    new_name = input("请输入第个同学姓名：").strip()
    if new_name:
        classnames.append(new_name)

print(f"全班一共录入了{len(classnames)}位同学。")
```

---

### 2.2 `loop-01.py` —— 整个文件都是注释

**现状**：20 行全部是 `#` 注释，**没有任何可执行语句**，是一个"笔记文件"而不是程序。

**内容价值**：它记录了 while + continue + break 的正确组合：

```python
while True:
    score = int(input("请输入成绩"))
    if score > 100 or score < 0:   # 条件本身是对的
        print("成绩输入不合法")
        continue                    # 回到 while 开头，跳过下面的 break
    ...
    break                           # 合法才走到这里，退出循环
```

**问题**

1. 无法运行 → 无法验证 → **你无法确认自己是否真的理解了 `continue` 和 `break` 的分工**。`continue` 跳过本轮剩余语句、`break` 直接跳出循环，这两个词只差几个字母，靠读注释记不住。
2. **没有退出通道**：如果使用者一直输入非法值，`while True` 会无限循环，只能 Ctrl+C。真实程序必须在循环里留一个"输入 q 退出"。
3. **`int(input())` 没有防护**：输入 "abc" 会抛 `ValueError` 直接崩掉。这是本套代码里出现频率最高的隐患（见第六章）。
4. 第 3 行注释 `#应该是大于100 和小于0` 与代码 `> 100 or < 0` 一致，说明这里你已经改对了；但《学习总结》里说"错误现场是 `score < 100 or score < 0`"，说明这段代码被改写过多轮，**建议保留一个能跑的版本 + 用注释记录"错误版本长什么样"**，而不是把整段注释掉。

**建议的可用版本**

```python
while True:
    text = input("请输入成绩（输入 q 退出）：").strip()
    if text.lower() == "q":
        break
    if not text.isdigit():          # 先判断"能不能转"，再转
        print("请输入数字")
        continue
    score = int(text)
    if score < 0 or score > 100:    # 先写小的边界，读起来更顺
        print("成绩必须在 0~100 之间")
        continue
    print(f"{score} 分，" + ("合格" if score >= 60 else "不合格"))
```

---

### 2.3 `count-01.py` —— 计数器 + break（唯一一个逻辑完整的小程序）

```python
count = 0
while count < 5:                       # 条件控制次数，不用 break 也能退出
    name = input("请输入你的名字（提示：姓谷）：")

    if name == "谷明真":
        print("欢迎回家！游戏结束。")
        break                          # 命中就提前退出
    else:
        count = count + 1              # 只有答错才计数 —— 这个设计是对的
        print(f"不认识你！你还有 {5 - count} 次机会。\n")

if count == 5:                         # 循环自然结束后再判断，思路清晰
    print("尝试次数太多，账号已锁定！")
```

**做得好的地方**

- `while 条件` 与 `break` 混用得当：次数由计数器兜底，正确时提前退出。
- 把"计数"放在 `else` 分支里，**只有失败才 +1**，所以第 5 次答对仍然算成功——这个细节很多人会写错。
- 循环外的 `if count == 5` 用来区分"循环是走完的还是被 break 的"，是很实用的技巧。

**问题**

1. 第 10 行 `count = count + 1` 可以写 `count += 1`（第 26 行的注释里就用了 `count = count+1`，风格不统一）。
2. 第 27 行行尾有一串空格（`   `），这类"看不见的字符"正是缩进报错的常见来源。
3. 第 23 行注释里的 `elif input(name) >= 5:` 是**无效代码**（`input()` 返回字符串，和整数比较会 `TypeError`），而且 `input(name)` 会把姓名当成提示语再要一次输入——这段注释留着会形成错误记忆，建议直接删掉。
4. 姓名没 `strip()`：多打一个空格就永远猜不对。
5. 没有"输入 q 放弃"的出口。

---

### 2.4 `check_age.py` —— 另一个"纯注释"文件

**现状**：全文 35 行都是注释，包含四段练习：if/else 成年判断、成绩 if/elif/else、姓名判断、while 计数打印。

**问题**

1. 与 `loop-01.py` 同样的问题：**不可运行 = 不可验证**。
2. 第 33 行有一整行只有空格的"幽灵行"（`                    `），有些编辑器会把它当成缩进块的一部分，是潜在的 `IndentationError` 来源。
3. 里面 `if score > 100 or score <0:` 的空格风格不统一（`<0` vs `> 100`）。

**建议**：把这两个纯注释文件合并成一个 `01_basics_practice.py`，每段练习后面加 `assert` 自测，例如：

```python
def check_age(age):
    return "已成年" if age >= 18 else "未成年"

assert check_age(18) == "已成年"
assert check_age(17) == "未成年"
print("全部通过")
```

这样"学过"就变成了"验证过"。

---

### 2.5 `average-01.py` —— 列表累加求平均

```python
scores = []

for i in range(5):
    s = int(input(f"请输入第{i}个成绩："))   # 第 8 行：下标从 0 开始
    scores.append(s)

total = 0
for s in scores:                              # 手动累加
    total = total + s

average = total/len(scores)                    # 第 15 行：没有防空

print(f"所有成绩：{scores}")
print(f"总分是{total}，平均分是{average}")
```

**实测输出**

```
请输入第0个成绩：请输入第1个成绩：...请输入第4个成绩：
所有成绩：[60, 70, 80, 90, 100]
总分是400，平均分是80.0
```

**问题**

1. **[显示错误] 第 8 行**：`第{i}个` 从"第 0 个"开始，人读起来别扭，应为 `{i+1}`。这是典型的 **off-by-one（差一错误）**，是编程里最常见的错误类型之一。
2. **[可简化] 第 11-13 行**：手写累加循环完全等价于 `total = sum(scores)`。你已经会用 `sum()`（`list-01.py` 注释里提过），但这里没用——学过的内置函数要形成"条件反射"。
3. **[崩溃风险] 第 15 行**：如果 `scores` 为空，`total/0` → `ZeroDivisionError`。当前 `range(5)` 保证了非空，但只要以后改成"用户想输几个输几个"，就会立刻炸。
4. `int(input())` 无防护，输入非数字直接崩。
5. 变量 `s` 同时是循环变量（第 7 行）和累加变量（第 12 行），**同名但含义不同**，读代码时容易混淆；这类"变量复用"是 bug 温床。

---

### 2.6 `dictionary-01.py` —— 字典 + 菜单（未持久化的版本）

```python
contacts = {}
print("欢迎使用简易通讯录！")

while True:
    print("\n--- 菜单 ---")
    ...
    choice = input("请选择操作（输入1/2/3）：")

    if choice == "1":
        name = input("请输入联系人姓名：")
        if name in contacts:                      # 先查重 —— 顺序正确（历史 bug 已修）
            print(f"你添加的{name}已经存在！")
        else:
            phone = input("请输入联系人电话：")
            contacts[name] = phone
            print(f"已保存：{name}的电话时{phone}")   # 第 22 行：错别字"时"
    elif choice == "2":
        if len(contacts) == 0:
            print("通讯录还是空的哦！")
        else:
            for name, phone in contacts.items():   # 同时拿键和值，写法正确
                print(f"姓名：{name},电话：{phone}")
    elif choice == "3":
        break
    else:
        print("无效的选择，请重新输入")
```

**这段代码是进步最大的一段**：菜单循环、`in` 查重、`.items()` 遍历、`else` 兜底无效输入，四个模式全部到位。

**问题**

1. 第 22 行错别字："电话**时**" → "电话**是**"。
2. `len(contacts) == 0` 可以写成 `if not contacts:`（Python 的"真值判断"惯用法，更短更好读）。
3. `choice` 没有 `strip()`，输入 " 1"（前面带空格）会走到 `else` 分支。
4. 数据只在内存里，**退出即丢失**——这正是下一课 `07` 要解决的问题，进度安排合理。
5. 没有"修改联系人"和"重名覆盖"策略。

---

### 2.7 `06_function_contacts.py` —— 第一个函数版程序（有 P0 崩溃）

**结构**：`contacts = {}` 全局字典 → 4 个函数 → `main()` 菜单 → 末尾直接调用 `main()`。

#### 函数 1：`add_contacts()`（第 3-10 行）

```python
def add_contacts():
    name = input("请输入联系人姓名：")
    if name in contacts:
        print(f"你添加的{name}已经存在了！")
    else:
        phone = input("请输入联系人电话：")
        contacts[name] = phone        # 直接改全局字典
        print(f"已保存：{name}，电话：{phone}")
```

- **签名**：`()` 无参数、无返回值。
- **依赖**：外部全局变量 `contacts`（函数内部只做"读 + 改元素"，没有 `contacts = ...` 赋值，所以不算修改全局绑定的变量，**不需要 `global` 也能跑通**）。
- **优点**：先判断重复、再要电话，顺序正确——这是你在 `dictionary-01.py` 里踩过坑之后修好的。
- **缺点**：把 `input()` 写在函数里，导致这个函数**没法被测试，也没法复用**（想批量导入就不能用）。合理的拆法是"输入归 `main`，处理归函数"。

#### 函数 2：`show_contacts()`（第 12-18 行）

```python
def show_contacts():
    if len(contacts) == 0:
        print("通讯录还是空的哦！")
    else:
        for name, phone in contacts.items():
            print(f"姓名：{name}，电话：{phone}")
```

- 只读，不改状态，安全。
- 建议改成 `if not contacts:`。

#### 函数 3：`delete_contacts()`（第 20-41 行）—— **P0 缺陷在这里**

```python
def delete_contacts():
    if len(contacts)  == 0:                  # 注意这里有两个空格，PEP8 多余空格
        print("通讯录还是空的哦！")             # 【缺少 return】
    else:
        names = list(contacts.keys())         # names 只在这个分支里被赋值
        print("---请选择要删除的联系人编号：---")
        for i in range(len(names)):
            print(f"{i+1}.{names[i]}")

    choice = input("请输入要删除的编号：")     # 第 29 行：缩进只有 4 空格 → 属于函数体，两个分支都会执行

    if choice.isdigit():
        choice = int(choice)
        if 1<= choice<= len(names):           # 第 33 行：空通讯录时 names 不存在
            target_name = names[choice -1]
            del contacts[target_name]
            print(f"已成功删除:{target_name}")
        else:
            print("输入的编号超出范围了！")
    else:
        print("请输入有效的数字！")
```

**实测（真实崩溃）**

```
请选择操作(输入1/2/3/4):通讯录还是空的哦！
请输入要删除的编号：Traceback (most recent call last):
  File "...\06_function_contacts.py", line 33, in delete_contacts
    if 1<= choice<= len(names):
UnboundLocalError: cannot access local variable 'names' where it is not associated with a value
```

**为什么是 `UnboundLocalError` 而不是 `NameError`（这是重点，务必理解）**

- Python 在**编译**函数时，只要发现函数体里对 `names` 有赋值语句（`names = ...`），就会把 `names` 判定为**局部变量**，整个函数内都按局部变量处理。
- 当走"空通讯录"分支时，赋值语句没被执行 → 局部变量 `names` 从未绑定 → 访问时报 `UnboundLocalError`。
- 如果函数里**完全没有** `names = ...`，那才会去全局找，报的是 `NameError`。
- 结论：**"函数里没赋值过的变量"和"外部同名变量"的关系，取决于这个函数里有没有赋值语句**。这是 Python 作用域最容易踩的坑，你的《学习总结》完全没有覆盖，但它这次真的让你的程序崩了。

**修法（三处）**

```python
def delete_contacts():
    if not contacts:
        print("通讯录还是空的哦！")
        return                              # 1) 早返回，直接结束函数

    names = list(contacts.keys())            # 2) 移出 else，逻辑更平
    print("---请选择要删除的联系人编号：---")
    for index, name in enumerate(names, start=1):   # 用 enumerate 代替 range(len())
        print(f"{index}.{name}")

    choice = input("请输入要删除的编号：").strip()
    if not choice.isdigit():
        print("请输入有效的数字！")
        return
    number = int(choice)
    if not 1 <= number <= len(names):        # 3) 边界判断单独一层，读起来是"不合法就退出"
        print("输入的编号超出范围了！")
        return
    target_name = names[number - 1]
    del contacts[target_name]
    print(f"已成功删除：{target_name}")
```

这个"**先挡掉非法情况并 return，主流程保持在最外层**"的写法叫**卫语句（guard clause）**，能把嵌套层级压平，是后面最该养成的习惯。

#### 函数 4：`main()`（第 43-65 行）

```python
def main():
    print("欢迎使用建议通讯录！")      # 错别字："建议" → "简易"
    while True:
        print("\n--- 菜单 ---")
        ...
        choice = input(f"请选择操作(输入1/2/3/4):")   # f-string 里没有 {}，f 多余（F541）
        if choice == "1":
            add_contacts()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            delete_contacts()
        elif choice == "4":
            print("退出程序。再见！")
            break
        else:
            print("无效的选择！")

main()      # 第 67 行：模块级直接调用
```

- 职责单一（只做分发），结构正确。
- **调用方式有问题**：`main()` 写在模块顶层，意味着 `import 06_function_contacts` 会立刻启动交互菜单并卡住 —— 这个文件永远无法被别的文件复用、无法写单元测试。正确写法：

```python
if __name__ == "__main__":     # 只有直接运行本文件时才执行
    main()
```

### 2.8 `07-file-test.py` —— 函数 + JSON 持久化

在 `06` 的基础上增加了 `load_data()` 和 `save_data()`，并把删除功能的缩进改对了（说明你已经意识到 06 的问题），但引入了新 bug。

#### 函数 1：`load_data()`（第 9-13 行）

```python
FILE_NAME = "contacts_data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return{}          # 第 13 行：return 与 {} 之间缺空格
```

- **优点**：`os.path.exists` 做了"文件不存在"的判断，`with open` + `encoding="utf-8"` 写得完全正确（`with` 会自动关闭文件，即使中途报错也会关）。
- **P1 缺陷**：`os.path.exists` 只判断"文件存不存在"，**不判断"文件里有没有内容"**。文件被清空（0 字节）时，`json.load()` 会抛 `json.JSONDecodeError`，而且是在**模块导入阶段**执行 `contacts = load_data()`，所以**程序连菜单都进不去，直接崩在启动时**。这正是你《学习总结》第 6 条记录的问题，**但代码还没改**。
- 失败的影响范围：不是"某一步操作失败"，而是"整个程序无法启动"，这就是为什么它比普通 bug 更严重。

**修法**

```python
def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("通讯录文件损坏或无法读取，已按空通讯录启动。")
        return {}
    if not isinstance(data, dict):        # 防止文件里是 [] 或 "abc"
        print("通讯录文件格式不正确，已按空通讯录启动。")
        return {}
    return data
```

#### 函数 2：`save_data()`（第 15-17 行）

```python
def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)
```

- **用对了三个关键参数**：`ensure_ascii=False`（中文原样写入，不变成 `\u5f20`）、`indent=4`（格式化，人能读）、`encoding="utf-8"`。
- **缺点**：直接读全局 `contacts`，与 `load_data` 不对称（一个靠返回值，一个靠全局）。更干净的写法是 `save_data(data)` 接收参数。
- **风险**：`"w"` 模式会先清空文件再写；如果写到一半程序被杀掉，文件就是空的 —— 下次启动就会撞上上面的 `JSONDecodeError`。**这两个 bug 是连锁的**。进阶做法是先写临时文件再 `os.replace()`，但现阶段知道这个风险即可。

#### 函数 3-5：`add_contacts()` / `show_contacts()` / `delete_contacts()`

与 06 基本一致，区别是增删后都调用了 `save_data()`（持久化闭环完整，这点做得很好）。

**新引入的 bug 在第 47 行：**

```python
for i in range(len(names)):
    print(f"{i+1}"),{names[i]}      # 第 47 行
```

**实测输出**（真实运行，先添加"测试"再选删除）：

```
---请选择要删除的联系人编号 ---
1
请输入要删除的编号：
```

**只打印了编号 `1`，姓名"测试"不见了。**

原因：这行代码被解析成一个**元组表达式** `(print(f"{i+1}"), {names[i]})`。

- 前半段 `print(f"{i+1}")` 正常输出编号；
- 后半段 `{names[i]}` 是**集合（set）字面量**，值被创建出来后**直接丢弃**，没有参与打印；
- 整个元组被当作表达式求值，结果没人接收。

正确写法（沿用 06 的写法即可）：

```python
print(f"{i+1}.{names[i]}")
```

> 附带一个知识点：`{x}` 在"赋值/表达式"上下文里是**集合**，在 `f"..."` 里面是**替换字段**，在 `d = {...}` 里是**字典**。同一个花括号三种身份，这是 Python 里很容易看走眼的地方，也是这行代码"看起来像模板字符串"却静默出错的原因。

另外：`07` 的删除函数把 `choice = input(...)` 放在了 `else` 里面（缩进 8 空格），所以空通讯录时**不会**崩溃 —— 这一点 07 比 06 是对的。

**其余问题**

- 第 63 行 `print("欢迎使用建议通讯录！")` 错别字仍在。
- 第 84 行 `main()` 仍是模块级直接调用，没有 `if __name__ == "__main__":`。
- 文件名 `07-file-test.py` 带连字符，**不能 `import`**（`import` 需要合法标识符）。同理：`list-01.py`、`loop-01.py`、`count-01.py`、`average-01.py`、`dictionary-01.py`、`12-total-points.py` 都不可导入。
- 数据文件名是**相对路径**，依赖"当前工作目录"。在别的目录下双击运行，会生成到别处，表现为"我明明存了，怎么打不开"。

### 2.9 `09_rps_game.py` —— 石头剪刀布（有 P0 缺陷）

```python
stats = {"玩家赢": 0, "电脑赢": 0, "平局": 0}
round_count = 0
MAX_ROUNDS = 5

while True:
    if round_count >= MAX_ROUNDS:        # 想在第 5 局后结束
        print("游戏结束")
        ...
        break

    print("\n---第{round_count + 1}局，请出拳 ---")   # 第 28 行：缺 f 前缀
    ...
    choice = input("请输入数字（0/1/2/3）：")
    if choice == "3":
        break
    if choice not in ["0","1","2"]:
        continue
    ...
    if user_choice == computer_choice:
        stats["平局"] += 1
    elif (user_choice == 0 and computer_choice == 1) or \
         (user_choice == 1 and computer_choice == 2) or \
         (user_choice == 2 and computer_choice == 0):
        stats["玩家赢"] += 1
    else:
        stats["电脑赢"] += 1

round_count += 1      # 第 69 行：缩进 0 → 在 while 循环【外面】
```

**两个真 bug**

1. **[P0] 第 69 行缩进错了**：`round_count += 1` 顶格写，属于模块级代码，`while` 循环永远执行不到它 → `round_count` 恒为 0 → `round_count >= MAX_ROUNDS` 永远为假 → **"5 局结束并判定胜负"的功能完全失效，只能靠输入 3 手动退出**。
2. **[P1] 第 28 行缺 `f` 前缀**：打印出来是字面量 `---第{round_count + 1}局---`。

**实测证据**（连打 6 局合法输入）：

```
---第{round_count + 1}局，请出拳 ---
---第{round_count + 1}局，请出拳 ---
（共出现 7 次）
退出游戏，最终战绩：
```

7 次局号提示、**没有出现任何"游戏结束"**，证明 5 局上限从未生效。

**写得好的地方**

- 胜负判定矩阵完全正确：0 石头 / 1 剪刀 / 2 布，`0>1`、`1>2`、`2>0` 三条都对。
- `if choice not in ["0","1","2"]` 做了输入校验，并且放在 `continue` 前，脏数据进不来。
- 用 `\` 做多行条件续行——能跑，但 PEP8 更推荐用括号：

```python
    elif (user_choice == 0 and computer_choice == 1
          or user_choice == 1 and computer_choice == 2
          or user_choice == 2 and computer_choice == 0):
```

**其他**

- 胜利后的"最终战绩"打印，在"自然结束"和"主动退出"两处重复了两遍，建议抽成 `print_summary()` 函数（这正好是练习"无参数函数复用"的机会）。
- `names = ["石头","剪刀","布"]` 每轮都重新创建，应提到循环外。
- 没有 `strip()`；`random.randint(0,2)` 的边界是**闭区间**（含 0 和 2），这一点用对了。

### 2.10 `10_add_game.py` —— 数字比大小（规则最完整的一个）

**做得好的地方**（比 09 明显进步）：

- 用 `nums` 列表存历史输入，用 `len(nums)` 当计数器 —— **用数据结构代替计数器变量**，这是很聪明的写法，天然避免了 09 那种"计数器忘记 +1"的 bug。
- 开局把规则打印清楚（3 行说明），交互友好。
- 结束时会打印 `nums`、`sum(nums)` 和战绩，信息完整。
- 输入校验覆盖 1~4。

**问题**

1. **[规则漏洞] 第 59-67 行**：数字相等时（例如双方都是 3），会走到最后的 `else`，打印"电脑赢了"。规则里只说"谁大谁赢、和为 5 平局"，**没有定义相等怎么办**。实测这种情况确实可能发生。建议显式处理：

```python
    if user_num + computer_num == 5:
        print("和为 5，平局")
        stats["平局"] += 1
    elif user_num > computer_num:
        print("你赢了")
        stats["玩家赢"] += 1
    elif user_num < computer_num:
        print("电脑赢了")
        stats["电脑赢"] += 1
    else:
        print("数字相同，平局")        # 把未定义的情况显式补上
        stats["平局"] += 1
```

2. `MAX_TIMES - len(nums)` 在每轮算两次，可提到变量里（小事）。
3. 结束条件 `len(nums) >= MAX_TIMES` 放在循环开头 —— 正确，保证"只输 5 次"。
4. 文件名 `10_add_game.py` 与 `10_make_data.py` 编号重复，建议区分（例如 `10a/10b` 或按主题重命名）。

### 2.11 `10_make_data.py` —— 生成 CSV

```python
import csv

data = [["姓名","班级","语文","数学","英语"],
        ["张三","一班",85,92,78],
        ...]

with open("scores.csv","w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

**这个文件有两个"高级正确点"，而《学习总结》完全没提：**

1. `newline=""`：Windows 上如果不写这个参数，CSV 每行之间会**多出一个空行**（因为 `csv` 自己写 `\r\n`，文本模式又转换一次）。你写对了。
2. `writerows()` 一次写多行，比循环 `writerow()` 更简洁。

**问题**

1. 结尾没有 `if __name__ == "__main__":`，`import` 时会直接重写文件。
2. `encoding="utf-8"` 生成的文件用 Excel 直接双击打开会乱码（Excel 需要 BOM）。如果在 Windows 上主要用 Excel 看，应写 `encoding="utf-8-sig"`；如果只给 pandas 读，`utf-8` 就够。
3. 数据是"列表的列表"，表头单独放在第 0 行，靠人为约定。如果改用 `csv.DictWriter` + 字典列表，可读性更好（这是"字典"知识的自然延伸，你还没练到）。

### 2.12 `11_analysis.py` —— pandas 筛选与统计

```python
df = pd.read_csv("scores.csv")

passed_chines = df[df["语文"] >= 60]        # 布尔索引
average_math = df["数学"].mean()            # Series 均值
print(f"全班的数学平均分是：{average_math:.1f}分")   # 保留 1 位小数，正确

double_good = df[(df["数学"] >80) &(df["英语"] >80)]   # 多条件必须 & + 括号

bad_English_names = df[df["英语"] < 60]["姓名"]        # 链式索引
```

**实测输出**（节选）

```
全班的数学平均分是：79.0分
   姓名  班级  语文  数学  英语
1  李四  一班  76  88  90
4  孙七  三班  88  95  92
==== 英语不及格的名单 ====
5    周八
Name: 姓名, dtype: str
```

**问题**

1. **`passed_chines` 拼写错误**（应为 `passed_chinese`）；`bad_English_names` 用了驼峰+下划线混合。同一个文件里三种命名风格并存，说明命名还没形成规范。PEP8：变量/函数用 `snake_case`。
2. **第 18-20 行缺少小标题**：`print("")` 之后直接输出表格，读者不知道这是"双科优秀名单"。三个板块只有这一个没有标题，输出可读性不一致。
3. **链式索引** `df[mask]["姓名"]` 在 pandas 里不推荐（可能返回副本并触发 `SettingWithCopyWarning`）。规范写法是 `.loc`：

```python
bad_english_names = df.loc[df["英语"] < 60, "姓名"]
```

4. **返回的是 Series 而不是列表**：输出里带 `Name: 姓名, dtype: str`。如果只想看名单，用 `list(...)` 或者 `.tolist()`。
5. `pd.read_csv` 没写 `encoding`。现在能跑是因为 `scores.csv` 是纯 UTF-8；**一旦你用 Excel 打开后按默认方式保存，文件会变成 GBK，`read_csv` 立刻 `UnicodeDecodeError`**。建议固定写 `pd.read_csv("scores.csv", encoding="utf-8")`，或者更稳的 `utf-8-sig`。
6. `>80` 缺空格（PEP8 不一致）。

### 2.13 `12-total-points.py` —— 总分与排序

```python
df["总分"] = df[["语文","数学","英语"]].sum(axis=1)   # axis=1 按行求和，正确
df = df.sort_values(by="总分", ascending=False)      # 降序，正确
print(df[["姓名","总分"]].head(3))                    # 取前 3
```

**实测输出**

```
   姓名   总分
4  孙七  275
2  王五  259
0  张三  255
```

**知识点（也是你还没总结到的）**

- 输出左边的 `4 / 2 / 0` 不是排名，是**原始行索引**。排序不会重排索引，所以看起来"名次乱了"。要得到 1/2/3 需要：

```python
df = df.sort_values(by="总分", ascending=False).reset_index(drop=True)
```

- `df[["语文","数学","英语"]]` 用了**双重方括号**（选出多列形成新表），`axis=1` 表示横向求和。这两个点是 pandas 的高频易错处，你写对了。
- 第 10 行 `print("")` 是多余的空白行。
- 没有 `round(1)`，如果以后有小数总分，会显示一长串。

### 2.14 `12_charts.py` —— matplotlib 绘图

```python
plt.rcParams['font.sans-serif'] = ['SimHei']     # 解决中文乱码
plt.rcParams['axes.unicode_minus'] = False       # 解决负号显示成方块

subjects = ["语文","数学","英语"]                  # 第 11-15 行：整块复制了两遍
average_scores = [df["语文"].mean(), df["数学"].mean(), df["英语"].mean()]
subjects = ["语文","数学","英语"]
average_scores = [df["语文"].mean(), df["数学"].mean(), df["英语"].mean()]

plt.figure(figsize=(8,5))
plt.bar(subjects, average_scores, color=['skyblue','orange','lightgreen'])
plt.title("各科平均分对比图", fontsize=16)
plt.xlabel("科目", fontsize=12)
plt.xlabel("平均分", fontsize=12)          # 第 22 行：应为 ylabel

for i, v in enumerate(average_scores):
    plt.text(i, v + 1, f"{v:1f}", ha='center', fontsize=12)   # 第 25 行：格式符错

plt.show()

plt.figure(figsize=(8,5))
plt.plot(df["姓名"], df["数学"], marker='o', color='red', linestyle='--')
plt.title("学生数学成绩折线图", fontsize=16)
plt.xlabel("姓名")
plt.xlabel("分数")                        # 第 35 行：应为 ylabel
plt.grid(True)
plt.show()
```

**四个问题**

1. **[P1] 第 22、35 行 `ylabel` 写成了 `xlabel`**：两次都错，说明不是手滑，而是**对这个 API 没形成记忆**。后果：Y 轴没有名称，X 轴标签被覆盖成"平均分"/"分数"，图能出来但语义是错的。这正是《学习总结》第 7 条记录的，**仍未修**。
2. **[P1] 第 25 行 `f"{v:1f}"` 格式符错误**。实测：

```
:1f   -> 85.333333
:.1f  -> 85.3
```

   `1` 是"最小宽度"，`f` 是"浮点类型"，精度没写时默认 **6 位小数**。所以柱子上方会显示 `85.333333` 这种长串。正确写法 `f"{v:.1f}"`（你已经在 `11_analysis.py` 里写对过 `{average_math:.1f}`，说明是迁移时丢了那个点）。

   > 格式符语法速记：`{值:[填充][对齐][符号][宽度][,][.精度][类型]}`，例如 `{v:>8.2f}` = 右对齐、宽 8、保留 2 位小数、浮点。

3. **第 11-15 行整块复制粘贴**，重复计算了两遍均值（浪费且容易改漏一处）。
4. **两张图共用 `plt.show()` 流程**：`plt.show()` 是阻塞的，关掉第一张后才会创建第二张；而且没有 `plt.close()`，图对象会一直挂着。做多图时建议：

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))    # 一张画布两个子图
axes[0].bar(subjects, average_scores)
axes[0].set_title("各科平均分")
axes[0].set_ylabel("平均分")                        # 注意是 set_ylabel
axes[1].plot(df["姓名"], df["数学"], marker="o")
axes[1].set_ylabel("分数")
fig.tight_layout()
plt.savefig("charts.png", dpi=150)                  # 先存盘，再显示
plt.show()
```

另外 `['SimHei']` 在没装该字体的机器上会静默变方块，建议写 `['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']` 作为回退链。

---

## 三、10 个自定义函数逐个详解（含统计结论）

| # | 函数 | 位置 | 参数 | 返回值 | 读全局 | 写全局 |
|---|---|---|---|---|---|---|
| 1 | `add_contacts()` | 06:3 | 无 | `None` | `contacts` | 改 `contacts[name]` |
| 2 | `show_contacts()` | 06:12 | 无 | `None` | `contacts` | 无 |
| 3 | `delete_contacts()` | 06:20 | 无 | `None` | `contacts` | `del` |
| 4 | `main()` | 06:43 | 无 | `None` | `contacts`（间接） | 间接 |
| 5 | `load_data()` | 07:9 | 无 | `dict` | 常量 `FILE_NAME` | 无 |
| 6 | `save_data()` | 07:15 | 无 | `None` | `contacts` | 写文件 |
| 7 | `add_contacts()` | 07:21 | 无 | `None` | `contacts` | 改 + 写文件 |
| 8 | `show_contacts()` | 07:32 | 无 | `None` | `contacts` | 无 |
| 9 | `delete_contacts()` | 07:40 | 无 | `None` | `contacts` | `del` + 写文件 |
| 10 | `main()` | 07:62 | 无 | `None` | `contacts`（间接） | 间接 |

**统计结论（这就是最需要补的一课）**

- **带参数的函数：0 / 10**
- **有返回值的函数：1 / 10**（只有 `load_data`）
- **用 `return` 提前结束的函数：0 / 10** —— 而 06 的崩溃，恰好就是"少了一个 `return`"
- **写 `if __name__ == "__main__":` 的文件：0 / 14**

`def` 只是"把代码装进盒子"，**函数的真正价值在参数（输入）和返回值（输出）**。你现在所有函数都靠全局变量通信，等于把盒子的线全接到同一块电路板上，所以：

- 无法测试：`add_contacts()` 内部调 `input()`，不给键盘输入就跑不了；
- 无法复用：换一个界面（网页/命令行参数）就得重写；
- 容易出作用域 bug：`06` 的 `UnboundLocalError` 就是这么来的。

**同一份逻辑，改成"参数 + 返回值"后长这样：**

```python
def add_contact(contacts, name, phone):
    """新增联系人。返回 (是否成功, 提示信息)。"""
    if not name:
        return False, "姓名不能为空"
    if name in contacts:
        return False, f"{name} 已经存在"
    contacts[name] = phone
    return True, f"已保存：{name}，电话：{phone}"

# 调用方负责输入输出
ok, msg = add_contact(contacts, name, phone)
print(msg)
```

这样 `add_contact` 可以直接用断言测试，也能被任何界面调用。**这是你从"会写 def"到"会用函数"的关键一跳。**

---

## 四、语法与格式：三档盘点

### A. 已牢固掌握（代码证据充分）

| 语法点 | 证据 |
|---|---|
| 变量、`int()`/`str()` 转换 | 全部文件 |
| `input()` / `print()` | 全部文件 |
| f-string 基本用法 | `f"同学：{name}"` |
| f-string 精度 `{x:.1f}` | `11_analysis.py:15` |
| `if/elif/else`、`while`、`for...in range()` | 全部 |
| `break` / `continue` | `count-01.py`、`09` |
| `+=` 自增 | `09:59`、`10_add_game:61` |
| `len()` / `sum()` / `append()` | `list-01.py`、`10_add_game` |
| 列表下标、`range(len())` | `06:26`、`09:50` |
| 字典 `{}` 创建、`in` 判重、`.items()`、`del` | `dictionary-01.py`、`06` |
| `try` 之外的输入分支校验 `isdigit()` | `06:31`、`07:50` |
| 链式比较 `1 <= x <= n` | `06:33`（写法正确，但没说清原理） |
| 函数定义与调用、菜单分发 | `06`、`07` |
| `with open()` 上下文管理器 | `07`、`10_make_data` |
| `json.dump/load` + `ensure_ascii`/`indent` | `07` |
| `csv.writer` + `newline=""` | `10_make_data`（很到位） |
| `os.path.exists` | `07:10` |
| pandas 布尔索引、多条件 `&` + 括号 | `11_analysis` |
| `.mean()` / `.sum(axis=1)` / `.sort_values` / `.head()` | `11`、`12` |
| matplotlib 中文字体、柱状图、折线图、标注 `plt.text` | `12_charts` |
| `enumerate` 遍历 | `12_charts:24` |
| `\` 续行 | `09:60-62` |
| `random.randint` 闭区间 | `09`、`10_add_game` |

### B. 会用但不牢（有错例）

| 语法点 | 问题 | 位置 |
|---|---|---|
| f-string 前缀 | 写了 `{}` 却漏 `f` | `09:28` |
| 格式符 | `:1f` 应为 `:.1f` | `12_charts:25` |
| 缩进决定归属 | 循环体外的 `+1` 导致功能失效 | `09:69` |
| 缩进决定归属（2） | `input` 少缩进一级，空分支崩溃 | `06:29` |
| `print` 参数 | `print(x),{y}` 误以为能拼接 | `07:47` |
| `label` 成对使用 | `xlabel` 写了两次 | `12_charts:22,35` |
| 命名规范 | `passed_chines` / `bad_English_names` / `figure` 混用 | `11` |
| 元组 vs 集合 | `{names[i]}` 被当成集合丢弃 | `07:47` |

### C. 完全没用到（这就是"没总结到"的语法面）

| 语法/特性 | 为什么必须有 | 在哪个文件里本该用 |
|---|---|---|
| **函数参数与返回值** | 函数的本质 | `06`/`07` 全部 |
| **`if __name__ == "__main__":`** | 让文件可导入、可测试 | 全部 14 个 |
| `return` 早返回（卫语句） | 扁平化嵌套、防 `UnboundLocalError` | `06:20` |
| **局部/全局作用域规则（`UnboundLocalError` 原理）** | 你已经被它坑过 | `06:33` |
| 默认参数 / 关键字参数 | 写 `def show(contacts, verbose=False)` | `07` |
| **`try/except/else/finally`** | 文件、类型转换都必须 | `07:12`、所有 `int(input())` |
| `str.strip()` / `.lower()` / `.split()` / `.join()` | 输入清洗，几乎所有 bug 的根因 | 全部 `input()` |
| `ValueError` 的捕获 | `int("abc")` 必炸 | `loop-01`、`average-01` |
| **列表推导式** | 目前全是 `for + append` | `list-01`、`12_charts:12` |
| 字典 `.get(key, default)` | 避免 `KeyError` | `dictionary-01`、`06` |
| 字典推导式 / `sorted(d.items(), key=...)` | 通讯录排序 | `07` |
| 元组（unpacking）、集合 `set()` | 去重、判重更快 | 全缺 |
| 切片 `scores[1:3]`、负索引 `scores[-1]` | 列表基本功 | `list-01` |
| `enumerate(..., start=1)` | 编号从 1 开始 | `06:26` |
| `zip()` | 同时遍历两个列表 | `12_charts` |
| `round()` / `Decimal` | 金额、平均分取整 | `average-01` |
| `print(..., end="")` / `sep=` | 控制输出格式 | 全部 |
| 真值判断（`if not contacts:`） | 比 `len()==0` 更 Pythonic | `06`、`dictionary-01` |
| **`Path`/`pathlib`、绝对路径** | 避免"换个目录就找不到文件" | `07`、`10_make_data` |
| 模块拆分（`import` 自己的文件） | 文件名必须符合标识符 | 带 `-` 的 6 个文件 |
| 文档字符串 / 类型注解 | 让别人（和 3 个月后的你）看懂 | 10 个函数全部缺 |
| 断言 `assert` / `unittest` / `pytest` | 让"学过"变成"验证过" | 全部 |
| pandas `.loc` / `.iloc` | 规范取值，避免链式索引 | `11:23` |
| pandas `.reset_index(drop=True)` | 排序后名次才连续 | `12-total-points:7` |
| pandas `groupby` | "按班级统计平均分"是一个现成的问题 | `11` |
| `pd.read_csv(encoding=...)` | 防 GBK/UTF-8 打架 | `11`、`12` |
| matplotlib `savefig` / `tight_layout` / `subplots` | 出图存档、多图排版 | `12_charts` |

---

## 五、Bug 清单（按严重度排序，均给定位与修法）

### P0 — 会导致崩溃或核心功能失效

| # | 问题 | 位置 | 现象 | 修法 |
|---|---|---|---|---|
| 1 | `delete_contacts()` 空通讯录时未 `return`，`names` 未赋值 | `06_function_contacts.py:20-41`（`input` 在 29 行，`len(names)` 在 33 行） | 实测 `UnboundLocalError` 直接退出程序 | 空分支末尾加 `return`，并把 `names` 提到函数开头 |
| 2 | `round_count += 1` 写在 `while` 外面 | `09_rps_game.py:69` | 实测局数恒为 0，"5 局结束判胜负"永不触发 | 缩进 4 空格移进循环体 |
| 3 | `load_data()` 不处理空/损坏 JSON | `07-file-test.py:9-13` | 文件被清空后，**启动即崩**（`JSONDecodeError`），菜单都进不去 | 加 `try/except (json.JSONDecodeError, OSError)` + `isinstance` 校验 |

### P1 — 功能可见错误

| # | 问题 | 位置 | 现象 | 修法 |
|---|---|---|---|---|
| 4 | 删除列表打印写成元组表达式 | `07-file-test.py:47` | 实测只显示 `1`，姓名丢失 | `print(f"{i+1}.{names[i]}")` |
| 5 | 局号缺 `f` 前缀 | `09_rps_game.py:28` | 实测打印字面量 `{round_count + 1}` | 加 `f` |
| 6 | Y 轴标签写成 `xlabel`（两处） | `12_charts.py:22,35` | 图无 Y 轴标题，X 轴标签被覆盖 | 改为 `plt.ylabel(...)` |
| 7 | 格式符 `:1f` | `12_charts.py:25` | 实测柱顶显示 `85.333333` | 改为 `:.1f` |
| 8 | 人数打印成列表 | `list-01.py:19` | 实测"一共录入了['张三',...]位同学" | `{len(classnames)}` |
| 9 | 序号从 0 开始 | `average-01.py:8` | 实测"请输入第0个成绩" | `{i+1}` |

### P2 — 健壮性 / 可读性 / 规范

| # | 问题 | 位置 | 修法 |
|---|---|---|---|
| 10 | `int(input())` 无 `ValueError` 防护 | `loop-01`、`average-01` 等 | 先 `isdigit()` 或 `try/except` |
| 11 | 所有 `input()` 无 `strip()` | 全部 | `.strip()`（`choice` 尤其必要） |
| 12 | 数字相等时判"电脑赢" | `10_add_game.py:59-67` | 显式补平局分支 |
| 13 | `main()` 模块级调用，不可导入 | `06:67`、`07:84` | `if __name__ == "__main__": main()` |
| 14 | 6 个文件名带连字符，不可 `import` | `list-01.py` 等 | 改下划线：`list_01.py` |
| 15 | 两个文件都以 `10` 开头 | `10_add_game` / `10_make_data` | 重命名区分 |
| 16 | 两个文件整篇注释，不可运行 | `loop-01.py`、`check_age.py` | 保留可运行版本 + `assert` 自测 |
| 17 | 错别字：`电话时`、`建议通讯录` | `dictionary-01:22`、`06:44`、`07:63` | 改正 |
| 18 | `print(f"...")` 无占位符仍加 `f` | `06:52` | 去掉 `f` |
| 19 | `len(x)==0` 不用真值判断 | `06`、`dictionary-01` | `if not x:` |
| 20 | 重复代码块 | `12_charts:11-15`、`09` 的战绩打印 | 提函数/删重复 |
| 21 | 排序后未重置索引 | `12-total-points` | `.reset_index(drop=True)` |
| 22 | 链式索引 | `11:23` | `.loc[mask, "姓名"]` |
| 23 | CSV 相对路径 + 无编码参数 | `07`、`11`、`12` | `Path` + `encoding="utf-8"` |
| 24 | 残留无关演示代码 / 空行 / 行尾空格 | `list-01:1-5`、`count-01:27`、`12-total:10` | 清理 |

---

## 六、《学习总结.txt》没覆盖到的方面（重点章节）

### 6.1 先看一张"病历本闭环"对照表

《学习总结.txt》第二部分记录了你 7 条典型错误。我逐条回到代码里核对，结果是：

| 病历条目 | 总结里说了 | 现在的代码 | 是否真的修好 |
|---|---|---|---|
| 1. `or` 用错（`score < 0 or score > 100`） | 已记录 | `loop-01.py:3` 代码已是 `> 100 or < 0`，但**整段被注释** | 无法验证（不可运行） |
| 2. 先存后查重（顺序问题） | 已记录 | `dictionary-01.py:17`、`06:5`、`07:23` 都是**先查后存** | 已修好 |
| 3. `=`/`-` 手滑、`frist.py`、变量首字母大写 | 已记录 | 错别字仍在（`电话时`、`建议通讯录`、`passed_chines`） | 部分未修 |
| 4. `round_count += 1` 写在循环外 | 已记录 | `09_rps_game.py:69` **仍在循环外** | **未修（P0）** |
| 5. `len(contacts) == "0"` | 已记录 | 已改为 `== 0` | 已修好 |
| 6. 空文件导致 `json.load` 崩溃 | 已记录 | `07:12` **没有 try/except** | **未修（P0）** |
| 7. `plt.xlabel` 写两次 | 已记录 | `12_charts.py:22,35` **仍然是 xlabel** | **未修（P1）** |

**这张表本身就是最重要的结论**：你的"诊断能力"已经建立起来了，但"诊断 → 改代码 → 跑一遍确认"这一步没走完。建议把《学习总结》当成一份 **TODO 清单**，每条后面加一个"已修复 + 验证输出"，否则它只是一份读后感。

### 6.2 概念层面漏掉的（比语法更重要）

1. **函数的作用域规则**：为什么 `06` 报 `UnboundLocalError` 而不是 `NameError`。核心：**函数内只要有赋值语句，该名字在整个函数内都是局部变量**。总结里一个字没提，而这恰好是你唯一一次真正的崩溃。
2. **`return` 的语义**：`return` 不只是"返回值"，更是"提前结束函数"。你的 10 个函数**没有一个用过它**，所以没想到"空通讯录要 return 走人"。卫语句（guard clause）是把嵌套压平的通用手法。
3. **参数的两种风格**：位置参数 vs 关键字参数、默认值、`*args`/`**kwargs`（暂不需要），但"函数应该通过参数接收数据、通过返回值输出结果"这个原则必须建立。
4. **可测试性**：为什么 `add_contacts()` 里不该写 `input()`。判断标准很简单：**这个函数能不能在不碰键盘和屏幕的情况下被调用？** 不能，就说明它把"输入输出"和"业务逻辑"耦合在一起了。
5. **异常是控制流的一部分**：`try/except` 不是为了"让报错消失"，而是为了"在系统边界（用户输入、文件、网络）把非预期情况翻译成可理解的行为"。你只把它当成"JSON 崩溃的补丁"，没有把它当成一种常规写法。
6. **相对路径 vs 当前工作目录**：`"scores.csv"` 指的是"启动时所在目录"，不是"脚本所在目录"。这是"我本地能跑，换个地方就找不到文件"的最常见原因。
7. **数据结构选择**：用 `nums` 的 `len()` 代替计数器（`10_add_game` 做对了），用列表存多条记录 vs 用字典做索引 —— 选择结构本身就是设计，而不只是语法。
8. **程序边界**：哪些数据来自"外部"（用户、文件、网络），哪些是"内部可信"的。边界上必须校验，内部不必层层防御。你现在的校验位置是对的（`choice`、`isdigit`），但外部输入没做 `strip()` 和类型防护，边界还没封严。

### 6.3 语法/API 层面漏掉的

1. **`{v:1f}` vs `{v:.1f}`**：格式符的语法结构（宽度 / 精度 / 类型），总结只说"保留小数用 `:.1f`"，没说 `:1f` 会变成 6 位小数。
2. **`print(a), b` 不是拼接**：逗号在表达式层面构造元组，`{names[i]}` 是集合。同一个花括号的三种含义（集合 / 字典 / f-string 替换字段）。
3. **f-string 的 `f` 前缀是语法的一部分**：漏了就变成普通字符串，而且**不报错**，属于"静默失败"，最危险。
4. **缩进的语义**（不只是"对齐好看"）：`09` 的 `+1` 少缩进 4 格、`06` 的 `input` 少缩进 4 格，两次都是"能用语法跑、但逻辑全变"。
5. **`enumerate()` 与 `range(len())` 的区别**：你两处用了 `range(len())`（`06:26`、`09:50`），一处用了 `enumerate`（`12_charts:24`），说明会用但没固定成习惯。
6. **`sum()` / `min()` / `max()`**：`average-01.py` 手写累加，说明"内置函数"还没进入条件反射。
7. **列表推导式**完全没有出现：`[df["语文"].mean(), df["数学"].mean(), df["英语"].mean()]` 正是 `[df[c].mean() for c in subjects]` 的典型场景。
8. **`dict.get()`** 没有出现：以后做"修改联系人"、"统计词频"会立刻需要它。
9. **`str` 方法族**（`strip/split/join/replace/startswith`）几乎没用过，而输入清洗是 bug 第一来源。
10. **`if __name__ == "__main__":`** 从未出现，导致 14 个文件都是"一导入就执行"。
11. **`assert` / `pytest`** 从未出现，"学过 → 验证过"缺少最后一步。
12. **文档字符串与类型注解**：`def load_data() -> dict:` 一行注解就能省掉很多猜测。
13. **PEP8 细节**：`=` 两侧空格、逗号后空格、`return {}`、双空格（`len(contacts)  == 0`）、行尾空格、多余的空 `print("")`。
14. **`python -m py_compile` / 静态检查**：`flake8`、`ruff` 能直接揪出 `f-string 无占位符`、缺空格、未使用变量 `i`、未定义名字等问题，比人眼快得多。

### 6.4 数据分析 / 可视化层面漏掉的

1. **CSV 编码三角问题**：`utf-8`（pandas 友好） vs `utf-8-sig`（Excel 友好） vs `gbk`（Excel 另存默认）。现在 `scores.csv` 是纯 UTF-8（实测无 BOM），所以能跑；Excel 一介入就可能坏。
2. **`newline=""` 的必要性**：Windows 上写 CSV 不加它会多出空行。你写对了，但总结没记录"为什么"。
3. **索引不是名次**：`sort_values` 后左侧仍是原始索引（`4/2/0`），要 `reset_index(drop=True)`。
4. **`.loc` vs 链式索引**：`df[mask]["姓名"]` 可能拿到副本，规范写法 `.loc[mask, "姓名"]`。
5. **Series 的输出形态**：不带 `.tolist()` 会打印 `Name: 姓名, dtype: str` 等元信息。
6. **`axis=0` 与 `axis=1` 的区别**：`axis=1` 才是"按行求和"（每个学生的总分）。你用对了，但总结里只写了"`.sum(axis=1)`"，没解释 axis 的含义。
7. **matplotlib 的中文字体链**：`['SimHei']` 单字体在别的机器上会静默变方块，应该给回退列表。
8. **`plt.show()` 是阻塞的**、多图应 `subplots` + `savefig` + `close`。
9. **`groupby`**：`11_analysis.py` 手工筛"一班/二班"，其实 `df.groupby("班级")["语文"].mean()` 一行就够。这是"分组聚合"的入门点。
10. **数据校验**：读进来的 CSV 没有检查行数、缺失值（`df.isna().sum()`）、成绩是否越界（`df[(df["数学"]<0)|(df["数学"]>100)]`）。真实数据一定脏。

### 6.5 工程与学习流程层面漏掉的

1. **文件命名规范**：课程编号用 `-`（`list-01.py`）不可导入；`06_`/`07_` 用下划线，两套风格混用；两个 `10_` 重名。建议统一 `NN_主题.py`。
2. **一个文件一个程序**：14 个文件里 2 个是纯注释、好几个是"练习碎片"。建议整理成 `01_basics/02_structures/03_functions/04_files/05_pandas` 五个目录。
3. **版本管理**：没有 git。改坏了没法回退，也看不到"错误版本 → 正确版本"的演进（而这正是学习最有价值的部分）。
4. **验证习惯**：本次复盘能确认的 4 个 bug，全都只有**真正运行**才暴露（`UnboundLocalError`、局号字面量、只打印编号、`85.333333`）。读代码时它们看起来都"很像对的"。
5. **总结要带可执行证据**：好的总结格式是「错误现象 → 最小复现代码 → 正确代码 → 运行输出」，你现在是「错误现象 → 避坑指南」，缺后两段。
6. **调试手段**：没有用过断点、`print(repr(x))`、`type(x)` 来确认类型。例如 `07:47` 打印出 `{'张三'}`（带花括号）就会立刻暴露集合问题。

---

## 七、下一步怎么做（按顺序，4 步）

1. **修 3 个 P0**（30 分钟，收益最大）
   - `06` 加 `return`；`09` 的 `round_count += 1` 缩进进循环；`07` 的 `load_data` 加 `try/except`。
   - 每改一个，**跑一遍并保存输出**，贴到《学习总结》对应条目后面，把"病历本"变成"已修复清单"。
   已经修复

2. **把函数升级成"带参数 + 带返回值"**（1 小时）
   - 目标：`add_contact(contacts, name, phone) -> tuple[bool, str]`，`save_data(data)`，`load_data() -> dict`。
   - 验收标准：能写 3 行 `assert` 测出"重名返回 False"，全程不出现 `input()`。

3. **加一层输入防护 + 主入口**（30 分钟）
   - 所有 `input()` 加 `.strip()`；所有 `int()` 前先判断或包 `try`；所有文件末尾加 `if __name__ == "__main__":`。
   - 验收标准：乱输入（空回车、字母、空格、超大数字）都不会让程序退出。

4. **完成 pandas 的"下一步"**（1 小时）
   - `df.groupby("班级")[["语文","数学","英语"]].mean()`；`reset_index(drop=True)`；`.loc` 取值；`encoding` 显式声明；`subplots` + `savefig` 一次出两张图。
   - 验收标准：新增一个 `13_report.py`，输出"班级排名 + 三科对比图 PNG"，不打开窗口也能存盘。

---

### 附：一句话记住这次复盘的 4 个教训

1. **总结完必须回改代码，并跑一次**——否则病历本只是读后感（6.1 节有 3 条未修的现成证据）。
2. **函数要有参数和返回值**，别靠全局变量通信；`return` 也用来"提前退出"。
3. **带 `{}` 的字符串别忘了 `f`**；`{v:1f}` 不等于 `{v:.1f}`；`print(a), b` 不是拼接。
4. **缩进就是逻辑**：`+1` 少缩一格 → 功能失效；`input` 少缩一格 → 程序崩溃。

---

*报告生成时间：2026-10-30；基于工作区内 14 个 `.py` 文件的静态通读 + 6 次实际运行验证。*
