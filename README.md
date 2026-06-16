# dev-utils

A collection of small CLI scripts and utilities I kept rewriting from scratch. Decided to just keep them in one place.

Nothing groundbreaking — just stuff I actually use.

## what's in here

### `clean-branches.sh`
Deletes all local git branches that have already been merged into main.

```bash
./clean-branches.sh
# → deleted: feature/login-page
# → deleted: fix/navbar-overflow
# → kept: main, dev
```

### `env-check.py`
Scans a project directory and reports any `.env` variables referenced in code that aren't defined in `.env.example`. Helps avoid "works on my machine" issues.

```bash
python env-check.py ./my-project
# Missing from .env.example:
#   STRIPE_WEBHOOK_SECRET (found in server/routes/billing.js)
#   REDIS_URL (found in server/cache.js)
```

### `screenshot-pdf.py`
Takes a list of URLs and exports a PDF with screenshots of each page. Useful for quick design reviews.

```bash
python screenshot-pdf.py urls.txt output.pdf
```

### `rename-batch.py`
Bulk renames files in a directory using a pattern. Supports regex.

```bash
python rename-batch.py ./photos "IMG_(\d+)" "photo_\1"
# IMG_001.jpg → photo_001.jpg
# IMG_002.jpg → photo_002.jpg
```

## install / use

No package needed. Just clone and run the scripts directly:

```bash
git clone https://github.com/Nhdez777/dev-utils.git
cd dev-utils

# Python scripts — need Python 3.10+
pip install -r requirements.txt

# Shell scripts — make executable first
chmod +x clean-branches.sh
```

## adding more

I'll keep adding things here as I build them. If something feels like I've written it three times before, it goes in here.
