import os
import glob
from bs4 import BeautifulSoup


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")

    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    meta = head.find("meta", attrs={"name": "robots"})
    if meta:
        meta["content"] = "noindex"
    else:
        meta = soup.new_tag("meta", **{"name": "robots", "content": "noindex"})
        head.insert(0, meta)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))


def main():
    directory = "application/static/archive/chaos-of-the-mind"
    pattern = os.path.join(directory, "*.htm")
    files = glob.glob(pattern)
    for filepath in files:
        print(f"Processing {filepath}")
        process_file(filepath)


if __name__ == "__main__":
    main()
