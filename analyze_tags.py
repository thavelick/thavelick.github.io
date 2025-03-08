#!/usr/bin/env python3
import sqlite3
from bs4 import BeautifulSoup

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze HTML tags in article_content and optionally print inner HTML for selected tags")
    parser.add_argument("--tags", type=str, help="Comma-separated list of tags to print inner HTML")
    args = parser.parse_args()
    selected_tags = set(x.strip().lower() for x in args.tags.split(',')) if args.tags else None
    # Open connection to the database
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    # Query posts for slug and article_content
    c.execute("SELECT slug, article_content FROM posts")
    rows = c.fetchall()
    
    for slug, article_content in rows:
        if article_content:
            soup = BeautifulSoup(article_content, 'html.parser')
            if selected_tags:
                found = {}
                for tag in selected_tags:
                    element = soup.find(tag)
                    if element:
                        found[tag] = element.decode_contents().strip()
                if found:
                    details = ", ".join(f"{t}: {found[t]}" for t in sorted(found))
                    print(f"{slug}: {details}")
                else:
                    print(f"{slug}: (no matching tags found)")
            else:
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
