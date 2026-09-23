import difflib

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes text similarity using difflib.SequenceMatcher.
    In a production system with working C-extensions, we would use 
    SentenceTransformers and Cosine Similarity.
    """
    if not text1 or not text2:
        return 0.0
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def deduplicate_events(events, threshold=0.75):
    """
    Near-duplicate detection across similar articles.
    Returns a deduplicated list of events and the reduction rate.
    """
    if not events:
        return [], 0.0
        
    unique_events = []
    duplicate_count = 0
    
    for current_event in events:
        is_duplicate = False
        current_text = current_event.get("text", "")
        
        for unique_event in unique_events:
            unique_text = unique_event.get("text", "")
            sim = calculate_similarity(current_text, unique_text)
            
            # If text is highly similar, consider it a duplicate
            if sim >= threshold:
                is_duplicate = True
                break
                
        if is_duplicate:
            duplicate_count += 1
        else:
            unique_events.append(current_event)
            
    reduction_rate = duplicate_count / len(events)
    return unique_events, reduction_rate
