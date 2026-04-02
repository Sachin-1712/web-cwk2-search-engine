import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

INDEX_FILE_PATH = os.path.join("data", "index.json")

def save_index(data: Dict[str, Any], filepath: str = INDEX_FILE_PATH):
    """
    Persists the index data to a JSON file.
    """
    logger.info(f"Saving index to {filepath}...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved index to {filepath}.")
    except Exception as e:
        logger.error(f"Failed to save index: {e}")

def load_index(filepath: str = INDEX_FILE_PATH) -> Dict[str, Any]:
    """
    Loads the index data from a JSON file.
    """
    logger.info(f"Loading index from {filepath}...")
    if not os.path.exists(filepath):
        logger.error(f"Index file {filepath} not found. Please build the index first.")
        return {}
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded index from {filepath}.")
        return data
    except Exception as e:
        logger.error(f"Failed to load index: {e}")
        return {}
