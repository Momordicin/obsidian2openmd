import re
from datetime import datetime


def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")


def convert_frontmatter_tags(md_file):
    """Convert Obsidian block-style tags in the YAML frontmatter to Fuwari's
    inline list.

        tags:              ->   tags: [Reading, Foo]
          - Reading
          - Foo

    No-op when there is no leading frontmatter, no block-style tags, or the
    tags are already inline.
    """
    # Frontmatter must be the very first block: --- ... ---
    m = re.match(r'^---[ \t]*\r?\n(.*?\r?\n)---[ \t]*(?:\r?\n|$)', md_file, re.DOTALL)
    if not m:
        return md_file
    fm = m.group(1)   # frontmatter body, between the --- fences

    def repl(match):
        items = re.findall(r'^[ \t]*-[ \t]*(.+?)[ \t]*$',
                           match.group(1), re.MULTILINE)
        items = [i for i in items if i]
        return f'tags: [{", ".join(items)}]\n'

    new_fm = re.sub(r'^tags:[ \t]*\r?\n((?:[ \t]*-[ \t]*.+\r?\n?)+)',
                    repl, fm, flags=re.MULTILINE)
    if new_fm == fm:
        return md_file
    return md_file[:m.start(1)] + new_fm + md_file[m.end(1):]


def preprocess_md(md_file):
    # Normalise Obsidian block-style frontmatter tags to Fuwari's inline list
    md_file = convert_frontmatter_tags(md_file)

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
