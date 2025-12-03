from app.utils.matching import find_best_match

def test_matching():
    candidates = [
        "Ethiopia Yirgacheffe G1",
        "Colombia Supremo",
        "Brazil Santos No.2",
        "Guatemala Antigua SHB",
        "Kenya AA FAQ"
    ]
    
    test_cases = [
        ("Ethopia Yirgacheffe", "Ethiopia Yirgacheffe G1"), # Typo
        ("Yirgacheffe Ethiopia", "Ethiopia Yirgacheffe G1"), # Order
        ("Colombia Sup", "Colombia Supremo"), # Partial
        ("Brazil Santos", "Brazil Santos No.2"), # Partial
        ("Kenya AA", "Kenya AA FAQ"), # Partial
        ("Blue Mountain", None) # No match
    ]
    
    print("Testing Fuzzy Matching...")
    for query, expected in test_cases:
        match, score = find_best_match(query, candidates)
        result = "✅" if match == expected else "❌"
        print(f"{result} Query: '{query}' -> Match: '{match}' (Score: {score})")

if __name__ == "__main__":
    test_matching()
