# Tristan Havelick's Blog

* Clone: `git clone https://github.com/thavelick/thavelick.github.io.git`
* Install deps: `uv sync`
* Init DB: `uv run flask --app application init-db`
* Populate DB: `uv run scripts/populate_db.py --rebuild-db`
* Run app: `uv run flask --app application run --debug`
* Run tests: `uv run python -m unittest`
* Generate static files: `uv run python application/freeze.py`
* Deployment: Automatic via GitHub Actions on push


