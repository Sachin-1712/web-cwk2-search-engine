import re
from typing import List, Dict, Set
from collections import defaultdict

def tokenize(text: str) -> List[str]:
    """
    Normalize text into lowercase word tokens for consistent indexing/search.
    """
    text = text.lower()
    # Remove all non-alphanumeric characters except whitespace
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens

class Indexer:
    """Builds and reloads the positional inverted index used by search."""

    def __init__(self):
        # term -> { doc_id: [pos1, pos2, ...] }
        self.inverted_index: Dict[str, Dict[int, List[int]]] = defaultdict(lambda: defaultdict(list))
        # doc_id -> token count
        self.doc_lengths: Dict[int, int] = {}
        # Keep original docs for retrieval
        self.documents: Dict[int, dict] = {}
        
    def build_index(self, docs: List[dict]):
        """
        Build postings lists where each term maps to document IDs and positions.
        """
        for doc in docs:
            doc_id = doc['doc_id']
            self.documents[doc_id] = doc
            
            # Treat quote text, author, and tags as one searchable document.
            content = f"{doc['text']} {doc['author']} {' '.join(doc['tags'])}"
            tokens = tokenize(content)
            
            self.doc_lengths[doc_id] = len(tokens)
            
            for pos, token in enumerate(tokens):
                self.inverted_index[token][doc_id].append(pos)

    def get_index_data(self) -> dict:
        """
        Return JSON-serializable index components for persistence.
        """
        # Convert defaultdicts to regular dicts for JSON serialization
        inverted_index_dict = {
            term: dict(doc_postings) 
            for term, doc_postings in self.inverted_index.items()
        }
        
        return {
            "inverted_index": inverted_index_dict,
            "doc_lengths": self.doc_lengths,
            "documents": self.documents,
            "total_docs": len(self.documents)
        }
        
    def load_index_data(self, data: dict):
        """
        Restore persisted index data and convert JSON string keys back to ints.
        """
        self.inverted_index = defaultdict(lambda: defaultdict(list))
        for term, doc_postings in data.get("inverted_index", {}).items():
            int_postings = {int(doc_id): positions for doc_id, positions in doc_postings.items()}
            self.inverted_index[term] = defaultdict(list, int_postings)
            
        self.doc_lengths = {int(k): v for k, v in data.get("doc_lengths", {}).items()}
        self.documents = {int(k): v for k, v in data.get("documents", {}).items()}
