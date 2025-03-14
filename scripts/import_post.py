#!/usr/bin/env python3
import sqlite3
import os
import subprocess


def parse_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    # Find the separator (first occurrence of '---')
    try:
        sep_index = lines.index("---")
    except ValueError:
        raise Exception("Draft file missing front matter separator '---'")
    front_matter_lines = lines[:sep_index]
    markdown_content = "\n".join(lines[sep_index + 1 :]).strip()

    metadata = {}
    for line in front_matter_lines:
        if ":" in line:
            key, value = line.split(":", 1)
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


def normalize_publish_date(date_str):
    import datetime

    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("publish_date must be in YYYY-MM-DD format: " + date_str)
    return dt.strftime("%Y-%m-%d 00:00:00")


def import_post(post_path, db_path):
    metadata, markdown_content = parse_post(post_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    slug = metadata.get("slug")
    cur.execute("SELECT id FROM posts WHERE slug = ?", (slug,))
    row = cur.fetchone()
    if row:
        post_id = row[0]
        cur.execute(
            "UPDATE posts SET title=?, markdown_content=?, publish_date=? WHERE id=?",
            (
                metadata.get("title"),
                markdown_content,
                normalize_publish_date(metadata.get("publish_date")),
                post_id,
            ),
        )
        cur.execute("DELETE FROM post_categories WHERE post_id = ?", (post_id,))
    else:
        cur.execute(
            "INSERT INTO posts (slug, title, markdown_content, publish_date) VALUES (?, ?, ?, ?)",
            (
                slug,
                metadata.get("title"),
                markdown_content,
                normalize_publish_date(metadata.get("publish_date")),
            ),
        )
        post_id = cur.lastrowid

    # Process categories (assume comma-separated if multiple)
    categories = [
        c.strip() for c in metadata.get("categories", "").split(",") if c.strip()
    ]
    for cat in categories:
        cat_id = get_category_id(conn, cat)
        cur.execute(
            "INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)",
            (post_id, cat_id),
        )

    conn.commit()
    conn.close()


def dump_database(db_path):
    result = subprocess.check_output(["sqlite3", db_path, ".dump"], text=True)
    with open("blog.sql", "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "instance", "blog.db")
    if len(sys.argv) < 2:
        print("Usage: {} path-to-post".format(sys.argv[0]))
        sys.exit(1)
    post_path = sys.argv[1]
    import_post(post_path, db_path)
    dump_database(db_path)
