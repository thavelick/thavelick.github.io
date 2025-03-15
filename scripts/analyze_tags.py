#!/usr/bin/env python3
from bs4 import BeautifulSoup

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze HTML tags in an HTML file and optionally print inner HTML for selected tags")
    parser.add_argument("filepath", type=str, help="Path to an HTML file")
    parser.add_argument("--tags", type=str, help="Comma-separated list of tags to print inner HTML")
    args = parser.parse_args()
    selected_tags = set(x.strip().lower() for x in args.tags.split(',')) if args.tags else None

    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.filepath}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    slug = os.path.basename(args.filepath)
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
            print(f"{slug}: (no selected tags found)")
    else:
        tags = {tag.name for tag in soup.find_all()}
        if tags:
            tag_list = sorted(tags)
            print(f"{slug}: {','.join(tag_list)}")
        else:
            print(f"{slug}: (no tags found)")

if __name__ == '__main__':
    main()
