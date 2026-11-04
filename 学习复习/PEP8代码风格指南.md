# PEP 8 Python 代码风格指南（整合版）

> 来源：Python 官方 PEP 8 *Style Guide for Python Code*（https://peps.python.org/pep-0008/），文档字符串规范见 PEP 257。
> 适用场景：Python 3 项目编写、代码评审、入职规范培训。
> 一句话原则：**可读性优先**；风格约定服务于人，而非服务于教条。

---

## 0. 总则：一致性

PEP 8 把"可读性"放在首位，并给出**三层一致性的优先级**（越靠后越重要）：

1. 与本指南一致；
2. 与**项目内**其他代码一致；
3. 与**你正在修改的那段代码周围**的风格一致。

进入一个既有代码库时，先看别人怎么写：如果都用双引号，你也用双引号。风格指南的意义在于一致性，而冲突时用判断力取舍：

> A foolish consistency is the hobgoblin of little minds. —— Emerson（PEP 8 引用此句提醒：不要为了机械对齐而写出更差的代码）

PEP 8 同时明确，**有些约定允许被有意打破**：例如项目已有的风格与本指南冲突时保持原有风格；或某条规则会让代码明显更难读时。有疑问时不要靠"压缩到一行"来省行数。

对新项目，PEP 8 建议直接用格式化工具（Black / Ruff formatter）强制风格，把人工精力留给 API 设计；只有需要偏离工具默认（如行宽）时才需要在文档中解释。

---

## 0.1 一条元原则

"可读性 counts"具体体现在：变量与函数命名应**有意义且可读**；注释描述"为什么"而非"做了什么"（做什么应由代码本身表达）；风格服务于降低阅读成本，而非增加心智负担。

---

## 1. 代码布局（Code Lay-out）

### 1.1 缩进

- 每级缩进 **4 个空格**。
- 续行有两种合法写法：**与左括号后第一个元素对齐**，或使用**悬挂缩进**（首行不放参数）。
- 使用悬挂缩进时，建议再加一级缩进，使参数行与函数体明显区分。

```python
# 正确：与左括号内的参数对齐
foo(long_argument_1, long_argument_2,
    long_argument_3, long_argument_4)

# 正确：悬挂缩进 + 额外一级缩进（首行不放参数）
foo(
    long_argument_1,
    long_argument_2,
    long_argument_3,
)

# 正确：函数体与参数列表缩进不同层，避免视觉混淆
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# 错误：续行额外缩进，看起来像新的代码块
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# 错误：续行没有比函数体多出可辨识的缩进层级
foo = long_function_name(
var_one, var_two,
var_three, var_four)
```

### 1.2 空格还是 Tab

- **空格是首选的缩进方式**；Tab 只用于保持与使用了 Tab 的既有代码一致。
- Python 3 禁止混用 Tab 与空格做缩进；混用的文件必须整体转换为一种（`2to3` 或编辑器批量替换）。Python 2 时代的 `-t` / `-tt` 检查选项在 3.x 已移除。
- 编辑器应配置为输入 Tab 时插入 4 个空格；显示 Tab 时给出可见标记。

### 1.3 行最大长度

- 所有行 **不超过 79 字符**。
- docstring、注释这类**纯文本块不超过 72 字符**（续行缩进后再折行）。
- 项目内自由使用的行长度限制应**不超过 99 字符**；只有当团队明确同意时才可用 80–100 的折行。
- 限制行长提升多窗格并排阅读、版本控制工具（如 diff）的可用性。
- 折行优先使用**隐式续行**：括号、方括号、花括号内换行不需要反斜杠（折行位置见 1.4）。

```python
# 正确：括号内隐式续行，无需反斜杠
result = (left_hand_side
          + right_hand_side)

# 正确：多个上下文管理器共用一行括号
with open('one') as f, open('two') as g:
    ...

# 正确：反斜杠续行（仅在无法隐式续行时使用，如过长的 with 语句）
with open('/very/long/path/one') as f, \
     open('/very/long/path/two') as g:
    ...
```

### 1.4 二元运算符处折行

PEP 8 对新代码推荐 **Knuth 风格**：**在二元运算符之前折行**，这样每行开头的运算符一眼可见，无需逐字符检查行尾。

```python
# 推荐
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction)

# 旧代码常见，不推荐给新代码
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction)
```

若已有代码库使用另一种风格，保持一致即可。

### 1.5 空行

- 顶层函数、类定义之间：**2 个空行**。
- 类内的方法定义之间：**1 个空行**。
- 相关的全局变量赋值组之间可插入 1 个空行。
- 函数内部**逻辑分组**之间可按需插入空行，但不要滥用。
- 文件首部：`#!/usr/bin/env python3` 与模块 docstring / import 之间空 1 行；import 块与首个顶层定义之间空 2 行。
- 每行只允许一条语句（禁止 `x = 1; y = 2` 这类分号压缩写法）。

### 1.6 源文件编码

- 遵循 **PEP 263**：需要非默认编码时用 `# -*- coding: utf-8 -*-` 声明，且必须位于第 1 或第 2 行。
- **core Python 库代码一律使用 UTF-8**，不使用其他编码（仅测试特殊编码行为的代码例外）。
- Python 3 源文件默认即 UTF-8，通常**不需要**显式声明；不要混用编码声明与字节串技巧。

### 1.7 导入约定

**分组顺序**（组间空 1 行，组内不排序除非项目另有约定）：

1. 标准库（future 导入单独成组，置于最顶）
2. 第三方库
3. 本地 / 项目内模块

```python
import os
import sys
from typing import Optional

import requests
from flask import Flask

from myproject.config import settings
from myproject.utils import helpers
```

规则要点：

- **每个模块单独一行 import**（`from` 一次导入多个名字可以合并）：

```python
# 正确
import os
import sys

# 正确：同一 from 导入多个名字
from subprocess import Popen, PIPE

# 错误：整模块用逗号合并
import sys, os
```

- **推荐绝对导入**，更清晰且失败更早（尤其在 `sys.path` 被操纵时）：

```python
import mypkg.sibling           # 绝对导入
from . import mylib            # 显式相对导入（包内）
from ..mylib import myfunc     # Python 3 中相对导入必须显式
```

- 函数内部导入只有在**规避循环依赖、加速启动、隔离平台相关依赖**等合理场景才允许，并且要在 docstring 或注释中说明原因。
- **避免 `from module import *`**：污染命名空间、静态工具无法解析同名符号。
- 包与模块的**文件名必须是合法 Python 标识符**（全小写、不含短横线），否则 `import` 直接语法报错。
- `__future__` 导入必须位于模块 docstring 之后、其他代码之前（注释可在其前）。

### 1.8 模块的特殊变量名（dunder）

模块级"双下划线"变量（`__all__`、`__author__`、`__version__` 等）**放在模块 docstring 之后、其他 import 之前**（`__future__` 例外，必须最靠前）。

```python
"""One line docstring.

Multi line description.
"""

__all__ = ["foo", "bar"]
__version__ = "0.4"

import threading
```

`__all__` 只影响 `from module import *` 的行为，因此**只为确实打算被 `import *` 使用的模块**定义它；不要把内部名字或从别的模块导入的名字（包括 `os.path` 这类）写进去。

### 1.9 日志相关命名

- 获取 logger 用标准命名：`logger = logging.getLogger(__name__)`。
- 在库代码中不要配置 handler，交由应用侧配置。

### 1.10 字符串

- **单引号与双引号等价**，但同一项目内保持一致。
- **docstring 一律使用双引号**（PEP 257）。
- 字符串内含引号时，用双引号包裹以避免转义：`"don't"` 优于 `'don\'t'`。
- 三元组引号中，**结束引号独占一行**；多行文本的第一行紧跟开始引号。

```python
def cos(x):
    """Return the cosine of x, in radians.

    The leading space in this comment is important.
    """
    ...
```

- f-string 中表达式内不要重复使用同类引号（Python 3.12+ 已放开限制，但跨版本代码仍应保守）。
- 字符串前缀统一**小写**：`r`、`b`、`f`、`u`，组合写作 `rb`（不要 `Rb`、`B`）。小写前缀在不同字体下不易误读。
- 数字字面量中的幂后缀建议用**大写 `E`**（`1E10`），因为小写 `e` 在某些字体里易与 `0` 混淆。

---

## 2. 表达式与语句中的空白（Whitespace）

### 2.1 应避免的空白

- 括号、方括号、花括号的**内侧**：

```python
# 正确
spam(ham[1], {eggs: 2})
# 错误
spam( ham[ 1 ], { eggs: 2 } )
```

- 逗号、分号、冒号**之前**：

```python
# 正确
if x == 4: print(x, y); x, y = y, x
# 错误
if x == 4 : print(x , y) ; x , y = y , x
```

- 函数调用的左括号、索引/切片的左括号**之前**：

```python
# 正确
spam(eggs, 'stray')
lower = ham[1:9]
# 错误
spam (eggs, 'stray')
lower = ham [1:9]
```

- 单元素元组的逗号后不要加空格（`foo = (0,)` 正确，`foo = (0, )` 错误）。
- **赋值运算符 `=` 两侧各 1 个空格**；但作为**关键字参数或默认值**的 `=` 两侧**不加空格**：

```python
# 正确
i = i + 1
submit(a, b)
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

- 当 `=` 同时用于**类型标注和默认值**时，只在 `=` 两侧加空格，`:` 之前不加、之后加：

```python
def multiply(m: int, x: float) -> int: ...
def tagged(name: str, *, color: str = "white"): ...
```

### 2.2 建议的空白

- 二元运算符两侧各 1 个空格：`a = b + c`、`x < y and y <= z`。
- 幂运算 `**` 优先级最高：当**两侧都是简单标识符/字面量**时不加空格（`x = x**2`、`e = mc**2`）；指数本身是复杂表达式时才加空格。
- 为体现运算优先级，**高优先级运算可以少加空格**，但必须在整段内保持一致：

```python
# 正确：* 优先级高于 -，紧贴写以体现层次
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

- 逗号、分号之后加 1 个空格。
- 冒号在切片中两侧空格一致，`k[: hi + j]` 这类表达式要把它当成整体：

```python
ham[1:9], ham[x + y : j]
```

- 扩展切片中 `::` 两侧一致（都无空格或都有空格）：`ham[lower+offset : upper+offset]`。
- 行末**不要有尾随空白**（trailing whitespace）：`re.sub(r'\s+$', '', s, flags=re.M)` 可清理。

### 2.3 为对齐而使用的额外空格

在**一组相关的连续赋值**中，用额外空格把 `=` 对齐是可以接受的，有助于快速比较取值：

```python
# 可接受
x           = 1
y           = 2
long_name   = 3
```

但不建议：为了对齐而在不相关的语句间补空格；跨多行的复杂表达式里做列对齐；以及把多条语句挤在同一行来配合对齐。若对齐维护成本高（新增变量就要重排），直接放弃对齐。

### 2.4 其他空白提示

- 语句独占一行。
- 不要在语句末尾使用分号（多语句合一）来压缩代码。

---

## 3. 尾随逗号（Trailing Commas）

- **只有一个元素的元组必须加尾随逗号**：`foo = (0,)`。
- 尾随逗号在以下情况是**可选但合法**的：参数列表、索引/切片、字面量集合。
- **尾随逗号只用于多行结构**；单行不要加。
- 多行的字面量、参数列表使用尾随逗号能让版本控制 diff 更干净（新增元素时上一行不被改动）：

```python
# 推荐
GROUND_NEUTRAL_SIX = [
    0.506,
    0.479,
    0.509,
]

# 不推荐：新增元素会改动上一行
GROUND_NEUTRAL_SIX = [
    0.506,
    0.479,
    0.509
]
```

- 若右括号与结构首行在同一行，则不要加尾随逗号。

---

## 4. 注释（Comments）

- **能自解释的代码优于注释**；注释要简短、切中要点。
- 注释必须以 `#` 加 1 个空格开头。
- **块注释**：与所描述代码同缩进；`#` 后 1 空格；段落内行首 1 空格；句子结尾用句点；空行用只含一个 `#` 的行分隔。
- **内联注释**：尽量少用；与代码至少隔 **2 个空格**，`#` 后 1 空格；右侧对齐不是必须。
- **实现注释**（放在函数/类下方，缩进一致）：说明实现细节、为何如此实现、算法复杂度等，只有当实现本身不自明时才写。
- **不要写与代码矛盾的注释**——过时注释比没有注释更糟。
- **TODO 注释**格式：

```python
# TODO(负责人): 描述这一行需要做什么
# TODO(tim.golden@python.org): Refactor this to use a cleaner approach.
```

- 块注释中的段落：以 `#` 开头，行内缩进 1 空格。
- 标点符号与句子间空格规范：句末用句点。

---

## 5. 文档字符串（Documentation Strings）

遵循 **PEP 257**，要点：

- 所有公共模块、函数、类、方法都应有 docstring；私有函数也可（说明用途与调用条件）。
- 多行 docstring：首行是**简短、面向读者的一行摘要**（祈使句、首字母大写、句末不加句点）；第二行空行；随后是详细说明。
- 结束 `"""` **单独占一行**；单行 docstring 的结束引号与开始引号同一行。
- 类：docstring 描述其行为，并在下一段列出公开方法（遵循同样的摘要格式）。
- 方法/函数：描述其行为、副作用、参数与返回值的**语义**，而不是实现细节；参数文档可用类型标注替代。

```python
def fetch_data(url: str, *, timeout: float = 5.0) -> dict:
    """Fetch JSON from a URL.

    Raises:
        TimeoutError: if the request exceeds ``timeout``.
    """
```

---

## 6. 命名约定（Naming Conventions）

> 核心原则：**对用户可见的名称具有约定意义**，不要随意混用；对用户不可见的内部名称可以自由使用，但仍推荐一致。

### 6.1 命名风格一览

| 风格 | 形态 | 典型用途 |
| --- | --- | --- |
| Python 风格函数 | `lowercase` / `lower_case_with_underscores` | 函数、变量、参数、方法 |
| 常量 | `UPPERCASE_WITH_UNDERSCORES` | 模块级常量 |
| 私有 | `_leading_underscore` | 内部实现细节 |
| 混入类 | `CapWords` + `Mixin` 后缀 | `SocketMixin`，标识"仅用于多重继承"的类 |
| 异常 | `CapWords` + `Error` 后缀 | 异常类 |
| 类 / 类型 | `CapWords`（CamelCase，无下划线） | 类、类型别名、TypeVar |
| 保护变量 | `_leading_underscore` | 非公共接口 |
| 名称改写 | `__leading_double_underscore` | 类内避免子类命名冲突 |
| 魔术 | `__both_leading_and_trailing__` | 解释器定义或协议方法 |
| 类型参数 | `T`、`_T`、`AnyStr`、`Num`、`_VT_co` | 泛型变量 |

### 6.2 描述性命名

命名应表达意图，避免拼音、缩写堆砌、单字母（循环计数 `i`、`j` 等短范围例外）。

### 6.3 应避免的名称

- 避免单字母名 `l`、`O`、`I`（易与数字 `1`、`0` 混淆）。需要"长度"时用 `length` 或大写 `L`。
- 以下划线开头或结尾的名称在包 `import *` 时不会被导入（这是特性，不是问题）。
- 避免与关键字冲突；需要时用尾随下划线：`id_`、`class_`。
- 避免使用 `__` 结尾（除魔术方法外）。
- 避免使用保留给解释器的 `__xxx__` 形式自定义名称。

### 6.4 ASCII-only 标识符

core Python 库中**标识符必须只用 ASCII**，且应使用英文单词。非 ASCII 的字符串与注释才允许，且应遵循 Unicode 规范化（PEP 3131 允许非 ASCII 标识符，但库代码不建议）。

### 6.5 包与模块名

- 短、全小写；模块名可用下划线，**包名尽量避免下划线**（历史兼容包除外，如 `import gui_modules` 不如 `import guimodules`）。
- 目录名与模块名一致：`sampledir/sample.py`。

### 6.6 类名（含异常）

- 类名使用 **CapWords**：`ClassName`、`MyException`。
- 内置兼容名可保留小写（如 `intSet` 应写成 `IntSet`）。
- 内部类可用下划线前缀。
- **Mixin 类名后缀 `Mixin`**（如 `SocketMixin`），以便一眼识别其特殊用途；`SocketServerMixin` 也可。

### 6.7 类型变量名

- 类型变量（`TypeVar`）使用 **CapWords 且尽量短**：`T`、`AnyStr`、`Num`、`_KT`。
- 表示协变 / 逆变的类型变量，分别加后缀 `_co` / `_contra`：`T_co`、`T_contra`。
- 模块内部的私有类型变量加单下划线前缀：`_T`。
- 相关 typing 构件的社区惯例（PEP 8 指向 PEP 484 及 typing 规范）：`ParamSpec` 用 `P`，`TypeVarTuple` 用带复数 `s` 的名字（如 `Ts`），`TypeAlias` 用 CapWords。

### 6.8 异常名

- 异常是类，因此同样使用 CapWords。
- **只有当异常确实表示"错误"时才加 `Error` 后缀**（`ReadError`、`ParseError`）；用作控制信号的异常不加后缀（如内置的 `StopIteration`）。
- 自定义异常应继承自 `Exception`（直接或间接），不要继承 `BaseException`。

### 6.9 全局变量名

- 全局变量**只应在模块内使用**，跨模块导入需要显式（如 `modname.globalname`）。
- 常量式全局变量用全大写；非常量全局变量按函数/变量命名规则（小写下划线）。
- 不建议通过 `from mod import globalname` 隐式使用他模块全局变量。

### 6.10 函数与方法参数

- 方法与实例方法第一个参数用 `self`；类方法第一个参数用 `cls`。`self`/`cls` 并非强制，但强烈建议遵循，以便区分方法与函数。
- 避免遮蔽外层变量；确需时在文档中说明。

### 6.11 函数与变量名

- 函数名：`lowercase_with_underscores`，**动词或动宾短语**（`read_file`、`send_email`）。
- 变量名：名词或名词短语；**下划线仅用于分隔单词**（`user_name`）；不用于起始/结尾（除前述避开关键字）。
- 单下划线开头表示"非公共"：`_helpers`、`_retry_count`。
- 双下划线开头触发名称改写（name mangling），用于避免子类命名冲突。

### 6.12 实例变量与方法

- 方法名遵循函数命名规则（小写下划线）。
- 非公共的方法与实例变量只用**一个**下划线前缀。
- 当**方法名与实例属性名可能冲突**时，给属性加下划线前缀（`self._name`），再用 `@property` 暴露公开读接口 `name`；一致的这种做法可避免属性与方法互相遮蔽。
- 基类中不希望被子类误调用的方法用双下划线（触发名称改写）；**预期由子类重写**的方法必须用单下划线。
- 类级别的常量仍用 `UPPER_CASE`；实例变量用小写下划线。

### 6.13 常量

- 模块级常量：`UPPERCASE_WITH_UNDERSCORES`（`MAX_OVERFLOW = 5`）。
- 类级常量同样；但注意**无法真正强制不可变**，靠约定。

### 6.14 继承与私有

- 若基类设计为可由子类访问，则**不要使用 `__` 前缀**（会改写名称，破坏继承）；用 `_` 前缀。
- 若基类不希望被子类触碰，可用 `__`。
- 子类若需要重写"名为 `__x`"的方法，应显式定义 `_ClassName__x` 以避免脆弱继承（尽量规避这种设计）。

### 6.15 公共与内部接口

- 只在文档中声明的接口是公共的；**未文档化的默认视为内部**。
- 内部接口允许随时变化，公共接口遵循版本兼容性承诺。
- 显式声明公共 API：在模块 `__all__` 中列出。
- 明确标记内部 API：单下划线前缀；此时**不需要**在文档中承诺兼容性。
- 若某接口内部使用、但通过 `from x import y` 暴露给外部（例如测试需要），应显式文档化。

---

## 7. 编程建议（Programming Recommendations）

### 7.1 PEP 8 的原文建议

- **与单例比较一律用 `is` / `is not`**：`if foo is None:`；不要用 `== None`。同时注意 `if x:` 与 `if x is not None:` 语义不同——当 `x` 可能是空容器、`0` 等"假值"时，后者才是你想要的。
- 捕获异常要**精确**：`except OSError as err:` 优于裸 `except:`；裸 `except:` 会连 `SystemExit`、`KeyboardInterrupt` 一起吞掉。
- `try` 块只包含**真正可能抛异常的那几行**，避免误捕获其他代码的异常。
- 用 `raise NewError(...) from err` 显式保留异常链。
- 判断类型用 `isinstance()`，不要用 `type(x) == T`（无法处理子类）。
- 用 `if x:` / `if not x:` 的隐式真值判断，而不是 `if len(seq) == 0:`、`if seq == []:`；但要区分 `None` 与空值场景。
- **不要用可变对象作默认参数**（`def f(a=[]):` 的经典陷阱），默认用 `None`，函数体内再初始化。
- 布尔语义清晰：写 `return bool(x)`，不要写 `return x == True`；也不要依赖 `1`/`0` 当布尔。
- 不要在 `if` 条件里做赋值；不要把多条语句用分号挤在同一行。
- `lambda` 只在"必须内联一个极短函数对象"时使用；否则定义具名函数（有名字、可 docstring、traceback 可读）。
- 返回值一致：一个函数要么所有分支都 `return <表达式>`，要么不混用"带值 return"与"裸 return / 隐式 None"。
- **类型标注的空白**（PEP 8 指向 PEP 484）：`:` 之前无空格、之后 1 空格；`->` 两侧各 1 空格；同一行既有标注又有默认值时，只在 `=` 两侧加空格：

```python
def f(a: int, b: str = "x") -> bool:
    x: int = 1
```

- 标注不是义务：可按项目渐进添加；公共 API 加标注能同时替代部分文档。
- PEP 8 已增设 **Annotations** 小节（2024 年更新）：Python 标准库现已接受在标准库代码中使用类型注解，并给出了具体的空白与书写规范（`->` 两侧空格、`:` 之后空格、复杂类型用括号折行等）。

### 7.2 现代实践补充（不属于 PEP 8 原文，但与之一致）

- 资源管理用 `with`；路径操作用 `pathlib` 而非手工字符串拼接。
- 循环用 `enumerate()` / `zip()`，避免手工维护下标。
- 可执行模块的入口放在 `if __name__ == "__main__":`。
- 库代码只 `logger = logging.getLogger(__name__)`，不配置 handler；输出策略交由应用侧。
- 优先标准库与显式实现，避免依赖 `sys.path` 顺序技巧。

---

## 8. 工具化落地（把规范变成可执行的）

| 目的 | 工具 | 说明 |
| --- | --- | --- |
| 格式化 | **Black / Ruff format** | 默认行宽 88，需要 PEP 8 严格 79 时显式配置 |
| 静态检查 | **Ruff**、flake8 + pycodestyle | `select = ["E", "W", "F", "I"]` |
| 导入排序 | **isort**（Ruff 的 `I` 规则已覆盖） | 分组 stdlib / third-party / first-party |
| 命名检查 | pep8-naming（`N` 规则） | 类名 CapWords、函数名 snake_case |
| docstring | pydocstyle（D 规则） | 对齐 PEP 257 |
| 提交前 | pre-commit | 保证 CI 与本地一致 |

```toml
# pyproject.toml 示例：向 PEP 8 对齐
[tool.ruff]
line-length = 79

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "D", "UP", "B"]
ignore = ["D203", "D213"]  # 选择与 PEP 257 一致的一条规则即可

[tool.ruff.lint.pydocstyle]
convention = "pep257"

[tool.black]
line-length = 79

[tool.isort]
profile = "black"
line_length = 79
```

> 注意：Black 默认 88 字符与 PEP 8 的 79 存在有意分歧。团队选定其一后**全局一致**，比数值本身更重要。

---

## 9. 评审自检清单

- [ ] 4 空格缩进，无 Tab/空格混用
- [ ] 行 ≤ 79（docstring/注释 ≤ 72）
- [ ] 顶层定义间隔 2 空行，方法间隔 1 空行
- [ ] 续行用悬挂缩进；二元运算符前折行
- [ ] import 分组（stdlib / 第三方 / 本地），无 `import *`，无逗号合并 import
- [ ] 特殊 dunder 位于 docstring 后、import 前
- [ ] 括号/逗号/冒号附近无多余空白；`=` 用于默认值时两侧无空格
- [ ] 单元素元组有尾随逗号；多行结构使用尾随逗号
- [ ] 注释 `# ` 后有空格；内联注释与代码间隔 ≥ 2 空格；无过时注释
- [ ] 公共模块/函数/类有 docstring，摘要为祈使句
- [ ] 类 CapWords、函数/变量 snake_case、常量 UPPER_CASE、错误型异常加 `Error` 后缀、TypeVar 用短名 `T`
- [ ] `self` / `cls` 首参；内部实现加 `_` 前缀；公共 API 用 `__all__`
- [ ] 用 `is None`、`isinstance`、`with`；无裸 `except`；无可变默认参数
- [ ] `if __name__ == "__main__":` 保护可执行入口
- [ ] CI 中 ruff/black 通过

---

## 10. 相关规范链接

- PEP 8 — Style Guide for Python Code：https://peps.python.org/pep-0008/
- PEP 257 — Docstring Conventions：https://peps.python.org/pep-0257/
- PEP 263 — Defining Python Source Code Encodings：https://peps.python.org/pep-0263/
- PEP 3120 — Using UTF-8 as default source encoding：https://peps.python.org/pep-3120/
- PEP 3131 — Supporting Non-ASCII Identifiers：https://peps.python.org/pep-3131/
- PEP 484 — Type Hints（注解写法的依据）：https://peps.python.org/pep-0484/
- pycodestyle（PEP 8 的官方检查器，规则编号 E/W 即来自本指南）：https://pycodestyle.pycqa.org/
- Ruff 规则表 / Black 文档：可作为团队落地细则与补充
