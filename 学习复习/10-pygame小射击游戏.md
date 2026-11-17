# 10 · pygame 小射击游戏（`game/` 四个文件）

> 类别定位：多文件协作 + 游戏主循环 + 帧率 + 碰撞检测。
> 四个文件都真实跑过。主循环的「不操作也会死」用了带帧号插桩的副本取证；帧率数字来自 `SDL_VIDEODRIVER=dummy` 的无头运行，真实窗口可能不同。

## 本类文件

| 文件 | 行数 | 作用 | 关注点 |
| --- | --- | --- | --- |
| [game/game_main.py](../game/game_main.py) | 113 | 初始化、主循环、碰撞、计分 | 无入口保护、Clock 建在循环里、结束后不退出 |
| [game/ship.py](../game/ship.py) | 33 | 飞船：移动、边界、绘制 | 四个独立 `if`，斜向速度 √2 |
| [game/bullet.py](../game/bullet.py) | 18 | 子弹：出生位置、向上飞 | 每次发射新建 Surface |
| [game/alien.py](../game/alien.py) | 45 | 外星人：横移、下落 | 上面 24 行是注释掉的旧版；新旧两套位置策略 |

`game/` 下没有 `__init__.py`，四个文件之间用**绝对导入**（`from ship import Ship`）。

---

## 一、入口点：三种跑法，只有两种工作

实测：

| 命令 | 结果 |
| --- | --- |
| `python game/game_main.py`（仓库根） | 正常启动，窗口循环，exit=124（被 timeout 杀掉） |
| `cd game && python game_main.py` | 正常启动 |
| `python -m game.game_main`（仓库根） | `ModuleNotFoundError: No module named 'ship'` |
| `python -c "import game.game_main"` | 同上 |

具体报错位置：

```text
File "E:\python源码\python工作区\lreaning\game\game_main.py", line 4, in <module>
    from ship import Ship
ModuleNotFoundError: No module named 'ship'. Did you mean: 'scipy'?
```

原因：直接跑脚本时，`sys.path[0]` 是**脚本所在目录**（`game/`），所以 `import ship` 找得到；用 `-m game.game_main` 时，`sys.path[0]` 是**当前目录**（仓库根），包内模块必须以 `game.ship` 或相对导入出现，裸 `ship` 找不到。

两种修法，选一种：

```python
# A. 保持直接运行，改成包内相对导入
from .ship import Ship
from .bullet import Bullet
from .alien import Alien

# B. 保持绝对导入，但把 game 当普通目录，永远用
#    python game/game_main.py
```

A 需要 `game/__init__.py`。我在副本里验证过：加空 `__init__.py` + 三行相对导入后，`python -m game.game_main` 能正常启动（exit=124，无 traceback）。

---

## 二、`import` 就会开打：没有 `if __name__ == "__main__"`

`game_main.py` 从第 8 行起全是模块级代码，主循环直接写在文件底部。实测在 `game/` 目录里：

```text
python -c "import game_main; print('导入完成')"
```

3 秒超时后进程仍在跑（exit=124），`导入完成` 没有打印。也就是说：**任何 `import game_main` 都会启动游戏并卡在循环里**，包括测试、文档工具、IDE 的自动补全。

标准写法：

```python
def main():
    pygame.init()
    ...
    while True:
        ...

if __name__ == "__main__":
    main()
```

搬进函数后，所有模块级全局（`score`、`fleet_direction`、`aliens`、`bullets`、`my_ship`）要么变成局部变量 + 参数传递，要么在函数里声明 `global`。这不是「加两行」那么小，但它是可测试、可导入的前提。

---

## 三、`Alien` 有两个版本

[alien.py:1-24](../game/alien.py#L1-L24) 整段被注释：

```python
# import random
# class Alien:
#     def __init__(self, screen):
#         ...
#         self.rect.x = random.randint(0, self.screen_rect.right - self.rect.width)
#         self.rect.y = random.randint(-100, -40)
#     def update(self):
#         self.rect.y += self.speed
```

旧版：自己随机出生、自己向下掉，不需要主循环配合。但如果只取消类的注释、忘了取消 `import random`，第一只外星人创建时就会 `NameError: name 'random' is not defined`。

[alien.py:26-45](../game/alien.py#L26-L45) 是现用版：

```python
class Alien:
    def __init__(self, screen, x, y):
        ...
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self, direction):
        self.rect.x += self.speed * direction

    def drop_down(self):
        self.rect.y += 20
```

新版：位置由外面塞进来，横向移动由主循环统一指挥，碰边时统一 `drop_down()`。这是正确的方向——**敌人的行为由「舰队」统一决定，而不是每只自己随机**。

代价是 `Alien` 不再能单独使用：`Alien(screen)` 会缺两个参数。`game_main.py:39-41` 那三行注释掉的旧循环也因此失效：

```python
# for i in range(10):
#     new_alien = Alien(screen)
#     aliens.append(new_alien)
```

---

## 四、舰队几何：45 只，9 列 × 5 行

[game_main.py:21-36](../game/game_main.py#L21-L36) 的计算，实测复算：

```text
外星人尺寸: 40 x 40
可用横向: 800 - 2*40 = 720      列数: 720 // 80 = 9
可用纵向: 600 - 3*40 - 80 = 400  行数: 400 // 80 = 5
总数: 45
```

初始坐标：

```text
列 x: 40, 120, 200, ..., 680      （最右 right = 720）
行 y: 40, 120, 200, 280, 360      （最下 bottom = 400）
飞船: x=370, y=520, 60x80          （top=520）
```

最下行到飞船顶部还有 `520 - 400 = 120` px，每次碰边下落 20 px，所以**至少 6 次下落**才进入飞船的垂直范围；是否撞上还取决于当时飞船的横向位置。

运行日志实测（带帧号插桩的副本）：

```text
第 1 次下落: frame=81
第 2 次下落: frame=201
第 3 次下落: frame=321
第 4 次下落: frame=441
第 5 次下落: frame=561
第 6 次下落: frame=681
第 7 次下落: frame=801
飞船被撞毁，游戏结束！frame=801
```

两次下落间隔 120 帧：舰队从一端扫到另一端正好 120 px。第 7 次下落时最下行 `bottom=540`，与飞船 `top=520` 重叠，且横向恰好覆盖飞船，于是 `colliderect` 成立。

---

## 五、不操作也会死：实测 23.13 秒

用同一个插桩副本、不发送任何按键：

```text
[  0.12s] pygame-ce 2.5.8 (SDL 2.32.10, Python 3.15.0)
[  1.78s] 第 1 次下落: frame=81
[ 23.13s] 飞船被撞毁，游戏结束！frame=801
```

关键点：

- 游戏不靠「外星人落到屏幕底部」结束，而是先撞上飞船。底部判定在 [game_main.py:86-89](../game/game_main.py#L86-L89)，飞船碰撞在 [:90-93](../game/game_main.py#L90-L93)，两者都在同一个 `for alien` 循环里，谁先命中谁生效。
- 只要玩家不动，飞船停在底部中央，第 7 次下落的横向位置刚好覆盖它。
- 这个时间会随帧率变化。帧率高，同样的 801 帧用时就短；帧率低就更久。所以「23 秒」不是游戏设计值，是**当前机器 + 当前帧率**的实测值。

---

## 六、帧率与 `Clock`：`tick(60)` 不等于 60 fps

[game_main.py:112](../game/game_main.py#L112)：

```python
pygame.time.Clock().tick(60)
```

每帧**新建**一个 `Clock` 再 `tick`。三种写法在同一台机器、同样的 dummy 驱动下实测（各跑 300 帧）：

| 写法 | 300 帧耗时 | 实测 fps |
| --- | --- | --- |
| 每帧 `pygame.time.Clock().tick(60)`（现状） | 7.44s | 40.32 |
| 循环外建一次 `clock = pygame.time.Clock()`，循环内 `clock.tick(60)` | 6.68s | 44.91 |
| 完全不 `tick` | 0.43s | 690.15 |

两个结论：

1. **循环体本身很快**：不限制时 690 fps，单帧约 1.45 ms。45 个外星人 + 少量子弹的绘制在 dummy 驱动下不是瓶颈。
2. **每帧新建 `Clock` 多花了约 0.76 ms/帧**，而且 `tick(60)` 并没有把帧率压到 60——它每次从「新建时刻」重新计时，等待的是固定 16.7ms，叠加在已经花掉的绘制时间上，所以最终低于 60。

正确写法：

```python
clock = pygame.time.Clock()      # 循环外一次
while True:
    ...
    clock.tick(60)               # 循环内只调用
```

`Clock` 的职责是「记录上一帧到这一帧的时间」，它必须跨帧存活。建在循环里，等于每帧都失忆。

> 这里的数字来自无头 dummy 驱动。真实窗口受 vsync、窗口管理器、显卡影响，可能接近 60，也可能更低。**测量方法比数字更重要**：先打印 300 帧耗时，再决定要不要优化。

---

## 七、游戏结束后不退出

`game_active = False` 之后：

- 事件循环仍然响应 `QUIT`（关窗口能退出）；
- 飞船、子弹、外星人都停止更新（[game_main.py:50](../game/game_main.py#L50) 的 `if game_active:` 包住了整段）；
- 每帧仍然绘制场景和 `GAME OVER` 文本；
- 但**没有「按键重开」也没有自动退出**，玩家只能关窗口。

如果想让「撞毁 → 停 1.5 秒 → 退出」：

```python
if not game_active:
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    ...
    pygame.display.flip()
    pygame.time.wait(1500)
    return
```

`return` 需要主循环在函数里；这也回到第二节「先加 `main()`」的问题。

另一个边界：**打光所有外星人不会胜利**。`aliens` 变成空列表后，边缘检测和碰撞循环都不执行，`game_active` 仍是 True，屏幕空空如也，游戏继续。需要补一个 `if not aliens: game_active = False` 或进入下一关。

---

## 八、模块级全局：现在能用，搬进函数就要 `global`

[game_main.py:13-19](../game/game_main.py#L13-L19)：

```python
score = 0
game_active = True
my_ship = Ship(screen)
bullets = []
aliens = []
fleet_direction = 1
```

主循环在模块级，所以：

```python
score += 10                 # :69
fleet_direction = -1        # :74
game_active = False         # :87
```

都是**重新绑定模块级名字**，不需要 `global`。一旦把主循环搬进 `def main()`，这三行会变成局部变量，必须在函数开头声明：

```python
def main():
    global score, game_active, fleet_direction
```

更干净的做法是把它们收进一个 `Game` 类，或者用 `nonlocal` 配合嵌套函数。当前规模下，至少要知道「现在能用是因为都在模块级」。

`create_fleet(screen, aliens)` [game_main.py:21](../game/game_main.py#L21) 收了 `screen` 和 `aliens` 两个参数，却在第 27 行直接用了全局 `my_ship`：

```python
ship_height = my_ship.rect.height
```

参数和全局混用，函数就不够独立。把 `ship` 也作为参数传进来，`create_fleet` 才能单独测试。

---

## 九、`Ship`：斜向速度是 √2 倍

[ship.py:24-32](../game/ship.py#L24-L32) 是四个独立 `if`：

```python
if self.moving_right and self.rect.right < self.screen_rect.right:
    self.rect.x += 1
if self.moving_left and self.rect.left > 0:
    self.rect.x -= 1
if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
    self.rect.y += 1
if self.moving_up and self.rect.top > 0:
    self.rect.y -= 1
```

实测：

```text
只按右:        dx=1 dy=0  位移=1.000
按右+下:       dx=1 dy=1  位移=1.414
贴右边界按右:  x 变化=0
贴左边界按左:  x 变化=0
```

边界钳制是对的：`rect.right < screen.right` 和 `rect.left > 0` 都写对了，实测贴边后不再移动。斜向快 41% 是这类写法的常见副作用，横版/纵版游戏里通常可以接受；要严格等速就归一化：

```python
import math
dx = (self.moving_right - self.moving_left)
dy = (self.moving_down - self.moving_up)
if dx and dy:
    dx *= math.sqrt(0.5)
    dy *= math.sqrt(0.5)
self.rect.x += dx
self.rect.y += dy
```

另外，飞船初始 `bottom = 600`，所以一开始按下键不会动（已经在底边）。这是边界条件，不是 bug。

---

## 十、遍历时删除：写法是对的

子弹循环 [game_main.py:59-70](../game/game_main.py#L59-L70)：

```python
for bullet in bullets[:]:          # 副本
    bullet.update()
    if bullet.rect.bottom <= 0:
        bullets.remove(bullet)     # 删原列表
        continue
    for alien in aliens[:]:        # 每颗子弹一个新的副本
        if bullet.rect.colliderect(alien.rect):
            bullets.remove(bullet)
            aliens.remove(alien)
            score += 10
            break
```

`bullets[:]` 和 `aliens[:]` 都是浅拷贝，遍历副本、删除原列表，不会「边遍历边跳过元素」。这是正确写法，比 `for x in list: list.remove(x)` 安全得多。

外星人移动循环 [game_main.py:83-93](../game/game_main.py#L83-L93) 则直接遍历 `aliens[:]` 并在命中时 `break`，也安全。

一个风格问题：第 59 行用副本、第 72 行直接遍历原列表。两处目的不同（前者要删、后者只读），但读代码时容易以为不统一。可以在注释里写清「这里只读，不需要副本」。

---

## 十一、绘制与命名

- `blitme()` 是教材里的叫法（`blit` + `me`），不是 Python 社区通用命名。更常见的写法是 `draw(surface)`。
- [ship.py:8-9](../game/ship.py#L8-L9) 在 `Ship.__init__` 里创建一个 60x80 的纯色 `Surface` 当飞船；`Alien` 每只建一个 40x40；`Bullet` 每次发射建一个 5x15。45 只外星人就是 45 个 Surface。当前规模没问题；如果要做上百个敌人，应该在类外建一次、复用，或者用 `pygame.sprite.Sprite` + `Group`。
- `for bullet in bullets:bullet.blitme()` [game_main.py:103](../game/game_main.py#L103) 把循环体写在同一行。PEP 8 要求分开写，且这种一行循环在调试时不好下断点。

---

## 十二、其他可以直接删的死代码

| 位置 | 内容 | 处理 |
| --- | --- | --- |
| [alien.py:1-24](../game/alien.py#L1-L24) | 整个旧版 `Alien` | 确认不再需要后删除，或移到 `legacy/` |
| [game_main.py:3](../game/game_main.py#L3) | `# import random` | 当前主循环不用 random，删 |
| [game_main.py:39-41](../game/game_main.py#L39-L41) | 旧的随机生成 10 只 | 删，已被 `create_fleet` 取代 |
| [game_main.py:94-99](../game/game_main.py#L94-L99) | 旧的 `sys.exit()` 结束逻辑 | 删，已被 `game_active` 取代 |
| [alien.py:25](../game/alien.py#L25) | 一行中文需求注释 | 可以保留，说明设计意图 |

注释掉的代码不会执行，但会增加阅读成本；git 已经能保存历史，不需要靠注释留档。

---

## 十三、如果要继续改：推荐顺序

1. **先加 `if __name__ == "__main__":`**（第二节）。这一步最大，但做完之后测试和导入都不再启动游戏。
2. **`Clock` 移到循环外**（第六节），再测一次 300 帧耗时。
3. **加 `settings.py`**：把 `800x600`、`60`、`40`、`20`、`10`、`1` 这些魔法数字集中。
4. **修游戏结束**：撞毁后停 1.5 秒退出，或按 R 重开；同时补「外星人全灭」的胜利分支。
5. **把 `create_fleet` 的 `my_ship` 改成参数**，让它能独立测试。
6. **考虑 `pygame.sprite.Group`**：碰撞检测、批量绘制、批量删除都由引擎管，代码会短很多。

每一步改完都跑一次，并记录「改前/改后」的帧率或结束时间。这个项目最大的价值不是画面，而是让你第一次面对「全局状态 + 帧循环 + 多文件导入」三件事同时出现。

---

## 十四、错题清单

| 现象 | 根因 | 对策 |
| --- | --- | --- |
| `-m game.game_main` 报 `No module named 'ship'` | 绝对导入 + `-m` 的搜索根是 cwd | 加 `__init__.py` + 相对导入，或只用直接运行 |
| `import game_main` 卡住 | 主循环在模块级 | `if __name__ == "__main__"` + `main()` |
| 帧率不到 60 | `Clock` 每帧新建 | 循环外建一次 |
| 不操作 23 秒就死 | 外星人碰边下落，第 7 次覆盖飞船 | 这是当前参数下的正常结果；要改就调速度/下落量/初始行数 |
| 打光外星人游戏不结束 | 没有胜利判定 | `if not aliens: ...` |
| 撞毁后只能关窗口 | 没有结束态处理 | 停 1.5 秒 `return` 或按键重开 |
| 斜向移动更快 | 两个轴各加 1 | 归一化，或接受 |
| 搬进 `main()` 后分数不加 | 没写 `global` | 声明 `global` 或改成类/参数 |

---

## 十五、练习

1. 只加 `if __name__ == "__main__":` 和 `main()`，让 `import game_main` 不再启动游戏（提示：把全局变量改成 `main()` 的局部变量，或先全部 `global`）。
2. 把 `Clock` 移到循环外，跑 300 帧并记录 fps；再和本篇的 40.32 / 44.91 对比。
3. 加 `settings.py`，把窗口尺寸、帧率、外星人尺寸、下落距离、子弹速度、每只分值集中管理。
4. 实现「外星人全灭 → 显示 YOU WIN → 退出」。
5. 给飞船加 `speed` 属性，并让斜向移动严格等速（提示：归一化）。
6. 用 `pygame.sprite.Sprite` + `Group` 重写 `Bullet` 和 `Alien`，对比代码行数与碰撞逻辑。

---

## 参考

- 类的继承与重写（`Ship` / `Alien` 都可以做成类层次）：[06-面向对象入门.md](06-面向对象入门.md)
- 游戏里的 `try/except` 与失败分支：[07-异常处理与程序健壮性.md](07-异常处理与程序健壮性.md)
- 给 `Ship.update` 这类纯逻辑写测试：[09-模块与单元测试.md](09-模块与单元测试.md)
