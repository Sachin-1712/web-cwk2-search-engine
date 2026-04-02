PRD.md

COMP3011 Coursework 2 — Mini Search Engine CLI

Project Name

Search Engine Tool for quotes.toscrape.com

⸻

1. Project Overview

This project implements a command-line search engine in Python that:
	1.	Crawls pages from a target website
	2.	Builds an inverted index with statistics
	3.	Stores and reloads the index
	4.	Supports single-word and multi-word search queries
	5.	Provides structured CLI commands for interaction

Target website:

https://quotes.toscrape.com/

The system demonstrates understanding of:
	•	web crawling
	•	indexing pipelines
	•	inverted index structures
	•	query retrieval algorithms
	•	persistence
	•	testing strategies
	•	CLI interface design

Primary assessment deliverables:
	•	working implementation
	•	GitHub repository
	•	compiled index file
	•	5-minute demonstration video

⸻

2. Objectives

Build a modular Python search engine pipeline:

crawl → tokenize → normalize → index → store → query

System must:
	•	respect 6-second politeness window
	•	build inverted index with statistics
	•	support CLI commands
	•	include automated tests
	•	be demonstration-ready
	•	follow clean architecture practices

⸻

3. Target Users

Primary:
	•	coursework marker
	•	instructor reviewing implementation

Secondary:
	•	student developer demonstrating system

⸻

4. Functional Requirements

FR1 — Web Crawler

Crawler must:
	•	start from homepage
	•	follow pagination links
	•	avoid revisiting pages
	•	extract quotes text
	•	extract author names
	•	extract tags
	•	handle HTTP errors
	•	respect politeness delay ≥ 6 seconds

Crawler stops when no next page exists.

Example crawl flow:

page/1
page/2
page/3
...


⸻

FR2 — Text Processing Pipeline

Each page undergoes:

HTML → text extraction → tokenization → normalization → indexing

Normalization rules:
	•	lowercase conversion
	•	punctuation removal
	•	whitespace splitting
	•	empty-token filtering

Optional enhancement:
	•	stopword removal

⸻

FR3 — Inverted Index Construction

Index structure:

word → page → statistics

Statistics required:
	•	frequency
	•	positions

Example:

{
  "life": {
    "/page/1/": {
      "frequency": 2,
      "positions": [3, 19]
    }
  }
}

Supports efficient retrieval and ranking.

⸻

FR4 — Index Persistence

build command

crawl website
build inverted index
save index.json

load command

read index.json
restore index

Persistence format:

JSON


⸻

FR5 — Query Engine

print command

Input:

print nonsense

Output:

Word: nonsense
Pages:
 /page/2/
 /page/5/
Frequency:
 ...


⸻

find command

Single word:

find life

Multi-word:

find good friends

Returns:

pages containing ALL query terms

Implementation:

set intersection

Optional ranking:

sort by frequency score

⸻

FR6 — Edge Case Handling

Must handle:

Case	Behaviour
empty query	error message
unknown word	return empty result
index not loaded	prompt user
network failure	retry or skip
duplicate pages	ignore


⸻

5. Non-Functional Requirements

Performance

Crawler delay:

≥ 6 seconds/request

Index lookup:

O(1)

Search complexity:

O(n intersections)


⸻

Code Quality

Must include:
	•	modular structure
	•	docstrings
	•	type hints
	•	defensive programming
	•	logging
	•	error handling

⸻

6. CLI Specification

Example session:

> build
Index built successfully.

> load
Index loaded successfully.

> print life
Word occurs in:
 /page/1/
 /page/4/

> find life love
Matching pages:
 /page/2/


⸻

7. Repository Architecture

search-engine-tool/
│
├── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   ├── storage.py
│   └── main.py
│
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│
├── data/
│   └── index.json
│
├── requirements.txt
├── README.md
└── PRD.md


⸻

8. Module Responsibilities

crawler.py

Responsibilities:

fetch pages
extract links
extract text
respect politeness window

Functions:

crawl()
extract_links()
extract_quotes()


⸻

indexer.py

Responsibilities:

tokenization
normalization
frequency tracking
position tracking

Functions:

tokenize()
build_index()
update_index()


⸻

storage.py

Responsibilities:

save index
load index

Functions:

save_index()
load_index()


⸻

search.py

Responsibilities:

lookup words
intersect postings
rank results

Functions:

print_word()
find_query()


⸻

main.py

Responsibilities:

CLI interface
command routing
state management


⸻

9. Data Model Specification

Index dictionary format:

Dict[
  word,
  Dict[
    page,
    Dict[
      frequency,
      positions
    ]
  ]
]

Example:

index[word][page]["frequency"]
index[word][page]["positions"]


⸻

10. Algorithms

Crawl Algorithm

visited = set()
queue = [start_url]

while queue not empty:
    url = pop
    request page
    parse content
    extract text
    extract next link
    wait 6 seconds


⸻

Index Algorithm

for word in tokens:
    if word not index:
        create entry
    update frequency
    append position


⸻

Query Algorithm

Single word:

return index[word]

Multi-word:

pages = intersect(
    index[word1],
    index[word2],
    ...
)


⸻

11. Testing Plan

Coverage target:

≥ 80%

Unit tests:

test_tokenizer()
test_index_update()
test_save_load()
test_single_word_search()
test_multi_word_search()
test_missing_word()
test_empty_query()

Integration tests:

crawl → index → search pipeline

Mock tests:

mock requests.get


⸻

12. Git Workflow Plan

Recommended commits:

init project structure
implement crawler
implement tokenizer
implement indexer
implement persistence
implement CLI
implement search logic
add tests
add README
final polish


⸻

13. README Requirements

Must include:

project overview
installation steps
usage examples
command descriptions
testing instructions
dependencies
architecture diagram


⸻

14. Distinction-Level Extensions (80–100 Band)

Implement advanced features:

TF-IDF Ranking

Rank pages using:

TF-IDF(term, document)

Improves relevance scoring.

⸻

Boolean Search Support

Allow:

find life AND love
find life OR hope
find life NOT death


⸻

Phrase Matching

Example:

find "good friends"

Use positional index matching.

⸻

Query Suggestions

Implement:

did you mean: friendship?

Use:
	•	prefix matching
	•	edit distance

⸻

Index Compression

Optional:

delta encoding
gap encoding

Reduce memory footprint.

⸻

Performance Benchmarking

Measure:

crawl time
index build time
query latency
memory usage

Display statistics in CLI.

⸻

Retry Logic

Handle network failures:

retry 3 times
fallback skip page


⸻

Stopword Filtering

Ignore words like:

the
is
and
of


⸻

CLI Help Command

Provide:

help

Outputs usage instructions.

⸻

15. Video Demonstration Plan

Structure:

0–2 minutes

Run:

build
load
print
find


⸻

2–3.5 minutes

Explain:

crawler design
index structure
search algorithm


⸻

3.5–4 minutes

Run tests

⸻

4–4.5 minutes

Show git history

⸻

4.5–5 minutes

GenAI reflection

⸻

Add distinction-level extensions:

- TF-IDF ranking
- Boolean queries
- phrase queries
- query suggestions
- stopword filtering
- benchmarking utilities
- retry logic
- CLI help command

Ensure clean modular architecture, docstrings, logging, type hints, and coursework-ready documentation.

