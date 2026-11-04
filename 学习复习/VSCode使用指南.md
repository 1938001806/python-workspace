# VS Code 使用指南

> 适用版本：2026 年稳定版（Windows 为主，macOS 键位在括号内标注）
> 覆盖范围：新手上手 · 快捷键速查 · 配置与效率 · 场景工作流 · 故障处理
> 快捷键均核对自官方 [Default keyboard shortcuts](https://code.visualstudio.com/docs/reference/default-keybindings)，配置项以官方文档+设置界面可搜索到为准；如你改过键位请以本地 `键盘快捷方式` 编辑器为准。

---

## 0. 五分钟导航（先找到你要的那节）

| 你是谁 / 想干什么 | 直接看 |
| --- | --- |
| 刚装好，不知道从哪下手 | 第 1 章 |
| 想把操作速度提上来 | 第 2 章速查表 |
| 想改设置、同步配置、换台机器接着用 | 第 3 章 |
| 想少用鼠标 | 第 4 章 |
| Python / 前端 / Git / 调试 / 远程 | 第 5 章 |
| 出问题了（卡、乱码、扩展失效） | 第 6 章 |

### 0.1 怎么验证本文（也适用于任何网传配置）

VS Code 的键位和设置项**随版本变化**，第三方教程里大量键名是编造的——写错不会报错，只会静默失效。动手前先在本机确认：

| 要确认的东西 | 权威入口 |
| --- | --- |
| 设置项是否存在、取值范围、作用域 | `Ctrl+,` 图形界面搜索键名（搜不到 = 本机版本没有它） |
| 命令 ID（写 `keybindings.json` 要用） | `Ctrl+K Ctrl+S` 键位编辑器 → 右上"显示所有命令" → 右键 → 复制命令 ID |
| 某设置属于用户/工作区/机器作用域 | 设置项右侧的 `User` / `Workspace` 标签 |
| 扩展是否还在维护 | 扩展页看"最近更新时间"，再看其仓库 issue 活跃度 |
| 当前版本新增了什么 | `Ctrl+Shift+P` → `Help: Release Notes…` |

本文中标注"随版本变动"的条目（AI 键位、终端分屏键位、Copilot 计费）请以本机结果为准。

---

## 1. 新手快速上手

### 1.1 安装

1. 从官网 [code.visualstudio.com](https://code.visualstudio.com/download) 下载 User 安装包（无需管理员权限，装在 `%LOCALAPPDATA%\Programs\Microsoft VS Code`）。
2. 安装时勾选这两项，之后会省很多麻烦：
   - **创建桌面快捷方式**
   - **将"通过 Code 打开"操作添加到 Windows 资源管理器文件/目录上下文菜单**
3. 中文界面：`Ctrl+Shift+X` 打开扩展市场 → 搜 `Chinese (Simplified)` → 安装 **中文（简体）语言包** → 右下角提示后重启。

### 1.2 命令行工具 `code`

装好后终端里可用：

```powershell
code .                 # 用当前目录作为项目打开
code path\to\file.txt  # 打开单个文件
code -a .              # 把目录加入当前工作区（多根工作区）
code -d a.txt b.txt    # 用 VS Code 做 diff 对比
code -n                # 新窗口
code --list-extensions # 列出已装扩展
code --install-extension ms-python.python   # 命令行装扩展
code --diff --wait a b   # 作为 git 的 difftool（--wait 阻塞到关闭）
```

若提示 `code` 不是内部命令：`Ctrl+Shift+P` → 输入 `Shell Command: Install 'code' command in PATH`（Windows 一般安装时已配好；Git Bash 里需在 PATH 中含 `...\Microsoft VS Code\bin`）。

### 1.3 界面五个区

```
┌──────────┬─────────────────────────────┬──────────┐
│ ①活动栏   │  ③编辑器区（可分组成多列）      │ ④面板     │
│ (Activity│   ②侧边栏：资源管理器/搜索/      │ (终端、    │
│  Bar)    │   源代码管理/运行/扩展          │  问题、    │
│          │   ⑤ 编辑器标签页 / Breadcrumb   │   输出)    │
├──────────┴─────────────────────────────┴──────────┤
│ ⑥状态栏：分支、错误数、语言模式、编码、换行符、行:列    │
└───────────────────────────────────────────────────┘
```

常用显隐：`Ctrl+B` 侧边栏 · `Ctrl+J` 面板 · `Ctrl+Shift+E` 资源管理器 · `Ctrl+Shift+X` 扩展。

### 1.4 第一个项目：用"文件夹"而不是"文件"

**这是新手最重要的一条习惯。** 打开单个文件（`Ctrl+O`）时，搜索、Git、扩展的很多能力都不完整；正确做法是 `文件 → 打开文件夹`，或直接终端里 `code .`。

打开文件夹后你会立刻获得：
- 全局搜索（`Ctrl+Shift+F`）限定在项目内
- 源代码管理面板自动识别 Git 仓库
- `settings.json`、`tasks.json`、`launch.json` 可以按项目生效
- 语言服务器能解析跨文件引用

### 1.5 必须记住的 6 个动作

| 动作 | 键位 | 说明 |
| --- | --- | --- |
| 命令面板 | `Ctrl+Shift+P`（⌘⇧P） | VS Code 的总入口，所有功能都能搜到 |
| 快速打开文件 | `Ctrl+P`（⌘P） | 输文件名即可；后面加 `:` 跳行、加 `@` 跳符号、加 `#` 搜符号 |
| 保存 | `Ctrl+S` | 建议开启自动保存，见 §3.2 |
| 集成终端 | `` Ctrl+` `` | 在项目目录里直接跑命令 |
| 侧边跳转 | `Ctrl+Tab` | 按住 Ctrl 连按 Tab 在已打开文件间切换 |
| 撤销一切 | `Ctrl+Z` / `Ctrl+Shift+Z` | 时间机器：`Ctrl+Shift+P` → `Timeline: Focus on Timeline View` 可看文件历史版本 |

### 1.6 项目根目录会长出的三个文件

```
你的项目/
├── .vscode/
│   ├── settings.json    # 本项目的设置，覆盖用户设置
│   ├── launch.json      # 调试配置（按 F5 时用）
│   └── tasks.json       # 构建/运行任务（Ctrl+Shift+B 时用）
└── .editorconfig        # 团队统一的缩进/换行规范（VS Code 原生识别）
```

`settings.json` / `tasks.json` / `launch.json` 是 VS Code 的"项目配置三件套"。多人协作时，把 `.vscode/` 提交进 Git，团队配置就能自动一致。

### 1.7 卸载 / 保留配置

- 卸载程序不影响你的配置；配置保存在下面两处（重装即恢复）。
- 想彻底重置：删除 `%APPDATA%\Code`（设置/扩展状态）与 `%USERPROFILE%\.vscode\extensions`（扩展本体）。删除前建议先备份或导出 Profile（见 §3.4）。

---

## 2. 快捷键速查表

> 未标注括号的为 Windows/Linux；macOS 常规映射：`Ctrl→⌘`、`Alt→⌥`、`Shift→⇧`。

### 2.1 全局与文件

| 操作 | 键位 |
| --- | --- |
| 命令面板 | `Ctrl+Shift+P` / `F1` |
| 快速打开文件 | `Ctrl+P` |
| 打开文件 / 新建文件 | `Ctrl+O` / `Ctrl+N` |
| 保存 / 全部保存 | `Ctrl+S` / `Ctrl+K S` |
| 另存为 | `Ctrl+Shift+S` |
| 关闭编辑器 / 关闭窗口 | `Ctrl+W` / `Alt+F4` |
| 重新打开刚关闭的编辑器 | `Ctrl+Shift+T` |
| 钉住编辑器（不被预览复用） | `Ctrl+K Enter` |
| 新建窗口 / 打开主题切换 | `Ctrl+Shift+N` / `Ctrl+K Ctrl+I` |
| 复制文件路径 / 在资源管理器中显示 | `Ctrl+K P` / `Ctrl+K R` |
| 更改语言模式 | `Ctrl+K M` |

### 2.2 编辑（提速主力）

| 操作 | 键位 |
| --- | --- |
| 剪切/复制整行（不选中文本时） | `Ctrl+X` / `Ctrl+C` |
| 删除整行 | `Ctrl+Shift+K` |
| 在下/上方插入空行 | `Ctrl+Enter` / `Ctrl+Shift+Enter` |
| 上/下移动行 | `Alt+↑/↓` |
| 上/下复制行 | `Shift+Alt+↑/↓` |
| 选词并添加下一个相同词（多光标） | `Ctrl+D` |
| 选中全部相同词 | `Ctrl+Shift+L` |
| 选中当前单词 | `Ctrl+F2` |
| 选中整行 | `Ctrl+L` |
| 在每列末尾加光标（列选择） | `Ctrl+Shift+Alt+↑/↓` 或 `Ctrl+Alt+↑/↓` |
| 跳到配对括号 | `Ctrl+Shift+\` |
| 缩进 / 反缩进 | `Ctrl+]` / `Ctrl+[` |
| 折叠 / 展开代码块 | `Ctrl+Shift+[` / `Ctrl+Shift+]` |
| 全部折叠 / 全部展开 | `Ctrl+K Ctrl+0` / `Ctrl+K Ctrl+J` |
| 切换注释 | `Ctrl+/` |
| 块注释 | `Shift+Alt+A` |
| 强制格式化整个文档 | `Shift+Alt+F` |
| 格式化选中部分 | `Ctrl+K Ctrl+F` |
| 删除行尾空格 | `Ctrl+K Ctrl+X` |
| 扩大/缩小智能选区 | `Shift+Alt+→` / `Shift+Alt+←` |
| 重命名符号 | `F2` |

### 2.3 查找替换

| 操作 | 键位 |
| --- | --- |
| 查找 / 替换 | `Ctrl+F` / `Ctrl+H` |
| 下一个 / 上一个匹配 | `Enter` / `Shift+Enter` |
| 选中全部匹配 | `Alt+Enter` |
| 区分大小写 / 全字 / 正则 | `Alt+C` / `Alt+W` / `Alt+R` |
| 跨文件搜索 / 跨文件替换 | `Ctrl+Shift+F` / `Ctrl+Shift+H` |
| 展开搜索结果详情 | `Ctrl+Shift+J` |
| 下一个 / 上一个搜索结果 | `F4` / `Shift+F4` |

### 2.4 导航与代码智能

| 操作 | 键位 |
| --- | --- |
| 跳转到定义 / 侧栏打开定义 | `F12` / `Ctrl+K F12` |
| 速览定义（不离开当前文件） | `Alt+F12` |
| 查看所有引用 | `Shift+F12` |
| 跳回上/下一个位置 | `Alt+←` / `Alt+→` |
| 跳到行 | `Ctrl+G` |
| 工作区按符号名跳转 | `Ctrl+T` |
| 当前文件内符号列表 | `Ctrl+Shift+O`（输入 `:` 可按类型分组） |
| 触发智能补全 | `Ctrl+Space` |
| 参数提示 | `Ctrl+Shift+Space` |
| 快速修复 / 重构建议 | `Ctrl+.`（灯泡） |
| 跳到下一个/上一个错误或警告 | `F8` / `Shift+F8` |
| 打开问题面板 | `Ctrl+Shift+M` |

### 2.5 界面、窗口与布局

| 操作 | 键位 |
| --- | --- |
| 侧边栏显隐 / 面板显隐 | `Ctrl+B` / `Ctrl+J` |
| 资源管理器 / 搜索 / 源代码管理 / 运行 / 扩展 | `Ctrl+Shift+E` / `F` / `G` / `D` / `X` |
| 输出面板 | `Ctrl+Shift+U` |
| 集成终端 | `` Ctrl+` `` |
| 编辑器分组（左右拆分） | `Ctrl+\` |
| 在 1/2/3 分组间聚焦 | `Ctrl+1` / `Ctrl+2` / `Ctrl+3` |
| 把编辑器移到另一分组 | `Ctrl+Shift+PageUp/PageDown`（或用 `Ctrl+P` 后输 `>` 搜命令 `Move Editor into ...`） |
| 放大 / 缩小界面 / 重置缩放 | `Ctrl+=` / `Ctrl+-` / `Ctrl+Numpad0` |
| 全屏 / 禅模式（退出按 `Esc` 两次） | `F11` / `Ctrl+K Z` |
| Markdown 预览 / 侧边预览 | `Ctrl+Shift+V` / `Ctrl+K V` |
| 侧边栏/面板/状态栏焦点切换 | `Ctrl+K ←/→/↓/↑` |

### 2.6 调试与任务

| 操作 | 键位 |
| --- | --- |
| 启动 / 继续 | `F5` |
| 不调试直接运行 | `Ctrl+F5` |
| 停止 | `Shift+F5` |
| 切换断点 | `F9` |
| 单步跳过 / 步入 / 步出 | `F10` / `F11` / `Shift+F11` |
| 运行生成任务 | `Ctrl+Shift+B` |

### 2.7 内置 AI / Chat 相关（默认键位，随版本变动较大）

| 操作 | 键位 |
| --- | --- |
| 打开聊天面板 | `Ctrl+Alt+I` |
| Agent 模式 | `Ctrl+Shift+I` |
| 行内聊天（选中代码直接改） | `Ctrl+I` |
| 快速聊天（一次性提问，不落历史） | `Ctrl+Shift+Alt+L` |
| 新建会话 | `Ctrl+N`（在聊天面板聚焦时） |

> AI 功能依赖扩展与账号，键位可能与你本机不同。核对方法：`Ctrl+K Ctrl+S` 打开键盘快捷方式，搜 `chat`。

### 2.8 学习快捷键的正确方式

不要背表。做法：`Ctrl+K Ctrl+S` 打开键位编辑器 → 搜索命令名看当前绑定 → 双击条目按新键即可改，右键可"当条件（when）""复制链接""移除键位"。要直接改文件：`Ctrl+Shift+P` → `Preferences: Open Keyboard Shortcuts (JSON)`（对应 `%APPDATA%\Code\User\keybindings.json`）。查命令 ID 用同界面的"显示所有命令"视图（右上角键盘图标）。

---

## 3. 配置与效率进阶

### 3.1 设置的层级与优先级

优先级从低到高（后者覆盖前者）：

```
默认 → 用户 → 远程(机器) → 工作区 → 文件夹 → 语言特定/资源特定
```

- **用户设置**：全局，对所有窗口生效。Windows 路径 `%APPDATA%\Code\User\settings.json`（即 `C:\Users\你\AppData\Roaming\Code\User\settings.json`）。
- **工作区设置**：`.vscode/settings.json`，只对打开该工作区生效，适合提交进 Git 共享。
- **文件夹设置**：多根工作区里对某个文件夹单独生效，优先级高于工作区设置。
- 打开方式：`Ctrl+,` 是图形界面；`Ctrl+Shift+P` → `Preferences: Open User Settings (JSON)` 是直接改文件。

**实操建议**：图形界面用来"发现"设置项（有说明和 `when` 提示），日常偏好写在 `settings.json` 里——文本便于版本管理、便于分享、便于对比 diff。

### 3.2 一份高价值的基础配置

把下面内容放进用户 `settings.json`，按需删改。每项都写了为什么值得开：

```jsonc
{
  // ---- 编辑体验 ----
  "editor.fontSize": 14,
  "editor.tabSize": 4,                      // 前端项目常设 2
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,        // 别让文件类型自动改你的缩进策略
  "editor.rulers": [80, 100],               // 软参考线，控制行宽
  "editor.guides.bracketPairs": true,       // 括号配对缩进参考线
  "editor.bracketPairColorization.enabled": true,
  "editor.linkedEditing": true,             // 改 HTML 标签名时结束标签同步
  "editor.stickyScroll.enabled": true,      // 顶部固定显示当前所在函数/作用域
  "editor.renderWhitespace": "boundary",    // 只在词边界显示空格点
  "editor.inlineSuggest.enabled": true,     // 补全行内灰色预览
  "editor.suggestSelection": "first",       // 总选第一个，行为可预测（默认 "recentlyUsed"）
  "editor.acceptSuggestionOnEnter": "on",
  "editor.multiCursorModifier": "ctrlCmd",  // 多光标用 Ctrl+点击（Alt+点击改为跳定义）

  // ---- 保存时自动化：效率提升最大的一组 ----
  "editor.formatOnSave": true,
  "editor.formatOnPaste": false,
  "files.autoSave": "afterDelay",           // 可选："onFocusChange" / "onWindowChange"
  "files.autoSaveDelay": 1000,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",            // 保存时跑 ESLint/Ruff 自动修复
    "source.organizeImports": "explicit"    // 保存时整理 import
  },

  // ---- 文件行为 ----
  "files.eol": "\n",                        // 统一 LF，避免 Windows 换行污染 diff
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "files.trimFinalNewlines": true,
  "files.exclude": { "**/.git": true, "**/node_modules": true },
  "files.watcherExclude": {                 // 关键：减少 CPU/句柄占用
    "**/node_modules/**": true,
    "**/.git/objects/**": true,
    "**/dist/**": true,
    "**/.venv/**": true
  },
  "files.associations": { "*.env*": "plaintext" },
  "search.exclude": { "**/node_modules": true, "**/dist": true, "**/*.lock": true },
  "search.useIgnoreFiles": true,            // 全局搜索尊重 .gitignore
  "explorer.fileNesting.enabled": true,     // 把 .ts/.js/.map 等折叠到主文件下
  "explorer.confirmDelete": false,
  "explorer.compactFolders": false,         // 避免 a/b/c 单链目录被压成一行

  // ---- 终端 ----
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.fontFamily": "MesloLGS NF",   // 配合 Nerd Font 图标
  "terminal.integrated.scrollback": 10000,
  "terminal.integrated.copyOnSelection": true,
  "terminal.integrated.env.windows": { "PYTHONIOENCODING": "utf-8" }, // 治中文乱码

  // ---- 调试 / Git ----
  "debug.console.fontSize": 13,
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,            // 无暂存时提示直接提交全部
  "git.blame.editorDecoration.enabled": true, // 内置行内 blame，无需 GitLens
  "gitlens.currentLine.enabled": false,     // 若装了 GitLens，避免与内置 blame 重复
  "scm.diffDecorationsGutterPattern": { "added": true, "modified": true },

  // ---- 界面 ----
  "workbench.colorTheme": "Default Dark Modern",
  "workbench.iconTheme": "vscode-icons",
  "zenMode.hideActivityBar": false,         // 禅模式下仍保留活动栏
  "workbench.startupEditor": "none",        // 每次打开别再看欢迎页
  "workbench.editor.enablePreview": false,  // 单击文件不再复用同一个标签页（强烈推荐）
  "workbench.editor.showTabs": "multiple",
  "window.commandCenter": true,
  "window.titleBarStyle": "custom",
  "window.restoreWindows": "all",           // 重开时恢复上次的窗口/工作区
  "window.confirmSaveUntitledWorkspace": false,

  // ---- 扩展与安全 ----
  "extensions.autoUpdate": true,
  "security.workspace.trust.untrustedFiles": "open",  // 安全让步，见 §3.6

  // ---- 语言特定：只对某类文件生效 ----
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.tabSize": 4,
    "files.trimTrailingWhitespace": true    // Python 尾部空格有语义风险，仍建议保留 true
  },
  "[javascript]": { "editor.tabSize": 2, "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescript]": { "editor.tabSize": 2, "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[json]":     { "editor.tabSize": 2, "editor.defaultFormatter": "vscode.json-language-features" },
  "[markdown]": { "editor.wordWrap": "on", "files.trimTrailingWhitespace": false }
}
```

三个"立刻见效"的项，如果只改三条就改这些：

```jsonc
"editor.formatOnSave": true,          // 保存即格式化
"workbench.editor.enablePreview": false, // 不再"一个标签页反复被替换"
"files.watcherExclude": { "**/node_modules/**": true } // 大项目不再风扇狂转
```

### 3.3 键位自定义

`keybindings.json` 位置：`%APPDATA%\Code\User\keybindings.json`。语法要点：`command`、`key`、`when`（生效上下文）、`args`。

```jsonc
[
  // 用 Ctrl+Shift+E 打开终端（覆盖默认"资源管理器"）
  { "key": "ctrl+shift+e", "command": "workbench.action.terminal.toggleTerminal" },

  // 只在编辑器里有选区时，Alt+↑/↓ 才是移动行；否则不拦截
  { "key": "alt+up", "command": "editor.action.moveLinesUpAction",
    "when": "editorTextFocus && !editorReadonly" },

  // 组合键示例：Ctrl+K 后按 T 打开任务面板
  { "key": "ctrl+k t", "command": "workbench.view.extensions", "when": "focusedView != 'extensions'" },

  // 解绑一个烦人的默认键位
  { "key": "ctrl+shift+t", "command": "-workbench.action.reopenClosedEditor" }
]
```

命令名怎么找：`Ctrl+K Ctrl+S` 打开键位编辑器 → 右上角图标"显示所有命令" → 右键命令 → **复制命令 ID**。前缀 `-` 表示移除绑定。

### 3.4 Profiles 与 Settings Sync：跨机器带走你的环境

**Profiles（配置集）** 是设置 + 扩展 + 键位 + 代码片段 + 任务 + 界面状态的组合；**Settings Sync** 负责把它们同步到别的机器。

| 需求 | 做法 |
| --- | --- |
| 换机/重装后恢复 | `Ctrl+Shift+P` → `Settings Sync: Turn On…` → 用 GitHub 或 Microsoft 账号 → 勾选要同步的类别（含 Profiles） |
| 前端 / Python / 临时杂活分环境 | `Profiles: Create Profile…` → 从"空"或"现有配置"复制；状态栏左下角点齿轮切换 Profile |
| 分享给同事/自己备份 | `Profiles: Export Profile…` → 生成 `.code-profile` 文件或 GitHub Gist 链接；对方 `Profiles: Profile from URL…` 导入 |
| 想同步"设置但不同步扩展" | 同步开 → `Settings Sync: Configure…` 取消勾选扩展 |

要点：机器相关设置（本地路径等）不会进导出文件——换机器后仍需检查绝对路径类配置。查找 `settings.json` 的具体路径用 `Preferences: Open Settings (JSON)` 里的文件链接，别手敲。

### 3.5 代码片段（Snippets）

- 项目级：`.vscode/snippets/*.code-snippets`（`snippets` 目录）或按语言的 `*.json`。
- 用户级：`Ctrl+Shift+P` → `Preferences: Configure User Snippets` → 选语言。

```jsonc
{
  "Debug print": {
    "prefix": "dbg",
    "body": ["console.log('$1', ${1:arg});"],
    "description": "打印变量"
  },
  "Python 函数头": {
    "prefix": "defh",
    "body": ["def ${1:name}(${2:args}) -> ${3|None,str,int|}:",
             "\t\"\"\"${4:说明}\"\"\"",
             "\t${0:pass}"]
  }
}
```

`$1` 是第一个停靠点，`${3|a,b|}` 是下拉选择，`$TM_SELECTED_TEXT` 可包裹选中文本。

### 3.6 扩展管理（效率与安全的平衡点）

- 安装/禁用入口：`Ctrl+Shift+X`。已装列表用 `@installed`，禁用中的用 `@disabled`，冲突排查用 `@running`。
- **性能优先**：先尝试内置能力再装扩展。语法高亮、括号匹配、多光标、Git 基础操作、终端、任务、调试都内置。
- **按工作区禁用**：扩展齿轮 → `(工作区) Disable`，避免 Python 项目和前端项目互相拖慢。
- **扩展导致卡顿的判定法**：`Ctrl+Shift+P` → `Start Extension Bisect`，它自动二分你的扩展列表找出肇事者；或用 `code --disable-extensions .` 对比启动速度。
- **工作区信任**：打开陌生仓库时 VS Code 会限制部分扩展执行（防恶意脚本）。个人机器上如果嫌烦，可设 `security.workspace.trust.untrustedFiles`，但要清楚这是安全让步——不要对随手下载的仓库关掉信任。

### 3.7 任务（tasks.json）：把重复命令固化

`Ctrl+Shift+P` → `Tasks: Configure Default Build Task` → 选/写 `tasks.json`。之后 `Ctrl+Shift+B` 一键跑。

```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "dev",
      "type": "shell",
      "command": "npm run dev",
      "isBackground": true,
      "problemMatcher": []            // 后台任务需空匹配器，否则报"无法解析"
    },
    {
      "label": "test: unit",
      "type": "shell",
      "command": "npm test -- --run",
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": ["$tsc"]     // 让报错出现在"问题"面板，可点击跳转
    }
  ]
}
```

`problemMatcher` 是任务系统的价值所在：编译器/测试的输出被解析成可点击的错误列表。内置变量 `${workspaceFolder}`、`${file}`、`${fileBasenameNoExtension}` 可在 command 里用。

### 3.8 多根工作区

`文件 → 将文件夹添加到工作区…`，再 `文件 → 工作区另存为…` 得到 `.code-workspace`：

```jsonc
{
  "folders": [
    { "path": "../backend" },
    { "path": "../frontend", "name": "前端" }
  ],
  "settings": { "editor.tabSize": 2 }
}
```

适合"前端 + 后端一起改"的场景。注意：Git 面板会分别显示两个仓库的状态。

### 3.9 命令行/自动化打开方式速记

```powershell
code --user-data-dir E:\vscode-sandbox .   # 独立配置目录，测试扩展不污染主环境
code --extensions-dir E:\vscode-exts .     # 独立扩展目录（便携化）
```

想彻底便携：下载官网 **ZIP** 版解压，在 VS Code 根目录（与 `bin` 同级）新建一个名为 `data` 的文件夹——存在该目录即进入便携模式，设置与扩展都写在这里，不碰 `%APPDATA%\Code`；"关于"框里会显示 Portable。

---

## 4. 高效编辑工作流

### 4.1 多光标三连（最省时间的技巧）

| 场景 | 操作 |
| --- | --- |
| 同一文件里逐个改同名变量 | `Ctrl+D`（选中第一个词，连按扩展下一个） |
| 一次全部改 | `Ctrl+Shift+L` |
| 在若干行行首同时输入 | `Ctrl+Shift+Alt + 方向键` 列选择，或按住 `Alt` 拖鼠标 |
| 给每行末尾加分号 | 列选择到行尾 → `Shift+Alt+→` 到行末 → 输入 |
| 按内容加光标 | `Ctrl+Shift+P` → `Add Cursor to Line Ends`，或 `Find` 里 `Alt+Enter` |

### 4.2 选择与重构

1. `Shift+Alt+→` 连续扩大选区（单词 → 字符串 → 表达式 → 块 → 函数），比鼠标拖准。
2. `Ctrl+.` 打开快速修复：提取变量/函数、加 try/catch、导入缺失模块、切换引号风格都在这里。
3. `F2` 重命名符号走语言服务器，跨文件同步，比全局替换安全得多。

### 4.3 搜索替换的正确姿势

- 局部：`Ctrl+H` → 打开 `Alt+K`（匹配多行/保留大小写）、`Alt+A`（全部替换前用 `Alt+Enter` 选中所有匹配逐个确认）。
- 正则替换里用捕获组：查找 `(\w+)\s*=\s*(\d+)` → 替换 `$1 = Number($2)`。
- 跨文件：`Ctrl+Shift+F` → 输入 `files to include: src/**/*.ts`、`files to exclude: **/*.spec.ts`；结果面板里可按目录折叠、逐文件展开预览。
- **替换前先按 `Tab` 键预览正则匹配效果**（搜索框会实时高亮），避免误伤。

### 4.4 阅读大型文件的流程

1. `Ctrl+T` 直接按符号名跳，别从文件头滚。
2. 开 `editor.stickyScroll.enabled` 常驻显示当前函数名。
3. `Ctrl+Shift+O` 看当前文件符号树；输入 `:` 按 kind 分组。
4. `Alt+F12` 速览定义，不打断当前阅读位置；`Alt+←` 跳回。
5. `Ctrl+F1`（或右键标签 → 拆分到下一组）把两个文件并排对照。

### 4.5 终端与编辑器的配合

- `` Ctrl+` `` 打开/隐藏终端（唯一被官方键位表列出的终端键位）。分屏/关闭等默认键位为 `Ctrl+Shift+5`（拆分）、`Ctrl+Shift+D`（终止）、`Alt+↑/↓`（在多个终端间切换）、`Ctrl+K`（清屏）——这几项**不是每个版本都稳定**，用 `Ctrl+K Ctrl+S` 搜 `terminal: split` / `kill` 核对你本机的实际绑定；也可以直接用面板右上角的 `+` 和下拉菜单。
- 链接可点击：终端里的文件路径 `Ctrl+点击` 直接在编辑器打开。
- 命令出错时，把选中内容交给 AI 解释/生成命令：`Ctrl+I`（终端内联聊天，需 AI 扩展与账号）。
- 让终端"跑在当前目录之上"：`Ctrl+Shift+P` → `Terminal: Select Default Profile` 选 PowerShell / Git Bash / WSL。
- 用 `Ctrl+P` 输入 `> ` 前缀直接执行命令（等价命令面板，但不占鼠标）。

### 4.6 时间线（Timeline）：没提交也有历史

即使某个文件从没进过 Git，VS Code 也会为编辑过的文件保留本地历史条目。做法：资源管理器选中文件 → 右键 → **Open Timeline / 打开时间线**（或面板底部 `Timeline` 视图）→ 点任意条目与当前版本做 diff → 右键条目复制内容或整体替换回去。误删未提交代码时这是第一站。

> 局限：本地历史有保留时长和大小上限，且换机器不带；重要内容仍然必须靠 Git。

---

## 5. 特定场景工作流

### 5.1 Git 工作流

**内置能力（不用装扩展就能覆盖日常）：**

| 能力 | 入口 |
| --- | --- |
| 暂存 / 部分暂存 | `Ctrl+Shift+G` → 文件旁 `+`；行级暂存：在 diff 视图选中行 → `Stage Selected Ranges` |
| 提交 / 推送 / 拉取 / 同步 | 提交框 + `⌄` 菜单；状态栏左下角分支处 |
| 分支与合并 | 状态栏分支名 → 顶部切换/创建；命令面板 `Git: Checkout to…`、`Git: Merge Branch…` |
| 冲突解决 | 冲突文件里 `Current Change / Incoming Change / Accept Both` 内联按钮 + 合并编辑器（3 栏，左=本地、中=结果、右=远端） |
| 提交历史图 | 内置 Commit Graph：源代码管理面板标题栏的图表/菜单入口，或 `Ctrl+Shift+P` 搜 `graph` 查看确切命令名（默认偏当前分支线性历史，需自行开启"显示所有分支/合并提交/标签"） |
| 行内 blame | `"git.blame.editorDecoration.enabled": true` 后光标所在行尾部显示作者与时间 |
| stash / 打标签 / revert | 命令面板搜 `Git: Stash` / `Git: Create Tag` / `Git: Revert Commit` |

**扩展补充（按需）：**

| 扩展 | 用途 | 取舍 |
| --- | --- | --- |
| Git Graph（`mhutchie.git-graph`） | 成熟的分支拓扑图 + 节点右键 checkout / cherry-pick / revert | 装前先把内置历史图试够；大仓库首次加载会慢几秒 |
| Git History | 单文件"一步步变成现在"的时间线 | 与 Git Graph 二选一，别都装 |
| GitLens | Inline blame、文件历史、Commit 图、PR、worktree 增强 | 由 GitKraken 维护，部分高级功能需登录/付费；且与内置 blame 重复，装它就把 `gitlens.currentLine.enabled` 关掉 |
| Error Lens | 把错误/警告直接显示在行尾 | 与内置 `git.blame` 同行显示会挤，选一种 |

**推荐工作流（日常一次提交的完整闭环）：**

```
1) Ctrl+Shift+G  → 看变更列表，逐个点开 diff
2) 行级暂存需要的部分（不要整文件无脑 +）
3) 提交框写信息 → Enter（或 Ctrl+Enter 带消息提交）
4) 状态栏"同步"→ 冲突时打开合并编辑器逐块决定
5) 打开内置提交图核对新提交落在哪个分支（找不到入口就 `Ctrl+Shift+P` 搜 `graph`）
```

Windows 凭据：确保 `git config --global credential.helper manager`（Git for Windows 自带 Git Credential Manager），否则每次推送都要输 token。

### 5.2 Python

扩展组合（免费、够用）：

| 扩展 ID | 作用 |
| --- | --- |
| `ms-python.python` | 解释器选择、调试、测试、环境（内含 Pylance 作为可选依赖） |
| `ms-python.vscode-pylance` | 语言服务器：补全、类型检查、跳转（基于开源 Pyright 引擎） |
| `ms-python.black-formatter` / `charliermarsh.ruff` | 格式化 / Lint（Ruff 快且可自动修复） |
| `ms-python.debugpy` | 调试适配器 |
| `ms-toolsai.jupyter` | Notebook |

关键设置：

```jsonc
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
  "python.terminal.activateEnvironment": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": { "source.fixAll.ruff": "explicit", "source.organizeImports.ruff": "explicit" }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"],
  "files.exclude": { "**/__pycache__": true, "**/.venv": true }
}
```

标准流程：

1. 终端创建环境：`python -m venv .venv` → VS Code 右下角会提示选择解释器，点它。
2. 选解释器命令：`Ctrl+Shift+P` → `Python: Select Interpreter`。
3. `.vscode/launch.json` 由 `Python: Create Django/Flask…` 或调试面板"创建 launch.json"生成；运行当前文件用 `Ctrl+F5`，调试用 `F5`（`"console": "integratedTerminal"` 才能正常输入 `input()`）。
4. 测试侧边栏（`Testing` 视图）自动发现 pytest 用例，可单个跑、重跑失败项。
5. **在 WSL/Linux 里开发 Python**：见 §5.5，比 Windows 原生 venv 更省事（依赖编译、路径问题少）。

### 5.3 前端（HTML/CSS/TS/React/Vue）

```jsonc
{
  "editor.tabSize": 2,
  "javascript.format.enable": false,           // 让 Prettier 独家负责，避免双重格式化
  "typescript.format.enable": false,
  "[javascriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "emmet.triggerExpansionOnTab": true,
  "emmet.includeLanguages": { "javascript": "javascriptreact" },
  "css.validate": false, "less.validate": false, "scss.validate": false, // 交给 stylelint
  "editor.quickSuggestions": {              // 字符串/注释内是否弹提示
    "other": true, "comments": false, "strings": "onWordStart"
  }
}
```

预览模式（单击文件总在同一个斜体标签里被替换掉）不止一个开关：

| 触发路径 | 对应设置 |
| --- | --- |
| 资源管理器单击 | `workbench.editor.enablePreview: false` |
| `Ctrl+P` 打开 | `workbench.editor.enablePreviewFromQuickOpen`（仅在上一项为 `true` 时才有意义） |
| 跳转定义等代码导航 | `workbench.editor.enablePreviewFromCodeNavigation` |
| 搜索结果里双击 | `search.editor.doubleClickBehaviour: "open"` |

另外：把文件拖到分组里产生的临时标签不受 `enablePreview` 控制；扩展内部调用 `showTextDocument` 时也不读这个设置。斜体标签可随时用 `Ctrl+K Enter` 转正。

扩展：`esbenp.prettier-vscode`、`dbaeumer.vscode-eslint`、`stylelint`、`bradlc.vscode-tailwindcss`（若用 Tailwind）、`Vue.volar`（Vue）。

必用内置能力：`editor.linkedEditing`（改标签同步闭合标签）、重命名符号 `F2`（跨文件改组件名）、`F12` 跳 TS 定义、CSS 变量/颜色预览、`Ctrl+Shift+P` → `Developer: Reload Window` 在扩展卡住时重载。

前端调试：
- 浏览器调试装 `ms-vscode.js-debug`（内置，Chrome/Edge 配置开箱可用）：

```jsonc
// .vscode/launch.json
{
  "type": "chrome", "request": "launch", "name": "本地调试",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/src",
  "sourceMaps": true
}
```

- Node 后端调试：`"type": "node"` + `"program": "${workspaceFolder}/src/index.ts"`（配 ts-node 或先用构建产物）。

### 5.4 调试（通用方法论）

`launch.json` 结构：`configurations`（怎么启动）+ `compounds`（组合启动）。常用字段：

| 字段 | 作用 |
| --- | --- |
| `type` / `request` | 语言调试器 / `launch`(VS Code 启动进程) 或 `attach`(接已运行进程) |
| `program` / `cwd` / `env` | 入口、工作目录、环境变量 |
| `args` | 命令行参数 |
| `console` | `integratedTerminal`（需要 stdin 时用）/ `internalConsole` |
| `justMyCode` | `false` 可步入库源码（Python 排障常用） |
| `sourceMaps` / `outFiles` | 断点落在源码而非编译产物 |
| `preLaunchTask` | 启动前先跑构建任务 |
| `postDebugTask` | 调试结束顺带停掉另一个会话 |

高频操作：`F9` 断点；条件断点（右键断点行号 → `编辑断点`，写表达式，支持命中次数）；日志点（不断住只打印，替代临时 `print`）；监视面板加表达式；调试工具条 `F10/F11/Shift+F11`；调用堆栈右键 → 打开源代码/跳出。

`attach` 到已运行进程的 Python 示例：

```jsonc
{ "name": "Attach", "type": "debugpy", "request": "attach",
  "connect": { "host": "127.0.0.1", "port": 5678 } }
// 程序侧：python -m debugpy --listen 5678 --wait-for-client app.py
```

### 5.5 远程开发（WSL / SSH / 容器 / 隧道）

四种方式，共同点：右下角/左下角的**远程指示器**或 `Ctrl+Shift+P` 连接；编辑器 UI 跑在本地，语言服务器与终端跑在远端。

| 方式 | 扩展 | 适合 | 连接入口（命令面板） |
| --- | --- | --- | --- |
| WSL | `ms-vscode-remote.remote-wsl` | Windows 上要 Linux 工具链（最省事的组合） | `WSL: Connect to Distribution…`；或在 WSL 里直接 `code .` |
| Remote-SSH | `ms-vscode-remote.remote-ssh` | 连服务器/实验室机器 | `Remote-SSH: Connect to Host…`（先配 `~/.ssh/config` 的 `Host` 别名 + `IdentityFile`） |
| Dev Containers | `ms-vscode-remote.remote-containers` | 团队统一环境、有 `devcontainer.json` 的仓库 | `Dev Containers: Reopen in Container`；也能从 Docker 内部连进容器 |
| Remote-Tunnels | `ms-vscode-remote.remote-tunnels` | 不方便配 SSH 的机器，外出访问家里电脑 | `Remote-Tunnels: Turn on Remote Tunnel Access…`（需登录） |

要点与坑：
- WSL 里首次使用会提示在 Linux 端安装 VS Code Server，等待即可；`code` 命令在 WSL 内部自动可用。
- 端口转发：面板 → `端口` 标签，远端监听端口自动出现在列表，`localhost:8080` 直接映射到本地浏览器。
- 远程里 `files.autoSave`、主题这类设置属于"用户/窗口"作用域，`"machine-overridable"` 作用域的设置（如解释器路径）要在**远程窗口里单独设**，别指望本地设置自动生效。
- SSH 反复要密码 → 用密钥 + `ssh-agent`；Windows 上确认 `ssh-agent` 服务启动（`Get-Service ssh-agent | Set-Service -StartupType Automatic`）。
- 磁盘：每个远程端会缓存 VS Code Server，长期不用可在远端删 `~/.vscode-server`。

### 5.6 Markdown / 文档写作（本指南同类产出适用）

内置即可：`Ctrl+Shift+V` 预览、`Ctrl+K V` 侧边预览、`Ctrl+Shift+O` 文档大纲、表格编辑器（`Markdown: Create Table`… 命令面板搜 `table`）。
建议 `"editor.wordWrap": "on"`（对 markdown 用 `[markdown]` 语言特定设置）、`"[markdown]": {"files.trimTrailingWhitespace": false}`（尾部两空格是换行语法）。
扩展按需：`Markdown All in One`（目录/列表自动续行/快捷键加粗斜体）、`markdownlint`（风格检查）、`yzhang.markdown-all-in-one` 与前者同名注意别装重复。

### 5.7 JSON / YAML / TOML / INI

- JSON 支持注释：文件首行加 `//` 前用 `jsonc` 语言模式（VS Code 的配置文件都是 jsonc）。`Ctrl+Shift+P` → `Change Language Mode` → `JSON with Comments`。
- 自动补全靠 schema：`"json.schemas": [{ "fileMatch": ["*.config.json"], "url": "./schema/x.json" }]`；或文件里写 `"$schema": "https://…"`。
- YAML 装 `redhat.vscode-yaml`，同样吃 `$schema`，能校验 GitHub Actions、K8s、`devcontainer.json` 等。
- **按文件类型指定打开方式**用 `workbench.editorAssociations`（值是 `glob → viewType` 的对象，不是数组）：

```jsonc
"workbench.editorAssociations": {
  "*.md": "vscode.markdown.preview.editor",  // 双击 .md 直接进预览
  "*.csv": "default"                         // 强制用文本编辑器，别用内置表格视图
}
```

`files.associations` 只管语法高亮，与"用哪个编辑器打开"无关，两者别混。写错 `viewType` 会静默回落到文本编辑器；要确认本机可用的标识，在标签页右键 → **Open With… / 打开方式…**，那里列出的就是当前文件可用的编辑器，右下角还能一键"配置默认编辑器"。

- **网上抄来的配置片段先验证再写**：不存在的键名不会报错，只会静默失效（这是"我明明设了却没效果"的头号原因）。验证方法：`Ctrl+,` 打开图形界面搜该键名 —— 搜不到就说明本机这个版本没有它；或在 `settings.json` 里看是否有自动补全与悬停说明。
- 只读/权限问题：文件被 `files.readonlyInclude` 标记、或工作区未信任，都会让改动看起来"保存了但没生效"。

### 5.8 AI 辅助编码（2026 现状）

- VS Code 内置 Chat/Agent 面板与 Copilot 类扩展配合使用；键位见 §2.7。
- GitHub Copilot 自 2026 年 6 月起转为**按 AI 积分用量计费**：Free 档约每月 2000 次补全 + 50 次聊天，Pro 约 $10/月含约 1500 积分（不同模型消耗不同）。补全与"下一个编辑建议"在付费档中不消耗积分。数字以官方 [copilot/plans](https://github.com/features/copilot/plans) 页为准，第三方来源可能滞后。
- 免费/自带密钥路线：开源扩展 `Cline`（MIT，无订阅，模型按量付费，可自带 OpenAI/Anthropic/DeepSeek/Ollama 等密钥）。
- 实用习惯：用 `Ctrl+I` 行内改选中代码（小改动最快）；跨文件需求才开 Agent；把 AI 产出当作"必须读一遍的补丁"，别直接提交。
- 隐私提醒：AI 扩展会把代码上下文发到远端。公司项目/涉密仓库前先确认策略；可用 `@workspace` 之类提示限定上下文，或对特定 Profile 不装 AI 扩展（这正是 §3.4 Profile 的用法之一）。

---

## 6. 常见问题排查

| 症状 | 排查顺序 |
| --- | --- |
| 启动/输入明显卡顿 | ①`Ctrl+Shift+P` → `Startup Performance` 看耗时；②`Start Extension Bisect` 二分扩展；③`code --disable-extensions .` 对照；④补 `files.watcherExclude`（node_modules/.git/dist/.venv） |
| 某个扩展"报错/失效" | 扩展页 → 该扩展 → `Extension Host` 日志；`Developer: Reload Window`；看是否版本要求高于当前 VS Code；实在冲突就按工作区禁用 |
| 终端中文乱码 | 设置 `"terminal.integrated.env.windows": {"PYTHONIOENCODING":"utf-8"}`；PowerShell 里 `chcp 65001`；文件本身编码不对时 `Ctrl+Shift+P` → `Reopen with Encoding`（**不是** `Save with Encoding`，先看是读取错还是存储错） |
| 文件右下角显示 CRLF，同事仓库全是 LF | `"files.eol": "\n"` + 项目 `.gitattributes` 里 `* text=auto eol=lf`；临时转换：`Change End of Line Sequence` |
| `git push` 反复要账号密码 | `git config --global credential.helper manager`；首次推送走浏览器授权；PAT 过期需重新授权 |
| 保存后没格式化 | 检查：①有没有装 formatter ②`[lang]` 里是否指定了 `editor.defaultFormatter`（多个格式化器时不指定会弹窗或静默失败）③`files.readonly`/项目被信任限制 |
| F5 无法调试 / "配置无效" | `launch.json` 的 `type` 是否拼对、对应扩展是否装、`preLaunchTask` 的 `label` 是否与 `tasks.json` 完全一致 |
| 全局搜索搜不到内容 | 检查 `search.exclude`、`useIgnoreFiles`（被 `.gitignore` 排除）、`search.followSymlinks`、是否在"已打开文件"范围里搜 |
| 远程连接一直转圈 | 远端删 `~/.vscode-server` 重下；确认远端磁盘/内存没爆；SSH 情况先纯终端 `ssh 别名` 验证；代理/防火墙拦截 |
| 想找回误删的未提交代码 | 文件右键 → `Open Timeline`（时间线里的本地历史条目）；已删除文件可从 `%APPDATA%\Code\User\History` 目录按内容搜索找回 |
| 想把环境彻底重置 | 先 `Preferences: Open Settings (JSON)` 备份文件 + `code --list-extensions > exts.txt`，再删 `%APPDATA%\Code` 与 `%USERPROFILE%\.vscode\extensions` |

**通用排查心态**：先二分（扩展/设置/项目文件），再定位，最后才卸载重装。重装 VS Code 通常不解决问题，因为配置和扩展在用户目录里活着。

---

## 7. 附录

### 7.1 关键文件路径（Windows）

| 内容 | 路径 |
| --- | --- |
| 用户设置 | `%APPDATA%\Code\User\settings.json` |
| 键位 | `%APPDATA%\Code\User\keybindings.json` |
| 代码片段 | `%APPDATA%\Code\User\snippets\` |
| 工作区设置 | `<项目>\.vscode\settings.json` |
| 已装扩展 | `%USERPROFILE%\.vscode\extensions` |
| 日志 | `%APPDATA%\Code\logs`（`Developer: Open Logs Folder`） |
| WSL/远程端缓存 | `~/.vscode-server`（Linux 侧） |
| 机器状态/界面状态 | `%APPDATA%\Code\User\globalStorage\state.vscdb` |

### 7.2 建议的学习顺序（两周计划）

| 天 | 目标 | 检验标准 |
| --- | --- | --- |
| 1–2 | 只用键盘打开文件、切文件、搜索 | 不开鼠标完成一轮改动 |
| 3–4 | 多光标 + `Ctrl+.` + `F2` | 一次批量改名不用正则 |
| 5–6 | 把自己的 `settings.json` 调成"保存即格式化" | 提交 diff 里没有空白改动 |
| 7 | 快捷键自定义 + Profile 建立 | 有 2 个 Profile，各装各的扩展 |
| 8–10 | Git 内置流程 + 冲突合并编辑器 | 独立完成一次 rebase/merge 冲突 |
| 11–12 | 调试：断点/条件断点/日志点 | 用日志点替代临时 print |
| 13 | `tasks.json` 固化项目命令 | `Ctrl+Shift+B` 起服务 |
| 14 | 远程开发（WSL 或 SSH） | 在远端跑通调试与端口转发 |

### 7.3 官方参考

- 文档主站：<https://code.visualstudio.com/docs>
- 默认键位：<https://code.visualstudio.com/docs/reference/default-keybindings>
- 设置：<https://code.visualstudio.com/docs/getstarted/settings>
- Profiles：<https://code.visualstudio.com/docs/editor/profiles>
- 远程开发总览：<https://code.visualstudio.com/docs/remote/remote-overview>
- 任务：<https://code.visualstudio.com/docs/editor/tasks> · 调试：<https://code.visualstudio.com/docs/editor/debugging>
- 发布说明（每月初，跟版本看新特性）：<https://code.visualstudio.com/updates>

---

*生成于 2026-11-04。键位与设置项核对自官方文档；Copilot 计费等第三方信息以官方定价页为准。若你的版本行为与本文不符，先在本机用命令面板/键位编辑器验证，再决定是否更新本文。*
