# Read a markdown file and print its content
file_path = "test.md"

import sys
import re
from datetime import datetime

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")


def preprocess_md(md_file):
    # Add formatted tag block of Fuwari
    style_str = f"""---
title: {title}
published: {datetime.now().strftime('%Y-%m-%d')} 
description: "{description}"
tags: {tags}
category: {category}
draft: false
---"""
    md_file = style_str + '\n' + md_file

    # Remove formatted tag block of Fuwari
    # md_file = re.sub(r'^---\n.*?\n---\n', '', md_file, flags=re.DOTALL)

    # Remove all [[]] links but remain the text inside
    md_file = re.sub(r'\[\[(.*?)\]\]\([^\)]+\)', r'\1', md_file)
    md_file = re.sub(r'\[\[(.*?)\]\]', r'\1', md_file)

    # Obsidian's boxlist to standard markdown task list
    md_file = re.sub(r'- \[ \]', r'[ ]', md_file)
    md_file = re.sub(r'- \[x\]', r'[x]', md_file)

    # Remove local links and keep external links
    md_file =  re.sub(r'\[([^\]]+)\]\((?!https?:\/\/)([^\)]+)\)', r'\1', md_file)

    # replace single newlines with double newlines except for lines ending with two spaces
    md_file = re.sub(r'(?<!  )\n', '  \n', md_file)
    return md_file

if __name__ == "__main__":
    # file_path = "test.md"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Type in file path or drag the file here, and press enter: \n")
    
    print(f"Processing file: {file_path}")
    title = input("Type in the title: ")
    description = input("Type in the description: ")
    tags = input("Type in the tags with commas: ").split(',')
    tags = list(set([tag.strip() for tag in tags]))
    tags = f"{tags}".replace("'", '"')
    category = input("Type in the category: ")

    # flag = input("Replace the original file? (y/n): ")
    # if flag.lower() == 'y' and input("Are you sure? This action cannot be undone. (y/n): ").lower() == 'y':
    #     result_path = file_path
    result_path = file_path[0:file_path.rfind('\\')+1] + 'Opensource_' + file_path[file_path.rfind('\\')+1:]

    md_file = read_markdown_file(file_path)
    md_file = preprocess_md(md_file)
    with open(result_path, 'w', encoding='utf-8') as file:
        file.write(md_file)
    print("Done!")
    print(f"Processed markdown file saved to '{result_path}'")
    input("Press Enter to exit...")