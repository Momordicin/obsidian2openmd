# Usage  
这个小工具方便博主将Obsidian笔记同步post到Fuwari网页,  
从而完成标准格式markdown文件的无痛转换.  
如删除本地笔记之间的link同时保留文本, 将link双城记, 转为双城记.  
  
Convert obsidian markdown to formatted markdown for Fuwari-styled website.  
Remove local link, re-format checkbox format, etc.  
# How to use it🚀
## Ready-to-use
Use it by typing in file path or draging the file to obsidian2openmd_x64.exe  
It will create a copy of formatted markdown for you.  
If you don't need Fuwari style frontmatters, use the obsidian2openmd_nofuwari_x64.zip   
  
![image](https://github.com/Momordicin/obsidian2openmd/blob/main/test/test_example.jpg)  
## Output  
![image](https://github.com/Momordicin/obsidian2openmd/blob/main/test/stylemarkdown.jpg)
The newest 2 posts are produced by Obsidian2openmd.
Welcome to [my blog](https://blog.laevatain.net/). 
## For developers🚀🚀
use commands below to build your own exe.
### For all developers
```python
pyinstaller --onefile main.py
```  
### For Fuwari Posters
```python
pyinstaller --onefile main_fuwari.py
```  
# What can we expect next  
后续可能加入对个人敏感信息, 如人名的自动模糊.  
Auto detection and removal of certain personal informations, it may require an offline private set-up when you use it first time.  
批量处理功能.  
One-step processing multiple posts.
# Reminder
为保证版本迭代时使用的安全性, 本软件只生成Opensource开头的markdown副本, 不删除原文档.  
To protect users' important files, this software is only designed for generating copies. Do not implement it to delete any original files.