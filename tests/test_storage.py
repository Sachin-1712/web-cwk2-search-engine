import os
import json
from src.storage import save_index, load_index

def test_save_and_load_index(tmp_path):
    # tmp_path is a pytest fixture providing a temporary directory unique to the test invocation
    data = {
        "inverted_index": {
            "test": {
                "1": [0, 5]
            }
        },
        "doc_lengths": {"1": 10},
        "documents": {"1": {"doc_id": 1, "text": "test document"}},
        "total_docs": 1
    }
    
    filepath = tmp_path / "test_index.json"
    
    # Test saving
    save_index(data, filepath=str(filepath))
    assert os.path.exists(filepath)
    
    with open(filepath, "r") as f:
        loaded_raw = json.load(f)
    assert loaded_raw["total_docs"] == 1
    assert "test" in loaded_raw["inverted_index"]
    
    # Test loading
    loaded_data = load_index(filepath=str(filepath))
    assert loaded_data["total_docs"] == 1
    assert loaded_data["doc_lengths"]["1"] == 10

def test_load_nonexistent_index(tmp_path):
    filepath = tmp_path / "does_not_exist.json"
    data = load_index(filepath=str(filepath))
    assert data == {}
