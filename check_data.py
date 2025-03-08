#!/usr/bin/env python3
import sqlite3

def check_data(db_path="blog.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, path, title FROM blog_entries")
    rows = c.fetchall()
    if rows:
        print("Blog Entries:")
        for row in rows:
            print(f"ID: {row[0]}, Path: {row[1]}, Title: {row[2]}")
    else:
        print("No entries found.")
    conn.close()

if __name__ == "__main__":
    check_data()
