import pytest
from src.indexer import Indexer, tokenize

def test_tokenize():
    text = "Hello, World! This is a Test-String... 123"
    tokens = tokenize(text)
    assert tokens == ["hello", "world", "this", "is", "a", "teststring", "123"]

def test_build_index(sample_documents):
    indexer = Indexer()
    # Convert Document objects to dicts as expected by Indexer
    docs = [doc.to_dict() for doc in sample_documents]
    indexer.build_index(docs)
    
    # Check document lengths
    assert len(indexer.doc_lengths) == 3
    
    # Check if words are indexed
    assert "albert" in indexer.inverted_index
    assert "choices" in indexer.inverted_index
    assert "shakespeare" in indexer.inverted_index
    
    # Check positional tracking for "to be or not to be"
    # Document 3: "To be or not to be, that is the question." Author: William Shakespeare Tags: existential
    # tokenized: ["to", "be", "or", "not", "to", "be", "that", "is", "the", "question", "william", "shakespeare", "existential"]
    doc3_to_positions = indexer.inverted_index["to"][3]
    assert doc3_to_positions == [0, 4]
    
    doc3_be_positions = indexer.inverted_index["be"][3]
    assert doc3_be_positions == [1, 5]

def test_get_load_index_data(sample_documents):
    indexer = Indexer()
    docs = [doc.to_dict() for doc in sample_documents]
    indexer.build_index(docs)
    
    data = indexer.get_index_data()
    
    assert "inverted_index" in data
    assert "doc_lengths" in data
    assert "documents" in data
    assert data["total_docs"] == 3
    
    new_indexer = Indexer()
    new_indexer.load_index_data(data)
    
    assert new_indexer.doc_lengths == indexer.doc_lengths
    assert "albert" in new_indexer.inverted_index
    # Note: dictionary keys in JSON become strings, so doc_id 3 becomes '3' internally if serialized/deserialized via json,
    # but load_index_data casts keys back to int!
    assert 3 in new_indexer.inverted_index["to"]
