# Python CLI Search Engine

Modular Python CLI search engine for quotes.toscrape.com.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
# Build the index (crawls quotes.toscrape.com, polite delay of 6s per page)
python -m src.main build

# Load the index into memory (just to check if it's there)
python -m src.main load

# Print stats / inverted index sample
python -m src.main print

# Find a multi-word intersection query
python -m src.main find life is

# Find an exact phrase query using quotes
python -m src.main find '"to be or not to be"'
```

## Testing

Run tests with coverage:
```bash
pytest tests/ --cov=src
```
