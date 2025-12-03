from thefuzz import process, fuzz
from typing import List, Tuple, Optional

def find_best_match(query: str, candidates: List[str], threshold: int = 60) -> Tuple[Optional[str], int]:
    """
    Find the best match for a query string from a list of candidates.
    Returns (match, score) or (None, 0) if no match found above threshold.
    """
    if not query or not candidates:
        return None, 0
    
    # Use extractOne to find the best match
    # scorer=fuzz.token_sort_ratio handles out of order words well (e.g. "Ethiopia Yirgacheffe" vs "Yirgacheffe Ethiopia")
    result = process.extractOne(query, candidates, scorer=fuzz.token_sort_ratio)
    
    if result:
        match, score = result
        if score >= threshold:
            return match, score
    
    return None, 0
