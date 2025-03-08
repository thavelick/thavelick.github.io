#!/usr/bin/env python3
import sqlite3
from bs4 import BeautifulSoup

def main():
    # Open connection to the database
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    # Query posts for slug and article_content
    c.execute("SELECT slug, article_content FROM posts")
    rows = c.fetchall()
    
    for slug, article_content in rows:
        if article_content:
            soup = BeautifulSoup(article_content, 'html.parser')
            # Using a set to ensure each tag appears only once per article
            tags = {tag.name for tag in soup.find_all()}
            if tags:
                tag_list = sorted(tags)
                print(f"{slug}: {','.join(tag_list)}")
            else:
                print(f"{slug}: (no tags found)")
        else:
            print(f"{slug}: (empty article_content)")
    
    conn.close()

if __name__ == '__main__':
    main()
