import pytest
import sys
from unittest.mock import patch, MagicMock
from src.main import main
from src.crawler import Document

def test_main_build(mocker):
    mocker.patch('sys.argv', ['main.py', 'build', '--max-pages', '1', '--delay', '0.1'])
    
    mock_docs = [
        Document(doc_id=1, text="Test text", author="Author", tags=["tag"], url="url")
    ]
    
    mock_crawl = mocker.patch('src.main.crawl_quotes', return_value=mock_docs)
    mock_save = mocker.patch('src.main.save_index')
    
    # We should also capture stdout if needed, but for coverage running it is enough
    main()
    
    mock_crawl.assert_called_once_with(max_pages=1, politeness_delay=0.1)
    mock_save.assert_called_once()

def test_main_build_failure(mocker, capsys):
    mocker.patch('sys.argv', ['main.py', 'build'])
    mocker.patch('src.main.crawl_quotes', return_value=[])
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code == 1

def test_main_load(mocker):
    mocker.patch('sys.argv', ['main.py', 'load'])
    mock_load = mocker.patch('src.main.load_index', return_value={"inverted_index": {}})
    
    main()
    mock_load.assert_called_once()

def test_main_load_failure(mocker):
    mocker.patch('sys.argv', ['main.py', 'load'])
    mocker.patch('src.main.load_index', return_value=None)
    
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1

def test_main_print(mocker):
    mocker.patch('sys.argv', ['main.py', 'print'])
    mocker.patch('src.main.load_index', return_value={"total_docs": 5, "inverted_index": {}})
    
    main()

def test_main_print_failure(mocker):
    mocker.patch('sys.argv', ['main.py', 'print'])
    mocker.patch('src.main.load_index', return_value=None)
    
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1

def test_main_find(mocker):
    mocker.patch('sys.argv', ['main.py', 'find', 'test', 'query'])
    
    mock_data = {
        "inverted_index": {"test": {"1": [0]}},
        "doc_lengths": {"1": 1},
        "documents": {"1": {"doc_id":1, "text":"test query", "author":"A", "tags":[], "url":""}},
        "total_docs": 1
    }
    
    mocker.patch('src.main.load_index', return_value=mock_data)
    mock_search = mocker.patch('src.search.SearchEngine.search', return_value=[(1.0, mock_data["documents"]["1"])])
    
    main()
    mock_search.assert_called_once_with("test query")

def test_main_find_no_results(mocker):
    mocker.patch('sys.argv', ['main.py', 'find', 'none'])
    
    mock_data = {
        "inverted_index": {},
        "doc_lengths": {},
        "documents": {},
        "total_docs": 0
    }
    mocker.patch('src.main.load_index', return_value=mock_data)
    
    main()

def test_main_find_failure(mocker):
    mocker.patch('sys.argv', ['main.py', 'find', 'query'])
    mocker.patch('src.main.load_index', return_value=None)
    
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1
    
def test_main_find_empty_query(mocker):
    mocker.patch('sys.argv', ['main.py', 'find', '   '])
    
    with pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 1

def test_main_help(mocker, capsys):
    mocker.patch('sys.argv', ['main.py'])
    
    main()
