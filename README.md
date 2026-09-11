# Obsidian2OpenMD

English | [简体中文](README.zh-CN.md)

A lightweight tool that helps bloggers convert Obsidian notes into standard, publish-ready Markdown for Fuwari-styled websites.

It removes local note links while preserving their text, reformats checkboxes, and can optionally inject Fuwari frontmatter. For example, `[[A Tale of Two Cities]]` becomes `A Tale of Two Cities`.

## Usage

### Ready-to-use application

#### GUI mode (recommended)

Open `obsidian2openmd.exe` to launch the graphical interface.

- Add tasks with **Add Files** or **Add Folder**.
- Folders may contain up to **2 levels** of subdirectories. The application asks you to select another folder if this limit is exceeded.
- Each task has its own checkbox. Folder rows support three states: ☑ all selected, ☒ partially selected, and ☐ none selected.
- Double-click the **Output Naming Rule** column to edit a naming rule. Editing a folder row applies the rule to all of its child files.
- The task list is saved automatically when the application closes and restored the next time it opens.
- Select **Plain** or **Fuwari** to switch between output formats.

#### Naming rules

| Input | Output |
| --- | --- |
| `Opensource_` (the default prefix when the output folder is the source folder and no rule is specified) | `Opensource_filename.md` |
| `xxx_` (prefix ending in `_`) | `xxx_filename.md` |
| `_yyy` (suffix beginning with `_`) | `filename_yyy.md` |
| `output.md` (exact filename) | `output.md` |

#### Setting the Fuwari post root directory

Set a default output directory for Fuwari posts. You can still customize the destination for individual tasks.

#### CLI mode (drag and drop)

Drag a `.md` file onto the executable to generate a copy with the `Opensource_` prefix, matching the behavior of earlier versions.

## UI example

![Obsidian2OpenMD user interface](https://github.com/Momordicin/obsidian2openmd/blob/main/test/uiexample.png)

## Output example

![Markdown output example](https://github.com/Momordicin/obsidian2openmd/blob/main/test/stylemarkdown.jpg)

The newest posts are produced by Obsidian2OpenMD. Welcome to [my blog](https://blog.laevatain.net/).

## For developers

### Project structure

```text
converter.py   ← Core processing functions
plain.py       ← CLI entry point for Plain mode
fuwari.py      ← CLI entry point for Fuwari mode
ui.py          ← GUI entry point and build target
res/           ← Icon assets
```

### Build command

```bash
pyinstaller --onefile --noconsole --icon=res/icon_app.ico --add-data "res/icon_app.ico;res" ui.py
```

## Roadmap

- Automatically archive image links with one-step image path configuration.
- Automatically detect and remove personal information, such as names, with a private offline setup.

## Important note

To protect your files, this application only creates copies and never deletes the original documents. Output filenames use the `Opensource_` prefix by default.
