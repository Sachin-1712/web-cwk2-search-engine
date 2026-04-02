# Quote Search Engine

A modular Python CLI search engine for quotes from [quotes.toscrape.com](http://quotes.toscrape.com/). This project implements a web crawler, an inverted indexer, and a ranked search engine.

## Project Overview and Purpose

This project is a CLI-based search engine designed to scrape quotes from a specific website, build a searchable inverted index with TF-IDF ranking, and provide an interface for querying quotes via intersection and exact phrase searches.

The system is composed of several modules:
- **Crawler**: Scrapes quotes from the website with a polite delay and retry logic.
- **Indexer**: Processes the text into an inverted index with term frequency (TF) and inverse document frequency (IDF) for ranking.
- **Storage**: Manages saving and loading the built index to/from the `data/` directory.
- **Search Engine**: Handles user queries, supports simple multiple word queries and exact phrase queries, returning ranked results.

## Dependencies and Installation

### Prerequisites
- Python 3.8+
- [Optional] Virtual environment (recommended)

### Dependencies
The project uses the following libraries:
- `requests`: To fetch web pages.
- `beautifulsoup4`: To parse HTML content.
- `pytest`, `pytest-cov`, `requests-mock`, `pytest-mock`: For testing and coverage.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sachin-1712/web-cwk2-search-engine.git
   cd web-cwk2-search-engine
   ```

2. **Set up a virtual environment (optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

The tool supports four primary commands via the `main.py` entry point. Use `python -m src.main` to run the commands.

### 1. Build the Index (`build`)
Crawls the website, builds the index, and saves it to `data/index.json`.

```bash
# Build with default parameters (6s delay)
python -m src.main build

# Build with a specific limit for testing
python -m src.main build --max-pages 2 --delay 1.0
```

### 2. Load the Index (`load`)
Loads the saved index into memory to verify it's valid.

```bash
python -m src.main load
```

### 3. Print Index Statistics (`print`)
Displays statistics or looks up a specific word.

```bash
# Print general statistics
python -m src.main print

# Print details for a specific word
python -m src.main print love
```

### 4. Find Quotes (`find`)
Search for quotes using multi-word intersection or exact phrase match.

```bash
# Multi-word intersection query
python -m src.main find life success

# Exact phrase query (wrap the phrase in double quotes within the shell argument)
python -m src.main find '"to be or not to be"'
```

## Testing Instructions

The project uses `pytest` for unit testing with coverage tracking.

### Run all tests
```bash
pytest
```

### Run tests with coverage report
```bash
pytest --cov=src tests/
```

The test suite covers:
- Crawling logic with mocked responses.
- Indexing and TF-IDF calculation accuracy.
- Search result ranking and phrase matching.
- JSON storage persistence.

---
**Coursework Repository Structure Compliance:**
- `src/`: Core logic (`crawler.py`, `indexer.py`, `search.py`, `main.py`).
- `tests/`: Unit tests (`test_crawler.py`, `test_indexer.py`, `test_search.py`).
- `data/`: Location for saved index files.
- `requirements.txt`: Project dependencies.
- `README.md`: This file.
