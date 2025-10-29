# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask-based personal blog and website that generates static HTML files for GitHub Pages deployment. Content is stored in a SQLite database and rendered through Jinja2 templates.

## Development Commands

- Install dependencies: `make deps` (uses uv)
- Initialize database: `make init-db`
- Restore database from backup: `make restore-db` (restores from blog.sql)
- Run development server: `make dev` (Flask debug mode)
- Run unit tests: `make test-unit`
- Run integration tests: `make test-integration`
- Generate static site: `make freeze` (outputs to public_html/)

## Architecture

### Key Components

- **application/__init__.py**: Flask app factory and route definitions. Uses a catchall route pattern that first checks for posts by slug, then falls back to static files.
- **application/models.py**: Post and Category models using raw SQL queries (no ORM).
- **application/db.py**: SQLite database connection management with Flask g context.
- **application/freeze.py**: Flask-Frozen configuration that generates static HTML from Flask routes. Registers generators for all posts and static archive files.
- **application/templates/**: Jinja2 templates. base.html is the parent template.

### Directory Structure

- `application/templates/`: Source HTML templates (work on these)
- `public_html/`: Generated static output (do not edit directly)
- `instance/blog.db`: SQLite database (gitignored)
- `blog.sql`: Database backup for restoration

### Content Flow

1. Content stored in SQLite database (posts table with slug, markdown_content, publish_date)
2. Flask routes query database via Post/Category models
3. Templates render content during development or static generation
4. `make freeze` generates complete static site to public_html/
5. GitHub Actions deploys public_html/ on push

### URL Routing

Routes follow this priority:
1. Explicit routes (/blog/, /recipes/, /books/, etc.)
2. Post slugs via catchall route (e.g., /welcome/ → post with slug "welcome")
3. Static files from application/static/

## Testing

- Unit tests: Test routes and basic functionality
- Integration tests: Test generated static HTML in public_html/
