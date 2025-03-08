#!/usr/bin/env python3
import os
import sqlite3
import re
import sys
from bs4 import BeautifulSoup

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS blog_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    article_content TEXT
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

def process_entries(root_dir, conn):
    c = conn.cursor()
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "index.html" in filenames:
            file_path = os.path.join(dirpath, "index.html")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                title = extract_title(content)
                article_content = extract_article_content(content)
                c.execute("INSERT INTO blog_entries (path, title, content, article_content) VALUES (?, ?, ?, ?)",
                          (file_path, title, content, article_content))
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
