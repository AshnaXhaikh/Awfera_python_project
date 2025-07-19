# app/database.py
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any

# Define the path for our JSON metadata file in the project root
METADATA_FILE = Path("metadata.json")

def _load_metadata() -> Dict[str, Any]:
    """Loads the metadata from the JSON file."""
    if not METADATA_FILE.exists():
        return {}
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

def _save_metadata(data: Dict[str, Any]):
    """Saves the metadata to the JSON file."""
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_file_record(file_id: str, username: str, original_filename: str):
    """Adds a new record for an uploaded file."""
    metadata = _load_metadata()
    metadata[file_id] = {
        "file_id": file_id,
        "username": username,
        "original_filename": original_filename,
        "upload_time_utc": datetime.now(timezone.utc).isoformat()
    }
    _save_metadata(metadata)

def get_file_record(file_id: str) -> Dict[str, Any] | None:
    """Retrieves a file record by its ID."""
    metadata = _load_metadata()
    return metadata.get(file_id)

def get_all_records() -> Dict[str, Any]:
    """Retrieves all file records."""
    return _load_metadata()

def delete_file_record(file_id: str) -> Dict[str, Any] | None:
    """Deletes a file record by its ID and returns the deleted record."""
    metadata = _load_metadata()
    deleted_record = metadata.pop(file_id, None)
    if deleted_record:
        _save_metadata(metadata)
    return deleted_record