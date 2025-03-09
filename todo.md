# TODO Checklist for Flask Migration Project

## 1. Flask Application Setup
- [ ] Create the `application/` directory structure:
  - [ ] Create `application/__init__.py` to initialize and configure the Flask app.
  - [ ] Create `application/db.py` (if needed) for encapsulating database connection logic.
- [ ] Set up the virtual environment and install dependencies (from `pyproject.toml`).

## 2. Template & Static Asset Migration
- [ ] Convert static HTML files into Jinja2 templates:
  - [ ] Migrate `public_html/index.html` into `application/templates/index.html` (integrate with a base layout).
  - [ ] Migrate `public_html/blog/index.html` into `application/templates/blog/index.html`.
  - [ ] Migrate `public_html/recipes/index.html` into `application/templates/recipes/index.html`.
- [ ] Create a common base template (`application/templates/base.html`) for consistent header, footer, and navigation.
- [ ] Move CSS, JavaScript, and image files from `public_html` into `application/static/`.

## 3. Database Integration & Dynamic Content
- [ ] Review and test `scripts/populate_db.py` to ensure `blog.db` is correctly populated.
- [ ] Implement Flask routes to serve dynamic content:
  - [ ] Route `/blog/<slug>` to display blog posts (query `posts` table).
  - [ ] Route `/recipes/<slug>` to display recipes (query `posts` table).
  - [ ] Homepage route `/` to combine dynamic and semi-static content.
- [ ] Integrate error handling for missing content (e.g., return 404 for non-existent posts) and log errors appropriately.

## 4. Legacy & Archive Content
- [ ] Plan for handling legacy static content:
  - [ ] Serve the `/archive` directory directly as static files.
  - [ ] For other legacy pages, decide whether to integrate them into Flask or leave them as static.
- [ ] Ensure links between new dynamic routes and legacy static pages remain consistent.

## 5. Error Handling, Logging & Testing
- [ ] Implement Flask error handlers (e.g., 404 and 500) with user-friendly messages.
- [ ] Add logging (using Flask's logging or Python’s logging module) for better traceability of issues.
- [ ] Write unit/integration tests for:
  - [ ] Database queries and data retrieval.
  - [ ] Template rendering and route responses.
  - [ ] Error handling paths.

## 6. Deployment & Documentation
- [ ] Update project deployment scripts/configuration to run the Flask app rather than serving static files.
- [ ] Update documentation:
  - [ ] README.md with instructions for local development and deployment.
  - [ ] spec.md with the latest architecture and migration plan.
- [ ] Confirm consistent URL structure and SEO considerations across the new dynamic and static contents.

## 7. Miscellaneous Tasks
- [ ] Verify that the html-to-markdown conversion (with ATX heading style) works as expected.
- [ ] Review any custom logic in `scripts/populate_db.py` for compatibility with the new structure.
- [ ] Conduct a final code review and comprehensive testing before merging changes.
