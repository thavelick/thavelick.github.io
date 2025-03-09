-- Clean up tables
DELETE FROM post_categories;
DELETE FROM posts;
DELETE FROM categories;
-- Insert a test category 'blog'
INSERT INTO categories (name) VALUES ('blog');
-- Insert a test post with category 'blog'
INSERT INTO posts (slug, title, markdown_content, publish_date) VALUES ('test-post', 'Test Post Title', 'This is **test** content', '2025-03-09 12:00:00');
-- Link blog post to blog category
INSERT INTO post_categories (post_id, category_id) VALUES (
  (SELECT id FROM posts WHERE slug='test-post'),
  (SELECT id FROM categories WHERE name='blog')
);
-- Insert a test category 'recipe'
INSERT INTO categories (name) VALUES ('recipe');
-- Insert a test post with category 'recipe'
INSERT INTO posts (slug, title, markdown_content, publish_date) VALUES ('recipes/test-recipe', 'Test Recipe Title', 'Recipe **content**', '2025-03-09 13:00:00');
-- Link recipe post to recipe category
INSERT INTO post_categories (post_id, category_id) VALUES (
  (SELECT id FROM posts WHERE slug='recipes/test-recipe'),
  (SELECT id FROM categories WHERE name='recipe')
);
