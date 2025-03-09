CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    article_content TEXT,
                    markdown_content TEXT,
                    publish_date DATETIME
                );
CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
CREATE TABLE IF NOT EXISTS post_categories (
                    post_id INTEGER,
                    category_id INTEGER,
                    PRIMARY KEY (post_id, category_id),
                    FOREIGN KEY (post_id) REFERENCES posts(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );
