#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup

def extract_main_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    # Attempt to extract the main article content: use the first "div" with class "post"
    main_content = soup.find('div', class_='post')
    if main_content is None:
        # Fallback to extracting the entire main content div
        main_content = soup.find('div', id='content')
    return main_content

def main():
    if len(sys.argv) < 2:
        print("Usage: {} path/to/file.html".format(sys.argv[0]))
        sys.exit(1)
    file_path = sys.argv[1]
    main_content = extract_main_content(file_path)
    if main_content is None:
        print("No main content found in file.")
        sys.exit(1)
    # Create the drafts directory if it doesn't exist
    output_dir = 'drafts'
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.basename(file_path)
    if basename == "index.html":
        parent = os.path.basename(os.path.dirname(file_path))
        basename = f"{parent}.html"
    output_path = os.path.join(output_dir, basename)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write(str(main_content))
    print("Main content extracted to {}".format(output_path))

if __name__ == '__main__':
    main()
