# Project Specification: Migration to a Flask-Driven Website

## Overview
This specification outlines the migration of a predominantly static website (served from `public_html`) to a dynamic Flask application driven by the SQLite database `blog.db`. The new architecture will serve dynamic content (e.g., blog posts, recipes) while preserving legacy static content (e.g., archives) where appropriate.

## Requirements
- **Python Version:** Preferably Python 3.12+ (as suggested by uv warnings)
- **Key Dependencies:**
  - Flask (for the web framework)
  - beautifulsoup4 (for HTML parsing)
  - html-to-markdown (for markdown conversion)
  - lxml (for XML parsing)
- **Database:** SQLite database (`blog.db`) containing:
  - `posts` table with fields for slug, title, content, article_content, markdown_content, publish_date.
  - `categories` table (e.g., blog, recipe)
  - `post_categories` linking posts to categories

## Architecture & Directory Structure
- **Root Directory:** Contains key files such as `pyproject.toml`, `blog.db`, `spec.md`, and possibly legacy static content.
- **Flask Application Folder (`application/`):**
  - `application/__init__.py`: Initializes the Flask app and database connection.
  - `application/routes.py` (or organized with Blueprints): Contains view functions for dynamic content.
  - `application/db.py` (optional): Encapsulates database connection logic (using sqlite3 or Flask-SQLAlchemy).
  - `application/templates/`: Jinja2 templates (including a common `base.html` layout).
  - `application/static/`: Contains static assets (CSS, JavaScript, images).
- **Legacy Static Content:**
  - Files in `/archive` remain fully static and are served directly.
  - Other static files (if necessary) can be integrated or referenced in Flask templates.

## Data Handling
- **Database Initialization & Population:**
  - Utilize `scripts/populate_db.py` to build and update `blog.db` and output a text-based SQL dump (`blog.sql`) for versioning.
- **Dynamic Content:**
  - Blog posts and recipes are rendered dynamically by querying `blog.db`.
  - URL routing (using slugs) maps specific paths (e.g., `/blog/<slug>`, `/recipes/<slug>`) to their corresponding database entries.
- **Static Content Integration:**
  - Certain pages (e.g., homepage, about, contact) that rely on legacy static HTML can be incorporated into the Flask templating system for consistent layout.
  - The `/archive` directory remains unmodified and is served as static files.

## Error Handling Strategy
- **Data Retrieval Errors:**
  - Routes must check for missing database entries, returning HTTP 404 responses if no matching post is found.
- **Template Rendering Errors:**
  - Use Flask's error handlers (for 404, 500, etc.) to display user-friendly error messages.
- **RSS & External Data:**
  - If the RSS file or external data is missing (as noted in earlier populate_db runs), log the error and provide fallback behavior.
- **Logging:**
  - Implement logging (using Flask’s built-in logging or Python’s logging module) for systematic error and access logging.

## Implementation Roadmap
1. **Set Up the Flask Application:**
   - Create the `app/` directory with subfolders for templates and static files.
   - Initialize a basic Flask app in `app/__init__.py`.
   - Define routing functions in `app/routes.py` to handle dynamic requests (e.g., blog posts, recipes).

2. **Migrate Static Files & Templates:**
   - Convert key static HTML pages (e.g., `public_html/index.html`, `public_html/blog/index.html`, `public_html/recipes/index.html`) into Jinja2 templates inside `app/templates/`.
   - Ensure common layout elements (header, footer, navigation) are moved into a base template (`base.html`).
   - Move CSS, JavaScript, and image assets into `app/static/`.

3. **Database Integration:**
   - Ensure `blog.db` is connected to the Flask app, allowing queries to fetch and render dynamic content.
   - Use `scripts/populate_db.py` to seed/update the database and generate `blog.sql`.

4. **Routing & URL Structure:**
   - Maintain URL consistency (e.g., `/blog/<slug>`, `/recipes/<slug>`).
   - Implement additional routes for the homepage and semi-static content.
   - Configure Flask to serve the `/archive` directory directly as static content, if desired.

5. **Testing & Incremental Integration:**
   - Begin with a few dynamic routes and test them thoroughly.
   - Validate that static content (e.g., from `/archive`) is served correctly.
   - Proceed incrementally, ensuring backward compatibility with internal links and SEO considerations.

6. **Deployment & Continuous Integration:**
   - Update project documentation (e.g., README, spec.md) to reflect new architecture.
   - Adjust deployment scripts/configuration to run the Flask app instead of serving static files.
   - Ensure version control includes migration steps and database dump updates.

## Additional Considerations
- **Deprecation of Legacy Code:**
  - Plan for phasing out unused static content from `public_html` that has been migrated to dynamic routes.
- **Developer Workflow:**
  - Provide clear instructions for setting up the development environment (e.g., creating virtual environments, running `uv run application`, etc.).
- **Future Enhancements:**
  - Consider adding Flask extensions for security, caching, and potentially an ORM (if not using raw SQLite).
  - Explore automated testing strategies for both the database interactions and dynamic page rendering.

This specification should provide a comprehensive outline for any developer to begin implementing the migration to a dynamic Flask-driven site powered by `blog.db`, while preserving necessary static content.
