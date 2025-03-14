#!/usr/bin/env python3
import sqlite3
import os
import subprocess

def parse_draft(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    # Find the separator (first occurrence of '---')
    try:
        sep_index = lines.index('---')
    except ValueError:
        raise Exception("Draft file missing front matter separator '---'")
    front_matter_lines = lines[:sep_index]
    markdown_content = "\n".join(lines[sep_index+1:]).strip()
    
    metadata = {}
    for line in front_matter_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    return metadata, markdown_content

def get_category_id(conn, category_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()
    return cur.lastrowid

def import_draft(draft_path, db_path):
    metadata, markdown_content = parse_draft(draft_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Insert post
    cur.execute("""
        INSERT INTO posts (slug, title, markdown_content, publish_date)
        VALUES (?, ?, ?, ?)
    """, (metadata.get('slug'), metadata.get('title'), markdown_content, metadata.get('publish_date')))
    post_id = cur.lastrowid

    # Process categories (assume comma-separated if multiple)
    categories = [c.strip() for c in metadata.get('categories', '').split(',') if c.strip()]
    for cat in categories:
        cat_id = get_category_id(conn, cat)
        cur.execute("INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)", (post_id, cat_id))
    
    conn.commit()
    conn.close()

def dump_database(db_path):
    result = subprocess.check_output(["sqlite3", db_path, ".dump"], text=True)
    print(result)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "instance", "blog.db")
    draft_path = os.path.join(script_dir, "..", "drafts", "you-arent-locked-in.md")
    import_draft(draft_path, db_path)
    dump_database(db_path)
