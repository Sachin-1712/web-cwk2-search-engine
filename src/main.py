import argparse
import sys
import logging
from src.crawler import crawl_quotes
from src.indexer import Indexer
from src.storage import save_index, load_index
from src.search import SearchEngine

def main():
    parser = argparse.ArgumentParser(description="Modular CLI Search Engine for quotes.toscrape.com")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # build command
    build_parser = subparsers.add_parser("build", help="Crawl the site, build the inverted index, and save to disk")
    build_parser.add_argument("--max-pages", type=int, default=None, help="Maximum number of pages to crawl (for testing purposes)")
    build_parser.add_argument("--delay", type=float, default=6.0, help="Politeness delay in seconds between requests")
    
    # load command
    load_parser = subparsers.add_parser("load", help="Load the saved index from disk into memory")
    
    # print command
    print_parser = subparsers.add_parser("print", help="Load the index and print structural statistics or info about a specific word")
    print_parser.add_argument("word", nargs="?", default=None, help="The word to look up in the index")
    
    # find command
    find_parser = subparsers.add_parser("find", help="Execute a search query against the index")
    find_parser.add_argument("query", nargs="+", help="The query terms. To match an exact phrase, use double quotes, e.g. '\"to be\"'")
    
    args = parser.parse_args()
    
    if args.command == "build":
        print(f"Starting build process (delay={args.delay}s, max_pages={args.max_pages})...")
        docs = crawl_quotes(max_pages=args.max_pages, politeness_delay=args.delay)
        
        if not docs:
            print("[ERROR] Failed to crawl any documents.")
            sys.exit(1)
            
        print(f"\n[SUCCESS] Scraped {len(docs)} unique quotes.")
        print("Building inverted index...")
        indexer = Indexer()
        # Convert objects to dicts for indexer
        indexer.build_index([doc.to_dict() for doc in docs])
        
        save_index(indexer.get_index_data())
        print("[SUCCESS] Build complete. Index is ready for searching.")
        
    elif args.command == "load":
        data = load_index()
        if not data:
            print("[ERROR] Index could not be loaded.")
            sys.exit(1)
        indexer = Indexer()
        indexer.load_index_data(data)
        print("[SUCCESS] Index successfully loaded into memory.")
        
    elif args.command == "print":
        data = load_index()
        if not data:
            print("[ERROR] Failed to load index data.")
            sys.exit(1)
        if args.word:
            word = args.word.lower()
            inverted = data.get('inverted_index', {})
            if word in inverted:
                postings = inverted[word]
                num_docs = len(postings)
                print(f"\n--- Postings for word: '{word}' ---")
                print(f"Found in {num_docs} document(s):\n")
                
                # Sorting by doc_id (they might be strings in the JSON)
                sorted_doc_ids = sorted(postings.keys(), key=lambda x: int(x))
                
                for d_id in sorted_doc_ids:
                    positions = postings[d_id]
                    freq = len(positions)
                    print(f"  - Document ID: {d_id}")
                    print(f"    Frequency:   {freq}")
                    print(f"    Positions:   {', '.join(map(str, positions))}")
                print("-" * (26 + len(word)))
            else:
                print(f"[INFO] Word '{word}' not found in the index.")
        else:
            print(f"\n--- Index Statistics ---")
            print(f"Total Documents:           {data.get('total_docs', 0)}")
            print(f"Total Terms in Vocabulary: {len(data.get('inverted_index', {}))}")
            print("-" * 24)
        
    elif args.command == "find":
        query_string = " ".join(args.query)
        
        # Determine if it was passed with quotes via shell argument
        # E.g. find '"to be"' -> args.query is ['"to be"']
        if not query_string.strip():
            print("Please provide a search query.")
            sys.exit(1)
            
        data = load_index()
        if not data:
            sys.exit(1)
            
        indexer = Indexer()
        indexer.load_index_data(data)
        
        search_engine = SearchEngine(indexer)
        print(f"--- Searching for: {query_string} ---\n")
        
        results = search_engine.search(query_string)
        
        if not results:
            print(f"[INFO] No matching quotes found for '{query_string}'.")
        else:
            print(f"[SUCCESS] Found {len(results)} matching quote(s):\n")
            for rank, (score, doc) in enumerate(results, 1):
                print(f"{rank}. [Score: {score:.4f}]")
                print(f"   \"{doc['text']}\"")
                print(f"   - {doc['author']}")
                print(f"   Tags: {', '.join(doc['tags'])}")
                print(f"   URL:  {doc['url']}\n")
                
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
