# Obsidian2OpenMD

[English](README.md) | 简体中文

这个小工具方便博主将 Obsidian 笔记同步发布到 Fuwari 网页，实现标准格式 Markdown 的无痛转换。

它可以删除本地笔记之间的链接并保留链接文本、重新格式化复选框，还可以选择性地注入 Fuwari frontmatter。例如，将 `[[双城记]]` 转换为 `双城记`。

## 使用方法

### 直接使用

#### GUI 模式（推荐）

直接打开 `obsidian2openmd.exe`，进入图形界面。

- 通过 **Add Files** 或 **Add Folder** 添加任务。
- 文件夹最多支持 **2 层**子目录，超过时会提示重新选择。
- 每个任务都可以单独勾选是否执行。文件夹支持三态选择：☑ 全选、☒ 部分选择、☐ 全不选。
- 双击 **Output Naming Rule** 列可修改输出命名规则；修改文件夹行时，规则会同步到其所有子文件。
- 关闭程序时会自动保存任务列表，下次打开时自动恢复。
- 选择 **Plain** 或 **Fuwari** 模式以切换输出格式。

#### 命名规则说明

| 输入 | 输出 |
| --- | --- |
| `Opensource_`（输出文件夹为源文件夹且未指定规则时使用的默认前缀） | `Opensource_filename.md` |
| `xxx_`（以 `_` 结尾的前缀） | `xxx_filename.md` |
| `_yyy`（以 `_` 开头的后缀） | `filename_yyy.md` |
| `output.md`（精确文件名） | `output.md` |

#### 设置 Fuwari post 根目录

可以设置 Fuwari post 的默认输出目录，同时仍可为单个任务自定义输出位置。

#### CLI 模式（拖拽）

将 `.md` 文件直接拖拽到可执行文件上，即可自动生成带有 `Opensource_` 前缀的副本，与旧版行为一致。

## UI 使用示例

![Obsidian2OpenMD 用户界面](https://github.com/Momordicin/obsidian2openmd/blob/main/test/uiexample.png)

## 输出示例

![Markdown 输出示例](https://github.com/Momordicin/obsidian2openmd/blob/main/test/stylemarkdown.jpg)

最新文章均由 Obsidian2OpenMD 生成。欢迎访问[我的博客](https://blog.laevatain.net/)。

## 开发者说明

### 项目结构

```text
converter.py   ← 核心处理逻辑
plain.py       ← CLI 入口，Plain 模式
fuwari.py      ← CLI 入口，Fuwari 模式
ui.py          ← GUI 主入口（打包目标）
res/           ← 图标资源
```

### 打包命令

```bash
pyinstaller --onefile --noconsole --icon=res/icon_app.ico --add-data "res/icon_app.ico;res" ui.py
```

## 后续计划

- 自动归档图片链接，只需一步配置图片路径。
- 自动检测并移除人名等个人敏感信息，支持离线私有化设置。

## 注意事项

为保证文件安全，本软件只生成副本，不会删除原文档。输出文件名默认使用 `Opensource_` 前缀。
