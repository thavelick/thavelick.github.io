import json
import llm
from application import create_app
from application.db import get_db


def generate_meta_description(title, content):
    model = llm.get_model("4o-mini")
    # Define a JSON schema for a meta description (max 160 characters for consistency)
    schema = {
        "title": "MetaDescription",
        "type": "object",
        "properties": {
            "meta_description": {
                "title": "Meta Description",
                "type": "string",
                "maxLength": 160,
            }
        },
        "required": ["meta_description"],
    }
    prompt_text = (
        "Write a concise, engaging meta description for a blog post "
        "given the title and its content. "
        "Ensure the meta description is no more than 160 characters and is not promotional. "
        f"Title: {title}\nContent: {content}"
    )
    response = model.prompt(prompt_text, schema=schema)
    try:
        result = json.loads(response.text())
        return result.get("meta_description", "")
    except Exception as e:
        print(f"Error generating meta description for title '{title}':", e)
        return ""


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Force update meta description even if already exists')
    args = parser.parse_args()
    app = create_app()
    with app.app_context():
        db = get_db()
        if args.force:
            posts = db.execute(
                "SELECT id, slug, title, markdown_content, meta_description FROM posts"
            ).fetchall()
        else:
            posts = db.execute(
                "SELECT id, slug, title, markdown_content, meta_description FROM posts WHERE meta_description IS NULL OR meta_description = ''"
            ).fetchall()
        for post in posts:
            meta = generate_meta_description(post["title"], post["markdown_content"])
            db.execute(
                "UPDATE posts SET meta_description = ? WHERE id = ?", (meta, post["id"])
            )
            print(f"Updated post {post['slug']} with meta description: {meta}")
        db.commit()
        import subprocess

        result = subprocess.run(
            ["sqlite3", "instance/blog.db", ".dump"], capture_output=True, text=True
        )
        with open("blog.sql", "w") as f:
            f.write(result.stdout)
        print("Database dumped to blog.sql")


if __name__ == "__main__":
    main()
