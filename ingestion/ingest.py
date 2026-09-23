import csv
import os

def read_corpus(filepath):
    """
    Simulates reading from an external feed/API by ingesting the CSV corpus.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Feed file not found: {filepath}")
    
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("Empty or malformed feed")
            
        for row in reader:
            if 'text' not in row or 'id' not in row:
                raise ValueError("Malformed record: missing required fields")
            records.append(row)
            
    return records
