#!/usr/bin/env python3
import os
import sqlite3
import re
import sys
import urllib.parse
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown
import email.utils
import subprocess


def convert_pub_date(date_str):
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return date_str


def slugify(rel_path):
    slug = rel_path.lstrip("/")
    if slug.endswith("/index.html"):
        slug = slug[: -len("/index.html")]
    elif slug.endswith(".html"):
        slug = slug[: -len(".html")]
    return slug


def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    article_content TEXT,
                    markdown_content TEXT,
                    publish_date DATETIME
                );"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );"""
    )
    c.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'blog')")
    c.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (2, 'recipe')")
    c.execute(
        """CREATE TABLE IF NOT EXISTS post_categories (
                    post_id INTEGER,
                    category_id INTEGER,
                    PRIMARY KEY (post_id, category_id),
                    FOREIGN KEY (post_id) REFERENCES posts(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );"""
    )
    conn.commit()
    return conn


def extract_title(html_content):
    match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        prefixes = ["Tristan Havelick --", "Tristan Havelick :"]
        for prefix in prefixes:
            if title.startswith(prefix):
                title = title[len(prefix):].strip()
                break
        return title
    return None


def extract_article_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    div = soup.find("div", class_="content")
    if div:
        for tag in div.find_all(["h1", "small"]):
            tag.decompose()
        for a in div.find_all("a", href="/blog"):
            print(f"Removing link with text: {a.get_text(strip=True)}")
            a.decompose()
        for tag in div.find_all(["article", "div"]):
            if tag != div:
                tag.unwrap()
        return div.decode_contents().strip()
    return ""


def get_publish_dates(rss_path):
    """
    Parse the rss.xml file and return a dict mapping normalized relative paths to publish dates.
    """
    publish_dates = {}
    try:
        with open(rss_path, "r", encoding="utf-8") as f:
            rss_content = f.read()
        soup = BeautifulSoup(rss_content, "xml")
        for item in soup.find_all("item"):
            link_tag = item.find("link")
            pub_date_tag = item.find("pubDate")
            if link_tag and pub_date_tag:
                link = link_tag.get_text().strip()
                pub_date = pub_date_tag.get_text().strip()
                parsed = urllib.parse.urlparse(link)
                path = parsed.path
                if path.endswith("/"):
                    norm_path = path + "index.html"
                else:
                    norm_path = path
                publish_dates[norm_path] = convert_pub_date(pub_date)
    except Exception as e:
        print(f"Error parsing RSS file {rss_path}: {e}")
    # Add hard-coded dates for entries that are missing publication dates
    hardcoded_dates = {
        "/how-to-verify-on-mastodon/index.html": "2022-11-06 00:00:00",
        "/readable-list/index.html": "2023-05-16 00:00:00",
        "/recipes/cajun-sausage-and-beans/index.html": "2023-10-25 00:00:00",
        "/recipes/chicken-tinga/index.html": "2023-10-15 00:00:00",
        "/recipes/pizza-dough/index.html": "2023-10-15 00:00:00",
        "/recipes/the-rice/index.html": "2023-10-15 00:00:00",
    }
    for path, date in hardcoded_dates.items():
        if path not in publish_dates:
            publish_dates[path] = date
    return publish_dates


def process_entries(root_dir, conn):
    c = conn.cursor()
    count = 0
    rss_path = os.path.join(root_dir, "rss.xml")
    publish_dates = get_publish_dates(rss_path)
    exclusions = [
        "/index.html",
        "/404.html",
        "/404/index.html",
        "/template.html",
        "/games/index.html",
        "/archive/index.html",
        "/books/index.html",
        "/blog/index.html",
        "/recipes/index.html",
        "/blogroll/index.html",
    ]
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            file_path = os.path.join(dirpath, filename)
            rel_path = "/" + os.path.relpath(file_path, root_dir).replace(os.sep, "/")
            if rel_path in exclusions:
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                title = extract_title(content)
                article_content = extract_article_content(content)
                markdown_content = (
                    convert_to_markdown(article_content, heading_style="atx")
                    if article_content
                    else ""
                )
                pub_date = publish_dates.get(rel_path, None)
                slug = slugify(rel_path)
                c.execute(
                    "INSERT INTO posts (slug, title, content, article_content, markdown_content, publish_date) VALUES (?, ?, ?, ?, ?, ?)",
                    (slug, title, content, article_content, markdown_content, pub_date),
                )
                post_id = c.lastrowid
                if slug.startswith("recipes"):
                    category_id = 2
                else:
                    category_id = 1
                c.execute(
                    "INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)",
                    (post_id, category_id),
                )
                print(f"Inserted: {file_path}")
                count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    conn.commit()
    print(f"Processed {count} entries.")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Populate the blog database with entries."
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default="public_html",
        help="Root directory of the blog content.",
    )
    parser.add_argument(
        "--rebuild-db",
        action="store_true",
        help="Drop and recreate the database structure before processing entries.",
    )
    args = parser.parse_args()
    db_path = "instance/blog.db"
    if args.rebuild_db:
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Removed existing database file.")
    conn = create_database(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM post_categories")
    c.execute("DELETE FROM posts")
    conn.commit()
    process_entries(args.root_dir, conn)
    conn.close()
    subprocess.run(["sqlite3", db_path, ".dump"], stdout=open("blog.sql", "w"))


if __name__ == "__main__":
    main()
