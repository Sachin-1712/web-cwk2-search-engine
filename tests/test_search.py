import pytest
from src.indexer import Indexer
from src.search import SearchEngine

@pytest.fixture
def mock_search_engine(sample_documents):
    indexer = Indexer()
    docs = [doc.to_dict() for doc in sample_documents]
    indexer.build_index(docs)
    return SearchEngine(indexer)

def test_intersection_match(mock_search_engine):
    # "thinking" appears in doc_id=1
    # "world" appears in doc_id=1
    results = mock_search_engine.search("thinking world")
    
    assert len(results) == 1
    score, doc = results[0]
    assert doc["doc_id"] == 1
    assert score > 0

def test_no_results(mock_search_engine):
    results = mock_search_engine.search("supercalifragilisticexpialidocious")
    assert len(results) == 0

def test_phrase_match(mock_search_engine):
    # This phrase should only match doc 3
    results = mock_search_engine.search('"to be or not to be"')
    assert len(results) == 1
    assert results[0][1]["doc_id"] == 3
    
    # "be to" doesn't exist in that exact sequence
    results2 = mock_search_engine.search('"be to"')
    assert len(results2) == 0
    
def test_phrase_match_edge_cases(mock_search_engine):
    # Single word phrase query should behave like a normal search
    results = mock_search_engine.search('"thinking"')
    assert len(results) == 1
    assert results[0][1]["doc_id"] == 1
    
    # Phrase query where individual words exist but never in that sequence
    results2 = mock_search_engine.search('"world thinking"')
    assert len(results2) == 0

def test_ranking_logic(mock_search_engine):
    # "our" is in doc 1 (two times) and doc 2 (two times)
    # let's see which gets ranked higher
    results = mock_search_engine.search("our")
    assert len(results) == 2
    
    # "our" appears twice in both, but doc 2 is shorter
    doc1 = results[0][1] if results[0][1]["doc_id"] == 1 else results[1][1]
    doc2 = results[0][1] if results[0][1]["doc_id"] == 2 else results[1][1]
    
    score1 = [score for score, doc in results if doc["doc_id"] == 1][0]
    score2 = [score for score, doc in results if doc["doc_id"] == 2][0]
    
    # TF is frequency / doc_length. Doc 2 is shorter, so it should rank higher for the same frequency.
    assert score2 > score1

def test_empty_query(mock_search_engine):
    assert mock_search_engine.search("") == []
    assert mock_search_engine.search("   ") == []
    assert mock_search_engine.search('""') == []
