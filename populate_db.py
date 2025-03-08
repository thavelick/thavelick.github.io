#!/usr/bin/env python3
import os
import sqlite3
import re
import sys
import urllib.parse
from bs4 import BeautifulSoup
import email.utils

def convert_pub_date(date_str):
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return date_str

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blog_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    article_content TEXT,
                    publish_date DATETIME
                );''')
    conn.commit()
    return conn

def extract_title(html_content):
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_article_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', class_='content')
    if div:
        return div.decode_contents().strip()
    return ""

def get_publish_dates(rss_path):
    """
    Parse the rss.xml file and return a dict mapping normalized relative paths to publish dates.
    """
    publish_dates = {}
    try:
        with open(rss_path, 'r', encoding='utf-8') as f:
            rss_content = f.read()
        soup = BeautifulSoup(rss_content, 'xml')
        for item in soup.find_all('item'):
            link_tag = item.find('link')
            pub_date_tag = item.find('pubDate')
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
    return publish_dates

def process_entries(root_dir, conn):
    c = conn.cursor()
    count = 0
    rss_path = os.path.join(root_dir, "rss.xml")
    publish_dates = get_publish_dates(rss_path)
    exclusions = ['/index.html', '/404.html', '/404/index.html', '/template.html', '/games/index.html', '/archive/index.html', '/books/index.html', '/blog/index.html']
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
            file_path = os.path.join(dirpath, filename)
            rel_path = "/" + os.path.relpath(file_path, root_dir).replace(os.sep, '/')
            if rel_path in exclusions:
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                title = extract_title(content)
                article_content = extract_article_content(content)
                pub_date = publish_dates.get(rel_path, None)
                c.execute("INSERT INTO blog_entries (path, title, content, article_content, publish_date) VALUES (?, ?, ?, ?, ?)",
                          (file_path, title, content, article_content, pub_date))
                print(f"Inserted: {file_path}")
                count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    conn.commit()
    print(f"Processed {count} entries.")

def main():
    # Use the first command line argument as the root directory, or default to the current directory.
    root_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    db_path = "blog.db"
    conn = create_database(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM blog_entries")
    conn.commit()
    process_entries(root_dir, conn)
    conn.close()

if __name__ == "__main__":
    main()
