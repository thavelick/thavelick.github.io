#!/usr/bin/env python3
"""
Generate an empty post template for use with import_post.py.

Usage:
    ./generate_empty_template.py <slug>
"""

import sys

def generate_template(filepath, slug, force=False):
    import os
    if os.path.exists(filepath) and not force:
        print(f"Error: file {filepath} already exists.")
        sys.exit(1)
    import datetime
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    title = slug.replace('-', ' ').title()
    content = f"""---
title: {title}
slug: {slug}
publish_date: {current_date}
categories: blog
---
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    force = False
    args = sys.argv[1:]
    if "--force" in args:
        force = True
        args.remove("--force")
    if len(args) < 1:
        print("Usage: {} [--force] <slug>".format(sys.argv[0]))
        sys.exit(1)
    import os
    slug = args[0].strip("/").strip()
    os.makedirs("drafts", exist_ok=True)
    output_path = os.path.join("drafts", f"{slug}.md")
    generate_template(output_path, slug, force)
    print(f"Template written to {output_path}")
