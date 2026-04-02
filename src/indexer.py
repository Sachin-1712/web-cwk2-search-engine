import re
from typing import List, Dict, Set
from collections import defaultdict

def tokenize(text: str) -> List[str]:
    """
    Lowercases the text, removes punctuation, and splits on whitespace.
    """
    text = text.lower()
    # Remove all non-alphanumeric characters except whitespace
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens

class Indexer:
    def __init__(self):
        # term -> { doc_id: [pos1, pos2, ...] }
        self.inverted_index: Dict[str, Dict[int, List[int]]] = defaultdict(lambda: defaultdict(list))
        # doc_id -> token count
        self.doc_lengths: Dict[int, int] = {}
        # Keep original docs for retrieval
        self.documents: Dict[int, dict] = {}
        
    def build_index(self, docs: List[dict]):
        """
        Builds the inverted index from a list of document dictionaries.
        """
        for doc in docs:
            doc_id = doc['doc_id']
            self.documents[doc_id] = doc
            
            # Combine text, author, and tags for indexing
            # Note: Positions will treat this as a single continuous text
            content = f"{doc['text']} {doc['author']} {' '.join(doc['tags'])}"
            tokens = tokenize(content)
            
            self.doc_lengths[doc_id] = len(tokens)
            
            for pos, token in enumerate(tokens):
                self.inverted_index[token][doc_id].append(pos)

    def get_index_data(self) -> dict:
        """
        Returns a dictionary representation of the index components for persistence.
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
        Loads the index from a dictionary representation.
        """
        self.inverted_index = defaultdict(lambda: defaultdict(list))
        for term, doc_postings in data.get("inverted_index", {}).items():
            int_postings = {int(doc_id): positions for doc_id, positions in doc_postings.items()}
            self.inverted_index[term] = defaultdict(list, int_postings)
            
        self.doc_lengths = {int(k): v for k, v in data.get("doc_lengths", {}).items()}
        self.documents = {int(k): v for k, v in data.get("documents", {}).items()}
