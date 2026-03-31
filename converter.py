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
    # Remove all [[]] links but remain the text inside
    md_file = re.sub(r'\[\[(.*?)\]\]\([^\)]+\)', r'\1', md_file)
    md_file = re.sub(r'\[\[(.*?)\]\]', r'\1', md_file)

    # Obsidian's boxlist to standard markdown task list
    md_file = re.sub(r'- \[ \]', r'[ ]', md_file)
    md_file = re.sub(r'- \[x\]', r'[x]', md_file)

    # Remove local links and keep external links
    md_file = re.sub(r'\[([^\]]+)\]\((?!https?:\/\/)([^\)]+)\)', r'\1', md_file)

    # replace single newlines with double newlines except for lines ending with two spaces
    md_file = re.sub(r'(?<!  )\n', '  \n', md_file)
    return md_file


def preprocess_md_fuwari(md_file, title, description, tags, category):
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

    # Remove all [[]] links but remain the text inside
    md_file = re.sub(r'\[\[(.*?)\]\]\([^\)]+\)', r'\1', md_file)
    md_file = re.sub(r'\[\[(.*?)\]\]', r'\1', md_file)

    # Obsidian's boxlist to standard markdown task list
    md_file = re.sub(r'- \[ \]', r'[ ]', md_file)
    md_file = re.sub(r'- \[x\]', r'[x]', md_file)

    # Remove local links and keep external links
    md_file = re.sub(r'\[([^\]]+)\]\((?!https?:\/\/)([^\)]+)\)', r'\1', md_file)

    # replace single newlines with double newlines except for lines ending with two spaces
    md_file = re.sub(r'(?<!  )\n', '  \n', md_file)
    return md_file
