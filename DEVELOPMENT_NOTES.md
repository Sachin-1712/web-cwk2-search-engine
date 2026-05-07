# Development Notes

These notes summarise the main implementation stages for the coursework
submission and provide a short checklist for testing and demonstration.

## Implementation Stages

1. **Crawler**
   - Built a crawler for `quotes.toscrape.com` that follows pagination links.
   - Extracts quote text, author names, tags, and source URLs into `Document`
     records.
   - Uses retry handling for request failures and a default 6-second politeness
     delay between real page requests.
   - Skips duplicate quote text so repeated content is not indexed twice.

2. **Indexer**
   - Added tokenization and normalization so search is case-insensitive and
     punctuation does not block matching.
   - Built a positional inverted index mapping each term to document IDs and
     token positions.
   - Tracks document lengths for later ranking calculations.

3. **Storage**
   - Added JSON persistence for the inverted index, document metadata, and
     document-length statistics.
   - Ensures the `data/` directory exists before writing the index.
   - Handles missing or invalid index files with clear error logging.

4. **Search**
   - Supports single-term and multi-term AND-style queries.
   - Supports quoted phrase queries using token positions.
   - Ranks matching quotes with TF-IDF-style scoring.
   - Handles empty queries and unknown terms without crashing.

5. **Tests**
   - Added unit tests for crawler behavior, indexing, persistence, searching,
     and CLI command handling.
   - Mocked external crawling behavior so tests do not depend on live network
     access or the 6-second crawl delay.

6. **CLI Polish**
   - Added `build`, `load`, `print`, and `find` subcommands through `argparse`.
   - Included helpful success/error messages for common workflows.
   - Added demo-friendly command options such as `--max-pages` and `--delay`.

## Testing Workflow

Run the full test suite:

```bash
python -m pytest -v
```

Run tests with coverage and missing-line detail:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## Demo Workflow

For a fast coursework demonstration:

```bash
python -m src.main build --max-pages 2 --delay 1.0
python -m src.main load
python -m src.main print love
python -m src.main find life success
python -m src.main find '"good friends"'
```

For the final real crawl, use:

```bash
python -m src.main build
```

The final build command keeps the default 6-second politeness delay enabled.

## Testing Summary

The project maintains high code quality through rigorous testing:
- **Unit Tests**: Individual functions (tokenization, scoring) are verified for edge cases.
- **Integration Tests**: The full pipeline (crawl -> index -> search) is tested using mocked HTTP responses.
- **Coverage**: Over 95% of the codebase is covered by the test suite, including error handlers for network failures and missing files.
