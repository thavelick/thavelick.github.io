# Tristan Havelick's Blog

* Clone: `git clone https://github.com/thavelick/thavelick.github.io.git`
* Install deps: `make deps`
* Initialize DB: `make init-db`
* Restore DB: `make restore-db`
* Run app in dev: `make dev`
* Run unit tests: `make test-unit`
* Run integration tests: `make test-integration`
* Generate static files: `make freeze`
* Deployment: Automatic via GitHub Actions on push

## Publishing a post

1. Scaffold a draft with prefilled front-matter (title, publish_date, default category): `./scripts/generate_empty_template.py my-new-post`. This writes `drafts/my-new-post.md`. Edit the body (and front-matter if needed):
    ```
    ---
    title: My New Post
    slug: my-new-post
    publish_date: 2026-05-10
    categories: blog
    ---
    Body content here.
    ```
2. Import: `make import` (batch — every `drafts/*.md`) or `make import-one POST=drafts/my-new-post.md` (single file). This UPSERTs into the local SQLite DB, dumps the DB to `blog.sql`, and moves the draft to `drafts-imported/<slug>.<timestamp>.md`.
3. Commit `blog.sql` and push. GitHub Actions handles the freeze and deploy.


