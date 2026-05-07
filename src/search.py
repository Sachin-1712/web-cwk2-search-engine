import math
import shlex
from typing import List, Dict, Tuple, Set
from src.indexer import Indexer, tokenize

class SearchEngine:
    """Runs query matching and TF-IDF ranking over an Indexer instance."""

    def __init__(self, indexer: Indexer):
        self.indexer = indexer
        
    def search(self, query_string: str) -> List[Tuple[float, dict]]:
        """
        Execute a query and return ranked ``(score, document)`` results.

        Quoted input uses phrase matching; unquoted input uses AND-style
        intersection so every query term must appear in each result.
        """
        if not query_string.strip():
            return []
            
        # A phrase query is deliberately simple for the CLI: one quoted phrase.
        is_phrase_query = query_string.startswith('"') and query_string.endswith('"')
        
        if is_phrase_query:
            clean_query = query_string[1:-1]
            tokens = tokenize(clean_query)
            if not tokens:
                return []
            result_doc_ids = self._phrase_match(tokens)
        else:
            tokens = tokenize(query_string)
            if not tokens:
                return []
            result_doc_ids = self._intersection_match(tokens)
            
        if not result_doc_ids:
            return []
            
        # Rank matching documents using normalized term frequency and smoothed IDF.
        # This ensures shorter quotes with frequent terms are ranked higher.
        ranked_results = []
        total_docs = len(self.indexer.documents)
        
        for doc_id in result_doc_ids:
            score = 0.0
            doc_length = self.indexer.doc_lengths.get(doc_id, 1) # Prevent division by zero
            
            for token in tokens:
                # Number of times token appears in this doc
                tf_raw = len(self.indexer.inverted_index.get(token, {}).get(doc_id, []))
                tf = tf_raw / doc_length
                
                # Document frequency: number of docs containing this token
                df = len(self.indexer.inverted_index.get(token, {}))
                idf = math.log((total_docs) / (df + 1)) + 1 # Smoothing
                
                score += tf * idf
                
            ranked_results.append((score, self.indexer.documents[doc_id]))
            
        # Sort descending by score
        ranked_results.sort(key=lambda x: x[0], reverse=True)
        return ranked_results

    def _intersection_match(self, tokens: List[str]) -> Set[int]:
        """
        Return document IDs that contain ALL the given tokens (AND logic).
        """
        result_docs = None
        for token in tokens:
            # Get set of docs containing this token
            docs_with_token = set(self.indexer.inverted_index.get(token, {}).keys())
            
            if result_docs is None:
                result_docs = docs_with_token
            else:
                result_docs = result_docs.intersection(docs_with_token)
                
            if not result_docs:
                break # Early exit if intersection is empty
                
        return result_docs if result_docs is not None else set()

    def _phrase_match(self, tokens: List[str]) -> Set[int]:
        """
        Return document IDs containing the exact token sequence.
        """
        # First, ensure all tokens exist in the document
        candidate_docs = self._intersection_match(tokens)
        if not candidate_docs:
            return set()
            
        if len(tokens) == 1:
            return candidate_docs
            
        valid_docs = set()
        
        for doc_id in candidate_docs:
            # Check positions for exact sequence
            # positions_list is a list of position lists: [[pos_t1], [pos_t2], ...]
            positions_list = [self.indexer.inverted_index[token][doc_id] for token in tokens]
            
            # Positional check: token i must appear at start position + i.
            for pos in positions_list[0]:
                is_match = True
                for i in range(1, len(tokens)):
                    # Check if the next token appears exactly one position after the current one
                    if (pos + i) not in positions_list[i]:
                        is_match = False
                        break
                if is_match:
                    valid_docs.add(doc_id)
                    break # One phrase match is enough to include the doc
                    
        return valid_docs
