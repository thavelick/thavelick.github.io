# TODO Checklist for Flask Migration Project

## 1. Flask Application Setup
- [x] Create the `application/` directory structure:
  - [x] Create `application/__init__.py` to initialize and configure the Flask app.
  - [x] Create `application/db.py` (if needed) for encapsulating database connection logic.
- [x] Set up the virtual environment and install dependencies (from `pyproject.toml`).

## 2. Template & Static Asset Migration
- [x] Convert static HTML files into Jinja2 templates:
  - [x] Migrate `public_html/index.html` into `application/templates/index.html` (integrate with a base layout).
  - [x] Migrate `public_html/blog/index.html` into `application/templates/blog/index.html`.
  - [x] Migrate `public_html/recipes/index.html` into `application/templates/recipes/index.html`.
- [x] Create a common base template (`application/templates/base.html`) for consistent header, footer, and navigation.
- [x] Move CSS, JavaScript, and image files from `public_html` into `application/static/`.

## 3. Database Integration & Dynamic Content
- [x] Review and test `scripts/populate_db.py` to ensure `blog.db` is correctly populated.
- [x] Implement Flask routes to serve dynamic content:
  - [x] Route `/blog/<slug>` to display blog posts (query `posts` table).
  - [x] Route `/recipes/<slug>` to display recipes (query `posts` table).
  - [x] Homepage route `/` to combine dynamic and semi-static content.
- [x] Integrate error handling for missing content (e.g., return 404 for non-existent posts) and log errors appropriately.
- [x] dry up duplicate queries
 [x] Make the RSS feed dynamic

## 4. Legacy & Archive Content
- [x] Plan for handling legacy static content:
  - [x] Serve the `/archive` directory directly as static files.
  - [x] For other legacy pages, decide whether to integrate them into Flask or leave them as static.
- [x] Ensure links between new dynamic routes and legacy static pages remain consistent.

## 4.5 Set up flask to static site generation
- [x] Use flask freeze to generate public_html

## 5. Error Handling, Logging & Testing
- [x] Write unit/integration tests for:
  - [x] Database queries and data retrieval.
  - [x] Template rendering and route responses.
  - [x] Error handling paths.

## 6. Deployment & Documentation
- [ ] Update documentation:
  - [x] README.md with instructions for local development and deployment.
  - [x] spec.md with the latest architecture and migration plan.
- [ ] Confirm consistent URL structure and SEO considerations across the new dynamic and static contents.

## 7. Miscellaneous Tasks
- [x] Verify that the html-to-markdown conversion (with ATX heading style) works as expected.
- [x] Review any custom logic in `scripts/populate_db.py` for compatibility with the new structure.
  - [x] Remove extraneous html columns
- [x] Conduct a final code review
- [ ] Write a blog post about this process
