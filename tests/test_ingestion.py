import pytest
import os
from ingestion.ingest import read_corpus
from ingestion.filter import is_english, is_relevant, filter_feed

def test_read_corpus_valid(tmp_path):
    p = tmp_path / "valid.csv"
    p.write_text("id,text\n1,The port is closed.\n")
    records = read_corpus(str(p))
    assert len(records) == 1
    assert records[0]["text"] == "The port is closed."

def test_read_corpus_empty(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("")
    with pytest.raises(ValueError, match="Empty or malformed feed"):
        read_corpus(str(p))

def test_read_corpus_malformed(tmp_path):
    p = tmp_path / "malformed.csv"
    # Missing 'text' column
    p.write_text("id,wrong_col\n1,Hello world\n")
    with pytest.raises(ValueError, match="Malformed record: missing required fields"):
        read_corpus(str(p))

def test_is_english_true():
    assert is_english("The quick brown fox is jumping over the lazy dog.") is True

def test_is_english_false():
    # Spanish sentence, shouldn't contain english stopwords
    assert is_english("El zorro marrón rápido salta sobre el perro perezoso.") is False
    assert is_english("") is False

def test_is_relevant_true():
    assert is_relevant("The port was closed due to a massive typhoon.") is True
    assert is_relevant("Workers are planning a strike.") is True

def test_is_relevant_false():
    assert is_relevant("The company released its quarterly earnings report today.") is False
    assert is_relevant("") is False

def test_filter_feed():
    records = [
        {"id": 1, "text": "The port is closed due to a strike."}, # English, relevant
        {"id": 2, "text": "The cat sat on the mat."}, # English, not relevant
        {"id": 3, "text": "El puerto está cerrado."} # Not English
    ]
    filtered = filter_feed(records)
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1
