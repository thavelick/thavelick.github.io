#!/usr/bin/env python3
import sqlite3
import argparse

def check_data(db_path, columns):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    valid_columns = ["id", "path", "title", "content", "article_content"]
    for col in columns:
        if col not in valid_columns:
            print(f"Invalid column: {col}. Valid columns: {', '.join(valid_columns)}")
            exit(1)

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

def main():
    parser = argparse.ArgumentParser(description="Check blog entries in the SQLite database.")
    parser.add_argument("--db", default="blog.db", help="Path to the SQLite database.")
    parser.add_argument("columns", nargs="*", default=["id", "path", "title", "article_content"],
                        help="Columns to display from the blog_entries table. Valid options: id, path, title, content, article_content")
    args = parser.parse_args()
    check_data(args.db, args.columns)

if __name__ == "__main__":
    main()
