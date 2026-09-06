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
        # '.' also matches '\r', so CRLF files leave a stray CR inside each
        # item, which breaks YAML parsing of the inline list — strip it.
        items = [i.strip() for i in items if i.strip()]
        eol = '\r\n' if '\r\n' in match.group(1) else '\n'
        return f'tags: [{", ".join(items)}]{eol}'

    new_fm = re.sub(r'^tags:[ \t]*\r?\n((?:[ \t]*-[ \t]*.+\r?\n?)+)',
                    repl, fm, flags=re.MULTILINE)
    if new_fm == fm:
        return md_file
    return md_file[:m.start(1)] + new_fm + md_file[m.end(1):]


def _hard_line_breaks(md_file):
    """Append two trailing spaces to line endings so single newlines survive
    as markdown hard breaks.

    Lines already ending with two spaces are left untouched. Fenced code
    blocks (``` or ~~~) are kept verbatim: adding trailing spaces there
    corrupts the code. Each line keeps its own LF/CRLF ending — appending
    the spaces before the original ending (not replacing '\n' with '  \n')
    is what keeps CRLF files from breaking.
    """
    lines = md_file.splitlines(keepends=True)
    out = []
    fence = None   # opening fence marker while inside a fenced code block
    for line in lines:
        body = line.rstrip('\r\n')
        eol = line[len(body):]
        stripped = body.lstrip()
        if fence is None:
            if stripped.startswith('```') or stripped.startswith('~~~'):
                fence = stripped[:3]
            elif not body.endswith('  '):
                line = body + '  ' + eol
        elif stripped.startswith(fence):
            fence = None
        out.append(line)
    return ''.join(out)


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
    md_file = _hard_line_breaks(md_file)
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
    md_file = _hard_line_breaks(md_file)
    return md_file
