# Obsidian2OpenMD

这个小工具方便博主将 Obsidian 笔记同步发布到 Fuwari 网页，完成标准格式 Markdown 的无痛转换。
例如删除本地笔记之间的 link 同时保留文本，将 `[[双城记]]` 转为 `双城记`。

A lightweight tool to convert Obsidian markdown to publish-ready markdown for Fuwari-styled websites.
Removes local links while keeping text, reformats checkboxes, and optionally injects Fuwari frontmatter.

---

# How to use 使用方法

## Ready-to-use 直接使用

### GUI 模式（推荐）/ GUI Mode (Recommended)

直接打开 `obsidian2openmd.exe`，进入图形界面。
Open `obsidian2openmd.exe` directly to launch the GUI.

- 通过 **Add Files** 或 **Add Folder** 添加任务
  Add tasks via **Add Files** or **Add Folder**
- 文件夹支持最多 **2 层**子目录，超过则会提示重新选择
  Folders support up to **2 levels** of subdirectories; a warning will appear if exceeded
- 每个任务可单独勾选 ☑ / ☐ 是否执行，文件夹支持三态全选 ☑ / 部分选 ☒ / 全不选 ☐
  Each task has an individual checkbox; folder rows support tri-state: ☑ all / ☒ partial / ☐ none
- 双击 **Output Naming Rule** 列可修改输出命名规则（双击文件夹行将同步到所有子文件）
  Double-click the **Output Naming Rule** column to edit; editing a folder row propagates to all children
- 任务列表在关闭程序时自动保存，下次打开自动恢复
  Task list is saved automatically on close and restored on next launch
- 选择 **Plain** 或 **Fuwari** 模式切换输出格式
  Switch between **Plain** and **Fuwari** mode for different output formats

### 命名规则说明 / Naming Rule

| 输入 Input | 效果 Output |
|---|---|
| `Opensource_`（默认，前缀）| `Opensource_filename.md` |
| `_draft`（后缀，以 `_` 开头）| `filename_draft.md` |
| `output.md`（精确文件名）| `output.md` |

### CLI 模式（拖拽）/ CLI Mode (Drag & Drop)

将 `.md` 文件直接拖拽到 exe 上，自动生成 `Opensource_` 前缀的副本，与旧版行为一致。
Drag and drop a `.md` file onto the exe to generate an `Opensource_`-prefixed copy, same as previous versions.

---

## Output 输出示例

![image](https://github.com/Momordicin/obsidian2openmd/blob/main/test/stylemarkdown.jpg)

The newest posts are produced by Obsidian2openmd.
Welcome to [my blog](https://blog.laevatain.net/).

---

## For developers 开发者

### 项目结构 / File Structure

```
converter.py   ← 核心处理逻辑 / Core processing functions
plain.py       ← CLI 入口，Plain 模式 / CLI entry, plain mode
fuwari.py      ← CLI 入口，Fuwari 模式 / CLI entry, Fuwari mode
ui.py          ← GUI 主入口（打包目标）/ GUI entry (build target)
res/           ← 图标资源 / Icon assets
```

### 打包命令 / Build Command

```bash
pyinstaller --onefile --noconsole --icon=res/icon_app.ico --add-data "res/icon_app.ico;res" ui.py
```

---

# What can we expect next 后续计划

- 图片 link 自动归档，需要配置 image 路径
  Auto-archive image links with one-step path configuration
- 对个人敏感信息（如人名）的自动模糊处理
  Auto-detection and removal of personal information, with offline private set-up

---

# Reminder 注意事项

为保证版本迭代时使用的安全性，本软件只生成副本，不删除原文档。输出文件名默认以 `Opensource_` 开头。

To protect users' important files, this software only generates copies and never deletes original files. Output filenames default to the `Opensource_` prefix.
