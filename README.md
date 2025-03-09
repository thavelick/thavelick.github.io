# Tristan Havelick's Blog

This project is a Flask web application. The repository is hosted at [https://github.com/thavelick/thavelick.github.io/tree/main](https://github.com/thavelick/thavelick.github.io/tree/main).

## Local Development Setup

### Clone the Repository

Clone the repository from GitHub:

```bash
git clone https://github.com/thavelick/thavelick.github.io.git
cd thavelick.github.io
```

### Install Dependencies

Install dependencies with `uv sync`:

```bash
uv sync
```

### Database Setup

To create an empty database, run:

```bash
uv run flask --app application init-db
```

To populate (or rebuild) the database from html in public_html run:

```bash
uv run scripts/populate_db.py --rebuild-db
```

### Running the Application

Run the Flask application in debug mode using uvicorn:

```bash
uv run flask --app application run --debug
```

### Deployment

Deployment happens automatically with GitHub Actions. Simply push your changes to the repository and the deployment pipeline will handle updates.

Enjoy developing and testing your site locally!
