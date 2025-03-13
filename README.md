# Tristan Havelick's Blog

* Clone: `git clone https://github.com/thavelick/thavelick.github.io.git`
* cd: `cd thavelick.github.io`
* Install deps: `uv sync`
* Init DB: `uv run flask --app application init-db`
* Populate DB: `uv run scripts/populate_db.py --rebuild-db`
* Run app: `uv run flask --app application run --debug`
* Run tests: `uv run python -m unittest`
* Deployment: Automatic via GitHub Actions on push


