#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown

def extract_main_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    # Attempt to extract the main article content: use the first "div" with class "post"
    main_content = soup.find('div', class_='post')
    if main_content is None:
        # Fallback to extracting the entire main content div
        main_content = soup.find('div', id='content')
    # Remove permalinks from main_content
    for a in main_content.find_all("a", class_="permalink"):
        a.decompose()
    # Remove amazon links
    for a in main_content.find_all("a", href=True):
        if "amazon.com" in a["href"]:
            a.replace_with(a.get_text())
    # (Removed meta paragraph removal to allow category extraction in main())
    # Remove feedback paragraphs from main_content
    for p in main_content.find_all("p", class_="feedback"):
        p.decompose()
    # If main_content is a <div> with class "post", unwrap it to remove the surrounding tag
    if main_content.name == "div" and "post" in main_content.get("class", []):
        children = list(main_content.children)
        main_content.unwrap()
        main_content = BeautifulSoup("".join(str(child) for child in children), 'html.parser')
    # Remove img tags from main_content
    for img in main_content.find_all("img"):
        img.decompose()
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
        basename = f"{parent}.md"
    else:
        basename = os.path.splitext(basename)[0] + ".md"
    output_path = os.path.join(output_dir, basename)
    
    # Extract front matter information from main_content
    title_tag = main_content.find('h2', class_='storytitle')
    if title_tag:
        title = title_tag.get_text(strip=True)
        title_tag.decompose()
    else:
        title = "No Title"
    date_tag = main_content.find('h1', class_='storydate')
    if date_tag:
        date_text = date_tag.get_text(strip=True)
        parts = date_text.split('.')
        if len(parts) == 3:
            month, day, year = parts
            if len(year) == 2:
                year = "20" + year
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            date_str = "1970-01-01"
        date_tag.decompose()
    else:
        date_str = "1970-01-01"
    meta_paras = main_content.find_all("p", class_="meta")
    categories = set()
    for p in meta_paras:
         for a in p.find_all("a", rel="category tag"):
             categories.add(a.get_text(strip=True).lower())
    for p in meta_paras:
         p.decompose()
    categories.add("blog")
    categories_list = ", ".join(sorted(categories))
    slug = os.path.splitext(basename)[0]
    front_matter = f"---\ntitle: {title}\npublish_date: {date_str}\ncategories: {categories_list}\nslug: {slug}\n---\n\n"
    
    markdown_content = convert_to_markdown(str(main_content), heading_style="atx")
    final_content = front_matter + markdown_content
    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write(final_content)
    print("Main content extracted to {}".format(output_path))

if __name__ == '__main__':
    main()
