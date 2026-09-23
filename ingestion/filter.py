import re

# BASELINE Language Detection: Stopword intersection
# For a production pipeline we'd use fasttext or langdetect, but for this 
# baseline we use common English stopwords.
ENGLISH_STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", 
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", 
    "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", 
    "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", 
    "if", "about", "who", "get", "which", "go", "me", "is", "with", "has"
}

# BASELINE Relevance Classifier: Keyword matching
# For production, we'd use a lightweight classification model (e.g. zero-shot or tuned BERT)
RELEVANT_KEYWORDS = {
    "strike", "weather", "port", "factory", "delay", "supply", "disrupt", 
    "flood", "typhoon", "shortage", "logistics", "shipping", "freight", "fire",
    "regulation", "tariff", "walkout", "halted"
}

def is_english(text: str) -> bool:
    """
    Baseline Language Detection: Checks for the presence of common English stopwords.
    Returns True if at least two unique stopwords are found.
    """
    if not text:
        return False
    words = set(re.findall(r'\b\w+\b', text.lower()))
    overlap = words.intersection(ENGLISH_STOPWORDS)
    return len(overlap) >= 2

def is_relevant(text: str) -> bool:
    """
    Baseline Relevance Classifier: Checks for supply chain disruption keywords.
    """
    if not text:
        return False
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return bool(words.intersection(RELEVANT_KEYWORDS))
    
def filter_feed(records):
    """
    Filters a list of ingested records, retaining only relevant English texts.
    """
    filtered = []
    for r in records:
        text = r.get("text", "")
        if is_english(text) and is_relevant(text):
            filtered.append(r)
    return filtered
