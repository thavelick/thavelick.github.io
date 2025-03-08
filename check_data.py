#!/usr/bin/env python3
import sqlite3
import argparse
import os

def check_data(db_path, columns):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA table_info(blog_entries)")
    columns_info = c.fetchall()
    valid_columns = [col_info[1] for col_info in columns_info]
    if not valid_columns:
        print("No valid columns found in blog_entries table.")
        exit(1)
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
    default_db = "blog.db"
    parser.add_argument("--db", default=default_db, help="Path to the SQLite database.")
    # Dynamically generate help text for columns from the db
    if os.path.exists(default_db):
        try:
            conn = sqlite3.connect(default_db)
            c = conn.cursor()
            c.execute("PRAGMA table_info(blog_entries)")
            columns_info = c.fetchall()
            valid_columns = [col_info[1] for col_info in columns_info]
            valid_columns_str = ", ".join(valid_columns) if valid_columns else "(no columns found)"
        except Exception as e:
            valid_columns_str = "(Could not retrieve valid columns)"
    else:
        valid_columns_str = "(Database not found: blog.db)"
    parser.add_argument("columns", nargs="*", default=["id", "path", "title", "article_content"],
                        help=f"Columns to display from the blog_entries table. Valid options: {valid_columns_str}")
    args = parser.parse_args()
    check_data(args.db, args.columns)

if __name__ == "__main__":
    main()
