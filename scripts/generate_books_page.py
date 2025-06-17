#!/usr/bin/env python3
"""
Generate books_from_goodreads.html from a CSV export.
"""
import csv
import os
import sys
from collections import defaultdict

def generate_books_html(groups, years):
    lines = []
    lines.append('{% extends "base.html" %}')
    lines.append('{% block title %}Tristan Havelick -- Books{% endblock %}')
    lines.append('{% block content %}')
    lines.append('  <a href="/">Tristan Havelick.com</a>')
    lines.append("  <h1>What I've Been Reading</h1>")
    for year in years:
        lines.append(f'  <h2>{year}</h2>')
        lines.append('  <ol reversed>')
        for book in groups[year]:
            title = book.get('Title', '').strip()
            author = book.get('Author', '').strip()
            lines.append(f'      <li>{title} by {author}</li>')
        lines.append('  </ol>')
    lines.append('{% endblock %}')
    return '\n'.join(lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: generate_books_page.py path/to/books.csv")
        sys.exit(1)
    csv_path = sys.argv[1]
    output_path = 'books_from_goodreads.html'
    groups = defaultdict(list)
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_added = row.get('Date Added', '').strip()
            if date_added:
                year = date_added.split('/')[0]
            else:
                year = 'Unknown Year'
            groups[year].append(row)
    years = sorted([y for y in groups if y != 'Unknown Year'], reverse=True)
    if 'Unknown Year' in groups:
        years.append('Unknown Year')
    html = generate_books_html(groups, years)
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Written books page to {output_path}")

if __name__ == '__main__':
    main()
