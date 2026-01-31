#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DRAFTS_DIR = Path(__file__).parent / "drafts"
POSTS_DIR = Path(__file__).parent / "posts"
INDEX_FILE = Path(__file__).parent / "index.html"

POST_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{excerpt}">
    <title>{title} - Technical Notes</title>
    <link rel="stylesheet" href="../style.css">
    <script src="../copy.js" defer></script>
</head>
<body>
    <nav>
        <a href="../index.html" class="site-title">Technical Notes</a>
        <a href="../index.html">Articles</a>
        <a href="../about.html">About</a>
        <a href="https://github.com/SARPAT">GitHub</a>
        <a href="https://x.com/SARAPATEL21">Twitter</a>
    </nav>

    <main>
        <a href="../index.html" class="back-link">Back to articles</a>

        <article>
            <header class="article-header">
                <h1>{title}</h1>
                <p class="article-meta">{date}</p>
            </header>

            <div class="article-content">
{content}
            </div>
        </article>
    </main>

    <footer>
    </footer>
</body>
</html>
'''

def parse_frontmatter(text):
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, text, re.DOTALL)
    if not match:
        return None, text
    
    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip().lower()] = value.strip()
    
    return frontmatter, match.group(2)

def markdown_to_html(md_text):
    html = md_text
    
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    
    html = re.sub(r'```(\w*)\n(.*?)```', lambda m: f'<pre><code>{escape_html(m.group(2).strip())}</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', html)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    lines = html.split('\n')
    result = []
    in_list = False
    list_items = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if not in_list:
                in_list = True
            list_items.append(f'<li>{stripped[2:]}</li>')
        else:
            if in_list:
                result.append('<ul>\n' + '\n'.join(list_items) + '\n</ul>')
                list_items = []
                in_list = False
            if stripped and not stripped.startswith('<'):
                result.append(f'<p>{stripped}</p>')
            elif stripped:
                result.append(stripped)
    
    if in_list:
        result.append('<ul>\n' + '\n'.join(list_items) + '\n</ul>')
    
    return '\n\n                '.join(result)

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def slugify(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def update_index(title, date, excerpt, filename):
    with open(INDEX_FILE, 'r') as f:
        content = f.read()
    
    new_entry = f'''<li>
                <a href="posts/{filename}">{title}</a>
                <span class="article-date">{date}</span>
                <p class="article-excerpt">{excerpt}</p>
            </li>

            '''
    
    pattern = r'(<ul class="article-list">\s*)'
    replacement = r'\1' + new_entry
    
    if f'posts/{filename}' in content:
        print(f"  Entry for {filename} already exists in index.html")
        return
    
    content = re.sub(pattern, replacement, content)
    
    with open(INDEX_FILE, 'w') as f:
        f.write(content)
    
    print(f"  Updated index.html")

def build_post(md_file):
    print(f"Building: {md_file.name}")
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    frontmatter, body = parse_frontmatter(content)
    
    if not frontmatter:
        print(f"  Error: No frontmatter found. Add title, date, excerpt at top.")
        return False
    
    title = frontmatter.get('title', 'Untitled')
    date = frontmatter.get('date', datetime.now().strftime('%B %d, %Y'))
    excerpt = frontmatter.get('excerpt', '')
    
    html_content = markdown_to_html(body.strip())
    
    html = POST_TEMPLATE.format(
        title=title,
        date=date,
        excerpt=excerpt,
        content=html_content
    )
    
    filename = slugify(title) + '.html'
    output_path = POSTS_DIR / filename
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"  Created: posts/{filename}")
    
    update_index(title, date, excerpt, filename)
    
    return True

def main():
    if not DRAFTS_DIR.exists():
        DRAFTS_DIR.mkdir()
        print(f"Created drafts/ directory")
    
    md_files = list(DRAFTS_DIR.glob('*.md'))
    
    if not md_files:
        print("No markdown files found in drafts/")
        print("\nTo create a new post, add a .md file to drafts/ with this format:")
        print('''
---
title: Your Post Title
date: January 17, 2026
excerpt: A brief description of your post
---

Your content here in Markdown...
''')
        return
    
    built = 0
    for md_file in md_files:
        if build_post(md_file):
            built += 1
    
    print(f"\nBuilt {built} post(s)")
    print("Run 'git add . && git commit -m \"New post\" && git push' to publish")

if __name__ == '__main__':
    main()
