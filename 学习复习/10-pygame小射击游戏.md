# pygame 小射击游戏：`game/` 里那四个文件

> 覆盖文件（`E:\python源码\python工作区\lreaning\game\`）：
> - [ship.py](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/ship.py)（33 行）
> - [bullet.py](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/bullet.py)（18 行）
> - [alien.py](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/alien.py)（45 行，上半段是注释掉的旧版）
> - [game_main.py](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py)（113 行，主循环）
>
> ⚠️ 环境是 **pygame-ce 2.5.8（SDL 2.32.10，Python 3.15.0）**。本机 pygame 没装，装的是 pygame-ce 社区版，两者 API 基本兼容。所有实测都在无头模式（`SDL_VIDEODRIVER=dummy`）跑，看不到窗口但逻辑和帧率都能测。

---

## 0. 这份代码的位置：你已经会「多文件协作」了

前面所有文档里的程序都是一个文件。这次你第一次拆成 4 个文件、用 `from ship import Ship` 组装——这一步比看起来重要，因为它立刻带来两类新问题（第 1、2 节都是）。拆文件本身，你已经做对了。

## 1. ⚠️ 相对目录 import 的边界：三种入口，只有一种坏

`game/` 没有 `__init__.py`，四个模块互为**同级模块**（隐式命名空间包）。四种跑法实测：

| 入口 | 结果（实测） |
|---|---|
| `cd game && python game_main.py` | ✅ 正常启动（脚本所在目录进 `sys.path[0]`） |
| `cd .. && python game/game_main.py` | ✅ 也能跑（`sys.path[0]` 仍是 `game/`，脚本的目录不是 cwd）——**我原先以为这条路会坏，实测是好的** |
| `cd .. && python -m game.game_main` | ❌ `ModuleNotFoundError: No module named 'ship'. Did you mean: 'scipy'?` |
| 别处 `import game_main` | ❌ **直接把整个游戏跑起来并卡死**（实测 8 秒不返回，见第 6 节） |

> **`python 路径/脚本.py` 用「脚本所在目录」当搜索根；`python -m 包.模块` 用「当前目录」当搜索根。** 这是 Python 最容易记错的一条规则。想两种都能跑，就把 `game` 做成真包（加 `__init__.py`）并改用 `from .ship import Ship`——但 `from .xxx` 只在包内有效，直接 `python game_main.py` 反而会报 `ImportError: attempted relative import with no known parent package`。**两种入口不能同时满足，必须选一种并固定下来。** 对你现在的规模：**固定用「在 `game/` 目录里 `python game_main.py`」最简单**。

## 2. `Alien` 有两个版本，注释里那个才是「能自己跑」的

[alien.py:4-23](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/alien.py#L4) 整段被注释掉了，[:26](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/alien.py#L26) 起是新版。差别不只是「多了 x, y 参数」：

```python
# 旧版（注释里）：自己随机出生、自己向下掉，不需要主循环配合
def __init__(self, screen):
    self.rect.x = random.randint(0, self.screen_rect.right - self.rect.width)
    self.rect.y = random.randint(-100, -40)
    self.speed = 1
def update(self):
    self.rect.y += self.speed        # 单参数：自己往下

# 新版：位置由外面塞进来，横向移动由主循环指挥
def __init__(self, screen, x, y): ...
def update(self, direction):          # ← 多了一个必填参数
    self.rect.x += self.speed * direction
def drop_down(self):
    self.rect.y += 20
```

后果：旧版是「天上下外星人」，新版是「整队横移 + 撞墙集体下沉」。**行为换了，但类名、`blitme()` 都没变**，所以主循环里 `alien.blitme()` 看不出差别——这就是第 3 节那个 bug 的来源。

> ⚠️ **`update()` 的签名变了，任何还在按旧方式调用的地方都会 `TypeError`。** 实测：`Alien.update()` 少传参数 → `TypeError: Alien.update() missing 1 required positional argument: 'direction'`。旧版留在注释里是隐患：三个月后你取消注释复用，报错点会出现在别的文件里。
>
> 要保留旧思路（下雨式掉落），**另起一个类名**，别同名不同行为：

```python
from alien import Alien          # game/alien.py，需与它同目录

class FallingAlien(Alien):
    """从顶上下 rain 的类型：不是「一队横移」，改行为就改类名。"""
    def update(self, direction=None):     # 兼容旧调用签名
        self.rect.y += self.speed
```

## 3. ⚠️ 边界判断写反了（这条会让游戏开局 0.6 秒就结束）

[game_main.py:73-82](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L73)：

```python
for alien in aliens:
    if alien.rect.right >= screen.get_rect().right:
        fleet_direction = -1
        for a in aliens:
            a.drop_down()
        break
    elif alien.rect.left <= 0:
        fleet_direction = 1
        ...
        break
```

意图是「最右边那只贴到右墙就整体往左；最左边那只贴到左墙就整体往右」。**实际写的是：任意一只**贴墙就改方向。`break` 又让每帧只看第一个命中的分支，于是：

- 舰队宽度**超过**屏幕宽时：某只在外面的外星人**每帧**都触发「右边界」→ 每帧全体 `drop_down()` 一次 → 每帧下掉 20 像素。
- 而且 `for alien in aliens` 是按创建顺序（一行一行），**永远先看第一行**，第二行的贴墙情况被 `break` 掉了。

实测（同一份 `game_main.py`，只把列数从 9 改成 30，其余逐字不动，`SDL_VIDEODRIVER=dummy`）：

```
game_main_counted.py   [插桩] 结束帧数=800 方向翻转次数=7  用时 23.02 秒
game_main_wide.py      [插桩] 结束帧数=6   方向翻转次数=7  用时 0.59 秒
```

**30 列版本第 6 帧就判负**（翻转记录是 `('右边界→左', 0), ('右边界→左', 1), ('右边界→左', 2) ...` 每帧一次）。列数一多，`create_fleet` 排出的舰队宽度 2400px 远超 800px 屏幕，最右几只一开始就在墙外 → 每帧全体下沉 20px → 6 帧下沉 120px 就撞船。这个 bug 平时被 `create_fleet` 的 9 列「恰好不超屏」掩盖着（9 列宽 720px < 800px）。

> **教训**：几何代码的边界条件要**用极端值测一次**，而不是只跑默认值。
>
> ⚠️ 但「窗口缩小一半」这条**我试了，测不出来**：把 `set_mode` 改成 `(400, 300)` 后，`create_fleet` 会按新屏幕重算成 4 列 × 1 行（实测 920 帧才判负、方向翻转 8 次，节奏完全正常）——因为舰队宽度是**跟着屏幕算的**，永远刚好放得下。
> **能触发这个 bug 的只有「舰队宽度 > 屏幕宽度」这一种情况**，所以我用 `number_aliens_x * 3`（30 列，宽 2400）强行造出来。现实里它什么时候会发生？你手动加 `Alien(screen, x, y)`、改成随机生成、或者把 `create_fleet` 的算法改掉的那一刻。

正确写法是「整队的最左/最右」，而不是「随便哪一只」：

```python
if aliens:
    fleet_right = max(a.rect.right for a in aliens)
    fleet_left = min(a.rect.left for a in aliens)
    if fleet_right >= screen.get_rect().right and fleet_direction > 0:
        fleet_direction = -1
        for a in aliens: a.drop_down()
    elif fleet_left <= 0 and fleet_direction < 0:
        fleet_direction = 1
        for a in aliens: a.drop_down()
```

`and fleet_direction > 0` 是关键：**只在朝墙的那个方向上才翻转**。否则翻完还停在墙边，下一帧又触发一次（就是你 30 列那 6 帧连续翻转的成因）。

⚠️ 别用 `aliens[0].rect.right` 当「整队最右」——你的 `aliens` 按行创建，`aliens[0]` 只是第一行第一列，`aliens[-1]` 是最后一行最后一列，`drop_down()` 之后各行还会错落。**必须 `max/min`**。

## 4. 真实帧率与那个 `Clock`（我上次把这条写错了，现在是实测版）

先说结论：**这段代码能跑，帧率却被压到 34 帧/秒，而 `tick(60)` 是 60 帧的上限。** 上次我写「每次新建 Clock 导致限速形同虚设、实测 909 帧/秒」——**那个数字复现不出来，撤回**。重测如下。

① 忠实复刻主循环、只加一个计数器（`game_main_counted.py`），不操作键盘跑到底：

```
[插桩] 结束帧数=800 方向翻转次数=7 剩余外星人=45
```

结束时刻 **23.02 秒**（`python -u game_main.py` 原样跑到打印「飞船被撞毁，游戏结束！」也实测到 23.01 秒，两种方式一致）。

$$800 \div 23.02 = 34.75 \text{ 帧/秒}，\quad 每帧 = \frac{23.02}{800} = 28.8 \text{ ms}$$

而 `tick(60)` 的节拍是 16.67 ms——**实际帧率只有上限的一半多。**

② 为什么慢？给循环装了计时表，把「循环体」和「tick 睡眠」分开累加（800 帧）：

```
[计时] 800 帧：循环体 0.36s，tick 睡眠 22.37s，合计 28.41 ms/帧
```

**循环体只占 0.36 秒（0.45 ms/帧），22.37 秒全花在 `tick()` 的睡眠上。** 于是「瓶颈是每帧 `font.render`」这个猜测也被排除——我把 render 挪出循环重测，帧率只从 34.71 变成 34.80，几乎没动。

③ 公平 A/B：同一个进程里，同样的每帧工作量，两种 Clock 写法交替各跑 800 帧：

```
fresh  800 帧  24.76 秒 = 32.30 帧/秒（30.96 ms/帧）
reuse  800 帧  22.80 秒 = 35.09 帧/秒（28.50 ms/帧）
fresh  800 帧  24.67 秒 = 32.42 帧/秒（30.84 ms/帧）
reuse  800 帧  22.67 秒 = 35.29 帧/秒（28.34 ms/帧）
none   800 帧   0.09 秒 = 8930.28 帧/秒（ 0.11 ms/帧）
```

两轮交叉重复，数值稳定。读法：

- 不限速时 `fill + 46 次 blit + 每帧 render + flip + event.get()` 只要 **0.11 ms/帧（8930 帧/秒）** ——绘制根本不是瓶颈。
- 两种 Clock 写法都**在限速**（不是我上次说的「形同虚设」）：pygame-ce 里 `Clock()` 构造时就记住起点，所以每帧新建也能睡够约一帧。
- 但**每帧新建仍然更慢**：30.9 ms vs 28.4 ms（约 8%，两轮一致）。原因是 `tick(60)` 的语义是「补足到 16.67 ms」，复用同一个 Clock 时它会扣除上一帧已经花掉的时间；每帧新建的 Clock 不知道上一帧花了多久，只能从头等满，于是多等一截。
- `get_fps()` 只有复用才读得到：实测 `reuse` 跑 120 次后 `get_fps() = 60.98`，而**每帧新建的 Clock 连续 5 次读到 `0.0`**。所以你现在这句根本没法用来查帧率。

④ 想真跑满 60：`tick_busy_loop(60)`（忙等，CPU 占用高，但帧率准）

```
tick(60)         400 帧 11.66 秒 = 34.30 帧/秒  get_fps()=34.01
tick_busy_loop(60) 400 帧  6.40 秒 = 62.51 帧/秒  get_fps()=62.50
```

⚠️ 这台机器上 `SDL_Delay(1)` 实测睡 1.00 ms（睡眠精度是 1ms），但 `tick` 系列仍到不了 60——`flip()` 在无头 dummy 驱动上的行为和真窗口不完全一样。**所以别把上面这些数字当结论，只当排查起点**：接上真实窗口后第一件事是打印 `clock.get_fps()` 自己量一次。

修法（照旧，但理由换成实测）：

```python
# 片段（示意 Clock 的放置位置，不能单独跑）：
clock = pygame.time.Clock()      # 循环外，只创建一次
while True:
    ...
    clock.tick(60)               # 复用：能限速，也能用 clock.get_fps() 看真实帧率
```

## 5. 不操作也会死：23 秒，且 45 只外星人一个没掉

上面那个实测值本身就是**平衡数据**——你现在完全没开枪，所以：

- 舰队每 120 帧撞一次墙、下沉 20px（实测翻转记录帧号 `80, 200, 320, 440, 560, 680, 800`，间隔严格 120）；
- 45 只外星人 **800 帧后一只没少**（`剩余外星人=45`）；
- 第 800 帧（23.02 秒）撞上停着的飞船 → 判负。

想「能撑 60 秒」或「需要打掉 10 只才安全」，就调 `Alien.speed`（现在是 1）、`drop_down` 的 20、以及 `create_fleet` 的行列数。**只有量过的数才能调**——所以先插桩计数，再改参数，改完再跑一遍对比。

（顺手算一下：120 帧撞一次墙 × 每帧 28.8ms ≈ **3.46 秒一次碰壁下沉**，7 次碰壁 × 20px 就把最低行从 400 推到 540 → 撞上 `top=520` 的飞船 → 800 帧 ≈ 23 秒。三个数和实测全对上。
>
> ⚠️ 更重要的推论：**帧率一改，整局时长就改。**第 6 节那个重写版把逻辑搬进函数后单测：同样 45 只、同样几何，判负发生在第 **801 帧**；如果 Clock 修好、真按 60 帧/秒跑，`801 ÷ 60 ≈ 13.4 秒`——比现在的 23 秒短 42%。也就是说你修完帧率，游戏会突然变难，`ALIEN_SPEED`、`drop_down` 的 20 全得重调。**先修帧率，再调平衡，顺序反了白调。**）

## 6. ⚠️ 没有 `if __name__ == "__main__"`：`import` 就开打

[game_main.py:8](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L8) 起全是模块级语句：`pygame.init()`、`set_mode`、`create_fleet(...)`、`while True:`。

实测：别的脚本里只写 `import game_main`，**8 秒仍未返回**（只打印了 pygame 版本横幅，然后进入游戏死循环）。你没法给这个游戏写单元测试，也没法做「开局界面 → 再进主循环」的重构。

`ship` / `bullet` / `alien` 三个文件只有类定义，模块级安全——**只有 `game_main.py` 需要这层保护**。

修法（整块可复制，直接当新版 `game_main.py`）：

```python
import sys
import pygame
from ship import Ship
from bullet import Bullet
from alien import Alien


def create_fleet(screen, aliens, my_ship):
    """整块可复制：列数改成由屏幕宽度和外星人宽度算出来，并保证不超出屏幕。"""
    alien_width = alien_height = 40
    margin = alien_width
    number_aliens_x = (screen.get_rect().width - 2 * margin) // (2 * alien_width)
    available_y = screen.get_rect().height - 3 * alien_height - my_ship.rect.height
    number_rows = available_y // (2 * alien_height)
    for row in range(number_rows):
        for col in range(number_aliens_x):
            aliens.append(Alien(screen, margin + 2 * alien_width * col,
                                alien_height + 2 * alien_height * row))


def handle_keydown(event, screen, my_ship, bullets, game_active):
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    if event.key == pygame.K_SPACE and game_active and len(bullets) < 5:
        bullets.append(Bullet(screen, my_ship))


def handle_events(screen, my_ship, bullets, game_active):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event, screen, my_ship, bullets, game_active)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT: my_ship.moving_right = False
            if event.key == pygame.K_LEFT: my_ship.moving_left = False


def update_fleet(screen, aliens, my_ship, fleet_direction):
    """返回 (新方向, 是否游戏结束)。边界判断用 max/min 整队。"""
    if not aliens:
        return fleet_direction, False
    right = max(a.rect.right for a in aliens)
    left = min(a.rect.left for a in aliens)
    if right >= screen.get_rect().right and fleet_direction > 0:
        fleet_direction, _ = -1, [a.drop_down() for a in aliens]
    elif left <= 0 and fleet_direction < 0:
        fleet_direction, _ = 1, [a.drop_down() for a in aliens]
    for a in aliens:
        a.update(fleet_direction)
    if max(a.rect.bottom for a in aliens) >= screen.get_rect().bottom:
        return fleet_direction, True
    if any(a.rect.colliderect(my_ship.rect) for a in aliens):
        return fleet_direction, True
    return fleet_direction, False


def update_bullets(bullets, aliens, score):
    """返回 (新子弹列表, 新分数)。删除用推导式，不在 for 里 remove。"""
    for b in bullets:
        b.update()
    alive = [b for b in bullets if b.rect.bottom > 0]
    for b in list(alive):
        for a in aliens[:]:
            if b.rect.colliderect(a.rect):
                aliens.remove(a)
                alive.remove(b)
                score += 10
                break
    return alive, score


def draw(screen, my_ship, bullets, aliens, font, score, game_active):
    screen.fill((0, 0, 50))
    my_ship.blitme()
    for b in bullets: b.blitme()
    for a in aliens: a.blitme()
    screen.blit(font.render(f"Score: {score}", True, (25, 255, 255)), (10, 10))
    if not game_active:
        over = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over, over.get_rect(center=(400, 300)))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("外星人入侵")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()          # 循环外创建，见第 4 节

    my_ship = Ship(screen)
    bullets, aliens = [], []
    create_fleet(screen, aliens, my_ship)
    score, fleet_direction, game_active = 0, 1, True

    while True:
        handle_events(screen, my_ship, bullets, game_active)
        if game_active:
            keys = pygame.key.get_pressed()
            my_ship.moving_right = keys[pygame.K_RIGHT]
            my_ship.moving_left = keys[pygame.K_LEFT]
            my_ship.moving_up = keys[pygame.K_UP]
            my_ship.moving_down = keys[pygame.K_DOWN]
            my_ship.update()
            bullets, score = update_bullets(bullets, aliens, score)
            fleet_direction, dead = update_fleet(screen, aliens, my_ship, fleet_direction)
            if dead:
                game_active = False
        draw(screen, my_ship, bullets, aliens, font, score, game_active)
        clock.tick(60)


if __name__ == "__main__":
    main()
```

这份把主循环里所有逻辑搬进了函数，状态从外面塞进去，每步都能单独测：

```python
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"     # 无头，不需要真窗口
import pygame
import game_main_v2 as G                     # 上面那份重写，存成 game_main_v2.py
from ship import Ship

pygame.init()
screen = pygame.display.set_mode((800, 600))
my_ship = Ship(screen)
aliens, bullets = [], []
G.create_fleet(screen, aliens, my_ship)
print(len(aliens), max(a.rect.right for a in aliens))

d, frame = 1, 0
while True:
    frame += 1
    d, dead = G.update_fleet(screen, aliens, my_ship, d)
    if dead:
        print(f"第 {frame} 帧判负，最低行 bottom={max(a.rect.bottom for a in aliens)}")
        break
```

实测：

```
45 720
第 801 帧判负，最低行 bottom=540
```

三个信息：`create_fleet` 由屏幕宽度算出 **9 列 × 5 行 = 45 只**，最右到 720（**没超出 800**，所以第 3 节那个「列数一多就每帧下沉」的病根被顺手治好了）；判负发生在第 801 帧，和原版第 800 帧只差 1 帧（因为 `update_fleet` 里把「移动」和「判负」放在了一次调用里）；**801 帧 ÷ 60 帧每秒 ≈ 13.4 秒**，比现在实测的 23.02 秒短 42%——这就是第 5 节说的「修好帧率，整局时长会跟着变」，改完 Clock 你必须重新调 `ALIEN_SPEED`。

再单独验一次「贴墙只翻一次」这条修复。⚠️ 关键是把上一次的 `d` **传回**下一次调用（模拟真实主循环），别传常量：

```python
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import game_main_v2 as G          # 上面那份重写存成 game_main_v2.py
import alien
from ship import Ship

pygame.init()
screen = pygame.display.set_mode((800, 600))

a = alien.Alien(screen, 0, 0)
a.rect.right = 820                 # 人造一只「已经在右墙外」的
d = 1
for i in range(3):
    d, dead = G.update_fleet(screen, [a], Ship(screen), d)
    print(f"修复版 第{i+1}次：方向={d} 判负={dead} bottom={a.rect.bottom} x={a.rect.x}")

print()
b = alien.Alien(screen, 0, 0)
b.rect.right = 820
d2 = 1
for i in range(3):                 # 逐字复现 game_main.py:73-84 的判断顺序
    for al in [b]:
        if al.rect.right >= screen.get_rect().right:
            d2 = -1
            for x in [b]: x.drop_down()
            break
        elif al.rect.left <= 0:
            d2 = 1
            for x in [b]: x.drop_down()
            break
    b.update(d2)
    print(f"原  版 第{i+1}次：方向={d2} bottom={b.rect.bottom} x={b.rect.x}")
```

实测：

```
修复版 第1次：方向=-1 判负=False bottom=60 x=779
修复版 第2次：方向=-1 判负=False bottom=60 x=778
修复版 第3次：方向=-1 判负=False bottom=60 x=777

原  版 第1次：方向=-1 bottom=60 x=779
原  版 第2次：方向=-1 bottom=80 x=778
原  版 第3次：方向=-1 bottom=100 x=777
```

看 `bottom` 那一列：**修复版 60/60/60（只下沉一次，之后往左走），原版 60/80/100（每帧下沉 20）**。第 3 节 30 列那个「6 帧下沉 120 像素判负」就是这个差异的放大版。

⚠️ 别在函数里用 `global fleet_direction`——搬进函数后赋值会变成 `UnboundLocalError`（实测 `cannot access local variable 'fleet_direction' where it is not associated with a value`）。**用返回值传状态**（上面 `return fleet_direction, dead`），别用 `global`——见 [08 号文档第 4 节](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/%E5%AD%A6%E4%B9%A0%E5%A4%8D%E4%B9%A0/08-%E7%AE%80%E6%98%93%E8%AE%A1%E7%AE%97%E5%99%A8.md)、[09 号文档第 13 节](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/%E5%AD%A6%E4%B9%A0%E5%A4%8D%E4%B9%A0/09-%E6%A8%A1%E5%9D%97%E4%B8%8E%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95.md)。

## 7. `score` 和 `fleet_direction` 能用，只是因为全在模块级

[game_main.py:68](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L68) `score += 10`、[:74](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L74) `fleet_direction = -1` 都在 `while True` 里直接改模块全局——**现在不报错**。但第 6 节搬进函数后就会报错。所以：

> 搬代码进函数之前，先把「藏在 while 循环里的全局变量」列一张表。你这张表上有 **4 个**：`score`、`fleet_direction`、`game_active`、`bullets`/`aliens`（后两个只 append 不重新绑定，暂时安全）。

顺带一个真 bug：`game_active = False` 之后**游戏永远停在 GAME OVER**，既不重开也不退出，只能关窗口。加个按键重开（第 6 节 `handle_keydown` 里可以扩）。

## 8. `ship.py` 的四个 `if`：对角线速度问题

[ship.py:24-32](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/ship.py#L24) 四个方向独立判断、各自 ±1，**没有 else**——写得对（对角线能同时移动）。但要意识到：

- 斜着走的合成速度是 `√(1²+1²) ≈ 1.414`，比直走快 41%。
- 现在的实现是**每帧 1 像素**，所以移动速度**和帧率挂钩**：第 4 节实测你的循环是 34.75 帧/秒，而设计意图是 60 帧/秒——**飞船实际只跑了设计速度的一半多**（34.75/60 ≈ 0.58 倍）。修好 Clock 之后，所有速度都会跟着变，游戏会突然变快。这是几何和帧率耦合的第二个例子。

解法是 delta-time（按经过的秒数移动，而不是每帧固定步长）：

```python
def update(self, dt):                 # dt：上一帧到这一帧过了多少秒
    speed = 240                       # 像素/秒，和帧率无关
    step = speed * dt
    if self.moving_right and self.rect.right < self.screen_rect.right:
        self.rect.x += step
```

`clock.tick(60)` 的返回值就是上一帧耗时（毫秒），所以主循环里 `dt = clock.tick(60) / 1000`。

## 9. `bullets` 边遍历边 `remove`：写法对了，但风格不统一

[game_main.py:59-70](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L59)：

```python
for bullet in bullets[:]:          # ← 遍历副本，正确
    ...
    for alien in aliens[:]:        # ← 同样正确
        if bullet.rect.colliderect(alien.rect):
            bullets.remove(bullet)
            aliens.remove(alien)
            score += 10
            break
```

两处都遍历副本再删原表，**没踩「边遍历边删」的坑**。但 [:83](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L83) `for alien in aliens[:]` 里只 `update` 和 `break`，没删东西——**这个切片是多余的**（实测：删掉后行为一致；`aliens[:]` 每帧复制 45 个引用，无害但会误导读者）。

更清爽的写法（第 6 节 `update_bullets` 用的就是这个）：

```python
# 片段（示意「重建列表而不是 remove」，需要上面那些名字已存在）：
bullets = [b for b in bullets if not b.off_screen()]
hit = {(id(b), id(a)) for b in bullets for a in aliens if b.rect.colliderect(a.rect)}
```

`remove` 的隐藏成本：`list.remove` 是 O(n) 扫描，且**按值比较**。你的 `Bullet`/`Alien` 没定义 `__eq__`，所以按对象身份比——安全。但如果哪天给 `Alien` 加了 `__eq__`（比如「坐标相同算同一个」），`bullets.remove(bullet)` 就会删错东西。所以**优先用推导式重建列表，别用 `remove`**。

## 10. `blitme` 的命名 + 每帧新建 `Surface`

`ship.blitme()` / `bullet.blitme()` / `alien.blitme()` 三个类各写一遍同样的两行—— pygame 教程的惯例，跟你写的没错，但值得知道还有第二种做法：**把精灵画到一张透明大图上再整体 blit**（`pygame.sprite.Group` + `draw()`）。你现在四个类四份 `blitme`，加个「护盾」类还得再写第三份。

另一个实测过的隐患——在循环里 `Ship(screen)` 每帧新建：

```python
import os, time
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
from ship import Ship

pygame.init()
screen = pygame.display.set_mode((800, 600))
t0 = time.perf_counter()
for _ in range(6000):
    s = Ship(screen); s.blitme()
print(f"{time.perf_counter() - t0:.3f} 秒")     # 实测 0.007 秒
```

6000 次 0.007 秒，看着便宜。但那是**没接 `pygame.display.flip()` 的纯 blit**。实际项目里每帧新建 `Surface` 会让 GC 和显存上传抖动——这也是为什么第 4 节修 Clock 前我怀疑过渲染，实测排除后结论是「渲染确实不是瓶颈，但别养成每帧 new 的习惯」。

## 11. `# import random` 和注释掉的旧逻辑

三处死代码：[game_main.py:3](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L3)、[:39-41](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L39)、[:94-99](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L94)，加 [alien.py](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/alien.py#L1) 上半段整个旧类。[:94-99](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L94) 那段注释掉的 `sys.exit()` 还留着「直接退出」的老思路——你现在改成 `game_active = False` 是对的（能显示 GAME OVER 而不是闪退），注释块可以放心删。

> `game/` 是这批文件里唯一一个**没进 git** 的目录（`git status` 显示 `?? game/`）。删注释之前先 commit 一次，否则「删错了」没有回退点。

## 12. 本文件错题清单

| 位置 | 现象 | 本质 |
|---|---|---|
| [game_main.py:73-82](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L73) | 任意一只贴墙就全体转向/下沉 | 该判断整队（`max/min`），且要限定转向条件。实测 30 列时 6 帧判负 |
| [game_main.py:112](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L112) | 每帧新建 `Clock`，实测 34.7 帧/秒 | tick 无法扣除上一帧耗时；且 `get_fps()` 读到 0.0 |
| [game_main.py:8](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L8) | 无 `if __name__`，`import` 即进入死循环（实测 8 秒不返回） | 代码全在模块级，无法复用也无法测试 |
| [alien.py:38](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/alien.py#L38) | `update(direction)` 签名变了，注释里旧版是 `update()` | 同名不同行为，`TypeError: missing 1 required positional argument` |
| [game_main.py:83](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L83) | 多余的 `aliens[:]` | 没删元素却复制列表（风格问题） |
| [ship.py:26](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/ship.py#L26) | 每帧固定 ±1 像素 | 速度和帧率耦合：实测 34.75 帧/秒 = 设计速度的一半多。delta-time 才是根治 |
| [game_main.py:68](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L68) | `score += 10` 藏在 while 里 | 搬进函数就 `UnboundLocalError`，先列全局变量清单 |
| 没有 `settings.py` | 800/600/45 个外星人/20px 硬编码在 4 个文件里 | 数值散落各处，改一个平衡参数要翻四个文件 |
| [game_main.py:46](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/game/game_main.py#L46) | `sys.exit()` 直接杀进程 | pygame 没 `quit()`，窗口有时残留；且没 `pygame.time.wait(50)` 让刷屏完成 |

**已经做对的**：
- ✅ 拆成 4 个文件、类职责单一（`Ship` 只管移动和画，`Bullet` 只管上升）
- ✅ 边界检查全用了 `<`/`>` 比较，没有 `rect` 越界崩溃
- ✅ 删除元素时 `for x in list[:]` 遍历副本（第 9 节）
- ✅ 键盘按下/松开用标志位 + `update()`，不在事件里直接改坐标——这是**正确架构**
- ✅ `colliderect` 用 pygame 现成方法，没手算矩形相交

## 13. 建议的下一步（按依赖顺序）

1. **先修第 6 节（加 `if __name__ == "__main__"`）**——不修这条，后面所有拆分都动不了。
2. **修第 4 节（Clock 挪到循环外）**，然后打印 `clock.get_fps()` 确认实际帧率，再看第 5 节那句「帧率变了整局时长也会变」。
3. **建 `settings.py`**：`WIDTH/HEIGHT/SHIP_SPEED/ALIEN_SPEED/BULLET_SPEED/FLEET_DROP`。第 5 节那些数字全放进去。
4. **修第 3 节（整队边界判断）**，然后用第 3 节那个 `number_aliens_x * 3` 的极端值再测一次——原版 6 帧判负，修好后应该和 9 列版一样能撑到几百帧（我实测的修复版是 801 帧）。
5. **加 `pygame.sprite.Group`**：`aliens = pygame.sprite.Group()` 之后 `aliens.update()`、`aliens.draw(screen)` 各一行替掉你手写的双层循环，`pygame.sprite.spritecollide(ship, aliens, False)` 替掉 `any(...)`。
6. **最后才做声音和图片**（`pygame.mixer.Sound("fire.wav").play()`）——你现在用的是纯色 `Surface`，架构稳了再换素材。

## 14. 三份新文档的定位

| 文档 | 你在学什么 |
|---|---|
| [08-简易计算器.md](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/%E5%AD%A6%E4%B9%A0%E5%A4%8D%E4%B9%A0/08-%E7%AE%80%E6%98%93%E8%AE%A1%E7%AE%97%E5%99%A8.md) | 表驱动、格式化、`float` 的边界 |
| [09-模块与单元测试.md](file:///E:/python%E6%BA%90%E7%A0%81/python%E5%B7%A5%E4%BD%9C%E5%8C%BA/lreaning/%E5%AD%A6%E4%B9%A0%E5%A4%8D%E4%B9%A0/09-%E6%A8%A1%E5%9D%97%E4%B8%8E%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95.md) | 「绿灯 ≠ 测过」 |
| 本篇 | 多文件协作 + **凡是不量就不许改**：帧率、舰队尺寸、游戏时长 |
