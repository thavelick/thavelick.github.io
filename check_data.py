#!/usr/bin/env python3
import sqlite3
import sys

def check_data(db_path="blog.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    valid_columns = ["id", "path", "title", "content", "article_content"]
    if len(sys.argv) > 1:
        columns = sys.argv[1:]
        for col in columns:
            if col not in valid_columns:
                print(f"Invalid column: {col}. Valid columns: {', '.join(valid_columns)}")
                exit(1)
    else:
        # default columns to show if none specified
        columns = ["id", "path", "title", "article_content"]

    query = "SELECT " + ", ".join(columns) + " FROM blog_entries"
    c.execute(query)
    rows = c.fetchall()
    if rows:
        print("Blog Entries:")
        for row in rows:
            out_items = []
            for col, val in zip(columns, row):
                if col in ("content", "article_content"):
                    snippet = " ".join(val.split()[:10])
                    out_items.append(f"{col.capitalize()}Snippet: {snippet}")
                else:
                    out_items.append(f"{col.capitalize()}: {val}")
            print(", ".join(out_items))
    else:
        print("No entries found.")
    conn.close()

if __name__ == "__main__":
    check_data()
