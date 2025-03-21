#!/usr/bin/env python3
"""
Generate an empty post template for use with import_post.py.

Usage:
    ./generate_empty_template.py <slug>
"""

import sys

def generate_template(filepath, slug):
    import datetime
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    content = f"""---
title:
slug: {slug}
publish_date: {current_date}
categories: blog
---
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <slug>".format(sys.argv[0]))
        sys.exit(1)
    import os
    slug = sys.argv[1].strip("/").strip()
    os.makedirs("drafts", exist_ok=True)
    output_path = os.path.join("drafts", f"{slug}.md")
    generate_template(output_path, slug)
    print(f"Template written to {output_path}")
