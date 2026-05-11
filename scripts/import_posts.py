#!/usr/bin/env python3
import datetime
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path


def parse_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if lines and lines[0] == "---":
        try:
            sep_index = lines[1:].index("---") + 1
        except ValueError:
            raise Exception("Draft file missing closing front matter separator '---'")
        front_matter_lines = lines[1:sep_index]
        markdown_content = "\n".join(lines[sep_index + 1 :]).strip()
    else:
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
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("publish_date must be in YYYY-MM-DD format: " + date_str)
    return dt.strftime("%Y-%m-%d 00:00:00")


def import_post(post_path, conn):
    metadata, markdown_content = parse_post(post_path)
    cur = conn.cursor()

    slug = metadata.get("slug")
    if not slug:
        raise ValueError("Front matter missing required 'slug' field")
    if slug.startswith("/"):
        raise ValueError("Slug must not start with a slash")
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


def dump_database(db_path):
    abs_db_path = os.path.abspath(db_path)
    result = subprocess.check_output(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{abs_db_path}:/db.sqlite:ro",
            "sqlite3-compat",
            "/db.sqlite",
            ".dump",
        ],
        text=True,
    )
    with open("blog.sql", "w", encoding="utf-8") as f:
        f.write(result)


def collect_drafts(drafts_dir):
    return sorted(Path(drafts_dir).glob("*.md"))


def move_to_imported(draft_path, imported_dir):
    draft_path = Path(draft_path)
    imported_dir = Path(imported_dir)
    imported_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = imported_dir / f"{draft_path.stem}.{timestamp}.md"
    if destination.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing file: {destination}"
        )
    shutil.move(str(draft_path), str(destination))
    return destination


def main(argv=None, db_path=None, drafts_dir=None, imported_dir=None):
    if argv is None:
        argv = sys.argv[1:]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if db_path is None:
        db_path = os.path.join(script_dir, "..", "instance", "blog.db")
    if drafts_dir is None:
        drafts_dir = os.path.join(script_dir, "..", "drafts")
    if imported_dir is None:
        imported_dir = os.path.join(script_dir, "..", "drafts-imported")

    if argv:
        drafts = [Path(argv[0])]
    else:
        drafts = collect_drafts(drafts_dir)

    if not drafts:
        print("No drafts to import.")
        return 0

    conn = sqlite3.connect(db_path)
    imported = []
    current = None
    try:
        for draft in drafts:
            current = draft
            import_post(draft, conn)
            imported.append(draft)
    except Exception as e:
        print(f"Error importing {current}: {e}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    dump_database(db_path)
    for draft in imported:
        move_to_imported(draft, imported_dir)
    print(f"Imported {len(imported)} post(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
